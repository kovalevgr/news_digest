"""Fusion-discovery retrieval: surface the existing news clusters most related to a piece of the
owner's OWN material (docs/01_technical.md §2.1, §2.3; Phase 10 flagship intake).

The flagship/own-material flow (app.editor.sources) lets the owner ground an article in their own
text/files/URLs instead of a news cluster. This module is the discovery seam on top of that: given
that material, find the top-k existing clusters whose dedup vectors sit nearest to it, so the owner
can FUSE their work with the relevant news (cite it, react to it, frame against it).

The retrieval is the SAME deterministic pgvector cosine search the dedup stage already uses
(app.researcher.cluster._nearest_clustered): embed the query once via app.llm.embed, then ORDER BY
`items.embedding <=> query_vec` over the embedded items, joined to their clusters. It is NOT an
agent (hard rule 5) — one embed() call + a SELECT, no tools, no generation. The ONLY model call is
embed() (role "embedding", via the swappable role→provider seam — no model id).

We search over `items.embedding` (the dedup index — every clustered item carries a vector once it
has been embedded), NOT `articles.embedding` (kb.py's index, which is the owner's PUBLISHED corpus).
Items with a NULL embedding are excluded (an embedding is the only thing we can compare against).

Result shaping: multiple items can belong to one cluster, so we dedupe to DISTINCT clusters keeping
each cluster's NEAREST item (the item whose vector matched), order by ascending distance, and cap at
top_k. Each kept cluster reports a detached RelatedCluster (primitives only) so it survives the
session closing and renders without touching the ORM.

Coordination: reads `items`/`clusters`/`sightings` and nothing else; never writes, never calls
another stage, never publishes.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from sqlalchemy import select

from app.db.models import Cluster, Item, Sighting
from app.llm import embed  # module-level import = the test monkeypatch seam

log = logging.getLogger("editor.fusion")

# How many related clusters a single fusion discovery returns by default. The owner wants a SMALL
# shortlist of the most relevant news to fuse with, not the whole store — too many would bury the
# strongest matches. Env-overridable seam (FUSION_TOP_K) behind the late-binding accessor below;
# bad/non-positive values fall back so the cap is never accidentally disabled.
DEFAULT_FUSION_TOP_K = 5


def fusion_top_k() -> int:
    """Default number of related clusters per discovery (env FUSION_TOP_K). Falls back on
    absence/garbage/non-positive — a 0/negative k would make every discovery return nothing."""
    raw = os.environ.get("FUSION_TOP_K")
    if raw is None:
        return DEFAULT_FUSION_TOP_K
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad FUSION_TOP_K=%r — falling back to %s", raw, DEFAULT_FUSION_TOP_K)
        return DEFAULT_FUSION_TOP_K
    return val if val > 0 else DEFAULT_FUSION_TOP_K


@dataclass
class RelatedCluster:
    """One existing news cluster related to the owner's material — primitives only (detached from
    the ORM), so it survives the request session closing and renders into the web UI without
    touching a live row.

    `title` is the cluster's triage_title, falling back to the matched item's title, then
    "(untitled)". `topic` is the cluster's topic ("—" if none). `url` is the matched item's URL (or
    None). `distance` is the cosine distance of the matched (nearest) item to the query. `source_types`
    is the sorted distinct sighting source-type prefixes of the matched item (the bit before the
    first ':' in each source_key, e.g. 'hn', 'x_user', 'rss')."""
    cluster_id: str
    title: str
    topic: str
    url: str | None
    distance: float
    source_types: list[str]


def find_related_clusters(
    session, text: str, *, top_k: int | None = None
) -> list[RelatedCluster]:
    """The top-`top_k` existing clusters most related to `text` (the owner's own material).

    Embeds `text` once (role "embedding"), then cosine-searches `items.embedding` (the dedup index,
    excluding NULL-embedding items), joins each item to its cluster, dedupes to DISTINCT clusters
    keeping each cluster's NEAREST item, orders by ascending distance, and caps at `top_k`. Each kept
    cluster becomes a detached RelatedCluster (title/topic/url from the cluster + its matched item,
    source_types = the matched item's distinct sighting source-type prefixes).

    `top_k` defaults (when None) to the env-overridable accessor `fusion_top_k()` (FUSION_TOP_K,
    default 5) — the late-binding seam, matching kb_search. Pass an explicit int to override per call.

    Returns [] — never raises — when there is nothing to search: a blank/whitespace `text`, a
    non-positive `top_k`, or no embedded clustered items. A deterministic tiebreak (cluster id, then
    item id) after the distance keeps results stable when items are equidistant.

    Deterministic and coordination-only-through-Postgres: one embed() call (no tools, not an agent)
    plus SELECTs over items/clusters/sightings; it never writes and never publishes.
    """
    text = (text or "").strip()
    if not text:
        return []

    k = top_k if top_k is not None else fusion_top_k()
    if k <= 0:
        return []

    query_vec = embed([text])[0]
    distance = Item.embedding.cosine_distance(query_vec)

    # Every embedded, clustered item ordered nearest-first, with its cluster fields. Read in full and
    # dedupe in Python (single-user scale — hundreds of rows): the nearest items can all belong to one
    # cluster, so a SQL LIMIT here could starve us of distinct clusters; the Python pass keeps each
    # cluster's nearest item and stops at k. The cluster-id/item-id tiebreak makes equidistant rows
    # order deterministically.
    rows = session.execute(
        select(
            Cluster.id.label("cluster_id"),
            Cluster.triage_title,
            Cluster.topic,
            Item.id.label("item_id"),
            Item.title.label("item_title"),
            Item.url.label("item_url"),
            distance.label("distance"),
        )
        .join(Item, Item.cluster_id == Cluster.id)
        .where(Item.embedding.is_not(None))
        .order_by(distance.asc(), Cluster.id.asc(), Item.id.asc())
    ).all()

    # Dedupe to distinct clusters, keeping each cluster's nearest (first-seen, since rows are
    # distance-ascending) item, and stop once we have k clusters.
    kept: list = []  # (cluster_id, triage_title, topic, item_id, item_title, item_url, distance)
    seen_clusters: set[str] = set()
    for r in rows:
        if r.cluster_id in seen_clusters:
            continue
        seen_clusters.add(r.cluster_id)
        kept.append(r)
        if len(kept) >= k:
            break

    if not kept:
        return []

    # One batched read for the source-type prefixes of every matched item (no N+1), folded back to
    # the item it belongs to. The prefix is the bit before the first ':' in each sighting's
    # source_key (e.g. 'hn:...' -> 'hn', 'x_user:...' -> 'x_user').
    item_ids = {r.item_id for r in kept}
    types_by_item: dict[str, set[str]] = {iid: set() for iid in item_ids}
    sighting_rows = session.execute(
        select(Sighting.item_id, Sighting.source_key).where(Sighting.item_id.in_(item_ids))
    ).all()
    for item_id_, source_key in sighting_rows:
        prefix = (source_key or "").split(":", 1)[0]
        if prefix:
            types_by_item[item_id_].add(prefix)

    return [
        RelatedCluster(
            cluster_id=r.cluster_id,
            title=(r.triage_title or "").strip() or (r.item_title or "").strip() or "(untitled)",
            topic=(r.topic or "—"),
            url=r.item_url or None,
            distance=float(r.distance),
            source_types=sorted(types_by_item.get(r.item_id, set())),
        )
        for r in kept
    ]


__all__ = [
    "DEFAULT_FUSION_TOP_K",
    "fusion_top_k",
    "RelatedCluster",
    "find_related_clusters",
]
