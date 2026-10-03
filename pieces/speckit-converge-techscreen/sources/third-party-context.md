---
kind: source
title: "Third-party context for the spec-driven piece (fetched 2026-09-06)"
url: https://github.com/github/spec-kit/releases
url2: https://fabiensanglard.net/agent.md/index.html
url3: https://simonwillison.net/2026/Aug/19/conceptual-integrity-and-counting-lines-of-code/
url4: https://www.latent.space/p/attention-interface
---

## GitHub Spec Kit (WebFetch of README + releases, 2026-09-06)
- v1.0.0 on 2026-08-21 (one year after the first tracked release, 2025-08-07); v1.0.4 on 2026-09-02; 133.6k stars; "30+ AI coding agents".
- Workflow: `/speckit.constitution` → `specify` → `plan` → `tasks` → `implement` → **`converge`** (new: "validate implementation against specifications"); optional `clarify`, `analyze`, `checklist`.
- New extension workflows: bug-fix (assess → fix → test), idea assessment (intake → research → define → shape → decide).
- v1.0.0 changelog note: "adapting to breaking changes got cheap" with agent-based migrations, reducing the traditional value of semantic versioning.
- Integrations added Aug 13 – Sep 2: Mistral Vibe, Docker Agent, DeepSeek Harness.

## Fabien Sanglard — agent.md (2026-08-21)
A file the coding assistant loads at session start to enforce standards: minimal docs, short functions, early returns, enums over booleans, magic numbers into constants, private-by-default, seven commit-message rules. His timeline: mid-2025 code did not compile; Jan 2026 complex tasks but "spaghetti code with no comments"; from March 2026 with agent.md, near production quality. Names "context dilution": short sessions per feature, reload agent.md when quality drops.

## Simon Willison — Conceptual integrity and counting lines of code (2026-08-19)
LOC is a fair yardstick again if quality holds: humans 50–200 debugged lines/day, agents ~1,000. "Conceptual integrity" (Brooks, Mythical Man-Month): software that fits together and is unsurprising; agents undermine it by making feature additions cheap (Winchester Mystery House). New bottleneck: cognitive capacity to hold the codebase, not code production.

## Latent Space — The Evolution of the Agent Harness (2026-08-22, radar-verified)
Harness-Bench: same model scores 52.4–76.2 across harnesses (23.8 points, no weight change).
