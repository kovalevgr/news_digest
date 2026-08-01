"""Embed new items + dedup them into clusters (Phase 1 slice 3a).

This is the second dedup layer (docs/01_technical.md §2.1, decision (b)): the plain
URL-PK upsert in store.py already collapses the *same* canonical URL seen by several
sources into one item; this stage groups *different* URLs about the *same* story into
one **cluster** by vector similarity. It is the first real use of items.embedding,
items.cluster_id, and the clusters table.

Two decoupled stages, run in order by `embed_and_cluster`:

  1. embed_pending_items — items WHERE embedding IS NULL, in a capped batch: call
     app.llm.embed() on each item's text (the title in pass-1; full_text is None until
     pass-2) and write the vector. Embedding is a network call, so it is deliberately
     OUTSIDE the per-source poll transaction (poll.py never holds it) — re-runnable and
     isolated from polling.

  2. cluster_pending_items — items WHERE embedding IS NOT NULL AND cluster_id IS NULL,
     oldest-first. For each, find its nearest already-clustered neighbour by pgvector
     COSINE distance; if within the threshold, join that neighbour's cluster, else open a
     new one. This is online single-link-style grouping: matches the design's "each new
     item is embedded and grouped into one cluster by vector similarity", is order-stable
     (oldest item seeds its cluster), and is idempotent (an item already carrying a
     cluster_id is never reconsidered).

Deterministic code — the ONLY model call here is embed() (role "embedding", resolved by
the swappable role->provider seam in app.llm; no model id is hardcoded). No classifier,
no generation, no score: topic-classification of ambiguous items and cluster ranking are
the NEXT slices. clusters.score stays NULL here.
"""
from __future__ import annotations

import hashlib
import logging
import os
import uuid

from sqlalchemy import func, select, update

from app.config import Config, load_config
from app.db.models import Cluster, Item as ItemModel, Sighting
from app.db.session import get_session
from app.llm import embed

log = logging.getLogger("researcher.cluster")

# --- Dedup threshold (an intentionally-open decision — keep this the one place to tune) ---
#
# Grouping uses COSINE DISTANCE = 1 - cosine_similarity (pgvector's `cosine_distance`).
# Two items join one cluster when their distance is <= this cutoff.
#
# Default 0.17  ==  cosine similarity >= 0.83.  Rationale: with normalized text-embedding
# vectors, near-duplicate/same-story headlines typically sit at similarity ~0.85-0.95 while
# merely topic-adjacent items sit well below ~0.7; 0.83 is a deliberately CONSERVATIVE
# midpoint that favours precision (don't merge distinct stories) over recall (a missed
# merge just leaves two clusters, which ranking/triage tolerate). It is a starting point to
# revisit with real embeddings — override with env DEDUP_COSINE_MAX without touching code.
DEFAULT_DEDUP_COSINE_MAX = 0.17

# Cap how many items we embed per call so a backlog (e.g. first poll of a busy feed) is
# chunked into bounded network bursts rather than one giant request. Tunable via env.
DEFAULT_EMBED_BATCH_SIZE = int(os.environ.get("EMBED_BATCH_SIZE", "64"))


def dedup_cosine_max() -> float:
    """The cosine-distance cutoff for joining two items into one cluster (env-overridable).
    One place to tune the open dedup-threshold decision."""
    raw = os.environ.get("DEDUP_COSINE_MAX")
    if raw is None:
        return DEFAULT_DEDUP_COSINE_MAX
    try:
        return float(raw)
    except ValueError:
        log.warning("bad DEDUP_COSINE_MAX=%r — falling back to %s", raw, DEFAULT_DEDUP_COSINE_MAX)
        return DEFAULT_DEDUP_COSINE_MAX


def is_within_threshold(distance: float | None, *, cutoff: float | None = None) -> bool:
    """Pure decision helper: does this nearest-neighbour distance warrant joining its
    cluster? False when there is no neighbour (distance is None) or it is farther than the
    cutoff. Factored out so the threshold rule is unit-testable without a DB."""
    if distance is None:
        return False
    cutoff = dedup_cosine_max() if cutoff is None else cutoff
    return distance <= cutoff


def new_cluster_id() -> str:
    """Mint a fresh, opaque cluster id: `cl:` + sha256(uuid4) hex.

    Items hash their canonical URL for identity; a cluster has no such natural key (it is
    an emergent group), so we hash a random uuid4 — same opaque-hex shape as item ids, but
    collision-free and order-independent. The `cl:` prefix makes cluster ids self-describing
    in logs and joins."""
    return "cl:" + hashlib.sha256(uuid.uuid4().bytes).hexdigest()


def source_default_topic(owners: list[str]) -> str | None:
    """Resolve a NEW cluster's source-default topic from the owners of the item that seeds
    it (an owner is `topic:<name>` or `person:<name>`, from config — app.config.Source.owner).

    Rule (docs/01_technical.md §2.1 "topic tagging"):
      - any `topic:<name>` owner  -> that topic is the source-default (unambiguous).
      - person-only (only `person:<name>` owners) -> None: ambiguous, left for the cheap
        topic classifier in the NEXT slice. We do NOT classify here.

    If several distinct topics own the seed item, we still can't pick one deterministically,
    so we leave it None (also classifier territory). The common case — an item that came in
    via exactly one topic source — resolves cleanly.
    """
    topics = sorted({o.split("topic:", 1)[1] for o in owners if o.startswith("topic:")})
    if len(topics) == 1:
        return topics[0]
    return None


def _owners_for_item(session, item_id: str, cfg: Config) -> list[str]:
    """The config owners of every source that has a sighting of this item. Maps each
    sighting's source_key back to its config Source to read `.owner`; unknown keys (a source
    removed from config since ingest) are skipped."""
    source_keys = session.execute(
        select(Sighting.source_key).where(Sighting.item_id == item_id)
    ).scalars().all()
    owners: list[str] = []
    for key in source_keys:
        src = cfg.source_by_key(key)
        if src is not None:
            owners.append(src.owner)
    return owners


def embed_pending_items(session, *, batch_size: int = DEFAULT_EMBED_BATCH_SIZE) -> int:
    """Embed up to `batch_size` items that have no embedding yet; write the vectors.

    Selects items WHERE embedding IS NULL AND there is a usable title (oldest first for
    stable ordering), embeds their text in ONE app.llm.embed() batch call, and writes each
    vector back. Pass-1 text is the title (full_text is None until pass-2). The
    has-a-title predicate lives in SQL so LIMIT only ever pulls embeddable rows: untitled
    items (rss/hn can yield title=None) are real, and filtering them out in Python AFTER the
    LIMIT meant a batch that was entirely untitled returned 0 and stalled the drain loop,
    stranding titled items that sort after it. With the predicate in SQL the loop drains the
    whole titled backlog; untitled items stay NULL (they get a vector once they carry text in
    pass-2). Commits. Returns the number of items embedded. Safe to re-run: already-embedded
    items aren't re-selected.
    """
    pending = session.execute(
        select(ItemModel)
        .where(ItemModel.embedding.is_(None))
        .where(func.coalesce(func.trim(ItemModel.title), "") != "")
        .order_by(ItemModel.fetched_at.asc(), ItemModel.id.asc())
        .limit(batch_size)
    ).scalars().all()

    if not pending:
        return 0

    # Belt-and-braces: the SQL predicate above already excludes untitled rows; this guard is a
    # no-op unless the predicate ever changes.
    pending = [it for it in pending if (it.title or "").strip()]
    if not pending:
        return 0

    vectors = embed([it.title for it in pending])
    for it, vec in zip(pending, vectors):
        it.embedding = vec
    session.commit()
    log.info("embed: embedded %d item(s)", len(pending))
    return len(pending)


def _nearest_clustered(session, embedding) -> tuple[str | None, float | None]:
    """The (cluster_id, cosine_distance) of the already-clustered item nearest to `embedding`,
    or (None, None) if no clustered items exist yet. Uses pgvector's cosine_distance operator
    so the comparison happens in the DB (indexable later); only the single best row is read.

    The order-by carries a deterministic tiebreak (item id, then cluster id) after the
    distance: equidistant neighbours are common (identical vectors -> distance 0; identical
    titles via the fake provider), and ORDER BY distance alone leaves ties to the DB's
    arbitrary row order. Without the tiebreak an incoming item equidistant from two items in
    DIFFERENT clusters could join either one run-to-run, contradicting this module's stated
    order-stability. Ordering by item id (stable, unique) then cluster id makes the join
    choice the same every run."""
    distance = ItemModel.embedding.cosine_distance(embedding)
    row = session.execute(
        select(ItemModel.cluster_id, distance.label("distance"))
        .where(ItemModel.cluster_id.is_not(None))
        .where(ItemModel.embedding.is_not(None))
        .order_by(distance.asc(), ItemModel.id.asc(), ItemModel.cluster_id.asc())
        .limit(1)
    ).first()
    if row is None:
        return None, None
    return row.cluster_id, row.distance


def _claim_item(session, item: "ItemModel", cluster_id: str) -> bool:
    """Conditionally assign `item` to `cluster_id`, returning True iff THIS call won the claim.

    The assignment is a guarded `UPDATE items SET cluster_id=:c WHERE id=:id AND cluster_id IS
    NULL`: if a concurrent pass already clustered the item, the WHERE matches 0 rows and we
    return False (the caller skips it). This is the per-item concurrency guard that makes a
    double pass safe regardless of overlap. On a winning claim (1 row changed) we commit — both
    to persist the assignment and so the newly-clustered item is a real neighbour for the next
    loop iteration — and keep the in-session ORM object in sync (expire it so a later read sees
    the committed cluster_id rather than a stale None). On a loss we do NOT commit here; the
    caller decides whether a just-created orphan cluster needs rolling back.
    """
    result = session.execute(
        update(ItemModel)
        .where(ItemModel.id == item.id)
        .where(ItemModel.cluster_id.is_(None))
        .values(cluster_id=cluster_id)
    )
    if result.rowcount == 1:
        session.commit()  # commit per item so the cluster is a real neighbour next loop
        session.expire(item)  # drop the stale in-memory cluster_id=None; re-read on next access
        return True
    return False


def cluster_pending_items(session, *, cfg: Config | None = None) -> dict[str, int]:
    """Assign every embedded-but-unclustered item to a cluster, oldest first.

    For each item (embedding IS NOT NULL AND cluster_id IS NULL): find its nearest
    already-clustered neighbour by cosine distance; if within the threshold, join that
    cluster, else open a new one (status defaults to 'new'; topic = source-default when
    unambiguous, else NULL for the classifier slice; score stays NULL — ranking is next).
    Each assignment commits, so a long backlog makes incremental progress and a crash
    doesn't strand work.

    Online single-link grouping: processing oldest-first means an earlier item seeds the
    cluster a later near-duplicate joins, and an item that already has a cluster_id is never
    revisited — so re-running creates no new clusters and reassigns nothing (idempotent).

    Concurrency-safe: each assignment goes through `_claim_item`'s conditional `UPDATE ...
    WHERE cluster_id IS NULL`, so even if a second pass overlaps, an item is assigned at most
    once (the loser's UPDATE matches 0 rows and is skipped; a just-created orphan cluster is
    rolled back). `clustered`/`new_clusters` count only claims this pass actually won.

    Returns {"clustered": n, "new_clusters": k}.
    """
    cfg = cfg or load_config()
    stats = {"clustered": 0, "new_clusters": 0}

    # Concurrency guard is now IN PLACE (Phase 1 INTEGRATE): assignment is a conditional
    # `UPDATE items SET cluster_id=:c WHERE id=:id AND cluster_id IS NULL`, and we act only when
    # it reports 1 row changed. So even though the poller schedules this on a periodic job, two
    # overlapping passes can't double-assign the same item — whichever pass's UPDATE lands first
    # wins, the loser's UPDATE matches 0 rows and is skipped. (The scheduler ALSO pins the
    # process job to max_instances=1 + coalesce=True, so in practice passes don't overlap at all;
    # this conditional UPDATE is the belt-and-braces correctness guarantee independent of that.)
    pending = session.execute(
        select(ItemModel)
        .where(ItemModel.embedding.is_not(None))
        .where(ItemModel.cluster_id.is_(None))
        .order_by(ItemModel.fetched_at.asc(), ItemModel.id.asc())
    ).scalars().all()

    for item in pending:
        cluster_id, distance = _nearest_clustered(session, item.embedding)

        if is_within_threshold(distance):
            # Join the existing neighbour's cluster — but only if this item is still unclaimed.
            claimed = _claim_item(session, item, cluster_id)
            if claimed:
                stats["clustered"] += 1
            # else: a concurrent pass already clustered it -> skip; nothing to commit.
            continue

        # Open a new cluster. Create it FIRST (it is harmless even if the claim then loses: an
        # empty just-created cluster is simply never referenced and ranking skips it), then try
        # to claim the item into it. Only count the new cluster when the claim actually wins, so
        # new_clusters never overstates.
        owners = _owners_for_item(session, item.id, cfg)
        cluster = Cluster(
            id=new_cluster_id(),
            topic=source_default_topic(owners),
            # status defaults to 'new' (schema server_default); score stays NULL.
        )
        session.add(cluster)
        session.flush()  # make the cluster visible as a neighbour for later items
        claimed = _claim_item(session, item, cluster.id)
        if claimed:
            stats["new_clusters"] += 1
            stats["clustered"] += 1
        else:
            # Lost the race: another pass clustered this item. Roll back the orphan cluster we
            # just created so we don't leave an empty cluster behind, then move on.
            session.rollback()

    if stats["clustered"]:
        log.info(
            "cluster: assigned %d item(s) into %d new cluster(s)",
            stats["clustered"], stats["new_clusters"],
        )
    return stats


def embed_and_cluster(
    session=None,
    *,
    cfg: Config | None = None,
    batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
) -> dict[str, int]:
    """Driver: embed EVERY item that still lacks an embedding, then cluster everything
    embedded-but-unclustered.

    Runs the two stages back to back over the current DB. The embed stage is batched
    (DEFAULT_EMBED_BATCH_SIZE), so this loops embed_pending_items until it returns 0 — a full
    drain in one invocation, matching the docstrings and the `cluster` CLI help ("embed every
    item that still lacks an embedding"). Pass `session` to reuse an open one (tests);
    otherwise one is opened and closed here. Each stage commits its own work, so partial
    progress survives a failure in the other. The returned `embedded` is the total across all
    batches. Returns combined stats.
    """
    cfg = cfg or load_config()
    own_session = session is None
    session = session or get_session()
    try:
        embedded = 0
        while True:
            n = embed_pending_items(session, batch_size=batch_size)
            embedded += n
            if n == 0:
                break
        cluster_stats = cluster_pending_items(session, cfg=cfg)
    finally:
        if own_session:
            session.close()
    return {"embedded": embedded, **cluster_stats}


__all__ = [
    "DEFAULT_DEDUP_COSINE_MAX",
    "DEFAULT_EMBED_BATCH_SIZE",
    "dedup_cosine_max",
    "is_within_threshold",
    "new_cluster_id",
    "source_default_topic",
    "embed_pending_items",
    "cluster_pending_items",
    "embed_and_cluster",
]
