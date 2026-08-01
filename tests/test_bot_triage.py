"""Gate-1 bot core (app.bot.triage) — SDK-free logic.

Pure tests for callback_data encode/parse + message rendering, and DB-backed tests (guarded
by RUN_PG_TESTS) for the exactly-once claim, the decision transitions, token resolution, and
delivery selection.
"""
from __future__ import annotations

import os

import pytest

from app.bot.triage import (
    ACTION_APPROVE,
    ACTION_SKIP,
    cluster_token,
    encode_callback,
    format_message,
    parse_callback,
)


# --- pure: callback_data + rendering -------------------------------------------------------


def test_callback_roundtrip_and_within_telegram_limit():
    cid = "cl:" + "ab12cd34" * 8  # 64-hex body, the real cluster-id shape
    data = encode_callback(ACTION_APPROVE, cid)
    assert len(data.encode("utf-8")) <= 64           # Telegram's callback_data limit
    action, token = parse_callback(data)
    assert action == ACTION_APPROVE
    assert token == cluster_token(cid)
    assert cid.startswith("cl:" + token)             # token is a real prefix of the id body


def test_token_is_bounded_and_skip_action_encodes():
    cid = "cl:" + "f" * 64
    assert len(cluster_token(cid)) == 16
    assert encode_callback(ACTION_SKIP, cid).startswith("s:")


def test_encode_rejects_unknown_action():
    with pytest.raises(ValueError):
        encode_callback("x", "cl:deadbeef")


def test_parse_rejects_junk():
    assert parse_callback(None) is None
    assert parse_callback("") is None
    assert parse_callback("nope") is None          # no colon
    assert parse_callback("z:abc") is None         # unknown action
    assert parse_callback("a:") is None            # empty token


def test_format_message_escapes_and_includes_fields():
    class _C:
        triage_title = "Tooling <broken> & cheap"
        triage_summary = "A & B happened."
        topic = "ai"
        score = 0.4237

    msg = format_message(_C())
    assert "<b>Tooling &lt;broken&gt; &amp; cheap</b>" in msg
    assert "A &amp; B happened." in msg
    assert "topic: ai" in msg
    assert "0.42" in msg


# --- DB-backed: claim / decide / resolve / select ------------------------------------------

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


def _add_cluster(session, *, status="new", score=None, summary="A blurb", cid=None):
    from app.db.models import Cluster
    from app.researcher.cluster import new_cluster_id

    cid = cid or new_cluster_id()
    session.add(Cluster(id=cid, status=status, score=score, triage_title="t", triage_summary=summary))
    session.commit()
    return cid


@pg_only
def test_claim_for_send_is_exactly_once(session):
    from app.bot.triage import claim_for_send
    from app.db.models import Cluster

    cid = _add_cluster(session, status="new")
    assert claim_for_send(session, cid) is True            # first claim wins
    assert session.get(Cluster, cid).status == "sent"
    assert claim_for_send(session, cid) is False           # second claim loses (no longer 'new')
    assert session.get(Cluster, cid).status == "sent"


@pg_only
def test_revert_to_new_only_from_sent(session):
    from app.bot.triage import claim_for_send, revert_to_new
    from app.db.models import Cluster

    cid = _add_cluster(session, status="new")
    claim_for_send(session, cid)
    revert_to_new(session, cid)
    assert session.get(Cluster, cid).status == "new"       # back in the queue for next sweep

    # Revert must never resurrect a decided story.
    decided = _add_cluster(session, status="approved")
    revert_to_new(session, decided)
    assert session.get(Cluster, decided).status == "approved"


@pg_only
def test_decide_transitions_and_is_idempotent(session):
    from app.bot.triage import decide
    from app.db.models import Cluster

    # Approve from 'sent' -> 'approved'; a second decision is a no-op (already terminal).
    a = _add_cluster(session, status="sent")
    assert decide(session, a, approve=True) == "approved"
    assert session.get(Cluster, a).status == "approved"
    assert decide(session, a, approve=False) is None       # can't flip a decided story
    assert session.get(Cluster, a).status == "approved"

    # Skip from 'sent' -> 'skipped'.
    s = _add_cluster(session, status="sent")
    assert decide(session, s, approve=False) == "skipped"
    assert session.get(Cluster, s).status == "skipped"

    # Defensive: a tap can also decide a still-'new' story (no double delivery harm).
    n = _add_cluster(session, status="new")
    assert decide(session, n, approve=True) == "approved"


@pg_only
def test_resolve_by_token_unique_missing_and_ambiguous(session):
    from app.bot.triage import resolve_by_token, cluster_token

    cid = _add_cluster(session, status="new", cid="cl:" + "abcdef0123456789" + "00" * 24)
    token = cluster_token(cid)
    assert resolve_by_token(session, token) == cid          # unique prefix resolves
    assert resolve_by_token(session, "ffffffffffffffff") is None   # no match

    # Two clusters sharing the same 16-hex prefix -> ambiguous -> None (a safe no-op).
    shared = "abcdef0123456789"
    _add_cluster(session, status="new", cid="cl:" + shared + "11" * 24)
    assert resolve_by_token(session, shared) is None


@pg_only
def test_select_deliverable_only_new_with_summary_ordered(session):
    from app.bot.triage import select_deliverable

    high = _add_cluster(session, status="new", score=0.9, summary="s")
    low = _add_cluster(session, status="new", score=0.1, summary="s")
    _add_cluster(session, status="new", score=0.99, summary=None)   # excluded: no summary
    _add_cluster(session, status="sent", score=0.99, summary="s")   # excluded: already delivered

    ids = [c.id for c in select_deliverable(session, limit=10)]
    assert ids == [high, low]
    assert [c.id for c in select_deliverable(session, limit=1)] == [high]
