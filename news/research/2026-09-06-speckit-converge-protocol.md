---
title: "Experiment protocol — Spec Kit 0.7.4 → 1.0.x upgrade + /speckit.converge on T20 (TechScreen)"
date: 2026-09-06
status: planned
piece: idea 1 in 2026-09-05-article-picks.md (spec-driven), project_post
runs_in: the TechScreen Claude Code project (~/project_new/TechScreen, repo kovalevgr/tech-screen-ai)
results_to: pieces/<slug>/sources/techscreen-converge-results.md (kind: owner) in THIS repo
---

# Protocol: does `/speckit.converge` catch what a weak implementer got wrong?

Agent-facing brief for the TechScreen session. The owner runs this there; the writing
studio (news_digest) only consumes `results.md`. Owner approved (2026-09-06) using
TechScreen numbers publicly with product identity removed ("an internal AI interview
system"), so record numbers freely; strip client/product names in the results file.

## Question

TechScreen has been on GitHub Spec Kit 0.7.4 since 2026-04-18. Upstream shipped v1.0.0 on
2026-08-21 with a new `/speckit.converge` step that validates an implementation against its
spec. TechScreen also has a documented failure: the first T20 (orchestrator state machine)
implementation on Sonnet produced **13 design deviations** and was rolled back
(model-policy rev.2, 2026-08-03). Both the rolled-back attempt and the final Opus
implementation exist in git history.

**Does converge, run against the Sonnet attempt, find those 13 deviations? How many, which,
and what does it flag that the human reviewer did not?**

## Steps

0. **Guardrails.** New branch `036-speckit-1x-converge` off `main`. Do not merge until the
   owner says so. `auto_commit` stays off. Cloud DBs stay stopped (nothing here needs them).
   Follow TechScreen's model policy: the session model drives; mechanical runs on sonnet.
1. **Locate the 13 deviations.** Find where they are documented (PR body of the rolled-back
   attempt, a commit message, `specs/032-t20-state-machine/*`, or the reviewer output).
   Copy the list verbatim into `results.md` § A. Record the commit/branch of the Sonnet
   attempt and of the final implementation (`4c00996`, `2acb104`, `d8f0820`, `3618fb1`).
2. **Upgrade Spec Kit** to the latest 1.0.x (`uvx specify-cli` / `specify upgrade` per the
   upstream README at that moment). Record: before/after version, what changed under
   `.specify/` and `.claude/skills/speckit-*` (`git status --short`, count of files), whether
   the skills-not-slash-commands setup survived, anything broken, minutes spent. § B.
3. **Run converge on the FINAL T20** (the merged code) first, as the control: what does it
   report on code that passed the human reviewer gate? § C.
4. **Run converge on the SONNET attempt**: check out that state into a worktree (or revert
   the implementation files to the attempt's commit on the branch), same spec.md/plan.md,
   run converge, capture the full output. § D.
5. **Score.** For each of the 13 deviations: found / partially / missed. For each converge
   finding: true deviation / false positive / style-only. § E as a table.
6. **Cost + time** of each converge run (tokens if visible, wall clock). § F.
7. Optional, only if cheap: run the new `/speckit.analyze` or `/speckit.checklist` on the
   same two states and note whether they add anything converge did not.

## Output format — `results.md` (write it in the TechScreen repo under `specs/036-.../results.md`, then the owner copies it here)

```markdown
---
kind: owner
title: "Spec Kit 1.0 /speckit.converge vs a 13-deviation implementation — TechScreen, 2026-09"
date: <run date>
---
## A. The 13 deviations (verbatim list + where they were documented)
## B. Upgrade log (versions, file diff summary, breakages, minutes)
## C. Converge on the final implementation (control) — full output, then 3-line summary
## D. Converge on the Sonnet attempt — full output, then 3-line summary
## E. Scorecard
| # | Deviation | Converge on attempt | Notes |
| Converge finding | Verdict (true / false-positive / style) |
## F. Cost + time per run
## G. Owner's notes (what surprised, what was annoying, would you keep converge on?)
```

## Suggested prompt for the TechScreen session

```
Read /Users/kovalevgr/project/news_digest/news/research/2026-09-06-speckit-converge-protocol.md
and run it end to end on a new branch 036-speckit-1x-converge. Don't merge anything.
Write specs/036-speckit-1x-converge/results.md in the format the protocol gives.
Stop and ask me before the upgrade step if it wants to rewrite .claude/skills/speckit-*.
```

(Path above is the main checkout; if the news_digest branch is not merged yet, use the
worktree path `.claude/worktrees/github-pat-setup-644316/news/research/...`.)

## What the article will do with it

Three-pole framing (heavy process / standing rules file / nothing) with the owner's four
months of data (artifact size shrank 5–10× per feature; brain-authored specs after the
Sonnet rollback; reviewer-gate as the real quality lever) and this experiment as the
news hook: Spec Kit v1.0's converge step, tested against a known failure.
