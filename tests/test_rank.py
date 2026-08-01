"""Unit tests for cluster ranking (app.researcher.rank) — pure, no DB, no network.

These pin the deterministic ranking arithmetic that needs no Postgres:
  - per-platform native normalization (HN points and Reddit scores normalized SEPARATELY,
    so a small HN-points cluster isn't crushed by a large Reddit-score cluster),
  - the DISTINCT-source frequency count and its 0..1 normalization,
  - recency exponential half-life decay (newer > older, monotonic, half-life == 0.5),
  - the blend math + the weight-override seam.

The DB-backed proof (scores populate, ordering is sane) lives below, RUN_PG_TESTS-gated.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import pytest

import app.researcher.rank as rank
from app.researcher.rank import (
    DEFAULT_RECENCY_HALFLIFE_DAYS,
    DEFAULT_W_FREQUENCY,
    DEFAULT_W_NATIVE,
    DEFAULT_W_RECENCY,
    ClusterFeatures,
    native_rating,
    platform_of,
    recency_score,
    score_clusters,
)

UTC = timezone.utc
NOW = datetime(2026, 6, 14, 12, 0, 0, tzinfo=UTC)


# --- platform extraction from source_key ----------------------------------------------

def test_platform_is_the_source_key_prefix():
    # source_key is `<type>:` + json identity body (app.config.derive_source_key); the
    # platform is the substring before the first ':'.
    assert platform_of('hn:{"listing":"top"}') == "hn"
    assert platform_of('reddit_sub:{"id":"r/python","listing":"top"}') == "reddit_sub"
    assert platform_of('rss:{"url":"https://blog/feed"}') == "rss"
    assert platform_of("x_user:{}") == "x_user"


# --- native rating extraction ---------------------------------------------------------

def test_native_rating_picks_platform_primary_key():
    assert native_rating({"points": 120, "comments": 9}, "hn") == 120.0
    assert native_rating({"score": 340, "num_comments": 50}, "reddit_sub") == 340.0
    assert native_rating({"likes": 12}, "x_user") == 12.0


def test_native_rating_is_none_for_no_native_platforms():
    # rss/github/arxiv carry no native rating -> None (excluded from native normalization).
    assert native_rating({}, "rss") is None
    assert native_rating({"anything": 1}, "github") is None
    assert native_rating({"foo": 1}, "arxiv") is None


def test_native_rating_none_when_key_absent_or_nonnumeric():
    assert native_rating({"comments": 9}, "hn") is None        # comments is not the rating
    assert native_rating(None, "hn") is None
    assert native_rating({"points": "lots"}, "hn") is None     # non-numeric
    assert native_rating({"points": True}, "hn") is None       # bool is never a rating


# --- recency decay --------------------------------------------------------------------

def test_recency_is_one_at_age_zero_and_for_future():
    assert recency_score(NOW, NOW, halflife_days=3.0) == 1.0
    # Clock skew / future-dated item clamps to fresh, never > 1.
    assert recency_score(NOW + timedelta(hours=5), NOW, halflife_days=3.0) == 1.0


def test_recency_halves_at_one_halflife():
    one_halflife_ago = NOW - timedelta(days=3.0)
    assert recency_score(one_halflife_ago, NOW, halflife_days=3.0) == pytest.approx(0.5)
    two_halflives_ago = NOW - timedelta(days=6.0)
    assert recency_score(two_halflives_ago, NOW, halflife_days=3.0) == pytest.approx(0.25)


def test_recency_is_monotonic_newer_scores_higher():
    ages = [0, 1, 2, 4, 8, 16]  # days old
    scores = [recency_score(NOW - timedelta(days=d), NOW, halflife_days=3.0) for d in ages]
    # Strictly decreasing as items get older.
    assert all(earlier > later for earlier, later in zip(scores, scores[1:]))
    assert all(0.0 <= s <= 1.0 for s in scores)


def test_recency_no_time_basis_scores_zero():
    # A cluster with no published_at and no fetched_at can't be claimed fresh.
    assert recency_score(None, NOW) == 0.0


def test_recency_handles_naive_datetime():
    # A naive timestamp (DB can hand one back) is treated as UTC, not crashed on.
    naive = (NOW - timedelta(days=3.0)).replace(tzinfo=None)
    assert recency_score(naive, NOW, halflife_days=3.0) == pytest.approx(0.5)


# --- per-platform native normalization ------------------------------------------------

def _recency_neutralized(features):
    """Score the set with recency weighted out (newest_at all == NOW) so we can assert on
    the native/frequency axes in isolation."""
    return score_clusters(features, NOW)


def test_native_normalized_per_platform_not_cross_platform():
    """HN points (~hundreds) and Reddit scores (~thousands) must be normalized WITHIN their
    own platform. A cluster that tops HN should reach the native max (1.0 on its axis) even
    though its raw points are far below another cluster's raw Reddit score."""
    # All same recency + same frequency so only the native axis differs.
    hn_top = ClusterFeatures("hn_top", {"hn": 200.0}, distinct_sources=1, newest_at=NOW)
    hn_low = ClusterFeatures("hn_low", {"hn": 10.0}, distinct_sources=1, newest_at=NOW)
    rd_top = ClusterFeatures("rd_top", {"reddit_sub": 5000.0}, distinct_sources=1, newest_at=NOW)

    native = rank._normalize_native([hn_top, hn_low, rd_top])
    # Each platform min-maxes on its own: the HN leader and the Reddit leader both hit 1.0,
    # the HN laggard hits 0.0 — proving HN wasn't crushed by Reddit's larger raw scale.
    assert native["hn_top"] == pytest.approx(1.0)
    assert native["rd_top"] == pytest.approx(1.0)
    assert native["hn_low"] == pytest.approx(0.0)


def test_native_zero_for_clusters_without_native_signal():
    # rss-only cluster (no native platform) gets 0 on the native axis but still exists.
    rss_only = ClusterFeatures("rss", {}, distinct_sources=1, newest_at=NOW)
    hn = ClusterFeatures("hn", {"hn": 100.0}, distinct_sources=1, newest_at=NOW)
    native = rank._normalize_native([rss_only, hn])
    assert native["rss"] == 0.0
    assert native["hn"] == pytest.approx(1.0)


def test_native_axis_is_max_across_platforms_for_multiplatform_cluster():
    # A cluster seen on both HN and Reddit takes its STRONGEST platform's normalized score.
    multi = ClusterFeatures("multi", {"hn": 200.0, "reddit_sub": 10.0},
                            distinct_sources=2, newest_at=NOW)
    hn_low = ClusterFeatures("hn_low", {"hn": 0.0}, distinct_sources=1, newest_at=NOW)
    rd_top = ClusterFeatures("rd_top", {"reddit_sub": 100.0}, distinct_sources=1, newest_at=NOW)
    native = rank._normalize_native([multi, hn_low, rd_top])
    # On HN, multi(200) is the max -> 1.0; on Reddit, multi(10) is the min -> 0.0.
    # The cluster's native axis is the max of those -> 1.0.
    assert native["multi"] == pytest.approx(1.0)


# --- distinct-source frequency --------------------------------------------------------

def test_frequency_normalization_minmax_across_set():
    # distinct_sources: one URL seen by 3 sources => 3 (the cluster's frequency).
    a = ClusterFeatures("a", {}, distinct_sources=3, newest_at=NOW)
    b = ClusterFeatures("b", {}, distinct_sources=1, newest_at=NOW)
    c = ClusterFeatures("c", {}, distinct_sources=2, newest_at=NOW)
    freq = rank._normalize_frequency([a, b, c])
    assert freq["a"] == pytest.approx(1.0)   # most sources
    assert freq["b"] == pytest.approx(0.0)   # fewest sources
    assert freq["c"] == pytest.approx(0.5)   # midpoint (1..3 -> 0.5)


def test_frequency_all_equal_maps_to_one():
    # When every cluster has the same breadth, the axis doesn't differentiate (all 1.0),
    # rather than collapsing to 0 and silently dropping the signal.
    feats = [ClusterFeatures(str(i), {}, distinct_sources=2, newest_at=NOW) for i in range(3)]
    freq = rank._normalize_frequency(feats)
    assert all(v == pytest.approx(1.0) for v in freq.values())


# --- blend math + weight seam ---------------------------------------------------------

def test_blend_is_weighted_sum_of_the_three_axes():
    # Two clusters: one is the frequency+native leader, the other is fresher. With the
    # default weights (frequency strongest), the cross-source leader should win even if a
    # touch older.
    leader = ClusterFeatures("leader", {"hn": 500.0}, distinct_sources=3,
                             newest_at=NOW - timedelta(days=1))
    fresh_thin = ClusterFeatures("fresh", {"hn": 0.0}, distinct_sources=1, newest_at=NOW)
    scores = score_clusters([leader, fresh_thin], NOW,
                            w_native_=DEFAULT_W_NATIVE, w_freq_=DEFAULT_W_FREQUENCY,
                            w_recency_=DEFAULT_W_RECENCY, halflife_days=3.0)
    assert scores["leader"] > scores["fresh"]


def test_blend_exact_arithmetic():
    # Pin the exact weighted sum for two clusters so the formula can't silently drift.
    # native: hi=100 -> 1.0, lo=0 -> 0.0 ; freq: 4 -> 1.0, 1 -> 0.0 ; recency both fresh -> 1.0
    hi = ClusterFeatures("hi", {"hn": 100.0}, distinct_sources=4, newest_at=NOW)
    lo = ClusterFeatures("lo", {"hn": 0.0}, distinct_sources=1, newest_at=NOW)
    scores = score_clusters([hi, lo], NOW,
                            w_native_=0.35, w_freq_=0.45, w_recency_=0.20, halflife_days=3.0)
    # hi: 0.35*1 + 0.45*1 + 0.20*1 = 1.00 ; lo: 0.35*0 + 0.45*0 + 0.20*1 = 0.20
    assert scores["hi"] == pytest.approx(1.00)
    assert scores["lo"] == pytest.approx(0.20)


def test_weight_override_changes_ranking():
    """The weight seam actually re-orders results: a fresh-but-thin cluster can beat a
    cross-source leader if recency is weighted heavily enough."""
    leader = ClusterFeatures("leader", {"hn": 100.0}, distinct_sources=4,
                             newest_at=NOW - timedelta(days=10))   # old
    fresh = ClusterFeatures("fresh", {"hn": 0.0}, distinct_sources=1, newest_at=NOW)  # new

    # Default-ish: frequency dominates -> leader wins despite being old.
    freq_heavy = score_clusters([leader, fresh], NOW, w_native_=0.3, w_freq_=0.6,
                                w_recency_=0.1, halflife_days=3.0)
    assert freq_heavy["leader"] > freq_heavy["fresh"]

    # Recency-dominant override -> the fresh one wins (the seam changed the order).
    recency_heavy = score_clusters([leader, fresh], NOW, w_native_=0.0, w_freq_=0.1,
                                   w_recency_=0.9, halflife_days=3.0)
    assert recency_heavy["fresh"] > recency_heavy["leader"]


def test_weights_resolve_from_env(monkeypatch):
    for var, default, fn in [
        ("RANK_W_FREQUENCY", DEFAULT_W_FREQUENCY, rank.w_frequency),
        ("RANK_W_NATIVE", DEFAULT_W_NATIVE, rank.w_native),
        ("RANK_W_RECENCY", DEFAULT_W_RECENCY, rank.w_recency),
    ]:
        monkeypatch.delenv(var, raising=False)
        assert fn() == default
        monkeypatch.setenv(var, "0.7")
        assert fn() == 0.7
        monkeypatch.setenv(var, "garbage")  # bad value falls back to default
        assert fn() == default


def test_halflife_resolves_from_env(monkeypatch):
    monkeypatch.delenv("RANK_RECENCY_HALFLIFE_DAYS", raising=False)
    assert rank.recency_halflife_days() == DEFAULT_RECENCY_HALFLIFE_DAYS
    monkeypatch.setenv("RANK_RECENCY_HALFLIFE_DAYS", "7")
    assert rank.recency_halflife_days() == 7.0
    # Non-positive / garbage falls back to the default (no div-by-zero, no negative decay).
    monkeypatch.setenv("RANK_RECENCY_HALFLIFE_DAYS", "0")
    assert rank.recency_halflife_days() == DEFAULT_RECENCY_HALFLIFE_DAYS
    monkeypatch.setenv("RANK_RECENCY_HALFLIFE_DAYS", "nope")
    assert rank.recency_halflife_days() == DEFAULT_RECENCY_HALFLIFE_DAYS


def test_idempotent_same_data_same_scores():
    feats = [
        ClusterFeatures("a", {"hn": 100.0}, distinct_sources=3, newest_at=NOW - timedelta(days=1)),
        ClusterFeatures("b", {"reddit_sub": 50.0}, distinct_sources=1, newest_at=NOW),
    ]
    first = score_clusters(feats, NOW, w_native_=0.35, w_freq_=0.45, w_recency_=0.20, halflife_days=3.0)
    second = score_clusters(feats, NOW, w_native_=0.35, w_freq_=0.45, w_recency_=0.20, halflife_days=3.0)
    assert first == second


def test_module_exports_the_public_seam():
    for name in (
        "rank_clusters",
        "score_clusters",
        "score_cluster",
        "recency_score",
        "native_rating",
        "platform_of",
        "w_frequency",
        "w_native",
        "w_recency",
        "recency_halflife_days",
    ):
        assert hasattr(rank, name)


# --- DB-backed proof (guarded; the integrate phase runs it) ---------------------------

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"


@pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")
def test_rank_clusters_populates_scores_and_orders_sanely():
    """Seed three clusters by hand (a cross-source-heavy one, an HN-engagement one, an
    isolated rss one) and assert rank_clusters writes a score for each and the cross-source
    leader outranks the isolated single-source cluster. Runs inside a rolled-back tx."""
    import uuid

    from sqlalchemy import select

    from app.db.models import Cluster, Item as ItemModel, Sighting
    from app.db.session import engine, SessionLocal
    from app.researcher.rank import rank_clusters

    conn = engine.connect()
    outer = conn.begin()
    session = SessionLocal(bind=conn)
    run = uuid.uuid4().hex
    now = datetime(2026, 6, 14, 12, 0, 0, tzinfo=UTC)

    def add_item(cluster_id, suffix, published_at):
        iid = f"it:{run}:{suffix}"
        session.add(ItemModel(id=iid, cluster_id=cluster_id, title=suffix,
                              url=f"https://ex.com/{run}/{suffix}", published_at=published_at))
        return iid

    def add_sighting(item_id, source_key, engagement):
        session.add(Sighting(item_id=item_id, source_key=source_key, engagement=engagement))

    try:
        # Cluster MULTI: one item seen by 3 distinct sources (frequency-heavy), fresh.
        cl_multi = f"cl:{run}:multi"
        cl_hn = f"cl:{run}:hn"
        cl_rss = f"cl:{run}:rss"
        session.add_all([Cluster(id=cl_multi), Cluster(id=cl_hn), Cluster(id=cl_rss)])
        session.flush()

        m1 = add_item(cl_multi, "m1", now)
        add_sighting(m1, f'hn:{{"run":"{run}"}}', {"points": 80})
        add_sighting(m1, f'reddit_sub:{{"run":"{run}"}}', {"score": 300})
        add_sighting(m1, f'rss:{{"run":"{run}"}}', {})

        # Cluster HN: a single HN source with high points, fresh — engagement-heavy but
        # single-source.
        h1 = add_item(cl_hn, "h1", now)
        add_sighting(h1, f'hn:{{"run2":"{run}"}}', {"points": 500})

        # Cluster RSS: a single rss source, no native signal, a week old — should rank last.
        r1 = add_item(cl_rss, "r1", now - timedelta(days=7))
        add_sighting(r1, f'rss:{{"run2":"{run}"}}', {})
        session.flush()

        n = rank_clusters(session, now=now)
        # rank_clusters scores EVERY cluster that has items, not only our seeds: the persistent
        # dbdata volume legitimately carries clusters from earlier live runs. So assert it scored
        # at least our three, and verify the per-cluster outcome on our seeds below — never a
        # global ==3 count, which would be brittle against whatever else is in the store.
        assert n >= 3

        scores = dict(session.execute(
            select(Cluster.id, Cluster.score).where(Cluster.id.in_([cl_multi, cl_hn, cl_rss]))
        ).all())
        # Every scored cluster has a non-null score.
        assert all(scores[c] is not None for c in (cl_multi, cl_hn, cl_rss))
        # The isolated, week-old, no-native rss cluster ranks below both others.
        assert scores[cl_rss] < scores[cl_multi]
        assert scores[cl_rss] < scores[cl_hn]
    finally:
        session.close()
        outer.rollback()
        conn.close()
