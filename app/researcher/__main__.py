"""`python -m app.researcher <poll|cluster|classify|rank|process>` — one-shot drivers.

Developer/ops drivers for repeatable local runs (the continuous cadence loop lives in the
poller process — app/poller, app/researcher/schedule.py — this module does single passes):

  poll [TYPE ...]   Pass-1 ingest: poll every configured source of an implemented type once
                    and print per-source stats. TYPE args filter to specific source types
                    (e.g. `poll rss`); default polls all. Not-yet-built types are a skip note.

  cluster           Dedup-into-clusters: embed every item that still lacks an embedding,
                    then group all embedded-but-unclustered items into clusters by vector
                    similarity. Run it AFTER a poll to see clusters form end-to-end.

  classify          Topic-tag clusters: for every cluster whose topic is still NULL, ask the
                    cheap classifier (single model call, role "cheap") for a configured topic
                    or "other". NULL-only — never overwrites a source-default topic.

  rank              Recompute clusters.score for every cluster with items (pure deterministic
                    blended score: native engagement + cross-source frequency + recency).

  process           The full post-poll pipeline in order: embed_and_cluster -> classify ->
                    rank -> triage (the triage-summary call that gives the top NEW clusters a
                    title + blurb for Gate 1). This is exactly what the poller's periodic job
                    runs; the subcommand lets you drive one pass by hand after a poll (or over
                    the existing DB).

    python -m app.researcher poll            # all implemented sources, once
    python -m app.researcher poll rss        # only rss sources, once
    python -m app.researcher cluster         # embed + cluster the current DB, once
    python -m app.researcher classify        # topic-tag NULL-topic clusters, once
    python -m app.researcher rank            # (re)score every cluster, once
    python -m app.researcher process         # embed+cluster -> classify -> rank -> triage, once
"""
from __future__ import annotations

import logging
import sys

from app.adapters import available_types, is_implemented
from app.config import load_config
from app.researcher.cluster import embed_and_cluster
from app.researcher.classify import classify_pending_topics
from app.researcher.poll import poll_sources
from app.researcher.process import run_process
from app.researcher.rank import rank_clusters
from app.db.session import get_session

logging.basicConfig(level=logging.INFO, format="%(asctime)s [researcher] %(message)s")
log = logging.getLogger("researcher")


def _run_poll(type_filter: set[str] | None) -> int:
    cfg = load_config()

    sources = cfg.sources
    if type_filter:
        unknown = type_filter - set(
            s.type for s in cfg.sources
        )
        if unknown:
            log.warning("no configured sources of type(s): %s", sorted(unknown))
        sources = [s for s in sources if s.type in type_filter]

    implemented = [s for s in sources if is_implemented(s.type)]
    skipped = [s for s in sources if not is_implemented(s.type)]

    log.info(
        "polling %d source(s) (implemented types: %s); skipping %d not-yet-built",
        len(implemented), available_types(), len(skipped),
    )

    results = poll_sources(sources)

    polled = [r for r in results if r.ok]
    failed = [r for r in results if r.error and r.type in available_types()]
    total_new = sum(r.new_items for r in results)
    total_sightings = sum(r.sightings for r in results)
    log.info(
        "done: %d polled ok, %d failed, %d new items, %d sightings",
        len(polled), len(failed), total_new, total_sightings,
    )
    return 1 if failed else 0


def _run_cluster() -> int:
    """Embed + cluster the current DB once. Deterministic; the only model call is embed()."""
    stats = embed_and_cluster()
    log.info(
        "cluster done: embedded %d item(s), clustered %d into %d new cluster(s)",
        stats["embedded"], stats["clustered"], stats["new_clusters"],
    )
    return 0


def _run_classify() -> int:
    """Topic-tag NULL-topic clusters once. The classifier's ONE model call is role 'cheap'."""
    session = get_session()
    try:
        stats = classify_pending_topics(session)
    finally:
        session.close()
    log.info(
        "classify done: considered %d NULL-topic cluster(s), labeled %d",
        stats["considered"], stats["labeled"],
    )
    return 0


def _run_rank() -> int:
    """(Re)score every cluster with items once. Pure deterministic arithmetic — no model call."""
    session = get_session()
    try:
        scored = rank_clusters(session)
    finally:
        session.close()
    log.info("rank done: scored %d cluster(s)", scored)
    return 0


def _run_process() -> int:
    """The full post-poll pipeline once: embed_and_cluster -> classify -> rank -> triage.

    Shares the SAME implementation the poller's periodic job runs (app.researcher.process)
    so the manual driver and the scheduled job can never drift."""
    stats = run_process()
    log.info(
        "process done: embedded %d, clustered %d into %d new cluster(s); "
        "classify considered %d / labeled %d; ranked %d cluster(s); triaged %d cluster(s)",
        stats["embedded"], stats["clustered"], stats["new_clusters"],
        stats["considered"], stats["labeled"], stats["scored"], stats["triaged"],
    )
    return 0


_USAGE = "usage: python -m app.researcher <poll [TYPE ...] | cluster | classify | rank | process>"


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        log.error(_USAGE)
        return 2
    command, rest = argv[0], argv[1:]
    if command == "poll":
        return _run_poll(set(rest) or None)
    # The remaining commands take no positional args.
    noarg = {
        "cluster": _run_cluster,
        "classify": _run_classify,
        "rank": _run_rank,
        "process": _run_process,
    }
    if command in noarg:
        if rest:
            log.error("usage: python -m app.researcher %s  (takes no args)", command)
            return 2
        return noarg[command]()
    log.error("unknown command %r — %s", command, _USAGE)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
