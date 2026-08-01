"""APScheduler poll scheduler for the dedicated poller process.

The poller is one process whose entire job is to fire `poll_source(source)` on each
source's own cadence. So we use a BlockingScheduler: it owns the main thread and blocks
on `start()` — exactly what a single-purpose long-running process wants (no event loop to
share, no background thread to babysit). The cadence loop lives here; `poll_source` (in
app.researcher.poll) stays the per-source body it calls — one transaction per source,
failures isolated, never batched.

Two layers, split so the scheduling DECISION is testable without APScheduler or a DB:

  - build_jobs(cfg)  — PURE. Returns [(source, cadence_s)] for sources whose type has a
                       working adapter (available_types()), in config order. No imports of
                       APScheduler, no DB, no network. This is the unit-tested core.
  - build_scheduler  — wraps build_jobs and registers one IntervalTrigger job per source.
                       Imports APScheduler lazily (inside the function) so importing this
                       module — and build_jobs — never requires APScheduler to be present.

Per-job safety: each job is its own source (we never batch across sources, per
poll_source's contract); coalesce=True + max_instances=1 mean a slow poll can never stack
or run concurrently with itself — a missed tick collapses into a single catch-up run.
Random jitter spreads sources that share a cadence so they don't all fire on the same tick
(thundering herd). An optional small initial delay fires the first poll just after startup
instead of waiting a whole cadence.

Deterministic code — the researcher is not an agent and makes no model calls.
"""
from __future__ import annotations

import logging
import os
import random
from dataclasses import dataclass

from app.adapters import is_implemented
from app.config import Config
from app.researcher.poll import poll_source

log = logging.getLogger("researcher.schedule")

# Defaults for the open knobs (sensible, swappable seams — not settled decisions).
DEFAULT_JITTER_S = 30          # +/- spread so equal-cadence sources don't fire in lockstep
DEFAULT_STARTUP_DELAY_S = 5    # first poll fires shortly after boot, not a full cadence later

# The post-poll pipeline (embed_and_cluster -> classify -> rank -> triage) runs on its OWN
# periodic job, separate from the per-source poll jobs, so clusters/topics/scores/triage
# summaries form continuously as the poller ingests (Phase-1 Done: clusters form, carry a topic,
# and get a blended score; Phase-2 adds the triage-summary call so the top NEW clusters are ready
# for the bot to deliver at Gate 1). Default every 2 minutes: brisk enough that a just-polled item
# is clustered+scored+summarized within a couple of minutes, slow enough that the embed + triage
# model calls never thrash. Env-overridable seam (PROCESS_INTERVAL_S). The job is registered with
# max_instances=1 + coalesce=True so two pipeline passes can NEVER overlap — the one extra
# guarantee the cluster stage's per-item conditional UPDATE relies on at the job level.
DEFAULT_PROCESS_INTERVAL_S = 120
PROCESS_JOB_ID = "researcher:process"


def process_interval_s() -> int:
    """The interval (seconds) of the periodic process pipeline job (env PROCESS_INTERVAL_S).
    Falls back to the default on absence/garbage/non-positive — never a 0/negative interval."""
    raw = os.environ.get("PROCESS_INTERVAL_S")
    if raw is None:
        return DEFAULT_PROCESS_INTERVAL_S
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad PROCESS_INTERVAL_S=%r — falling back to %s", raw, DEFAULT_PROCESS_INTERVAL_S)
        return DEFAULT_PROCESS_INTERVAL_S
    return val if val > 0 else DEFAULT_PROCESS_INTERVAL_S


@dataclass(frozen=True)
class ScheduledJob:
    """One source's scheduling decision: poll `source` every `cadence_s` seconds.
    Returned by the pure planner so callers (and tests) can inspect what WOULD be
    scheduled without constructing an APScheduler instance."""

    source: object        # app.config.Source — kept loose to avoid a hard import cycle
    cadence_s: int

    @property
    def source_key(self) -> str:
        return self.source.source_key

    @property
    def type(self) -> str:
        return self.source.type


def build_jobs(cfg: Config) -> list[ScheduledJob]:
    """Plan the scheduler: one job per configured source whose type has a working adapter.

    PURE — no APScheduler, no DB, no network. Sources of not-yet-implemented types are
    dropped here (the caller logs them separately); config order is preserved so the plan
    is deterministic. Each job carries the source's own resolved `cadence_s` (the cascade
    source -> person -> defaults is already applied by the config loader)."""
    return [
        ScheduledJob(source=src, cadence_s=src.cadence_s)
        for src in cfg.sources
        if is_implemented(src.type)
    ]


def skipped_sources(cfg: Config) -> list[object]:
    """Configured sources whose adapter is not built yet — for a clear startup skip log.
    Pure companion to build_jobs (the two partition cfg.sources by implementability)."""
    return [src for src in cfg.sources if not is_implemented(src.type)]


def _run_process_job() -> None:
    """APScheduler entry point for the periodic post-poll pipeline.

    Thin wrapper around app.researcher.process.run_process so the job is a no-arg callable and
    a pass that raises never tears the scheduler down — the next tick simply retries (the whole
    pipeline is idempotent/re-runnable, coordinating only through Postgres). run_process is
    imported lazily so this module's pure planner (build_jobs) keeps importing without pulling
    in the DB/LLM dependency chain, mirroring the lazy APScheduler import in build_scheduler."""
    from app.researcher.process import run_process

    try:
        run_process()
    except Exception:  # noqa: BLE001 — isolate a failed pass; next tick retries.
        log.exception("process pipeline pass failed; will retry next interval")


def build_scheduler(
    cfg: Config,
    *,
    jitter_s: int = DEFAULT_JITTER_S,
    startup_delay_s: int = DEFAULT_STARTUP_DELAY_S,
    scheduler=None,
):
    """Build (or populate) a BlockingScheduler with one interval job per implemented source.

    APScheduler is imported here, lazily, so this module — and the pure build_jobs — import
    cleanly without it. Pass `scheduler` to populate an existing one (e.g. a test double);
    otherwise a fresh BlockingScheduler is created and returned.

    Each job:
      - fires `poll_source(source)` every `cadence_s` seconds (IntervalTrigger),
      - coalesce=True + max_instances=1 so a slow poll never stacks/overlaps itself,
      - adds up to `jitter_s` random jitter to avoid a thundering herd of equal cadences,
      - has a small initial `next_run_time` so the first poll fires just after startup.
    """
    from datetime import datetime, timedelta, timezone

    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.triggers.interval import IntervalTrigger

    scheduler = scheduler if scheduler is not None else BlockingScheduler()
    jobs = build_jobs(cfg)

    for i, job in enumerate(jobs):
        # Stagger first runs a little too, so equal-cadence sources don't all fire at boot.
        first_run = datetime.now(timezone.utc) + timedelta(
            seconds=startup_delay_s + (i * 2 if startup_delay_s else 0)
        )
        scheduler.add_job(
            poll_source,
            trigger=IntervalTrigger(seconds=job.cadence_s, jitter=jitter_s or None),
            args=(job.source,),
            id=job.source_key,
            name=f"{job.type}:{job.source_key}",
            replace_existing=True,
            coalesce=True,
            max_instances=1,
            next_run_time=first_run,
        )

    # The single-runner post-poll pipeline (embed_and_cluster -> classify -> rank -> triage).
    # Separate from the poll jobs and ALWAYS scheduled (even with zero implemented sources, so a
    # backlog left in the DB still gets clustered/ranked/triaged). max_instances=1 + coalesce=True
    # guarantee two pipeline passes never overlap — together with the cluster stage's conditional
    # per-item UPDATE, no item can be double-assigned. First run fires just after the poll jobs'
    # stagger so an initial poll has a chance to land items before the first pipeline pass.
    process_first_run = datetime.now(timezone.utc) + timedelta(
        seconds=startup_delay_s + len(jobs) * 2 + 5
    )
    scheduler.add_job(
        _run_process_job,
        trigger=IntervalTrigger(seconds=process_interval_s(), jitter=jitter_s or None),
        id=PROCESS_JOB_ID,
        name="researcher:process (embed+cluster -> classify -> rank -> triage)",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
        next_run_time=process_first_run,
    )
    return scheduler


def log_plan(cfg: Config) -> list[ScheduledJob]:
    """Log the scheduled jobs (type, cadence, key) and the skipped not-yet-built sources.
    Returns the planned jobs so a caller can reuse the same plan it just logged."""
    jobs = build_jobs(cfg)
    log.info("scheduling %d source(s):", len(jobs))
    for job in jobs:
        log.info("  %-10s every %-7ss  %s", job.type, job.cadence_s, job.source_key)
    log.info(
        "  %-10s every %-7ss  %s (single-runner, max_instances=1)",
        "process", process_interval_s(), PROCESS_JOB_ID,
    )
    skipped = skipped_sources(cfg)
    if skipped:
        log.info("skipping %d source(s) — adapter not built yet:", len(skipped))
        for src in skipped:
            log.info("  %-10s (deferred)  %s", src.type, src.source_key)
    return jobs


__all__ = [
    "ScheduledJob",
    "build_jobs",
    "skipped_sources",
    "build_scheduler",
    "log_plan",
    "process_interval_s",
    "DEFAULT_JITTER_S",
    "DEFAULT_STARTUP_DELAY_S",
    "DEFAULT_PROCESS_INTERVAL_S",
    "PROCESS_JOB_ID",
]
