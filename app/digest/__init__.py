"""Scheduled digest query over the rolling store (run in the bot process). Phase 6.

A weekly digest is a scheduled QUERY over the rolling store + ONE single-shot summarize —
deterministic code plus exactly one model call, NOT an agent and NOT a fresh poll
(docs/01_technical.md §2.5; build plan Phase 6). The implementation lives in app.digest.run;
this package re-exports the frozen public surface the bot wires against.

Public surface (the frozen contract):
  - DigestResult        — primitives-only result of a run (topic, article_id, cluster_ids, rollup)
  - DigestCluster       — one selected story's detached pass-1 metadata + provenance
  - run_digest          — select → summarize → create the digest article + cluster links
  - parse_digest_schedule — PURE: "sun 09:00" → APScheduler CronTrigger kwargs
  - select_digest_clusters — the windowed, covered-marker-filtered, score-ranked query
  - summarize_digest    — the ONE model call (role digest_role()), capped
  - build_digest_prompt — PURE prompt assembly
  - env seams: digest_role / digest_max_chars / digest_title_limit
"""
from app.digest.run import (
    DigestCluster,
    DigestResult,
    build_digest_prompt,
    digest_max_chars,
    digest_role,
    digest_title_limit,
    parse_digest_schedule,
    run_digest,
    select_digest_clusters,
    summarize_digest,
)

__all__ = [
    "DigestCluster",
    "DigestResult",
    "build_digest_prompt",
    "digest_max_chars",
    "digest_role",
    "digest_title_limit",
    "parse_digest_schedule",
    "run_digest",
    "select_digest_clusters",
    "summarize_digest",
]
