"""Poll scheduler planning (app.researcher.schedule) — pure, no DB, no network.

These pin the SCHEDULING DECISION, not APScheduler itself: build_jobs returns exactly one
job per implemented source at its resolved cadence, drops not-yet-built types (which
skipped_sources picks up instead), and preserves config order. We assert against both a
small synthetic Config and the real config.yaml, so the plan stays honest as adapters land.

A separate test exercises build_scheduler through a FAKE scheduler to confirm the per-job
safety options (coalesce / max_instances / interval seconds / jitter / initial run); it
importorskips APScheduler so it runs in the container but is skipped on a bare host.

The implemented/deferred split is read from the live registry (app.adapters.is_implemented)
rather than hardcoded, so these tests stay honest as adapters land — they assert the planner
faithfully mirrors whatever the registry currently considers buildable, not a frozen list.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from app.adapters import is_implemented
from app.config import Config, Source, load_config
from app.researcher.schedule import (
    DEFAULT_JITTER_S,
    PROCESS_JOB_ID,
    ScheduledJob,
    build_jobs,
    log_plan,
    process_interval_s,
    skipped_sources,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_YAML = REPO_ROOT / "config.yaml"

# Always-deferred (owner-credential-gated) source types. Reddit's OAuth JSON API adapter is
# still deferred (credential-gated); the X read-API adapter has since landed, so x_user is no
# longer here. These stay unscheduled regardless of which adapters have landed, so the
# real-config assertions can pin them as a stable lower bound on "skipped".
ALWAYS_DEFERRED_TYPES = {"reddit_sub"}


def _src(type_: str, key: str, cadence_s: int) -> Source:
    """A minimal Source — build_jobs only reads .type, .cadence_s, .source_key."""
    return Source(
        type=type_,
        identity={"k": key},
        cadence_s=cadence_s,
        owner=f"topic:test",
        source_key=f"{type_}:{key}",
    )


def _cfg(sources: list[Source]) -> Config:
    return Config(default_cadence_s=86400, sources=sources)


# ---------------------------------------------------------------------------
# build_jobs — the pure planner
# ---------------------------------------------------------------------------

def test_build_jobs_one_per_implemented_source_at_its_cadence():
    cfg = _cfg([
        _src("rss", "a", 3600),
        _src("rss", "b", 86400),
    ])
    jobs = build_jobs(cfg)
    assert [j.cadence_s for j in jobs] == [3600, 86400]
    assert [j.source_key for j in jobs] == ["rss:a", "rss:b"]
    assert all(isinstance(j, ScheduledJob) for j in jobs)
    # Job cadence is the source's own resolved cadence (cascade already applied upstream).
    assert all(j.cadence_s == j.source.cadence_s for j in jobs)


def test_build_jobs_excludes_unimplemented_types():
    # One source of every type; the planner keeps exactly the implemented ones (in order)
    # and drops the credential-gated ones — derived from the live registry, not hardcoded.
    all_sources = [
        _src("rss", "a", 3600),
        _src("reddit_sub", "ml", 86400),
        _src("hn", "best", 21600),
        _src("x_user", "karpathy", 172800),
        _src("github", "simonw", 86400),
        _src("arxiv", "cs.LG", 86400),
    ]
    cfg = _cfg(all_sources)
    jobs = build_jobs(cfg)
    expected_keys = [s.source_key for s in all_sources if is_implemented(s.type)]
    assert [j.source_key for j in jobs] == expected_keys
    assert {j.type for j in jobs} == {s.type for s in all_sources if is_implemented(s.type)}
    # The credential-gated types are never scheduled.
    assert ALWAYS_DEFERRED_TYPES.isdisjoint({j.type for j in jobs})


def test_build_jobs_preserves_config_order():
    cfg = _cfg([
        _src("rss", "first", 3600),
        _src("reddit_sub", "skipme", 3600),
        _src("rss", "second", 3600),
        _src("rss", "third", 3600),
    ])
    assert [j.source_key for j in build_jobs(cfg)] == ["rss:first", "rss:second", "rss:third"]


def test_build_jobs_empty_when_no_implemented_sources():
    # Only credential-gated (always-deferred) types -> nothing schedulable yet.
    cfg = _cfg([_src("reddit_sub", "ml", 3600), _src("reddit_sub", "csharp", 3600)])
    assert build_jobs(cfg) == []


def test_skipped_sources_is_the_complement_of_build_jobs():
    sources = [
        _src("rss", "a", 3600),
        _src("reddit_sub", "ml", 86400),
        _src("hn", "best", 21600),
    ]
    cfg = _cfg(sources)
    job_keys = {j.source_key for j in build_jobs(cfg)}
    skipped_keys = {s.source_key for s in skipped_sources(cfg)}
    # Every configured source is either scheduled or skipped — never both, never neither.
    assert job_keys.isdisjoint(skipped_keys)
    assert job_keys | skipped_keys == {s.source_key for s in sources}
    # The partition follows the live registry: skipped == exactly the unimplemented sources.
    assert skipped_keys == {s.source_key for s in sources if not is_implemented(s.type)}
    # reddit_sub is credential-gated, so it is always among the skipped here.
    assert "reddit_sub:ml" in skipped_keys


def test_scheduledjob_exposes_source_key_and_type():
    job = ScheduledJob(source=_src("rss", "x", 3600), cadence_s=3600)
    assert job.source_key == "rss:x"
    assert job.type == "rss"
    assert job.cadence_s == 3600


# ---------------------------------------------------------------------------
# Against the real authoritative config.yaml
# ---------------------------------------------------------------------------

def test_build_jobs_on_real_config_schedules_implemented_types():
    cfg = load_config(CONFIG_YAML)
    jobs = build_jobs(cfg)
    assert jobs, "config.yaml should have at least one schedulable source"
    # Every scheduled job's type is currently implemented; no credential-gated type slips in.
    assert all(is_implemented(j.type) for j in jobs)
    assert ALWAYS_DEFERRED_TYPES.isdisjoint({j.type for j in jobs})
    # Plan + skip partition exactly covers every configured source, with no overlap.
    job_keys = {j.source_key for j in jobs}
    skipped_keys = {s.source_key for s in skipped_sources(cfg)}
    assert job_keys | skipped_keys == {s.source_key for s in cfg.sources}
    assert job_keys.isdisjoint(skipped_keys)
    # Skipped types are exactly the not-yet-implemented ones (a superset of the always-deferred).
    assert {s.type for s in skipped_sources(cfg)} == {
        s.type for s in cfg.sources if not is_implemented(s.type)
    }
    assert ALWAYS_DEFERRED_TYPES <= {s.type for s in skipped_sources(cfg)}


def test_real_config_rss_jobs_carry_positive_cadence():
    cfg = load_config(CONFIG_YAML)
    for job in build_jobs(cfg):
        assert job.cadence_s > 0


def test_log_plan_returns_same_jobs_as_build_jobs(caplog):
    cfg = load_config(CONFIG_YAML)
    with caplog.at_level("INFO"):
        planned = log_plan(cfg)
    assert [j.source_key for j in planned] == [j.source_key for j in build_jobs(cfg)]


# ---------------------------------------------------------------------------
# build_scheduler — per-job safety options, via a fake scheduler
# ---------------------------------------------------------------------------

class _FakeScheduler:
    """Records add_job kwargs without needing a running APScheduler/DB."""

    def __init__(self):
        self.jobs: list[dict] = []

    def add_job(self, func, **kwargs):
        self.jobs.append({"func": func, **kwargs})


def _poll_jobs(fake) -> list[dict]:
    """The per-source poll jobs only — i.e. excluding the single periodic process job."""
    return [j for j in fake.jobs if j["id"] != PROCESS_JOB_ID]


def _process_job(fake) -> dict | None:
    return next((j for j in fake.jobs if j["id"] == PROCESS_JOB_ID), None)


def test_build_scheduler_sets_safety_options_per_job():
    pytest.importorskip("apscheduler")
    from app.researcher.poll import poll_source
    from app.researcher.schedule import build_scheduler

    cfg = _cfg([_src("rss", "a", 3600), _src("rss", "b", 86400)])
    fake = _FakeScheduler()
    returned = build_scheduler(cfg, scheduler=fake)
    assert returned is fake
    poll_jobs = _poll_jobs(fake)
    assert len(poll_jobs) == 2  # one per implemented source, deferred dropped

    for job, expected_cadence, expected_key in zip(poll_jobs, (3600, 86400), ("rss:a", "rss:b")):
        assert job["func"] is poll_source
        assert job["coalesce"] is True
        assert job["max_instances"] == 1
        assert job["id"] == expected_key
        assert job["replace_existing"] is True
        assert job["next_run_time"] is not None          # first poll fires shortly after boot
        # args carry exactly the one Source — never batched across sources
        assert len(job["args"]) == 1
        assert job["args"][0].source_key == expected_key
        trigger = job["trigger"]
        assert int(trigger.interval.total_seconds()) == expected_cadence
        assert trigger.jitter == DEFAULT_JITTER_S          # thundering-herd spread


def test_build_scheduler_registers_single_runner_process_job():
    """The post-poll pipeline (embed+cluster -> classify -> rank) is registered as ONE periodic
    job, separate from the poll jobs, with max_instances=1 + coalesce=True so two pipeline passes
    never overlap. It fires on its own interval (PROCESS_INTERVAL_S) shortly after boot."""
    pytest.importorskip("apscheduler")
    from app.researcher.schedule import build_scheduler

    cfg = _cfg([_src("rss", "a", 3600), _src("rss", "b", 86400)])
    fake = _FakeScheduler()
    build_scheduler(cfg, scheduler=fake)

    proc = _process_job(fake)
    assert proc is not None, "the periodic process pipeline job must be registered"
    assert proc["max_instances"] == 1          # single runner — passes never overlap
    assert proc["coalesce"] is True            # a missed tick collapses into one catch-up run
    assert proc["replace_existing"] is True
    assert proc["next_run_time"] is not None   # first pass fires shortly after boot
    assert not proc.get("args")                # no-arg callable; reads the whole DB
    trigger = proc["trigger"]
    assert int(trigger.interval.total_seconds()) == process_interval_s()


def test_build_scheduler_schedules_process_job_even_with_no_implemented_sources():
    """Even when no source has a built adapter, the process job is still scheduled — a backlog
    left in the DB (from a prior run / a sibling stage) must still get clustered and ranked."""
    pytest.importorskip("apscheduler")
    from app.researcher.schedule import build_scheduler

    # Both credential-gated -> no poll jobs, but the process job is always present.
    cfg = _cfg([_src("reddit_sub", "ml", 3600), _src("reddit_sub", "csharp", 3600)])
    fake = _FakeScheduler()
    build_scheduler(cfg, scheduler=fake)
    assert _poll_jobs(fake) == []              # no per-source poll jobs
    assert _process_job(fake) is not None      # the single-runner pipeline job is still there
