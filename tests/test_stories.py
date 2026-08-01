"""Unified "Stories" read layer (Phase 8 increment-1, backend half).

The dashboard is a single filterable Stories list, computed entirely in the read layer
(`app/web/queries.load_stories` / `unified_status_counts`) — no schema change. A Story is one of
three kinds:
  - "cluster":  an UNDRAFTED cluster (no own non-digest article); status = the cluster's.
  - "article":  a NON-digest article + its single linked cluster; status = the article's.
  - "digest":   a piece_type='digest' article spanning many clusters; status = the article's.
A cluster that grew its own hot_news/project_post draft appears ONCE as the article (NOT also a
cluster). A cluster merely COVERED by a digest still appears as a cluster row with in_digest=True,
keeping the cluster's OWN status (it is not relabelled to the digest's). The blended `score` lives
in the model but is intentionally NOT surfaced on StoryRow.

DB-backed and guarded by RUN_PG_TESTS (these are aggregate reads over real Postgres rows). Kept in
its own file so it doesn't clash with the parallel frontend slice editing the UI / test_web.py.
"""
from __future__ import annotations

import dataclasses
import os
import uuid

import pytest

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


# --- builders --------------------------------------------------------------------------------


def _make_cluster(session, *, status="new", topic="ai", triage_title="A story", score=0.5):
    from app.db.models import Cluster
    from app.researcher.cluster import new_cluster_id

    cid = new_cluster_id()
    session.add(Cluster(id=cid, status=status, topic=topic, score=score,
                        triage_title=triage_title, triage_summary="s"))
    session.flush()
    return cid


def _make_article(session, *, status="drafting", piece_type="hot_news", draft="# A\n\nbody"):
    from app.db.models import Article
    from app.editor.article import new_article_id

    aid = new_article_id()
    session.add(Article(id=aid, piece_type=piece_type, status=status, current_draft=draft))
    session.flush()
    return aid


def _link(session, article_id, cluster_id):
    from app.db.models import ArticleCluster

    session.add(ArticleCluster(article_id=article_id, cluster_id=cluster_id))
    session.flush()


def _item_in_cluster(session, cluster_id, *, url, title, source_keys):
    """One item in a cluster, observed by the given sighting source_keys (cross-source)."""
    from app.adapters.base import Item as AdapterItem, item_id
    from app.db.models import Item as ItemModel
    from app.researcher.store import upsert_item_and_sighting

    for sk in source_keys:
        upsert_item_and_sighting(session, AdapterItem(url=url, title=title), sk)
    session.flush()
    item = session.get(ItemModel, item_id(url))
    item.cluster_id = cluster_id
    session.flush()
    return item.id


# --- kind / status semantics -----------------------------------------------------------------


@pg_only
def test_undrafted_cluster_is_kind_cluster_with_its_status(session):
    from app.web.queries import load_stories

    cid = _make_cluster(session, status="approved", triage_title="Raw story")
    session.commit()

    rows = [r for r in load_stories(session) if r.cluster_id == cid]
    assert len(rows) == 1
    (r,) = rows
    assert r.kind == "cluster"
    assert r.effective_status == "approved"   # the cluster's own status
    assert r.title == "Raw story"
    assert r.key == cid
    assert r.cluster_id == cid
    assert r.article_id is None
    assert r.in_digest is False


@pg_only
def test_undrafted_cluster_title_falls_back(session):
    """No triage_title AND no item -> '(untitled)'."""
    from app.web.queries import load_stories

    cid = _make_cluster(session, status="new", triage_title=None)
    session.commit()

    (r,) = [r for r in load_stories(session) if r.cluster_id == cid]
    assert r.title == "(untitled)"
    assert r.topic == "ai"


@pg_only
def test_write_on_digest_covered_cluster_creates_own_article_not_the_digest(session):
    """Regression: a cluster only COVERED by a digest has no own draft, so Write /
    create_article_for_cluster must mint a FRESH hot_news article — never reopen + redraft the
    digest (which would clobber the rollup)."""
    from app.db.models import Article
    from app.editor.article import create_article_for_cluster, existing_article_for_cluster

    cid = _make_cluster(session, status="approved", triage_title="Covered story")
    digest_aid = _make_article(session, status="drafting", piece_type="digest",
                               draft="# Weekly digest\n\n- covered story")
    _link(session, digest_aid, cid)  # the digest "covered" marker
    session.commit()

    # A digest-covered cluster has NO own draft.
    assert existing_article_for_cluster(session, cid) is None

    new_aid = create_article_for_cluster(session, cid)  # defaults to hot_news
    assert new_aid != digest_aid
    assert session.get(Article, new_aid).piece_type == "hot_news"
    # The digest is untouched.
    digest = session.get(Article, digest_aid)
    assert digest.piece_type == "digest"
    assert digest.current_draft == "# Weekly digest\n\n- covered story"


@pg_only
def test_undrafted_cluster_title_falls_back_to_item_title(session):
    """No triage_title but the cluster has an item -> show the item's title, not '(untitled)'."""
    from app.web.queries import load_stories

    cid = _make_cluster(session, status="new", triage_title=None)
    _item_in_cluster(session, cid, url="https://ex.com/headline",
                     title="A Real Item Headline", source_keys=['rss:{"url":"x"}'])
    session.commit()

    (r,) = [r for r in load_stories(session) if r.cluster_id == cid]
    assert r.title == "A Real Item Headline"
    assert "rss" in r.source_types


@pg_only
def test_hot_news_article_is_one_article_row_not_also_a_cluster(session):
    """A cluster with its own hot_news article appears ONCE as kind=article (not also a cluster).
    Title comes from the draft's H1; status is the article's."""
    from app.web.queries import load_stories

    cid = _make_cluster(session, status="approved", triage_title="Cluster title", topic="llms")
    aid = _make_article(session, status="drafting", piece_type="hot_news",
                        draft="# Drafted Headline\n\nThe body.")
    _link(session, aid, cid)
    url = f"https://ex.com/a/{uuid.uuid4().hex}"
    _item_in_cluster(session, cid, url=url, title="src",
                     source_keys=['hn:{"sub":"x"}', 'x_user:{"handle":"y"}'])
    session.commit()

    rows = load_stories(session)
    # The cluster does NOT appear as its own cluster row.
    assert not any(r.kind == "cluster" and r.cluster_id == cid for r in rows)
    article_rows = [r for r in rows if r.article_id == aid]
    assert len(article_rows) == 1
    (r,) = article_rows
    assert r.kind == "article"
    assert r.effective_status == "drafting"     # the article's status, not the cluster's
    assert r.title == "Drafted Headline"        # first H1 of the draft
    assert r.key == aid
    assert r.cluster_id == cid
    assert r.topic == "llms"                    # from the linked cluster
    # source_types + original_url come from the linked cluster's items.
    assert r.source_types == ["hn", "x_user"]
    assert r.original_url == url
    assert r.in_digest is False


@pg_only
def test_article_title_falls_back_to_cluster_then_untitled(session):
    from app.web.queries import load_stories

    # Draft with no H1 -> falls back to the linked cluster's triage_title.
    cid = _make_cluster(session, triage_title="Cluster headline")
    aid = _make_article(session, piece_type="hot_news", draft="no heading here\n\njust body")
    _link(session, aid, cid)
    session.commit()
    (r,) = [r for r in load_stories(session) if r.article_id == aid]
    assert r.title == "Cluster headline"

    # No H1 and no triage_title -> "(untitled)".
    cid2 = _make_cluster(session, triage_title=None)
    aid2 = _make_article(session, piece_type="project_post", draft="body only")
    _link(session, aid2, cid2)
    session.commit()
    (r2,) = [r for r in load_stories(session) if r.article_id == aid2]
    assert r2.title == "(untitled)"
    assert r2.kind == "article"


@pg_only
def test_digest_is_its_own_kind_digest_row(session):
    from app.web.queries import load_stories

    aid = _make_article(session, status="pre_publish", piece_type="digest",
                        draft="# Weekly Roundup\n\n- a\n- b")
    session.commit()

    (r,) = [r for r in load_stories(session) if r.article_id == aid]
    assert r.kind == "digest"
    assert r.effective_status == "pre_publish"
    assert r.title == "Weekly Roundup"
    assert r.key == aid
    assert r.cluster_id is None
    assert r.article_id == aid


# --- Phase 10: flagship (own-material) articles ---------------------------------------------


def _make_flagship(session, *, piece_type="tech_explainer", draft="# Explainer\n\nbody",
                   owner_url=None):
    """A flagship article (no cluster) with one owner-material source. Returns the article id."""
    from app.db.models import Article
    from app.editor.sources import attach_owner_source, create_flagship_article

    aid = create_flagship_article(session, piece_type=piece_type)
    # Set the draft (create_flagship_article leaves current_draft None).
    session.get(Article, aid).current_draft = draft
    attach_owner_source(
        session, aid, kind=("url" if owner_url else "text"),
        content="owner material body", title=(None if owner_url else "My note"), url=owner_url,
    )
    session.flush()
    return aid


@pg_only
def test_flagship_article_is_kind_article_with_owner_source_type(session):
    """A flagship article (non-digest, NO linked cluster) surfaces as a kind='article' row with
    source_types=['owner'], topic='—', article_id set, cluster_id None."""
    from app.web.queries import load_stories

    aid = _make_flagship(session, draft="# My Explainer\n\nteach-down body")
    session.commit()

    (r,) = [r for r in load_stories(session) if r.article_id == aid]
    assert r.kind == "article"
    assert r.source_types == ["owner"]
    assert r.topic == "—"
    assert r.cluster_id is None
    assert r.article_id == aid
    assert r.title == "My Explainer"  # from the draft H1
    assert r.in_digest is False


@pg_only
def test_flagship_article_original_url_is_first_owner_url(session):
    """A flagship article's original_url is its first owner-source url (or None for text-only)."""
    from app.web.queries import load_stories

    url = f"https://ex.com/owner/{uuid.uuid4().hex}"
    aid = _make_flagship(session, owner_url=url)
    session.commit()
    (r,) = [r for r in load_stories(session) if r.article_id == aid]
    assert r.original_url == url

    # Text-only flagship → no url.
    aid2 = _make_flagship(session)
    session.commit()
    (r2,) = [r for r in load_stories(session) if r.article_id == aid2]
    assert r2.original_url is None


@pg_only
def test_flagship_article_counts_under_owner_source(session):
    """source_counts surfaces a flagship article under the 'owner' source type; it also contributes
    to its status count in unified_status_counts."""
    from app.web.queries import source_counts, unified_status_counts

    from app.db.models import Article

    aid = _make_flagship(session, piece_type="tech_explainer")
    session.get(Article, aid).status = "drafting"
    session.commit()

    assert source_counts(session).get("owner", 0) >= 1
    assert source_counts(session, status="drafting").get("owner", 0) >= 1
    # It contributes to the drafting status bucket.
    assert unified_status_counts(session)["drafting"] >= 1
    assert unified_status_counts(session, source="owner")["drafting"] >= 1


@pg_only
def test_digest_title_falls_back_to_weekly_digest(session):
    from app.web.queries import load_stories

    aid = _make_article(session, piece_type="digest", draft="no heading\n\njust a body")
    session.commit()
    (r,) = [r for r in load_stories(session) if r.article_id == aid]
    assert r.title == "Weekly digest"


@pg_only
def test_cluster_covered_by_digest_stays_cluster_with_indigest(session):
    """A cluster COVERED by a digest still appears as kind=cluster, in_digest=True, keeping its OWN
    status — it is NOT relabelled to the digest's status and NOT hidden."""
    from app.web.queries import load_stories

    cid = _make_cluster(session, status="sent", triage_title="Covered story")
    digest_aid = _make_article(session, status="published", piece_type="digest",
                               draft="# Digest\n\nrollup")
    _link(session, digest_aid, cid)   # the digest covers this cluster
    session.commit()

    rows = load_stories(session)
    cluster_rows = [r for r in rows if r.cluster_id == cid and r.kind == "cluster"]
    assert len(cluster_rows) == 1
    (cr,) = cluster_rows
    assert cr.kind == "cluster"
    assert cr.in_digest is True
    assert cr.effective_status == "sent"   # the cluster's status, NOT "published"
    assert cr.article_id is None
    # And the digest still has its OWN row.
    digest_rows = [r for r in rows if r.article_id == digest_aid and r.kind == "digest"]
    assert len(digest_rows) == 1
    assert digest_rows[0].effective_status == "published"


@pg_only
def test_source_types_and_original_url_deterministic(session):
    """source_types = sorted distinct prefixes; original_url = the lowest-id item's url (stable)."""
    from app.web.queries import load_stories

    cid = _make_cluster(session, status="approved")
    # Two items in the cluster; original_url must be deterministic (lowest item id).
    url1 = f"https://ex.com/one/{uuid.uuid4().hex}"
    url2 = f"https://ex.com/two/{uuid.uuid4().hex}"
    id1 = _item_in_cluster(session, cid, url=url1, title="One",
                           source_keys=['rss:{"url":"a"}'])
    id2 = _item_in_cluster(session, cid, url=url2, title="Two",
                           source_keys=['github:{"repo":"b"}', 'hn:{"sub":"c"}'])
    session.commit()

    (r,) = [r for r in load_stories(session) if r.cluster_id == cid and r.kind == "cluster"]
    assert r.source_types == ["github", "hn", "rss"]   # distinct, sorted across both items
    expected_url = url1 if id1 < id2 else url2          # the lowest item id's url
    assert r.original_url == expected_url


@pg_only
def test_cluster_with_no_items_has_empty_sources_and_no_url(session):
    from app.web.queries import load_stories

    cid = _make_cluster(session, status="new")
    session.commit()
    (r,) = [r for r in load_stories(session) if r.cluster_id == cid]
    assert r.source_types == []
    assert r.original_url is None


# --- filtering + counts ----------------------------------------------------------------------


@pg_only
def test_status_filter_returns_only_matching_rows(session):
    from app.web.queries import load_stories

    c_new = _make_cluster(session, status="new", triage_title="new one")
    c_appr = _make_cluster(session, status="approved", triage_title="approved one")
    a_draft = _make_article(session, status="drafting", piece_type="hot_news",
                            draft="# Drafting one")
    _link(session, a_draft, _make_cluster(session, status="approved"))
    session.commit()

    only_new = load_stories(session, status="new")
    assert all(r.effective_status == "new" for r in only_new)
    assert any(r.cluster_id == c_new for r in only_new)
    assert not any(r.cluster_id == c_appr for r in only_new)

    only_drafting = load_stories(session, status="drafting")
    assert all(r.effective_status == "drafting" for r in only_drafting)
    assert any(r.article_id == a_draft for r in only_drafting)

    # status=None returns everything (a superset of any single-status filter).
    everything = load_stories(session)
    assert len(everything) >= len(only_new) + len(only_drafting)


@pg_only
def test_unified_status_counts_zero_filled_and_sums_correctly(session):
    from app.web.queries import STATUS_SPECTRUM, load_stories, unified_status_counts

    # A clean slice of rows across several statuses.
    _make_cluster(session, status="new")
    _make_cluster(session, status="new")
    _make_cluster(session, status="skipped")
    a = _make_article(session, status="pre_publish", piece_type="hot_news", draft="# x")
    _link(session, a, _make_cluster(session, status="approved"))
    d = _make_article(session, status="published", piece_type="digest", draft="# d")
    session.commit()

    counts = unified_status_counts(session)
    # Every spectrum status is present (zero-filled) and in lifecycle order.
    assert list(counts.keys())[: len(STATUS_SPECTRUM)] == list(STATUS_SPECTRUM)
    assert set(STATUS_SPECTRUM).issubset(counts.keys())

    # The counts sum to the total story count, and match a recomputation from load_stories.
    rows = load_stories(session)
    assert sum(counts.values()) == len(rows)
    from collections import Counter
    recomputed = Counter(r.effective_status for r in rows)
    for status, n in recomputed.items():
        assert counts[status] == n
    # Per-status filter length equals the count.
    for status in STATUS_SPECTRUM:
        assert len(load_stories(session, status=status)) == counts[status]


@pg_only
def test_source_filter_returns_only_matching_source_rows(session):
    """load_stories(source="rss") returns only stories whose source_types contains "rss"."""
    from app.web.queries import load_stories

    c_rss = _make_cluster(session, status="new", triage_title="rss story")
    _item_in_cluster(session, c_rss, url=f"https://ex.com/r/{uuid.uuid4().hex}", title="r",
                     source_keys=['rss:{"url":"a"}'])
    c_hn = _make_cluster(session, status="new", triage_title="hn story")
    _item_in_cluster(session, c_hn, url=f"https://ex.com/h/{uuid.uuid4().hex}", title="h",
                     source_keys=['hn:{"sub":"b"}'])
    session.commit()

    only_rss = load_stories(session, source="rss")
    assert all("rss" in r.source_types for r in only_rss)
    assert any(r.cluster_id == c_rss for r in only_rss)
    assert not any(r.cluster_id == c_hn for r in only_rss)

    only_hn = load_stories(session, source="hn")
    assert all("hn" in r.source_types for r in only_hn)
    assert any(r.cluster_id == c_hn for r in only_hn)
    assert not any(r.cluster_id == c_rss for r in only_hn)

    # source=None returns everything (a superset of any single-source filter).
    everything = load_stories(session)
    assert any(r.cluster_id == c_rss for r in everything)
    assert any(r.cluster_id == c_hn for r in everything)


@pg_only
def test_digest_excluded_by_any_source_filter(session):
    """A digest (source_types=[]) matches no source filter — only "All" (source=None)."""
    from app.web.queries import load_stories

    c_rss = _make_cluster(session, status="new", triage_title="rss story")
    _item_in_cluster(session, c_rss, url=f"https://ex.com/r/{uuid.uuid4().hex}", title="r",
                     source_keys=['rss:{"url":"a"}'])
    d = _make_article(session, status="published", piece_type="digest", draft="# d")
    session.commit()

    rss_rows = load_stories(session, source="rss")
    assert not any(r.article_id == d for r in rss_rows)   # the digest is excluded
    assert any(r.cluster_id == c_rss for r in rss_rows)
    # source=None DOES include the digest.
    assert any(r.article_id == d for r in load_stories(session))


@pg_only
def test_status_and_source_filters_and_together(session):
    from app.web.queries import load_stories

    c_new_rss = _make_cluster(session, status="new", triage_title="new rss")
    _item_in_cluster(session, c_new_rss, url=f"https://ex.com/a/{uuid.uuid4().hex}", title="a",
                     source_keys=['rss:{"url":"a"}'])
    c_new_hn = _make_cluster(session, status="new", triage_title="new hn")
    _item_in_cluster(session, c_new_hn, url=f"https://ex.com/b/{uuid.uuid4().hex}", title="b",
                     source_keys=['hn:{"sub":"b"}'])
    c_appr_rss = _make_cluster(session, status="approved", triage_title="approved rss")
    _item_in_cluster(session, c_appr_rss, url=f"https://ex.com/c/{uuid.uuid4().hex}", title="c",
                     source_keys=['rss:{"url":"c"}'])
    session.commit()

    both = load_stories(session, status="new", source="rss")
    assert all(r.effective_status == "new" and "rss" in r.source_types for r in both)
    assert any(r.cluster_id == c_new_rss for r in both)
    # The status mismatch (approved/rss) and the source mismatch (new/hn) are both excluded.
    assert not any(r.cluster_id == c_appr_rss for r in both)
    assert not any(r.cluster_id == c_new_hn for r in both)


@pg_only
def test_source_counts_per_source_over_status_filtered_and_multivalued(session):
    """source_counts(status="new") counts per source over new stories; a story with two source types
    counts toward BOTH (so per-source counts need not sum to the story total)."""
    from app.web.queries import load_stories, source_counts

    # A new story observed by two source types -> counts toward rss AND hn.
    c_multi = _make_cluster(session, status="new", triage_title="multi")
    _item_in_cluster(session, c_multi, url=f"https://ex.com/m/{uuid.uuid4().hex}", title="m",
                     source_keys=['rss:{"url":"a"}', 'hn:{"sub":"b"}'])
    # Another new story, rss only.
    c_rss = _make_cluster(session, status="new", triage_title="rss only")
    _item_in_cluster(session, c_rss, url=f"https://ex.com/r/{uuid.uuid4().hex}", title="r",
                     source_keys=['rss:{"url":"c"}'])
    # An approved story (different status) — excluded by status="new".
    c_appr = _make_cluster(session, status="approved", triage_title="approved hn")
    _item_in_cluster(session, c_appr, url=f"https://ex.com/h/{uuid.uuid4().hex}", title="h",
                     source_keys=['hn:{"sub":"d"}'])
    # A digest contributes nothing (source_types=[]).
    _make_article(session, status="new", piece_type="digest", draft="# d")
    session.commit()

    counts = source_counts(session, status="new")
    # rss: c_multi + c_rss = 2; hn: c_multi only (c_appr is not "new") = 1.
    assert counts["rss"] == 2
    assert counts["hn"] == 1

    # Each source's count equals load_stories(status="new", source=…) length — cross-filter holds.
    new_rows = load_stories(session, status="new")
    for source, n in counts.items():
        assert len(load_stories(session, status="new", source=source)) == n
    # The multi-valued story makes the per-source counts exceed the story total here.
    assert sum(counts.values()) > len([r for r in new_rows if r.source_types])
    # No fixed universe / no zero-fill: only present sources are keys, and no digest key.
    assert set(counts.keys()) == {"rss", "hn"}


@pg_only
def test_unified_status_counts_cross_filtered_by_source(session):
    """unified_status_counts(source="rss") restricts the status counts to rss stories (still
    zero-filled over STATUS_SPECTRUM)."""
    from app.web.queries import STATUS_SPECTRUM, load_stories, unified_status_counts

    c_new_rss = _make_cluster(session, status="new", triage_title="new rss")
    _item_in_cluster(session, c_new_rss, url=f"https://ex.com/a/{uuid.uuid4().hex}", title="a",
                     source_keys=['rss:{"url":"a"}'])
    c_appr_rss = _make_cluster(session, status="approved", triage_title="approved rss")
    _item_in_cluster(session, c_appr_rss, url=f"https://ex.com/b/{uuid.uuid4().hex}", title="b",
                     source_keys=['rss:{"url":"b"}'])
    # An hn story — excluded by source="rss".
    c_new_hn = _make_cluster(session, status="new", triage_title="new hn")
    _item_in_cluster(session, c_new_hn, url=f"https://ex.com/c/{uuid.uuid4().hex}", title="c",
                     source_keys=['hn:{"sub":"c"}'])
    session.commit()

    counts = unified_status_counts(session, source="rss")
    # Still zero-filled over the full spectrum, in lifecycle order.
    assert list(counts.keys())[: len(STATUS_SPECTRUM)] == list(STATUS_SPECTRUM)
    # Only rss stories are counted: the new hn story does NOT inflate "new".
    assert counts["new"] == 1
    assert counts["approved"] == 1
    # Each bucket equals load_stories(status=…, source="rss") length — cross-filter holds.
    for status in STATUS_SPECTRUM:
        assert len(load_stories(session, status=status, source="rss")) == counts[status]
    # Sums to the rss-only story total.
    assert sum(counts.values()) == len(load_stories(session, source="rss"))


# --- ordering --------------------------------------------------------------------------------


@pg_only
def test_rows_ordered_by_updated_at_desc(session):
    """Newest activity first across kinds, by the row's OWN updated_at."""
    import time
    from app.web.queries import load_stories

    c_old = _make_cluster(session, status="new", triage_title="old cluster")
    session.commit()
    time.sleep(0.01)
    a_new = _make_article(session, status="drafting", piece_type="hot_news",
                          draft="# newest article")
    _link(session, a_new, _make_cluster(session, status="approved"))
    session.commit()

    rows = load_stories(session)
    keys = [r.key for r in rows]
    # The article touched last must come before the older cluster.
    assert keys.index(a_new) < keys.index(c_old)


# --- contract guard --------------------------------------------------------------------------


def test_storyrow_has_no_score_attribute():
    """StoryRow must NOT surface the blended score (contract). DB-free guard."""
    from app.web.queries import StoryRow

    field_names = {f.name for f in dataclasses.fields(StoryRow)}
    assert "score" not in field_names
    assert field_names == {
        "key", "kind", "effective_status", "title", "topic",
        "source_types", "original_url", "in_digest", "cluster_id", "article_id",
    }
