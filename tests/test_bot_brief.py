"""Morning-brief bot core (app.bot.brief) — SDK-free logic — Phase 9.

Pure tests for the daily scheduling plan and the roundup header, plus a DB-backed test (guarded
by RUN_PG_TESTS) for the windowed selection. No `import telegram`. Fixtures mirror
tests/test_bot_digest.py and tests/test_digest.py.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import pytest

from app.bot.brief import (
    BriefJob,
    build_brief_job,
    format_brief_header,
    select_brief_clusters,
)


# --- tiny stand-ins (keep the pure tests DB-/SDK-free) -------------------------------------


@dataclass
class _FakeBrief:
    """Mirrors app.config.Brief's shape the planner reads."""

    schedule: str
    window_s: int = 86400
    top_n: int = 10


class _FakeConfig:
    """The only attr build_brief_job touches is `.brief` (Brief | None)."""

    def __init__(self, brief):
        self.brief = brief


# --- build_brief_job (planner) -------------------------------------------------------------


def test_build_brief_job_none_when_no_brief():
    assert build_brief_job(_FakeConfig(None)) is None


def test_build_brief_job_carries_cron_window_top_n():
    job = build_brief_job(_FakeConfig(_FakeBrief(schedule="08:00", window_s=43200, top_n=7)))
    assert isinstance(job, BriefJob)
    assert job.cron_kwargs == {"hour": 8, "minute": 0}    # no day_of_week -> every day
    assert "day_of_week" not in job.cron_kwargs
    assert job.schedule == "08:00"
    assert job.window_s == 43200
    assert job.top_n == 7


def test_build_brief_job_single_digit_hour():
    job = build_brief_job(_FakeConfig(_FakeBrief(schedule="6:05")))
    assert job.cron_kwargs == {"hour": 6, "minute": 5}


# --- format_brief_header -------------------------------------------------------------------


def test_format_brief_header_pluralization():
    assert format_brief_header(1) == "📰 Morning brief — 1 new story"
    assert format_brief_header(3) == "📰 Morning brief — 3 new stories"
    assert format_brief_header(0) == "📰 Morning brief — 0 new stories"


# --- DB-backed: windowed selection ---------------------------------------------------------

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"
pg_only = pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")


@pytest.fixture()
def session():
    from app.db.session import engine, SessionLocal

    conn = engine.connect()
    outer = conn.begin()
    sess = SessionLocal(bind=conn, join_transaction_mode="create_savepoint")
    try:
        yield sess
    finally:
        sess.close()
        outer.rollback()
        conn.close()


def _add_cluster(session, *, status="new", score=None, summary="A blurb", created_at=None):
    """Insert a cluster with the given status/score/summary/created_at. Returns the id. Mirrors
    tests/test_bot_triage._add_cluster, adding created_at control for the window filter."""
    from app.db.models import Cluster
    from app.researcher.cluster import new_cluster_id

    cid = new_cluster_id()
    cluster = Cluster(id=cid, status=status, score=score, triage_title="t", triage_summary=summary)
    if created_at is not None:
        cluster.created_at = created_at
    session.add(cluster)
    session.commit()
    return cid


@pg_only
def test_select_brief_only_new_summarized_in_window_ordered(session):
    now = datetime.now(timezone.utc)
    high = _add_cluster(session, status="new", score=0.9, summary="s", created_at=now - timedelta(hours=1))
    low = _add_cluster(session, status="new", score=0.1, summary="s", created_at=now - timedelta(hours=2))
    _add_cluster(session, status="new", score=0.99, summary=None, created_at=now)            # no summary
    _add_cluster(session, status="sent", score=0.99, summary="s", created_at=now)            # already sent
    _add_cluster(session, status="new", score=0.99, summary="s", created_at=now - timedelta(days=2))  # out of window

    ids = [c.id for c in select_brief_clusters(session, window_s=86400, top_n=10, now=now)]
    assert ids == [high, low]   # only in-window, summarized, new — ordered score DESC


@pg_only
def test_select_brief_caps_at_top_n(session):
    now = datetime.now(timezone.utc)
    a = _add_cluster(session, status="new", score=0.9, summary="s", created_at=now)
    b = _add_cluster(session, status="new", score=0.5, summary="s", created_at=now)
    _add_cluster(session, status="new", score=0.1, summary="s", created_at=now)

    ids = [c.id for c in select_brief_clusters(session, window_s=86400, top_n=2, now=now)]
    assert ids == [a, b]   # top 2 by score


@pg_only
def test_select_brief_window_boundary(session):
    now = datetime.now(timezone.utc)
    just_in = _add_cluster(session, status="new", score=0.5, summary="s", created_at=now - timedelta(hours=23))
    just_out = _add_cluster(session, status="new", score=0.9, summary="s", created_at=now - timedelta(hours=25))

    ids = [c.id for c in select_brief_clusters(session, window_s=86400, top_n=10, now=now)]
    assert just_in in ids
    assert just_out not in ids   # older than the 24h window despite the higher score
