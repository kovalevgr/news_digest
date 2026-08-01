"""`python -m app.digest <topic>` — run one topic's digest once, by hand.

A developer/ops driver for repeatable local runs (the scheduled cadence lives in the bot
process — the bot wires run_digest onto an APScheduler CronTrigger built from each topic's
config schedule; this module does a single pass). It loads config.yaml, looks up the topic's
`digest` block, runs run_digest, and prints the result:

    python -m app.digest <topic>

Prints the created digest article id, the count + ids of the clusters it covers (the
covered-marker the next run filters on), and a short head of the dense rollup. Returns 0 on a
created digest, 0 with a "nothing eligible" note when the window holds no uncovered clusters
(run_digest returns None — not an error), and a usage error (2) for a missing/unknown topic.

Like the rest of the pipeline this coordinates only through Postgres and never publishes — it
just records the digest article + links and shows what it wrote.
"""
from __future__ import annotations

import logging
import sys

from app.config import load_config
from app.db.session import get_session
from app.digest.run import run_digest

logging.basicConfig(level=logging.INFO, format="%(asctime)s [digest] %(message)s")
log = logging.getLogger("digest")

_USAGE = "usage: python -m app.digest <topic>"


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 1:
        log.error(_USAGE)
        return 2
    topic = argv[0]

    cfg = load_config()
    digest_cfg = cfg.digests.get(topic)
    if digest_cfg is None:
        configured = sorted(cfg.digests)
        log.error(
            "no digest configured for topic %r — topics with a digest block: %s",
            topic, configured or "(none)",
        )
        return 2

    log.info(
        "running digest for topic %r (window=%dd, top_n=%d, schedule=%r)",
        topic, digest_cfg.window_days, digest_cfg.top_n, digest_cfg.schedule,
    )
    session = get_session()
    try:
        result = run_digest(session, topic, digest_cfg)
    finally:
        session.close()

    if result is None:
        log.info("no eligible clusters in the window — no digest article created")
        return 0

    log.info(
        "digest created: article %s covering %d cluster(s)",
        result.article_id, len(result.cluster_ids),
    )
    log.info("covered cluster ids: %s", result.cluster_ids)
    head = result.rollup[:500]
    log.info("rollup head:\n%s%s", head, "..." if len(result.rollup) > 500 else "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
