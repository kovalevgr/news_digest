"""Digest bot core (app.bot.digest) — SDK-free logic.

Pure tests for rollup chunking, delivery-message formatting, and the per-topic scheduling plan,
plus an SDK-free orchestration test of the deliver step against a FAKE bot and a stubbed
run_digest. No `import telegram`, no DB.

`build_digest_jobs` depends on `app.digest.parse_digest_schedule` (the frozen contract built in
a parallel slice). That import is lazy inside the planner, so this module always imports; the
planner test is guarded by `_digest_core_ready` so collection stays green even if the parallel
core hasn't landed yet (mirroring the *_ready skip-guard pattern).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from app.bot.digest import (
    DEFAULT_CHUNK_LIMIT,
    DigestJob,
    build_digest_jobs,
    chunk_message,
    deliver_digest,
    format_digest_delivery,
)


# Skip-guard: the frozen-contract parser may not exist yet (parallel slice). The planner imports
# it lazily, so only the planner test needs to skip — everything else stays green regardless.
try:
    from app.digest import parse_digest_schedule  # noqa: F401

    _digest_core_ready = True
except Exception:  # noqa: BLE001 — any import failure means the core isn't ready yet.
    _digest_core_ready = False

needs_digest_core = pytest.mark.skipif(
    not _digest_core_ready, reason="app.digest.parse_digest_schedule not importable yet"
)


# --- a tiny stand-in for the contract types (keeps these tests DB-/SDK-free) ----------------


@dataclass
class _FakeResult:
    """Mirrors app.digest.DigestResult's shape for the pure formatting/delivery tests."""

    topic: str = "ai"
    article_id: str = "ar:abc"
    cluster_ids: list = field(default_factory=lambda: ["cl:1", "cl:2", "cl:3"])
    rollup: str = "Story one.\nStory two."


@dataclass
class _FakeDigest:
    """Mirrors the bits of app.config.Digest the planner reads (.schedule)."""

    schedule: str
    window_days: int = 7
    top_n: int = 10


class _FakeConfig:
    """The only attr build_digest_jobs touches is `.digests` (topic -> Digest)."""

    def __init__(self, digests):
        self.digests = digests


class _FakeBot:
    """Records send_message calls so the deliver step is testable without the SDK."""

    def __init__(self):
        self.calls: list[dict] = []

    async def send_message(self, **kwargs):
        self.calls.append(kwargs)


# --- chunk_message -------------------------------------------------------------------------


def test_chunk_message_short_text_is_one_chunk():
    assert chunk_message("hello") == ["hello"]
    # Exactly at the limit is still one chunk.
    assert chunk_message("x" * 10, limit=10) == ["x" * 10]


def test_chunk_message_empty_is_no_chunks():
    assert chunk_message("") == []


def test_chunk_message_long_text_splits_within_limit_and_preserves_content():
    # 100 single-char lines -> joined length 100 + 99 separators ~ 199; chunk at 40.
    lines = [f"line{i:02d}" for i in range(40)]
    text = "\n".join(lines)
    chunks = chunk_message(text, limit=40)
    assert len(chunks) > 1
    assert all(len(c) <= 40 for c in chunks)
    # Re-joining the chunks on the split boundary reproduces the original (no content dropped).
    assert "\n".join(chunks) == text


def test_chunk_message_prefers_paragraph_then_line_boundaries():
    # Two paragraphs; a limit that comfortably holds one paragraph but not both should split AT
    # the blank-line boundary, so neither chunk ends mid-line.
    para_a = "alpha line one\nalpha line two"
    para_b = "beta line one\nbeta line two"
    text = f"{para_a}\n\n{para_b}"
    chunks = chunk_message(text, limit=len(para_a) + 2)  # holds para_a (+ a little), not both
    assert len(chunks) >= 2
    assert all(len(c) <= len(para_a) + 2 for c in chunks)
    assert "\n".join(chunks) == text
    # No chunk splits a word across its boundary: each chunk is whole lines.
    for c in chunks:
        for ln in c.split("\n"):
            assert ln == "" or ln in text


def test_chunk_message_hard_slices_an_overlong_single_line():
    # A single line longer than the limit must still be split (last-resort hard slice), never
    # emitted over-length, and still fully preserved.
    blob = "z" * 95
    chunks = chunk_message(blob, limit=40)
    assert len(chunks) == 3  # 40 + 40 + 15
    assert all(len(c) <= 40 for c in chunks)
    assert "".join(chunks) == blob


def test_chunk_message_default_limit_is_under_telegram_hard_limit():
    assert DEFAULT_CHUNK_LIMIT <= 4096
    big = "p" * 9000
    for c in chunk_message(big):
        assert len(c) <= DEFAULT_CHUNK_LIMIT


# --- format_digest_delivery ----------------------------------------------------------------


def test_format_digest_delivery_has_header_and_rollup():
    result = _FakeResult(topic="dotnet", cluster_ids=["cl:1", "cl:2", "cl:3"], rollup="The roundup.")
    msg = format_digest_delivery(result)
    assert "Weekly digest" in msg
    assert "dotnet" in msg
    assert "3 stories" in msg          # N = number of linked clusters
    assert "The roundup." in msg       # rollup carried verbatim
    # Header first, rollup after a blank line.
    assert msg.startswith("📰 Weekly digest — dotnet · 3 stories")
    assert "\n\n" in msg


def test_format_digest_delivery_singular_story():
    result = _FakeResult(topic="ai", cluster_ids=["cl:1"], rollup="One thing.")
    assert "1 story" in format_digest_delivery(result)
    assert "1 stories" not in format_digest_delivery(result)


# --- build_digest_jobs (planner) -----------------------------------------------------------


@needs_digest_core
def test_build_digest_jobs_one_per_topic_with_cron_kwargs():
    cfg = _FakeConfig(
        {
            "ai": _FakeDigest(schedule="sun 09:00"),
            "dotnet": _FakeDigest(schedule="sat 10:30"),
        }
    )
    jobs = build_digest_jobs(cfg)
    assert [j.topic for j in jobs] == ["ai", "dotnet"]          # dict order preserved
    assert all(isinstance(j, DigestJob) for j in jobs)
    assert jobs[0].cron_kwargs == {"day_of_week": "sun", "hour": 9, "minute": 0}
    assert jobs[1].cron_kwargs == {"day_of_week": "sat", "hour": 10, "minute": 30}
    # The job carries the source Digest and exposes its schedule.
    assert jobs[0].digest is cfg.digests["ai"]
    assert jobs[0].schedule == "sun 09:00"


@needs_digest_core
def test_build_digest_jobs_empty_when_no_digests():
    assert build_digest_jobs(_FakeConfig({})) == []


# --- deliver_digest (SDK-free orchestration with a fake bot) --------------------------------


@pytest.mark.asyncio
async def test_deliver_digest_sends_chunks_in_order():
    bot = _FakeBot()
    # A rollup long enough to force >1 chunk so we exercise ordering.
    long_rollup = "\n".join(f"item {i}" for i in range(2000))
    result = _FakeResult(topic="ai", rollup=long_rollup)
    n = await deliver_digest(bot, 12345, result, limit=200)

    assert n == len(bot.calls) > 1
    # Every call is plain text (no parse_mode) to the owner chat.
    assert all(c["chat_id"] == 12345 for c in bot.calls)
    assert all("parse_mode" not in c for c in bot.calls)
    # Chunks are sent in reading order and reproduce the formatted body.
    rebuilt = "\n".join(c["text"] for c in bot.calls)
    assert rebuilt == format_digest_delivery(result)
    # The header (first chunk) leads.
    assert bot.calls[0]["text"].startswith("📰 Weekly digest — ai")


@pytest.mark.asyncio
async def test_deliver_digest_none_sends_nothing():
    bot = _FakeBot()
    n = await deliver_digest(bot, 12345, None)
    assert n == 0
    assert bot.calls == []


@pytest.mark.asyncio
async def test_deliver_digest_short_rollup_is_single_message():
    bot = _FakeBot()
    result = _FakeResult(topic="ai", cluster_ids=["cl:1", "cl:2"], rollup="short and sweet")
    n = await deliver_digest(bot, 999, result)
    assert n == 1
    assert len(bot.calls) == 1
    assert bot.calls[0]["text"] == format_digest_delivery(result)
