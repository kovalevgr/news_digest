"""Cluster ranking — the deterministic blended cross-source score (Phase 1 slice 3c).

Ranking happens at the CLUSTER level (docs/01_technical.md §2.1 "Cluster ranking",
§3 decision 1/2). This stage reads what the dedup/cluster stage wrote and computes
`clusters.score`, a single blended float per cluster, from three axes:

  - native engagement — each cluster's items' sightings' native ratings (HN points,
    Reddit score, ...), normalized PER PLATFORM so we never compare an HN point count
    to a Reddit score raw. Sources with no native signal (rss/github/arxiv -> {})
    contribute 0 on this axis; they still score via frequency and recency.
  - cross-source frequency — the STRONGEST signal (the same story surfacing in many
    sources): the count of DISTINCT sighting sources across ALL items in the cluster
    (one URL seen by 3 sources counts as 3), normalized to 0..1 across the set.
  - recency — exponential half-life decay on the age of the cluster's newest item.

  score = w_native*native + w_freq*freq + w_recency*recency

This is PURE deterministic code — there is NO model call here (the researcher stays
deterministic; ranking is arithmetic). The only persisted output is clusters.score.

WHY a reference `now=` parameter instead of a wall-clock builtin: recency depends on
"now", and ranking must be reproducible/testable. `rank_clusters` resolves `now` from
the DB clock (SELECT now()) when the caller passes None, so the host's wall clock never
leaks in and tests can pin time explicitly.

Normalization is done across the CURRENT cluster set in one pass (min-max), which is the
simplest correct way to make heterogeneous raw signals comparable for a single-user store.
It means scores are RELATIVE to the set being ranked (re-ranking after new clusters arrive
can shift absolute scores) — acceptable: triage/digest only ever care about the ordering
within a ranking run, and re-running on the SAME data yields the SAME scores (idempotent).

Weights and the recency half-life are intentionally-open decisions (docs/03_build_plan.md):
module-level defaults with env overrides, each justified inline. Tune without touching code.
"""
from __future__ import annotations

import logging
import math
import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import func, select

from app.db.models import Cluster, Item as ItemModel, Sighting

log = logging.getLogger("researcher.rank")

# --- Blend weights (an intentionally-open decision — one place to tune) ---------------
#
# Cross-source frequency is the strongest signal in the design ("the same story surfacing
# in many sources"), so it carries the most weight. Native engagement is a strong but
# platform-local signal (and absent for half the source types), so it is second. Recency
# is a tie-breaker/freshness nudge rather than a primary driver — a great story a few days
# old should still beat a thin one from this hour — so it is smallest. The three default to
# 0.45 / 0.35 / 0.20 (they need not sum to 1; the blend is just a weighted sum, and equal
# data across clusters cancels out — only the relative weights matter for ordering).
DEFAULT_W_FREQUENCY = 0.45
DEFAULT_W_NATIVE = 0.35
DEFAULT_W_RECENCY = 0.20

# Recency half-life in DAYS: how old a cluster's newest item must be for its recency axis to
# fall to 0.5. Default 3d — long enough that a strong story stays competitive for a few days
# (hot-news triage cadence), short enough that week-old items decay clearly. Env-overridable.
DEFAULT_RECENCY_HALFLIFE_DAYS = 3.0


def _env_float(name: str, default: float) -> float:
    """Read an env override as a float, falling back to `default` on absence/garbage.
    Keeps every tunable a documented seam without scattering try/except at call sites."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        log.warning("bad %s=%r — falling back to %s", name, raw, default)
        return default


def w_frequency() -> float:
    return _env_float("RANK_W_FREQUENCY", DEFAULT_W_FREQUENCY)


def w_native() -> float:
    return _env_float("RANK_W_NATIVE", DEFAULT_W_NATIVE)


def w_recency() -> float:
    return _env_float("RANK_W_RECENCY", DEFAULT_W_RECENCY)


def recency_halflife_days() -> float:
    h = _env_float("RANK_RECENCY_HALFLIFE_DAYS", DEFAULT_RECENCY_HALFLIFE_DAYS)
    return h if h > 0 else DEFAULT_RECENCY_HALFLIFE_DAYS


# --- Native-engagement extraction (per-platform) --------------------------------------
#
# The platform of a sighting is the prefix of its source_key (`<type>:...`, see
# app.config.derive_source_key). Each platform that carries a native rating declares the
# engagement key(s) that ARE that rating, best-first; the first present numeric one wins.
# Platforms with no native rating are simply absent from this map and contribute 0 on the
# native axis (they still score via frequency). Comment counts are deliberately NOT the
# primary native rating (comments are a secondary signal, docs §2.1 "comment counts are only
# a ranking signal") — points/score/likes are the upvote-like rating we normalize.
_NATIVE_KEYS: dict[str, tuple[str, ...]] = {
    "hn": ("points",),               # app.adapters.hn -> {"points", "comments"}
    "reddit_sub": ("score",),        # Reddit JSON API -> {"score", "num_comments"}
    "x_user": ("likes", "favorites", "like_count"),  # X read API -> like-style metric
}


def platform_of(source_key: str) -> str:
    """The platform/type of a sighting = the `<type>` prefix of its source_key.

    source_key is `<type>:` + a json identity body (app.config.derive_source_key), so the
    substring before the FIRST ':' is the source type. That is enough to pick the right
    native-engagement key and to normalize within a platform — no config lookup needed.
    """
    return source_key.split(":", 1)[0]


def native_rating(engagement: dict | None, platform: str) -> float | None:
    """The single native rating scalar this sighting contributes, or None if the platform
    carries no native rating (or the value is missing/non-numeric).

    Pure: takes the engagement dict + platform and returns the first present, numeric
    rating key for that platform. None (not 0.0) signals "no native signal here" so the
    per-platform normalizer can exclude it from the min-max rather than treat it as a real
    zero rating (a genuine 0-point HN story is different from an rss item with no rating).
    """
    keys = _NATIVE_KEYS.get(platform)
    if not keys or not engagement:
        return None
    for key in keys:
        val = engagement.get(key)
        if isinstance(val, bool):  # bool is an int subclass; never a rating
            continue
        if isinstance(val, (int, float)):
            return float(val)
    return None


# --- Per-cluster feature extraction (pure, DB-agnostic) -------------------------------


@dataclass
class ClusterFeatures:
    """The three raw (un-normalized) inputs a cluster contributes to ranking.

    Kept as a plain dataclass so score_clusters() can be unit-tested with hand-built
    features — no DB, no network. The DB path (rank_clusters) builds these from sightings.
    """
    cluster_id: str
    # max native rating PER platform across the cluster's sightings (platform -> value).
    # Per-platform max (not sum) so a story upvoted on three HN-style feeds isn't double
    # counted on the native axis — cross-source breadth is the FREQUENCY axis's job.
    native_by_platform: dict[str, float]
    # distinct sighting sources across ALL items in the cluster (the frequency signal).
    distinct_sources: int
    # newest item age basis: the cluster's newest item published_at (fallback fetched_at).
    newest_at: datetime | None


def _max_native_by_platform(
    sightings: list[tuple[str, dict | None]],
) -> dict[str, float]:
    """Pure: collapse a cluster's (source_key, engagement) sightings into the MAX native
    rating per platform. Sightings whose platform has no native rating, or whose value is
    missing, are dropped. Returns {} when the cluster has no native signal at all."""
    out: dict[str, float] = {}
    for source_key, engagement in sightings:
        platform = platform_of(source_key)
        rating = native_rating(engagement, platform)
        if rating is None:
            continue
        prev = out.get(platform)
        if prev is None or rating > prev:
            out[platform] = rating
    return out


def recency_score(newest_at: datetime | None, now: datetime, *, halflife_days: float | None = None) -> float:
    """Exponential half-life decay of a cluster's age -> 0..1 (newer scores higher).

    score = 0.5 ** (age_days / halflife). At age 0 -> 1.0; at one half-life -> 0.5; it
    decays monotonically and never goes negative. Future-dated items (clock skew) clamp to
    age 0 -> 1.0. A cluster with no time basis at all (no published_at and no fetched_at)
    scores 0.0 — we can't claim it is fresh.
    """
    if newest_at is None:
        return 0.0
    halflife = recency_halflife_days() if halflife_days is None else halflife_days
    if halflife <= 0:
        halflife = DEFAULT_RECENCY_HALFLIFE_DAYS
    # Normalize both sides to tz-aware UTC so the subtraction is well-defined even if the DB
    # / caller hands us a naive datetime.
    if newest_at.tzinfo is None:
        newest_at = newest_at.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    age_days = (now - newest_at).total_seconds() / 86400.0
    if age_days <= 0:
        return 1.0
    return 0.5 ** (age_days / halflife)


def _minmax_normalize(values: dict[str, float]) -> dict[str, float]:
    """Pure min-max of a {key -> raw} map to {key -> 0..1}. When all raw values are equal
    (including a single-element set), every key maps to 1.0 — the signal is present and
    uniform, so it should neither vanish (0.0) nor distort ordering; with one cluster the
    axis simply doesn't differentiate. Keys absent from `values` are the caller's 0."""
    if not values:
        return {}
    lo = min(values.values())
    hi = max(values.values())
    if hi <= lo:
        return {k: 1.0 for k in values}
    span = hi - lo
    return {k: (v - lo) / span for k, v in values.items()}


def _normalize_native(features: list[ClusterFeatures]) -> dict[str, float]:
    """Per-cluster native axis (cluster_id -> 0..1), normalized PER PLATFORM.

    For each platform, min-max the clusters' max-rating-on-that-platform across the set;
    a cluster's native axis is then the MAX of its per-platform normalized scores (its
    strongest platform). Clusters with no native signal get 0.0. Doing the min-max within
    a platform is the whole point — it keeps HN points and Reddit scores on the same 0..1
    footing before they are combined.
    """
    # platform -> {cluster_id -> raw max rating on that platform}
    by_platform: dict[str, dict[str, float]] = defaultdict(dict)
    for f in features:
        for platform, rating in f.native_by_platform.items():
            by_platform[platform][f.cluster_id] = rating

    normalized: dict[str, float] = {f.cluster_id: 0.0 for f in features}
    for platform, raw in by_platform.items():
        for cid, norm in _minmax_normalize(raw).items():
            if norm > normalized[cid]:
                normalized[cid] = norm
    return normalized


def _normalize_frequency(features: list[ClusterFeatures]) -> dict[str, float]:
    """Per-cluster frequency axis (cluster_id -> 0..1): min-max of distinct_sources across
    the set. The strongest cross-source story maps to 1.0; the least-covered to 0.0 (or all
    to 1.0 when every cluster has the same breadth). Linear because distinct_sources is
    already a small bounded integer for a single user — no need to log-dampen."""
    raw = {f.cluster_id: float(f.distinct_sources) for f in features}
    return _minmax_normalize(raw)


def score_clusters(
    features: list[ClusterFeatures],
    now: datetime,
    *,
    w_native_: float | None = None,
    w_freq_: float | None = None,
    w_recency_: float | None = None,
    halflife_days: float | None = None,
) -> dict[str, float]:
    """PURE: blend the three normalized axes into {cluster_id -> score}. No DB, no network.

    Normalization (native per-platform, frequency across the set) is computed over exactly
    the `features` passed in, so this is the unit-testable core of ranking. Weights default
    to the env-resolved module defaults; tests pass explicit weights to pin the blend.
    """
    wn = w_native() if w_native_ is None else w_native_
    wf = w_frequency() if w_freq_ is None else w_freq_
    wr = w_recency() if w_recency_ is None else w_recency_

    native = _normalize_native(features)
    freq = _normalize_frequency(features)

    scores: dict[str, float] = {}
    for f in features:
        rec = recency_score(f.newest_at, now, halflife_days=halflife_days)
        scores[f.cluster_id] = (
            wn * native.get(f.cluster_id, 0.0)
            + wf * freq.get(f.cluster_id, 0.0)
            + wr * rec
        )
    return scores


def score_cluster(
    *,
    native_by_platform: dict[str, float],
    distinct_sources: int,
    newest_at: datetime | None,
    now: datetime,
    native_norm: dict[str, float] | None = None,
    freq_norm: dict[str, float] | None = None,
    w_native_: float | None = None,
    w_freq_: float | None = None,
    w_recency_: float | None = None,
    halflife_days: float | None = None,
) -> float:
    """PURE single-cluster blend for unit tests / callers that already hold normalized axes.

    Because native and frequency are normalized ACROSS the set, a single cluster in isolation
    can't normalize itself — so the caller supplies the already-normalized native/frequency
    components (each 0..1) via `native_norm`/`freq_norm`; only recency (self-contained) is
    computed here. With both omitted this degenerates to recency-only, which is what a
    lone-cluster ranking would yield. For ranking a real set, prefer score_clusters().
    """
    wn = w_native() if w_native_ is None else w_native_
    wf = w_frequency() if w_freq_ is None else w_freq_
    wr = w_recency() if w_recency_ is None else w_recency_
    nat = 0.0 if native_norm is None else max(native_norm.values(), default=0.0)
    frq = 0.0 if freq_norm is None else max(freq_norm.values(), default=0.0)
    rec = recency_score(newest_at, now, halflife_days=halflife_days)
    return wn * nat + wf * frq + wr * rec


# --- DB path --------------------------------------------------------------------------


def _resolve_now(session, now: datetime | None) -> datetime:
    """The reference time for recency. Defaults to the DB clock (SELECT now()) — NOT the
    host wall clock — so ranking shares the same clock as the stored timestamps and stays
    deterministic/testable when the caller pins `now`."""
    if now is not None:
        return now
    return session.execute(select(func.now())).scalar_one()


def _load_features(session) -> list[ClusterFeatures]:
    """Build per-cluster features from the DB for every cluster that has items.

    One pass over (cluster -> its items -> their sightings):
      - distinct_sources = COUNT(DISTINCT sightings.source_key) over the cluster's items
        (the cross-source frequency signal: one URL seen by 3 sources counts as 3, and the
        same source seeing two items in the cluster counts once — it is the same source).
      - native_by_platform = per-platform MAX native rating across those sightings.
      - newest_at = MAX(COALESCE(published_at, fetched_at)) over the cluster's items.

    Clusters with no items are skipped (nothing to rank from); their score is left untouched.
    """
    # newest_at per cluster (published_at preferred, fetched_at fallback).
    newest_basis = func.coalesce(ItemModel.published_at, ItemModel.fetched_at)
    newest_rows = session.execute(
        select(ItemModel.cluster_id, func.max(newest_basis))
        .where(ItemModel.cluster_id.is_not(None))
        .group_by(ItemModel.cluster_id)
    ).all()
    newest_at: dict[str, datetime | None] = {cid: ts for cid, ts in newest_rows}

    # All (cluster_id, source_key, engagement) sightings, joined through items.
    sighting_rows = session.execute(
        select(ItemModel.cluster_id, Sighting.source_key, Sighting.engagement)
        .join(Sighting, Sighting.item_id == ItemModel.id)
        .where(ItemModel.cluster_id.is_not(None))
    ).all()

    distinct_sources: dict[str, set[str]] = defaultdict(set)
    sightings_by_cluster: dict[str, list[tuple[str, dict | None]]] = defaultdict(list)
    for cid, source_key, engagement in sighting_rows:
        distinct_sources[cid].add(source_key)
        sightings_by_cluster[cid].append((source_key, engagement))

    features: list[ClusterFeatures] = []
    for cid in newest_at:  # one entry per cluster-with-items
        features.append(
            ClusterFeatures(
                cluster_id=cid,
                native_by_platform=_max_native_by_platform(sightings_by_cluster.get(cid, [])),
                distinct_sources=len(distinct_sources.get(cid, ())),
                newest_at=newest_at[cid],
            )
        )
    return features


def rank_clusters(session, now: datetime | None = None) -> int:
    """Recompute and persist clusters.score for every cluster that has items; commit.

    Idempotent: the score is a pure function of the current items/sightings/clusters and
    the reference `now`, so re-running on unchanged data writes the same values. `now`
    defaults to the DB clock (see _resolve_now) — pass it explicitly for deterministic tests.

    Scope note: only clusters that have at least one item are (re)scored — a cluster with no
    items has no signal to rank from, so its score is left as-is (NULL until it gains items).
    Returns the number of clusters scored.
    """
    ref_now = _resolve_now(session, now)
    features = _load_features(session)
    if not features:
        return 0

    scores = score_clusters(features, ref_now)
    for f in features:
        session.get(Cluster, f.cluster_id).score = scores[f.cluster_id]
    session.commit()
    log.info("rank: scored %d cluster(s)", len(features))
    return len(features)


__all__ = [
    "DEFAULT_W_FREQUENCY",
    "DEFAULT_W_NATIVE",
    "DEFAULT_W_RECENCY",
    "DEFAULT_RECENCY_HALFLIFE_DAYS",
    "ClusterFeatures",
    "platform_of",
    "native_rating",
    "recency_score",
    "score_clusters",
    "score_cluster",
    "rank_clusters",
    "w_frequency",
    "w_native",
    "w_recency",
    "recency_halflife_days",
]
