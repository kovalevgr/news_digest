"""`python -m app.poller` — the dedicated researcher poller process.

Loads config.yaml, builds a BlockingScheduler with one interval job per source whose
adapter is implemented (logging the not-yet-built ones it skips), then blocks: APScheduler
fires `poll_source` on each source's own cadence. Coordination is Postgres-only — this
process just polls; nothing calls it and it calls no other stage.

Shuts down cleanly on Ctrl-C / SIGTERM (so `docker compose stop` is graceful and an
in-flight poll's transaction isn't torn mid-commit by a hard kill)."""
from __future__ import annotations

import logging

from app.config import load_config
from app.researcher.schedule import build_scheduler, log_plan

logging.basicConfig(level=logging.INFO, format="%(asctime)s [poller] %(message)s")
log = logging.getLogger("poller")


def main():
    cfg = load_config()
    log.info("poller boot OK — %d source(s) resolved", len(cfg.sources))

    jobs = log_plan(cfg)
    if not jobs:
        log.warning("no sources have a built adapter yet — nothing to schedule; idling.")

    scheduler = build_scheduler(cfg)
    log.info("starting scheduler (Ctrl-C / SIGTERM to stop)…")
    try:
        # BlockingScheduler installs SIGINT/SIGTERM handlers and blocks here until stopped.
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("shutdown signal received — stopping scheduler…")
        scheduler.shutdown(wait=True)
        log.info("scheduler stopped; bye.")


if __name__ == "__main__":
    main()
