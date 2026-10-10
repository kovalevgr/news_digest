---
kind: owner
title: "TechScreen: ADR-017 (Spec Kit decision, 2026-04-18) + four months of numbers (collected 2026-09-06)"
url: (private repo kovalevgr/tech-screen-ai; product identity to be stripped in the piece: "an internal AI interview system")
---

## ADR-017 (2026-04-18) — verbatim core
Context: "Without a disciplined spec-first workflow, AI assistance produces fast-but-wrong code that costs more to revert than to write by hand." Evaluated: informal / custom in-house / GitHub Spec Kit. Decision: Spec Kit. Negative consequence acknowledged: "Adds ceremony for small features. Mitigated by the 'trivial changes can skip' carve-out."

## Numbers (git, 2026-04-19 → 2026-08-03)
| Fact | Value |
| --- | --- |
| Commits / merged PRs | 225 / 36 |
| Features under Spec Kit (`specs/*`) | 26 |
| Code (`app/**` py/ts/tsx) vs spec artifacts (`specs/` + `docs/contracts/`) | 28,794 vs 20,495 lines (0.71 spec lines per code line) |
| Spec artifacts per feature, first 19 features (001–022) | 340–1,897 lines; full set: research, data-model, quickstart, checklists, contracts |
| Spec artifacts per feature, last 8 features (028–035) | 56–216 lines; spec/plan/tasks only |
| Reviewer-gate fix commits (`fix(...): reviewer findings`) | 13 |
| Constitution | 20 invariants; §14 contract-first before parallel fan-out |
| Spec Kit version in repo before stage 1 | 0.7.4 (init 2026-04-19, skills mode, auto_commit off by choice) |

## Model policy rev.2 (CLAUDE.md, 2026-08-03) — verbatim core
"The main loop (the 'brain') owns ALL thinking artifacts: architecture and design decisions, docs/contracts/*, and the Spec Kit artifacts (spec.md, plan.md, tasks.md). Sub-agents receive finished designs and implement them faithfully; open details go to spec Clarifications, never into redesign." Trigger (session memory): the first Sonnet-implemented T20 attempt produced 13 documented design deviations and was rolled back; Opus then implemented "with ZERO contract deviations (26 gap-fill notes)".

## Known pains (session memory `techscreen-gotchas`)
`specs/*/tasks.md` checkboxes unreliable (features 001–007, 017 unchecked despite merged); stacked PRs do not auto-retarget; ceremony for small features.
