"""The weekly digest (app.digest).

Pure tests for schedule parsing, prompt assembly, and the single model call (the model
boundary), and DB-backed tests (guarded by RUN_PG_TESTS) for the windowed/covered-marker query,
the create-article-+-link run, and the non-repetition guarantee (build plan Phase 6 Done:
two overlapping runs do not repeat a story).
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timedelta, timezone

import pytest

from app.digest import (
    DigestCluster,
    DigestResult,
    build_digest_prompt,
    parse_digest_schedule,
    run_digest,
    select_digest_clusters,
    summarize_digest,
)


# --- pure: schedule parsing -----------------------------------------------------------------


def test_parse_schedule_basic():
    assert parse_digest_schedule("sun 09:00") == {"day_of_week": "sun", "hour": 9, "minute": 0}


def test_parse_schedule_single_digit_hour_and_minute():
    assert parse_digest_schedule("mon 9:05") == {"day_of_week": "mon", "hour": 9, "minute": 5}


def test_parse_schedule_all_days():
    for day in ("mon", "tue", "wed", "thu", "fri", "sat", "sun"):
        assert parse_digest_schedule(f"{day} 23:59")["day_of_week"] == day


def test_parse_schedule_tolerates_whitespace_and_case():
    assert parse_digest_schedule("  SUN 09:00 ") == {"day_of_week": "sun", "hour": 9, "minute": 0}


@pytest.mark.parametrize(
    "bad",
    [
        "",
        "sun",
        "sunday 09:00",      # not a 3-letter token
        "xyz 09:00",         # unknown day
        "sun 0900",          # no colon
        "sun 24:00",         # hour out of range
        "sun 09:60",         # minute out of range
        "sun ab:cd",         # non-numeric time
        "sun 09:00 extra",   # too many parts
    ],
)
def test_parse_schedule_raises_on_garbage(bad):
    with pytest.raises(ValueError):
        parse_digest_schedule(bad)


def test_parse_schedule_non_string_raises():
    with pytest.raises(ValueError):
        parse_digest_schedule(None)  # type: ignore[arg-type]


# --- pure: prompt assembly ------------------------------------------------------------------


def _dc(title, url, summary="", score=None, cid=None):
    return DigestCluster(
        cluster_id=cid or f"cl:{uuid.uuid4().hex}",
        title=title,
        summary=summary,
        url=url,
        score=score,
    )


def test_build_prompt_includes_topic_titles_urls_and_grounding():
    clusters = [
        _dc("GPT-5 released", "https://ex.com/a", summary="OpenAI shipped GPT-5."),
        _dc("New Rust release", "https://ex.com/b"),
    ]
    p = build_digest_prompt("ai", clusters)
    # Topic named.
    assert "ai" in p
    # Each story's title + provenance url present.
    assert "GPT-5 released" in p
    assert "https://ex.com/a" in p
    assert "New Rust release" in p
    assert "https://ex.com/b" in p
    # A present summary is carried; an absent one is simply omitted (no padding).
    assert "OpenAI shipped GPT-5." in p
    # Grounding language (hard rule 2): no-invent, owner forms opinions, carry provenance.
    low = p.lower()
    assert "only" in low
    assert "do not invent" in low or "not invent" in low
    assert "opinion" in low
    assert "source" in low or "provenance" in low


def test_build_prompt_untitled_fallback_and_no_link():
    p = build_digest_prompt("dotnet", [_dc("", "")])
    assert "(untitled)" in p
    assert "(no link)" in p


def test_build_prompt_empty_clusters_is_safe():
    p = build_digest_prompt("ai", [])
    assert "(no stories)" in p


# --- the ONE model call (monkeypatched module-level generate) -------------------------------


def test_summarize_uses_role_and_caps(monkeypatch):
    import app.digest.run as run_mod

    seen = {}

    def fake_generate(messages, role):
        seen["role"] = role
        seen["content"] = messages[0]["content"]
        return "x" * 50000  # runaway reply

    monkeypatch.setenv("DIGEST_ROLE", "generation_high")
    monkeypatch.setenv("DIGEST_MAX_CHARS", "100")
    monkeypatch.setattr(run_mod, "generate", fake_generate)

    out = summarize_digest("ai", [_dc("A story", "https://ex.com/a")])
    # The logical role was passed through (env override honored), never a model id.
    assert seen["role"] == "generation_high"
    # The prompt the model saw is the built digest prompt (topic present).
    assert "ai" in seen["content"]
    # Capped at digest_max_chars().
    assert len(out) == 100


def test_summarize_empty_clusters_skips_model(monkeypatch):
    import app.digest.run as run_mod

    def boom(*a, **k):
        raise AssertionError("generate must not be called on an empty cluster set")

    monkeypatch.setattr(run_mod, "generate", boom)
    assert summarize_digest("ai", []) == ""


def test_summarize_default_role(monkeypatch):
    import app.digest.run as run_mod

    monkeypatch.delenv("DIGEST_ROLE", raising=False)
    seen = {}

    def fake_generate(messages, role):
        seen["role"] = role
        return "rollup text"

    monkeypatch.setattr(run_mod, "generate", fake_generate)
    out = summarize_digest("ai", [_dc("S", "https://ex.com/a")])
    assert seen["role"] == "generation"
    assert out == "rollup text"


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


def _digest_cfg(*, window_days=7, top_n=10, schedule="sun 09:00"):
    from app.config import Digest

    return Digest(schedule=schedule, window_days=window_days, top_n=top_n)


def _make_cluster(
    session,
    *,
    topic="ai",
    status="new",
    score=None,
    triage_title=None,
    triage_summary=None,
    created_at=None,
    item_title="A headline",
    item_url=None,
):
    """Insert a cluster (+ one titled item with a url so provenance has signal). Returns the id.

    `created_at` lets a test place a cluster inside/outside the rolling window. Mirrors the
    test_triage._make_cluster helper, adding topic/created_at/url control for the digest query.
    """
    from app.adapters.base import Item as AdapterItem, item_id
    from app.db.models import Cluster, Item as ItemModel
    from app.researcher.cluster import new_cluster_id
    from app.researcher.store import upsert_item_and_sighting

    cid = new_cluster_id()
    cluster = Cluster(
        id=cid,
        topic=topic,
        status=status,
        score=score,
        triage_title=triage_title,
        triage_summary=triage_summary,
    )
    if created_at is not None:
        cluster.created_at = created_at
    session.add(cluster)
    session.flush()

    url = item_url or f"https://example.com/{uuid.uuid4().hex}"
    upsert_item_and_sighting(session, AdapterItem(url=url, title=item_title), "rss:a")
    session.flush()
    session.get(ItemModel, item_id(url)).cluster_id = cid
    session.flush()
    return cid


def _link_to_article(session, cluster_id, *, status="published", piece_type="hot_news"):
    """Link a cluster to a (separately created) article — the covered-marker. Returns article id."""
    from app.db.models import Article, ArticleCluster
    from app.editor.article import new_article_id

    aid = new_article_id()
    session.add(Article(id=aid, piece_type=piece_type, status=status, current_draft="x"))
    session.add(ArticleCluster(article_id=aid, cluster_id=cluster_id))
    session.flush()
    return aid


@pg_only
def test_select_excludes_covered_clusters(session):
    topic = f"sel-{uuid.uuid4().hex[:8]}"
    uncovered = _make_cluster(session, topic=topic, score=0.5)
    covered = _make_cluster(session, topic=topic, score=0.9)  # higher score, but covered
    _link_to_article(session, covered)

    ids = [c.cluster_id for c in select_digest_clusters(session, topic, window_days=30, top_n=100)]
    assert uncovered in ids
    assert covered not in ids  # excluded despite the higher score (the covered-marker)


@pg_only
def test_select_includes_skipped_clusters(session):
    topic = f"skip-{uuid.uuid4().hex[:8]}"
    skipped = _make_cluster(session, topic=topic, status="skipped", score=0.5)
    new = _make_cluster(session, topic=topic, status="new", score=0.4)

    ids = [c.cluster_id for c in select_digest_clusters(session, topic, window_days=30, top_n=100)]
    # skip means "no standalone post", not "omit from the rollup" — both eligible.
    assert skipped in ids
    assert new in ids


@pg_only
def test_select_respects_window(session):
    topic = f"win-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc)
    in_window = _make_cluster(session, topic=topic, score=0.5, created_at=now - timedelta(days=3))
    out_window = _make_cluster(session, topic=topic, score=0.9, created_at=now - timedelta(days=20))

    ids = [c.cluster_id for c in select_digest_clusters(session, topic, window_days=7, top_n=100)]
    assert in_window in ids
    assert out_window not in ids  # older than the 7d window


@pg_only
def test_select_respects_topic(session):
    topic = f"top-{uuid.uuid4().hex[:8]}"
    other = f"other-{uuid.uuid4().hex[:8]}"
    mine = _make_cluster(session, topic=topic, score=0.5)
    theirs = _make_cluster(session, topic=other, score=0.9)

    ids = [c.cluster_id for c in select_digest_clusters(session, topic, window_days=30, top_n=100)]
    assert mine in ids
    assert theirs not in ids


@pg_only
def test_select_orders_by_score_and_caps_top_n(session):
    topic = f"ord-{uuid.uuid4().hex[:8]}"
    low = _make_cluster(session, topic=topic, score=0.2)
    high = _make_cluster(session, topic=topic, score=0.9)
    mid = _make_cluster(session, topic=topic, score=0.5)

    ordered = [c.cluster_id for c in select_digest_clusters(session, topic, window_days=30, top_n=100)]
    assert ordered == [high, mid, low]  # score DESC

    # top_n caps the set (best first).
    capped = select_digest_clusters(session, topic, window_days=30, top_n=2)
    assert [c.cluster_id for c in capped] == [high, mid]


@pg_only
def test_select_gathers_title_summary_url(session):
    topic = f"meta-{uuid.uuid4().hex[:8]}"
    url = f"https://example.com/{uuid.uuid4().hex}"
    cid = _make_cluster(
        session, topic=topic, score=0.5,
        triage_title="Triage headline", triage_summary="A tidy blurb.",
        item_title="Item headline", item_url=url,
    )
    (c,) = select_digest_clusters(session, topic, window_days=30, top_n=10)
    assert c.cluster_id == cid
    assert c.title == "Triage headline"   # triage_title wins
    assert c.summary == "A tidy blurb."
    assert c.url == url                    # representative item url for provenance


@pg_only
def test_select_falls_back_to_item_title_when_no_triage(session):
    topic = f"fb-{uuid.uuid4().hex[:8]}"
    cid = _make_cluster(session, topic=topic, score=0.5, item_title="Only item title")
    (c,) = select_digest_clusters(session, topic, window_days=30, top_n=10)
    assert c.cluster_id == cid
    assert c.title == "Only item title"  # no triage_title -> first item title
    assert c.summary == ""               # no triage_summary -> empty


@pg_only
def test_run_digest_creates_article_and_links(session, monkeypatch):
    import app.digest.run as run_mod
    from app.db.models import Article, ArticleCluster

    monkeypatch.setattr(run_mod, "generate", lambda messages, role: "## Weekly digest\n\n- story")

    topic = f"run-{uuid.uuid4().hex[:8]}"
    c1 = _make_cluster(session, topic=topic, score=0.9)
    c2 = _make_cluster(session, topic=topic, score=0.5)

    result = run_digest(session, topic, _digest_cfg(window_days=30, top_n=10))
    assert isinstance(result, DigestResult)
    assert result.topic == topic
    assert set(result.cluster_ids) == {c1, c2}
    assert result.rollup == "## Weekly digest\n\n- story"

    art = session.get(Article, result.article_id)
    assert art is not None
    assert art.piece_type == "digest"
    assert art.status == "drafting"
    assert art.current_draft == "## Weekly digest\n\n- story"

    # Every selected cluster is linked (the covered-marker).
    linked = session.execute(
        ArticleCluster.__table__.select().where(ArticleCluster.article_id == result.article_id)
    ).all()
    assert {row.cluster_id for row in linked} == {c1, c2}


@pg_only
def test_run_digest_empty_returns_none_no_article(session, monkeypatch):
    import app.digest.run as run_mod
    from app.db.models import Article

    def boom(*a, **k):
        raise AssertionError("generate must not be called when there are no eligible clusters")

    monkeypatch.setattr(run_mod, "generate", boom)

    topic = f"empty-{uuid.uuid4().hex[:8]}"  # a topic with no clusters at all
    before = {a for (a,) in session.execute(Article.__table__.select().with_only_columns(Article.id)).all()}
    result = run_digest(session, topic, _digest_cfg(window_days=30, top_n=10))
    assert result is None
    after = {a for (a,) in session.execute(Article.__table__.select().with_only_columns(Article.id)).all()}
    assert before == after  # no empty digest article created


@pg_only
def test_run_digest_non_repetition_over_overlapping_windows(session, monkeypatch):
    """Build plan Phase 6 Done: two consecutive runs over OVERLAPPING windows do not repeat a
    story. Run 1 links its clusters via article_clusters (the covered-marker); run 2 — over the
    same overlapping window — must select a DISJOINT set, because run 1's stories are now covered.
    """
    import app.digest.run as run_mod

    monkeypatch.setattr(run_mod, "generate", lambda messages, role: "rollup")

    topic = f"rep-{uuid.uuid4().hex[:8]}"
    # Five clusters, all inside a wide window so both runs re-scan the same overlap.
    cids = [_make_cluster(session, topic=topic, score=0.9 - i * 0.1) for i in range(5)]

    cfg = _digest_cfg(window_days=30, top_n=3)

    run1 = run_digest(session, topic, cfg)
    assert run1 is not None
    first_set = set(run1.cluster_ids)
    assert len(first_set) == 3  # top 3 by score

    run2 = run_digest(session, topic, cfg)
    assert run2 is not None
    second_set = set(run2.cluster_ids)

    # The crux: run 2 repeats NOTHING from run 1 (run 1's clusters are now covered).
    assert first_set.isdisjoint(second_set)
    # And run 2 picks up the remaining uncovered clusters.
    assert second_set == set(cids) - first_set

    # A third run has nothing left -> None, no further article.
    run3 = run_digest(session, topic, cfg)
    assert run3 is None
