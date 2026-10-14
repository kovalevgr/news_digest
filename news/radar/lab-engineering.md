---
category: lab-engineering
updated: 2026-10-14
---

# Radar: lab-engineering

Technical-radar items for this category (sources in [`config/radar.json`](../config/radar.json)).
Appended by the daily routine under weekly headings; format matches topics files.

## 2026-W42

- **2026-10-14** — ⭐ [Redesigning source control](https://www.anthropic.com/engineering/redesigning-source-control) — Verified via WebFetch: Anthropic replaced git for its monorepo with an in-house system, Scion, as merge volume grew from ~2,500/day (May 2026) to 30,000+/day (September) driven by Claude coding agents, while git's distributed-client assumptions stopped fitting an always-online, agent/CI-heavy workload (~100GB main-branch history, ~25M CI checkouts/day). Scion moves commits/merges/blame/diffs server-side as cheap, lock-free "changesets," exposes everything via API so most jobs need no local repo, and makes working copies optional/sparse/virtualized. Reported results: ~200x less CPU/memory than the prior git-mirror fleet, checkouts in seconds instead of minutes, +25% CI capacity; built in 5 months by a 7-person team, with Claude itself rewriting a hand-written ingestion pipeline for 20x less memory and 4x the speed, and "superfan" Claude agents monitoring components in production. Direct hit on "AI agents in practice" + the owner's own Claude Code tooling — a concrete blueprint for source control once agents, not humans, are the primary client (authors note it is not a general git replacement).
