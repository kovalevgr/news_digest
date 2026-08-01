"""Digest bot core — SDK-free logic (docs/01_technical.md §2.5/§2.6; build plan Phase 6).

The deterministic, unit-testable heart of the bot's weekly-digest delivery: the scheduling
DECISION (one cron job per configured topic digest), the rollup -> Telegram chunking, and the
delivery-message formatting. Like app.bot.triage, this module is kept FREE of
`python-telegram-bot` (no `import telegram` anywhere) so it is testable without the SDK; the
async wiring + the AsyncIOScheduler live in app/bot/__main__.py and call into here.

The bot makes ZERO model calls and NEVER publishes. The digest's single model call (the rollup
summary) lives entirely inside `app.digest.run_digest`, a deterministic shared component the bot
merely TRIGGERS; the bot only delivers the resulting TEXT to the owner's chat. Stages coordinate
through Postgres only — the digest run uses its own DB session and the bot calls no other stage.

Idempotency is the digest core's job, not the bot's: a cron fire that finds nothing eligible
(because a prior run already linked those clusters via article_clusters) makes run_digest return
None, and the bot delivers nothing. So overlapping windows (e.g. a 14d window on a weekly
schedule) never repeat a story — the bot just relays whatever the deterministic run produced.

`parse_digest_schedule` (the "sun 09:00" -> CronTrigger-kwargs parser) lives in app.digest, the
frozen contract; we import it LAZILY inside build_digest_jobs so THIS module imports cleanly even
before that parallel slice lands (mirroring the lazy imports in app/bot/__main__.py).
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

log = logging.getLogger("bot.digest")

# Telegram's hard message limit is 4096 chars; we chunk at 4000 by default for headroom (the
# delivery header we prepend, plus any framing, must fit too). A swappable seam, not a settled
# decision.
DEFAULT_CHUNK_LIMIT = 4000


# --- pure: rollup chunking -----------------------------------------------------------------


def chunk_message(text: str, *, limit: int = DEFAULT_CHUNK_LIMIT) -> list[str]:
    """Split a (possibly long) rollup into Telegram-sendable chunks, each <= `limit` chars.

    PURE. Content is NEVER dropped: concatenating the chunks (re-joining with the boundaries we
    split on) reproduces the text. We prefer to split on natural boundaries — first paragraph
    breaks ("\\n\\n"), then single newlines — packing as many whole lines into a chunk as fit,
    so a chunk rarely ends mid-sentence. A single line longer than `limit` (rare: a giant URL or
    an unbroken blob) is hard-sliced into `limit`-sized pieces as a last resort, so we always
    honor the limit rather than emit an over-long chunk Telegram would reject.

    Edge cases:
      - a short text (<= limit) returns `[text]` (one chunk),
      - an EMPTY string returns `[]` (nothing to send — the caller sends no message),
      - `limit` is coerced to >= 1 defensively so the hard-slice path can't loop forever.
    """
    if not text:
        return []
    if limit < 1:
        limit = 1
    if len(text) <= limit:
        return [text]

    # Split into lines, keeping track of the separators so reconstruction is faithful. We work at
    # the line level and greedily pack lines into chunks; a blank line (paragraph break) is just
    # an empty line that gets packed like any other, so paragraph boundaries are preferred for
    # free (a chunk tends to break at a blank line because that's where slack appears).
    lines = text.split("\n")
    chunks: list[str] = []
    current = ""

    def _flush() -> None:
        nonlocal current
        if current:
            chunks.append(current)
            current = ""

    for i, line in enumerate(lines):
        # The separator that precedes this line within `current` (every line but the first in a
        # chunk is joined to the previous with a single "\n").
        piece = line if not current else "\n" + line
        if len(current) + len(piece) <= limit:
            current += piece
            continue

        # `line` doesn't fit appended to the current chunk. Flush what we have, then place the
        # line on its own — hard-slicing it if it is itself longer than `limit`.
        _flush()
        if len(line) <= limit:
            current = line
        else:
            # A single over-long line: emit full `limit`-sized slices, carry the remainder.
            start = 0
            while len(line) - start > limit:
                chunks.append(line[start:start + limit])
                start += limit
            current = line[start:]
    _flush()
    return chunks


# --- pure: delivery formatting -------------------------------------------------------------


def format_digest_delivery(result) -> str:
    """Render a DigestResult as the plain-text message body the bot sends to the owner.

    PURE: a short header — `📰 Weekly digest — {topic} · {N} stories` (N = number of clusters
    linked by the run) — a blank line, then the dense rollup verbatim. Plain text (no parse_mode
    at the send site), so the rollup's raw markdown is passed through untouched and can never trip
    Telegram's HTML/Markdown parser. Splitting the result into Telegram-sized chunks is
    chunk_message's job, applied by the caller AFTER this."""
    n = len(getattr(result, "cluster_ids", None) or [])
    stories = "story" if n == 1 else "stories"
    header = f"📰 Weekly digest — {result.topic} · {n} {stories}"
    rollup = getattr(result, "rollup", "") or ""
    return f"{header}\n\n{rollup}"


# --- pure: the scheduling plan -------------------------------------------------------------


@dataclass(frozen=True)
class DigestJob:
    """One topic's digest-scheduling decision: run the digest for `topic` (carrying its
    `app.config.Digest`) on the cron schedule described by `cron_kwargs` (CronTrigger kwargs,
    e.g. {"day_of_week": "sun", "hour": 9, "minute": 0}). Returned by the pure planner so
    callers (and tests) can inspect what WOULD be scheduled without constructing APScheduler."""

    topic: str
    digest: object       # app.config.Digest — kept loose to avoid a hard import cycle
    cron_kwargs: dict

    @property
    def schedule(self) -> str:
        return self.digest.schedule


def build_digest_jobs(cfg) -> list[DigestJob]:
    """Plan the digest scheduler: one job per topic in `cfg.digests`.

    PURE — no APScheduler, no DB, no network (mirrors researcher.schedule.build_jobs). Each job
    carries the topic, its `Digest`, and the CronTrigger kwargs parsed from `digest.schedule` via
    the frozen-contract `app.digest.parse_digest_schedule`. That parser is imported LAZILY here so
    THIS module (and build_digest_jobs's signature) imports even before the parallel digest core
    lands — the import is only resolved when the planner actually runs. `cfg.digests` order (a
    dict, insertion-ordered) is preserved, so the plan is deterministic. An empty `cfg.digests`
    yields `[]` (the bot simply schedules no digest jobs — still a valid, idle-clean boot)."""
    from app.digest import parse_digest_schedule

    return [
        DigestJob(
            topic=topic,
            digest=digest,
            cron_kwargs=parse_digest_schedule(digest.schedule),
        )
        for topic, digest in cfg.digests.items()
    ]


# --- SDK-free delivery helper (testable with a fake bot) ------------------------------------


async def deliver_digest(bot, chat_id, result, *, limit: int = DEFAULT_CHUNK_LIMIT) -> int:
    """Send a DigestResult to `chat_id` as one or more plain-text chunks, in order. Returns the
    number of chunks sent.

    SDK-free: `bot` is any object with an async `send_message(chat_id=..., text=...)` — the real
    telegram.Bot in __main__, or a fake in tests. PLAIN TEXT only (no parse_mode), so the rollup's
    raw markdown is delivered as-is and never errors on Telegram's parser. A None result (nothing
    eligible this run) sends nothing and returns 0 — the caller logs "nothing new". The body is
    formatted once, then chunk_message splits it so even a long rollup respects Telegram's limit;
    chunks are sent sequentially so they arrive in reading order."""
    if result is None:
        return 0
    body = format_digest_delivery(result)
    sent = 0
    for chunk in chunk_message(body, limit=limit):
        await bot.send_message(chat_id=chat_id, text=chunk)
        sent += 1
    return sent


__all__ = [
    "DEFAULT_CHUNK_LIMIT",
    "DigestJob",
    "chunk_message",
    "format_digest_delivery",
    "build_digest_jobs",
    "deliver_digest",
]
