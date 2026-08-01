"""Researcher (deterministic): scheduler, polling, dedup/clustering, ranking,
topic tagging. Implemented across Phase 1.

Pass-1 ingest — adapters -> items/sightings, with cursors:
  - app.researcher.store: the items/sightings upsert (dedup invariant) + cursor I/O.
  - app.researcher.poll:  the per-source poll runner (one transaction, isolated failures).
  - app.researcher.schedule: the APScheduler poll scheduler driving poll_source on cadence.
  - app.researcher.__main__: `python -m app.researcher poll [TYPE ...]` one-shot driver.

Dedup-into-clusters (slice 3a) — the second dedup layer, decoupled from polling:
  - app.researcher.cluster: embed pending items + group them into clusters by vector
    similarity (the first use of items.embedding/cluster_id and the clusters table).
    `python -m app.researcher cluster` runs it over the current DB.

NOTE: schedule.build_jobs (the pure planner) imports cleanly without APScheduler;
build_scheduler imports it lazily, so importing this package never requires APScheduler.
"""
from app.researcher.cluster import (
    cluster_pending_items,
    dedup_cosine_max,
    embed_and_cluster,
    embed_pending_items,
    is_within_threshold,
    new_cluster_id,
    source_default_topic,
)
from app.researcher.poll import PollStats, poll_source, poll_sources
from app.researcher.schedule import (
    ScheduledJob,
    build_jobs,
    build_scheduler,
    log_plan,
    skipped_sources,
)
from app.researcher.store import (
    load_cursor,
    save_cursor,
    upsert_item_and_sighting,
)

__all__ = [
    "PollStats",
    "poll_source",
    "poll_sources",
    "ScheduledJob",
    "build_jobs",
    "build_scheduler",
    "log_plan",
    "skipped_sources",
    "upsert_item_and_sighting",
    "load_cursor",
    "save_cursor",
    "cluster_pending_items",
    "dedup_cosine_max",
    "embed_and_cluster",
    "embed_pending_items",
    "is_within_threshold",
    "new_cluster_id",
    "source_default_topic",
]
