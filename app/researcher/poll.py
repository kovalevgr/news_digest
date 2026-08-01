"""Poll runner: drive one source (or many) through a single pass-1 poll cycle.

`poll_source` does the full per-source unit of work in ONE transaction:
    load cursor -> adapter.poll -> upsert each item + sighting -> save cursor -> commit.
Either the whole source's batch + its advanced cursor land together, or they roll back
together (so a crash mid-batch can't leave the cursor ahead of what was persisted).

Failures are isolated: a flaky feed or a not-yet-built adapter rolls back and is recorded
in the returned stats, never crashing the cycle — one bad source must not stop the rest.
This is deterministic code (the researcher is not an agent); it does pass-1 metadata only.

This runner is the per-poll body. The cadence loop (APScheduler firing each source on its
own interval) lives in app/researcher/schedule.py and calls poll_source per source; the
manual driver in app/researcher/__main__.py polls each source once.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

from app.adapters import get_adapter, is_implemented
from app.db.session import get_session
from app.researcher.store import load_cursor, save_cursor, upsert_item_and_sighting

log = logging.getLogger("researcher.poll")


@dataclass
class PollStats:
    """Outcome of polling one source. `new_items` counts items never seen by any source
    before (the future embed signal); `sightings` counts every item upserted this poll."""

    source_key: str
    type: str
    ok: bool = False
    not_modified: bool = False
    new_items: int = 0
    sightings: int = 0
    error: str | None = None

    def __str__(self) -> str:
        if self.error:
            return f"{self.source_key} ERROR: {self.error}"
        if self.not_modified:
            return f"{self.source_key} not-modified"
        return f"{self.source_key} ok: +{self.new_items} new / {self.sightings} sightings"


def poll_source(source, session=None) -> PollStats:
    """Poll one configured Source once. Owns its transaction; isolates its own failures.

    Pass `session` to reuse an open session (tests); otherwise one is opened and closed
    here. Returns PollStats either way — never raises for a per-source failure.

    CONTRACT: poll_source ALWAYS commits per source (so a source's batch + its advanced
    cursor land atomically, or roll back together). It commits even when a `session` is
    passed in — it never batches across sources. A scheduler driving many sources must
    therefore call poll_source once PER SOURCE and must NOT wrap multiple calls in one
    outer transaction expecting them to commit together; each source is its own unit.
    """
    stats = PollStats(source_key=source.source_key, type=source.type)
    own_session = session is None
    session = session or get_session()
    try:
        adapter = get_adapter(source.type)
        cursor = load_cursor(session, source.source_key)
        result = adapter.poll(source, cursor)

        if result.not_modified:
            # Still persist the cursor: a cheap idempotent upsert that refreshes
            # updated_at (a "last successfully polled" signal) and doesn't rely on a
            # cursor row already existing on this path.
            save_cursor(session, source.source_key, result.cursor)
            stats.ok = True
            stats.not_modified = True
            session.commit()
            return stats

        for item in result.items:
            if upsert_item_and_sighting(session, item, source.source_key):
                stats.new_items += 1
            stats.sightings += 1

        save_cursor(session, source.source_key, result.cursor)
        session.commit()
        stats.ok = True
    except Exception as exc:  # isolate per-source failure — never crash the cycle
        session.rollback()
        stats.error = f"{type(exc).__name__}: {exc}"
        log.warning("poll failed for %s: %s", source.source_key, stats.error)
    finally:
        if own_session:
            session.close()
    return stats


def poll_sources(sources) -> list[PollStats]:
    """Poll a list of sources once each, skipping not-yet-implemented types with a note.
    Each source gets its own transaction (via poll_source), so failures stay isolated."""
    results: list[PollStats] = []
    for source in sources:
        if not is_implemented(source.type):
            log.info("skip %s — adapter for %r not built yet", source.source_key, source.type)
            results.append(
                PollStats(source_key=source.source_key, type=source.type,
                          error=f"adapter for {source.type!r} not implemented")
            )
            continue
        stats = poll_source(source)
        log.info("%s", stats)
        results.append(stats)
    return results
