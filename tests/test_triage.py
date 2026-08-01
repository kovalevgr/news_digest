"""Triage summaries (app.researcher.triage).

Pure tests for prompt assembly + reply parsing (the model boundary), and DB-backed tests
(guarded by RUN_PG_TESTS) for candidate selection and the idempotent summarize stage.
"""
from __future__ import annotations

import os

import pytest

from app.researcher.triage import (
    build_triage_prompt,
    parse_triage_reply,
    select_triage_candidates,
    summarize_pending_triage,
)


# --- pure: prompt + parse ------------------------------------------------------------------


def test_build_prompt_has_markers_and_titles():
    p = build_triage_prompt(["GPT-5 released", "Reactions to GPT-5"])
    assert "TITLE:" in p and "SUMMARY:" in p
    assert "- GPT-5 released" in p
    assert "- Reactions to GPT-5" in p


def test_parse_reply_extracts_both_fields():
    title, summary = parse_triage_reply(
        "TITLE: GPT-5 ships\nSUMMARY: OpenAI released GPT-5. Early users report big gains.",
        titles=["GPT-5 released"],
    )
    assert title == "GPT-5 ships"
    assert summary == "OpenAI released GPT-5. Early users report big gains."


def test_parse_reply_strips_leading_dashes_and_whitespace():
    title, summary = parse_triage_reply("TITLE:  - Foo\nSUMMARY:  - Bar baz.", titles=["x"])
    assert title == "Foo"
    assert summary == "Bar baz."


def test_parse_reply_no_markers_falls_back_to_first_title():
    title, summary = parse_triage_reply("just some prose with no markers", titles=["First headline"])
    assert title == "First headline"
    assert summary == "just some prose with no markers"


def test_parse_reply_summary_only_marker():
    title, summary = parse_triage_reply("SUMMARY: only a summary here", titles=["Fallback title"])
    assert title == "Fallback title"
    assert summary == "only a summary here"


def test_parse_reply_empty_with_no_titles_is_none():
    assert parse_triage_reply("", titles=[]) is None
    assert parse_triage_reply("   ", titles=[]) is None


def test_parse_reply_caps_lengths():
    long_summary = "x" * 5000
    title, summary = parse_triage_reply(f"TITLE: t\nSUMMARY: {long_summary}", titles=["h"])
    assert len(summary) <= 1500


# --- DB-backed -----------------------------------------------------------------------------

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


def _minimal_cfg():
    from app.config import Config

    return Config(default_cadence_s=86400)


def _make_cluster(session, *, status="new", score=None, summary=None, title_text="A headline"):
    """Insert a cluster (+ one titled item so the summarizer has signal). Returns the id."""
    import uuid

    from app.adapters.base import Item as AdapterItem, item_id
    from app.db.models import Cluster, Item as ItemModel
    from app.researcher.cluster import new_cluster_id
    from app.researcher.store import upsert_item_and_sighting

    cid = new_cluster_id()
    session.add(Cluster(id=cid, status=status, score=score, triage_summary=summary))
    session.flush()
    url = f"https://example.com/{uuid.uuid4().hex}"
    upsert_item_and_sighting(session, AdapterItem(url=url, title=title_text), "rss:a")
    session.flush()
    session.get(ItemModel, item_id(url)).cluster_id = cid
    session.flush()
    return cid


@pg_only
def test_select_candidates_only_new_unsummarized_ordered_by_score(session):
    low = _make_cluster(session, status="new", score=0.2)
    high = _make_cluster(session, status="new", score=0.9)
    summarized = _make_cluster(session, status="new", score=0.99, summary="has one")  # excluded: summarized
    sent = _make_cluster(session, status="sent", score=0.95)                          # excluded: not 'new'
    approved = _make_cluster(session, status="approved", score=0.95)                  # excluded: not 'new'

    # Large top_n so the seeded rows are never truncated away by leftover candidates, then scope
    # every assertion to THIS test's ids: a shared/non-pristine DB may already hold other 'new',
    # unsummarized clusters, and those are none of this test's business. The savepoint `session`
    # fixture isolates our writes, but the candidate query reads the whole table.
    ids = select_triage_candidates(session, top_n=100_000)
    # Of our seeded rows, only the two new + unsummarized appear, best score first.
    assert [i for i in ids if i in {low, high}] == [high, low]
    # The summarized and non-'new' seeded rows are excluded.
    for excluded in (summarized, sent, approved):
        assert excluded not in ids


@pg_only
def test_select_candidates_respects_top_n_and_min_score(session):
    a = _make_cluster(session, status="new", score=0.9)
    b = _make_cluster(session, status="new", score=0.8)
    thin = _make_cluster(session, status="new", score=0.1)
    seeded = {a, b, thin}

    # top_n caps the result set. A shared/non-pristine DB may hold other 'new' candidates, so
    # assert the cap is honored (exactly top_n rows) rather than exact membership.
    assert len(select_triage_candidates(session, top_n=1)) == 1

    # Best-first ordering, scoped to our seeded rows (independent of any interleaved leftovers).
    all_ids = select_triage_candidates(session, top_n=100_000)
    assert [i for i in all_ids if i in seeded] == [a, b, thin]

    # min_score floor excludes the thin one (and any NULL-score cluster); of our seeded rows
    # only the two scoring >= 0.5 survive.
    filtered = select_triage_candidates(session, top_n=100_000, min_score=0.5)
    assert [i for i in filtered if i in seeded] == [a, b]
    assert thin not in filtered


@pg_only
def test_summarize_writes_and_is_idempotent(session, monkeypatch):
    from app.db.models import Cluster
    import app.researcher.triage as triage

    monkeypatch.setattr(
        triage, "generate", lambda messages, role: "TITLE: Crisp title\nSUMMARY: A tidy blurb."
    )

    cid = _make_cluster(session, status="new", score=0.7)
    stats = summarize_pending_triage(session, _minimal_cfg())
    assert stats["selected"] >= 1 and stats["summarized"] >= 1

    cluster = session.get(Cluster, cid)
    assert cluster.triage_title == "Crisp title"
    assert cluster.triage_summary == "A tidy blurb."
    assert cluster.status == "new"  # summarizing never advances status (the bot does that)

    # Second pass: the now-summarized cluster is no longer a candidate -> nothing re-summarized.
    stats2 = summarize_pending_triage(session, _minimal_cfg())
    assert cid not in select_triage_candidates(session, top_n=100)
    assert stats2["summarized"] == 0


@pg_only
def test_summarize_never_overwrites_existing_summary(session, monkeypatch):
    from app.db.models import Cluster
    import app.researcher.triage as triage

    monkeypatch.setattr(triage, "generate", lambda messages, role: "TITLE: New\nSUMMARY: New blurb.")
    cid = _make_cluster(session, status="new", score=0.5, summary="original blurb")

    summarize_pending_triage(session, _minimal_cfg())
    assert session.get(Cluster, cid).triage_summary == "original blurb"
