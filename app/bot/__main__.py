"""`python -m app.bot` — the Telegram Gate-1 triage bot (build plan Phase 2).

Thin ASYNC wiring around the SDK-free core in app.bot.triage. This module is the only place
that touches `python-telegram-bot`; all the cluster-status logic, callback encoding, and
rendering live in app.bot.triage so they stay unit-testable without the SDK.

Two responsibilities, both coordinating with the rest of the pipeline ONLY through Postgres
(the poller writes triage_* + status; this bot reads them and writes status back — stages never
call each other):

  1. DELIVERY loop — a background asyncio task (started in post_init, NOT via the job-queue
     extra) that every TELEGRAM_POLL_INTERVAL_S selects summarized-but-unsent clusters and pushes
     each as a triage card with [Approve][Skip] buttons. The card is rendered, then CLAIMED
     ('new' -> 'sent') BEFORE the Telegram send — claim-before-send is what makes delivery
     exactly-once across bot/poller restarts (a crash after claim leaves the card 'sent' and it
     is simply never re-selected). A send that fails after claiming is reverted ('sent' -> 'new')
     so the next sweep retries it. One bad sweep never kills the loop.

  2. CALLBACK handler — honored ONLY for the owner chat (TELEGRAM_OWNER_CHAT_ID); any other chat
     gets "Not authorized" and is ignored (hard rule + Phase-2 Done). A tap decodes to an
     action + token, resolves the token to a unique cluster, and applies the decision. On
     APPROVE the bot answers immediately, then runs the pass-2 full-text fetch
     (app.fetcher.fetch_cluster_full_text) OFF the event loop via run_in_executor with its OWN db
     session, and edits the card to show the result. On SKIP it marks and edits. An already-
     decided card reports "Already decided".

The bot makes ZERO model calls and NEVER publishes — it only delivers cards and reads/writes
clusters.status (plus triggering the deterministic pass-2 fetch, a shared component, on
approval). Secrets (TELEGRAM_TOKEN, TELEGRAM_OWNER_CHAT_ID) come from the ENVIRONMENT only.

If the token or owner chat id is unset we log a clear warning and idle (mirroring the Phase-0
stub) rather than crash-loop — the image still boots and stays up.
"""
from __future__ import annotations

import asyncio
import logging
import os

from app.bot.brief import (
    format_brief_header,
    select_brief_clusters,
)
from app.bot.triage import (
    ACTION_APPROVE,
    claim_for_send,
    decide,
    encode_callback,
    format_message,
    owner_chat_id,
    parse_callback,
    resolve_by_token,
    revert_to_new,
    select_deliverable,
)
from app.config import load_config
from app.db.session import get_session

logging.basicConfig(level=logging.INFO, format="%(asctime)s [bot] %(message)s")
log = logging.getLogger("bot")

# --- delivery knobs (open decision: the bot's DB-check interval / batch — env seams) -------
#
# How often the delivery loop sweeps the DB for summarized-but-unsent clusters. Default 300s
# (5 min): the owner doesn't need second-by-second pushes, and a relaxed cadence keeps the bot
# quiet. Env-overridable; falls back on garbage/non-positive so the loop can't spin or stall.
DEFAULT_POLL_INTERVAL_S = 300
# Max cards delivered per sweep, so a backlog trickles out rather than flooding the chat in one
# burst. Default 5 — a readable phone batch.
DEFAULT_DELIVER_BATCH = 5


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad %s=%r — falling back to %s", name, raw, default)
        return default
    return val if val > 0 else default


def poll_interval_s() -> int:
    return _env_int("TELEGRAM_POLL_INTERVAL_S", DEFAULT_POLL_INTERVAL_S)


def deliver_batch() -> int:
    return _env_int("TELEGRAM_DELIVER_BATCH", DEFAULT_DELIVER_BATCH)


# --- digest scheduling knobs ----------------------------------------------------------------
#
# The scheduler/cron timezone. The owner's digest schedules (e.g. "sun 09:00") are wall-clock
# intent, so we run the cron in an explicit timezone seam rather than the container's. Default
# "UTC" (deterministic, matches the rest of the pipeline's UTC timestamps); override per deploy
# via DIGEST_TZ (e.g. "Europe/Berlin").
DEFAULT_DIGEST_TZ = "UTC"
# A cron fire that the bot misses (process restart spanning the scheduled minute) should still
# run shortly after the bot is back, not be silently dropped — the digest is idempotent (a late
# run that finds nothing eligible delivers nothing), so a generous grace window is safe. 1 hour.
DIGEST_MISFIRE_GRACE_S = 3600


def digest_tz() -> str:
    """The timezone name passed to the AsyncIOScheduler / CronTrigger (env DIGEST_TZ, default
    UTC). A bad/unknown name falls back to UTC so a typo can never crash the scheduler build."""
    raw = os.environ.get("DIGEST_TZ")
    return raw.strip() if raw and raw.strip() else DEFAULT_DIGEST_TZ


def _keyboard(cluster_id: str):
    """The inline [Approve][Skip] keyboard for a card. Each button's callback_data is the
    compact `<action>:<token>` from encode_callback (well under Telegram's 64-byte limit)."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    from app.bot.triage import ACTION_SKIP

    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("✅ Approve", callback_data=encode_callback(ACTION_APPROVE, cluster_id)),
            InlineKeyboardButton("⏭ Skip", callback_data=encode_callback(ACTION_SKIP, cluster_id)),
        ]]
    )


# --- delivery loop -------------------------------------------------------------------------


async def _deliver_once(bot, chat_id: int) -> int:
    """One delivery sweep: push up to `deliver_batch()` summarized-but-unsent cards. Returns the
    number actually delivered.

    Ordering of operations per card is the exactly-once guard: render the message, then CLAIM
    ('new' -> 'sent') BEFORE sending. Only a winning claim proceeds to send; a lost claim (a
    racing sweep / a card already sent after a restart) is skipped. If the send raises AFTER a
    winning claim, we revert ('sent' -> 'new') so the next sweep retries — the card is never
    lost and never double-sent.

    DB work runs on a fresh session opened+closed here; the synchronous claim/revert calls are
    short and infrequent, so we keep them inline (the heavier pass-2 fetch on approval is the
    one path pushed to an executor)."""
    session = get_session()
    delivered = 0
    try:
        clusters = select_deliverable(session, limit=deliver_batch())
        for cluster in clusters:
            cluster_id = cluster.id
            text = format_message(cluster)         # render BEFORE claiming (claim is the gate)
            keyboard = _keyboard(cluster_id)
            if not claim_for_send(session, cluster_id):
                # Lost the claim (raced / already sent) — skip; nothing to undo.
                continue
            try:
                await bot.send_message(
                    chat_id=chat_id, text=text, parse_mode="HTML", reply_markup=keyboard
                )
            except Exception:  # noqa: BLE001 — a failed send must not lose the card.
                log.warning("send failed for cluster %s; reverting to 'new'", cluster_id, exc_info=True)
                revert_to_new(session, cluster_id)
                continue
            delivered += 1
    finally:
        session.close()
    return delivered


async def _delivery_loop(app) -> None:
    """The background delivery task: sweep on `poll_interval_s()` forever. One bad sweep is
    logged and swallowed so the loop never dies (the next tick retries; the whole pipeline is
    idempotent and DB-coordinated). Cancelled cleanly on shutdown."""
    chat_id = owner_chat_id()
    if chat_id is None:  # defensive: post_init only starts this when the owner is configured.
        return
    interval = poll_interval_s()
    log.info("delivery loop started: sweeping every %ss, batch %d", interval, deliver_batch())
    try:
        while True:
            try:
                n = await _deliver_once(app.bot, chat_id)
                if n:
                    log.info("delivered %d triage card(s)", n)
            except Exception:  # noqa: BLE001 — isolate a bad sweep; keep the loop alive.
                log.exception("delivery sweep failed; will retry next interval")
            await asyncio.sleep(interval)
    except asyncio.CancelledError:  # graceful shutdown
        log.info("delivery loop cancelled")
        raise


# --- handlers ------------------------------------------------------------------------------


def _is_owner(update) -> bool:
    """True iff the update's effective chat is the configured owner chat. Everything else is
    ignored (hard rule: the bot accepts commands/callbacks ONLY from TELEGRAM_OWNER_CHAT_ID)."""
    owner = owner_chat_id()
    chat = update.effective_chat
    return owner is not None and chat is not None and chat.id == owner


async def _on_start(update, context) -> None:
    """Owner-only /start: confirm the bot is alive. A non-owner gets no reply."""
    if not _is_owner(update):
        return
    await update.message.reply_text("Triage bot is alive. I'll send stories as they're ready.")


def _run_fetch(cluster_id: str) -> dict:
    """Run the pass-2 full-text fetch for an approved cluster on a thread (its OWN db session).

    Executed via run_in_executor so the synchronous, network-bound fetch never blocks the event
    loop. Opens and closes its own session because it runs off the loop thread; fetch_cluster_
    full_text isolates per-item failures internally. This is a deterministic shared component —
    the bot triggers it but adds no model call and no publishing."""
    from app.fetcher import fetch_cluster_full_text

    session = get_session()
    try:
        return fetch_cluster_full_text(session, cluster_id)
    finally:
        session.close()


async def _on_callback(update, context) -> None:
    """Inline-button handler for Gate-1 decisions — honored ONLY for the owner chat.

    Flow: authorize (non-owner -> "Not authorized", return) -> parse the callback -> resolve the
    token to a unique cluster -> apply the decision. On APPROVE we answer immediately, then run
    the pass-2 fetch off the loop and edit the card with the result. On SKIP we mark and edit. A
    tap on an already-decided card reports "Already decided". A junk/ambiguous token is a quiet
    no-op (answered so Telegram clears the spinner)."""
    query = update.callback_query
    if not _is_owner(update):
        # Authorize on the CHAT, not the user — the owner chat is the trust boundary.
        if query is not None:
            await query.answer("Not authorized")
        return

    parsed = parse_callback(query.data)
    if parsed is None:
        await query.answer("Unrecognized action")
        return
    action, token = parsed

    # All DB reads/writes for the decision share one short-lived session.
    session = get_session()
    try:
        cluster_id = resolve_by_token(session, token)
        if cluster_id is None:
            # Ambiguous or missing token -> safe no-op (never act on the wrong story).
            await query.answer("Story not found")
            return

        approve = action == ACTION_APPROVE
        new_status = decide(session, cluster_id, approve=approve)
    finally:
        session.close()

    if new_status is None:
        # Already terminal (a double-tap, or the other button on a decided card).
        await query.answer("Already decided")
        await _edit_caption(query, "✔ Already decided")
        return

    if approve:
        await query.answer("Approved — fetching full text…")
        await _edit_caption(query, "✅ Approved — fetching full text…")
        # Pass-2 fetch off the event loop (network-bound, its own session).
        loop = asyncio.get_running_loop()
        try:
            stats = await loop.run_in_executor(None, _run_fetch, cluster_id)
            await _edit_caption(
                query,
                f"✅ Approved — fetched full text for {stats['fetched']}/{stats['considered']} item(s).",
            )
        except Exception:  # noqa: BLE001 — approval already recorded; surface a fetch problem only.
            log.exception("pass-2 fetch failed for approved cluster %s", cluster_id)
            await _edit_caption(query, "✅ Approved — full-text fetch failed (will not block).")
    else:
        await query.answer("Skipped")
        await _edit_caption(query, "⏭ Skipped")


async def _edit_caption(query, suffix: str) -> None:
    """Append a status line to the delivered card and drop its buttons, so a decided card shows
    its outcome and can't be tapped again. Edit failures (message too old, identical content)
    are swallowed — the decision is already persisted; the card edit is cosmetic."""
    try:
        original = query.message.text_html if query.message else ""
        await query.edit_message_text(
            text=f"{original}\n\n<i>{suffix}</i>", parse_mode="HTML", reply_markup=None
        )
    except Exception:  # noqa: BLE001 — cosmetic; the status transition already committed.
        log.debug("edit_message_text failed (non-fatal)", exc_info=True)


# --- digest: scheduled per-topic run + delivery --------------------------------------------


def _run_digest_job(topic: str) -> object | None:
    """Run the deterministic weekly digest for one topic on a thread (its OWN db session).

    Executed via run_in_executor so the synchronous, DB-and-model-bound digest run never blocks
    the event loop (mirrors _run_fetch). Opens and closes its own session because it runs off the
    loop thread; reloads config so it reads the topic's current `Digest` (config is a file, not
    the DB). Returns the `DigestResult` (or None when nothing is eligible — the covered-marker
    already linked those clusters). app.digest.run_digest is the shared deterministic component
    that owns the single model call; the bot adds none and never publishes — it only relays text.

    A topic that has vanished from config since boot is a no-op (returns None). Imports are lazy
    so this module stays import-side-effect-free and so the parallel app.digest slice can land
    independently."""
    from app.digest import run_digest

    cfg = load_config()
    digest_cfg = cfg.digests.get(topic)
    if digest_cfg is None:
        log.warning("digest topic %r no longer in config — skipping run", topic)
        return None

    session = get_session()
    try:
        return run_digest(session, topic, digest_cfg)
    finally:
        session.close()


async def _run_digest_for_topic(app, topic: str) -> None:
    """The async cron entry point for one topic's digest: run it off the loop, then deliver.

    Wrapped so ONE failing job is logged and swallowed — it must never tear down the scheduler or
    the bot (hard rule: restart-safe; the next fire retries, the run is idempotent). Flow: run the
    deterministic digest in an executor (own session) -> if a DigestResult came back, deliver the
    dense rollup to the owner chat as ordered plain-text chunks via deliver_digest; if None,
    nothing was eligible (already-covered), so log and send nothing."""
    chat_id = owner_chat_id()
    if chat_id is None:  # defensive: we only schedule digests when the owner is configured.
        return
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, _run_digest_job, topic)
        if result is None:
            log.info("digest[%s]: nothing new (already covered) — delivering nothing", topic)
            return
        from app.bot.digest import deliver_digest

        n = await deliver_digest(app.bot, chat_id, result)
        log.info(
            "digest[%s]: delivered %d chunk(s) covering %d cluster(s) (article %s)",
            topic, n, len(result.cluster_ids), result.article_id,
        )
    except Exception:  # noqa: BLE001 — isolate a bad digest job; never kill the scheduler/bot.
        log.exception("digest job for topic %r failed; scheduler stays up, next fire retries", topic)


async def _run_brief(app) -> None:
    """The async cron entry point for the morning brief: one batched triage roundup.

    Wrapped so ONE failure is logged and swallowed — it must never tear down the scheduler or the
    bot (hard rule: restart-safe; the next fire retries, and per-card claims keep delivery
    exactly-once). Flow:

      - read the configured Brief (from bot_data["cfg"], reloading config if absent — config is a
        file, mirrors _run_digest_job), and the owner chat (return if unset),
      - select the window's top-N summarized-but-unsent clusters,
      - if NONE, send NOTHING (an empty morning — no header) and return,
      - else send the header first, then push each card via the SAME proven per-card path as the
        drip's _deliver_once: render -> CLAIM ('new' -> 'sent') BEFORE sending -> on a send failure,
        revert ('sent' -> 'new') and continue. This per-card claim-before-send IS the exactly-once
        guarantee — we do NOT claim the whole batch then send.

    The DB session is opened+closed here. The brief makes no model call and never publishes."""
    chat_id = owner_chat_id()
    if chat_id is None:  # defensive: we only schedule the brief when the owner is configured.
        return
    try:
        cfg = app.bot_data.get("cfg")
        if cfg is None:  # defensive: main() always sets it; reload rather than skip the brief.
            cfg = load_config()
        brief_cfg = cfg.brief
        if brief_cfg is None:  # brief vanished from config since boot — nothing to do.
            log.warning("brief no longer in config — skipping run")
            return

        session = get_session()
        try:
            clusters = select_brief_clusters(
                session, window_s=brief_cfg.window_s, top_n=brief_cfg.top_n, now=None
            )
            if not clusters:
                log.info("brief: nothing new in the window — delivering nothing (empty morning)")
                return
            await app.bot.send_message(chat_id=chat_id, text=format_brief_header(len(clusters)))
            delivered = 0
            for cluster in clusters:
                cluster_id = cluster.id
                text = format_message(cluster)        # render BEFORE claiming (claim is the gate)
                keyboard = _keyboard(cluster_id)
                if not claim_for_send(session, cluster_id):
                    # Lost the claim (raced / already sent) — skip; nothing to undo.
                    continue
                try:
                    await app.bot.send_message(
                        chat_id=chat_id, text=text, parse_mode="HTML", reply_markup=keyboard
                    )
                except Exception:  # noqa: BLE001 — a failed send must not lose the card.
                    log.warning(
                        "brief send failed for cluster %s; reverting to 'new'", cluster_id, exc_info=True
                    )
                    revert_to_new(session, cluster_id)
                    continue
                delivered += 1
            log.info("brief: delivered %d triage card(s)", delivered)
        finally:
            session.close()
    except Exception:  # noqa: BLE001 — isolate a bad brief run; never kill the scheduler/bot.
        log.exception("brief run failed; scheduler stays up, next fire retries")


def _build_scheduler(app, cfg):
    """Build an AsyncIOScheduler with ONE cron job per configured topic digest PLUS (iff a brief
    is configured) ONE daily morning-brief job, start it, and return it (with zero jobs when
    there's nothing scheduled — still started, for uniform shutdown).

    APScheduler is imported lazily here so this module imports without it (mirroring
    researcher.schedule.build_scheduler). The bot is ASYNC, so we use AsyncIOScheduler (it drives
    jobs on the running event loop), NOT a BlockingScheduler. Each digest job:
      - fires `_run_digest_for_topic(app, topic)` on its CronTrigger(**cron_kwargs) (from the pure
        planner build_digest_jobs, which parsed the topic's `digest.schedule`),
      - coalesce=True + max_instances=1 so a slow/overlapping run can never stack,
      - replace_existing=True (idempotent re-registration on restart),
      - a generous misfire_grace_time so a fire missed during a restart still runs shortly after.
    The brief job mirrors those safety options and fires `_run_brief(app)` daily at the configured
    wall-clock time. DIGEST_TZ governs the brief's wall-clock morning too (same scheduler tz). An
    empty `cfg.digests` + no brief adds no jobs (still a clean boot); we return the started
    scheduler regardless so _post_shutdown can stop it uniformly."""
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger

    from app.bot.brief import build_brief_job
    from app.bot.digest import build_digest_jobs

    tz = digest_tz()
    scheduler = AsyncIOScheduler(timezone=tz)
    jobs = build_digest_jobs(cfg)
    for job in jobs:
        scheduler.add_job(
            _run_digest_for_topic,
            trigger=CronTrigger(timezone=tz, **job.cron_kwargs),
            args=(app, job.topic),
            id=f"digest:{job.topic}",
            name=f"digest:{job.topic} ({job.schedule})",
            replace_existing=True,
            coalesce=True,
            max_instances=1,
            misfire_grace_time=DIGEST_MISFIRE_GRACE_S,
        )
        log.info("scheduled digest[%s] on '%s' (tz=%s)", job.topic, job.schedule, tz)
    if not jobs:
        log.info("no topic digests configured — digest scheduler idle")

    # The morning brief (Phase 9): one daily cron job iff configured. Reuses digest_tz() — the same
    # scheduler timezone — so DIGEST_TZ governs the brief's wall-clock morning too.
    if cfg.brief is not None:
        brief_job = build_brief_job(cfg)
        scheduler.add_job(
            _run_brief,
            trigger=CronTrigger(timezone=tz, **brief_job.cron_kwargs),
            args=(app,),
            id="brief",
            name=f"brief ({cfg.brief.schedule})",
            replace_existing=True,
            coalesce=True,
            max_instances=1,
            misfire_grace_time=DIGEST_MISFIRE_GRACE_S,
        )
        log.info("scheduled morning brief on '%s' (tz=%s)", cfg.brief.schedule, tz)

    scheduler.start()
    return scheduler


# --- wiring --------------------------------------------------------------------------------


async def _post_init(app) -> None:
    """Start the scheduler AND (unless a morning brief is configured) the triage drip AFTER the
    app initializes.

    Two delivery modes, mutually exclusive so a story is delivered exactly once:
      - NO brief: the background drip (_delivery_loop, a plain asyncio task — not the job-queue
        extra, so the bot has no dependency on python-telegram-bot[job-queue]) trickles cards out
        as they're summarized. Its handle is stashed on bot_data for clean cancellation.
      - brief configured: the drip is RETIRED — the daily brief job becomes the SOLE consumer of
        the deliverable pool, batching the morning roundup. We start no delivery task; _post_shutdown
        tolerates its absence.

    The AsyncIOScheduler (per-topic digest jobs + the optional brief job) drives on this same event
    loop and is stashed on bot_data so _post_shutdown can stop it. cfg is read from bot_data, where
    main() placed it (matching the existing config-once wiring style)."""
    cfg = app.bot_data.get("cfg")
    if cfg is None:  # defensive: main() always sets it; reload rather than skip scheduling entirely.
        cfg = load_config()

    if cfg.brief is None:
        # No brief -> the drip is the deliverer (existing behavior).
        app.bot_data["delivery_task"] = asyncio.create_task(_delivery_loop(app))
    else:
        # A brief is configured -> it replaces the drip; do not start _delivery_loop.
        log.info("morning brief configured — retiring the triage drip (brief is the sole deliverer)")

    app.bot_data["scheduler"] = _build_scheduler(app, cfg)


async def _post_shutdown(app) -> None:
    """Shut the scheduler and cancel the delivery loop (if it was started) on shutdown so we exit
    cleanly. The delivery task is absent when a morning brief is configured — guard the cancel."""
    scheduler = app.bot_data.get("scheduler")
    if scheduler is not None:
        try:
            scheduler.shutdown(wait=False)
        except Exception:  # noqa: BLE001 — shutdown is best-effort; don't block a clean exit.
            log.debug("scheduler shutdown raised (non-fatal)", exc_info=True)

    task = app.bot_data.get("delivery_task")
    if task is not None:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


def _idle(reason: str) -> None:
    """Boot-but-idle fallback when the bot can't run (no token / no owner): log clearly and
    sleep forever, mirroring the Phase-0 stub. The image stays up; it just does nothing — no
    crash-loop, no restart storm."""
    import time

    log.warning("bot idling: %s", reason)
    while True:
        time.sleep(3600)


def main() -> None:
    # Config load is the same boot sanity check the Phase-0 stub did (proves the image + config
    # are healthy). Sources/digests aren't used by the bot directly, but a failed load is a clear
    # early signal.
    cfg = load_config()
    log.info("bot boot OK — %d sources, digests: %s", len(cfg.sources), sorted(cfg.digests))

    token = os.environ.get("TELEGRAM_TOKEN")
    owner = owner_chat_id()
    if not token:
        return _idle("TELEGRAM_TOKEN is unset (set it in the environment to connect).")
    if owner is None:
        return _idle("TELEGRAM_OWNER_CHAT_ID is unset/invalid (the bot would have no owner).")

    from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler

    app = (
        ApplicationBuilder()
        .token(token)
        .post_init(_post_init)
        .post_shutdown(_post_shutdown)
        .build()
    )
    # Hand the already-loaded config to post_init via bot_data (config-once; matches the existing
    # wiring style) so the digest scheduler reads the same cfg main() validated at boot.
    app.bot_data["cfg"] = cfg
    app.add_handler(CommandHandler("start", _on_start))
    app.add_handler(CallbackQueryHandler(_on_callback))

    log.info("starting long-polling; owner chat %s", owner)
    app.run_polling()


if __name__ == "__main__":
    main()
