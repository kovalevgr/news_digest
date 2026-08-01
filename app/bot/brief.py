"""Morning-brief bot core — SDK-free logic (build plan Phase 9).

The deterministic, unit-testable heart of the bot's batched triage roundup: the scheduling
DECISION (one daily cron job that fires the brief), the windowed selection of summarized-but-
unsent stories, and the roundup header. Like app.bot.triage and app.bot.digest, this module is
kept FREE of `python-telegram-bot` (no `import telegram` anywhere) so it is testable without the
SDK; the async wiring + the AsyncIOScheduler live in app/bot/__main__.py and call into here.

The morning brief is an ALTERNATIVE to the triage drip: instead of trickling each card out as the
researcher summarizes it, the brief batches the day's deliverable pool into one scheduled roundup
at a configured wall-clock time (e.g. 08:00). When a brief is configured the drip is retired — the
brief becomes the SOLE consumer of the deliverable pool — so a story is still delivered exactly
once. The exactly-once guarantee is unchanged: it rests on app.bot.triage's per-card
claim-before-send (`claim_for_send`), which the bot wiring applies to each card the brief selects.

The brief makes ZERO model calls and NEVER publishes — it only reads what the researcher wrote
(`clusters.status` / `clusters.triage_*`) and the bot writes a status back. Stages coordinate
through Postgres only; the brief calls no other stage.

`parse_brief_schedule` (the "08:00" -> CronTrigger-kwargs parser) lives in app.config; we import it
LAZILY inside build_brief_job so THIS module imports cleanly and the planner stays pure.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy import nullslast, select

from app.db.models import Cluster

log = logging.getLogger("bot.brief")


# --- pure: the scheduling plan -------------------------------------------------------------


@dataclass(frozen=True)
class BriefJob:
    """The morning brief's scheduling decision: fire the roundup on the daily cron schedule
    described by `cron_kwargs` (CronTrigger kwargs, e.g. {"hour": 8, "minute": 0} — no
    day_of_week, so it fires every day), carrying the configured `schedule`/`window_s`/`top_n`.
    Returned by the pure planner so callers (and tests) can inspect what WOULD be scheduled
    without constructing APScheduler."""

    cron_kwargs: dict
    schedule: str
    window_s: int
    top_n: int


def build_brief_job(cfg) -> BriefJob | None:
    """Plan the brief scheduler: one daily job iff `cfg.brief` is set, else None.

    PURE — no APScheduler, no DB, no network (mirrors app.bot.digest.build_digest_jobs). The
    CronTrigger kwargs are parsed from `cfg.brief.schedule` via the frozen-contract
    `app.config.parse_brief_schedule` (imported LAZILY so THIS module imports without resolving
    it). The job carries the brief's window/top_n straight from `cfg.brief`. A missing `cfg.brief`
    yields None (the bot schedules no brief job — still a valid, idle-clean boot)."""
    if cfg.brief is None:
        return None
    from app.config import parse_brief_schedule

    return BriefJob(
        cron_kwargs=parse_brief_schedule(cfg.brief.schedule),
        schedule=cfg.brief.schedule,
        window_s=cfg.brief.window_s,
        top_n=cfg.brief.top_n,
    )


# --- pure: roundup header ------------------------------------------------------------------


def format_brief_header(n: int) -> str:
    """The plain-text header that leads the morning roundup: `📰 Morning brief — {n} new
    story`/`stories` (singular on n==1). PURE — the per-story cards that follow are rendered by
    app.bot.triage.format_message at the send site."""
    stories = "story" if n == 1 else "stories"
    return f"📰 Morning brief — {n} new {stories}"


# --- DB: windowed selection ----------------------------------------------------------------


def select_brief_clusters(session, *, window_s: int, top_n: int, now=None) -> list[Cluster]:
    """The summarized-but-unsent clusters for one morning roundup, best first.

    Predicate mirrors app.bot.triage.select_deliverable — status=='new' AND triage_summary IS NOT
    NULL (the researcher has summarized it and the bot hasn't sent it yet) — PLUS a rolling window
    filter: created_at >= (now or utcnow()) - window_s seconds, so the roundup only batches recent
    stories rather than the whole standing backlog. Ordered score DESC (NULLs last), created_at
    ASC, id ASC, capped at `top_n`. Returns full Cluster rows so the caller renders each card and
    then CLAIMS it (selection alone delivers nothing — claim_for_send is the exactly-once guard).

    `now` handling matches select_digest_clusters exactly: the cutoff is computed from `now` if
    given, else datetime.now(timezone.utc) (tz-aware UTC), so a test can pin the window."""
    cutoff = (now or datetime.now(timezone.utc)) - timedelta(seconds=window_s)
    return list(
        session.execute(
            select(Cluster)
            .where(Cluster.status == "new")
            .where(Cluster.triage_summary.is_not(None))
            .where(Cluster.created_at >= cutoff)
            .order_by(
                nullslast(Cluster.score.desc()),
                Cluster.created_at.asc(),
                Cluster.id.asc(),
            )
            .limit(top_n)
        ).scalars().all()
    )


__all__ = [
    "BriefJob",
    "build_brief_job",
    "format_brief_header",
    "select_brief_clusters",
]
