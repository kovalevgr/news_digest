---
kind: owner
title: "The model-tiering stack behind the experiment (owner's note, 2026-09-06; from CLAUDE.md v1.3, session memory, .claude/agents/*; product identity stripped)"
url: (private repo; CLAUDE.md §"Sub-agent model policy", rev. 2 of 2026-08-03)
---

## Three tiers of models, by role, not by task

1. **Brain (Fable, the session model).** One interactive main loop the owner drives. Owns every "thinking" artifact: architecture decisions, contracts in `docs/contracts/*`, and the whole spec kit (spec / plan / tasks). Also: adjudication of review findings, triage, PR bodies, environment glue (migrations, cleanups). The brain does not write features.
2. **Implementers (Opus).** Four sub-agents with frontmatter `model: opus`: backend, frontend, infra, prompt. They receive a finished design and translate it into code. Open details are recorded in spec Clarifications as "gap filled this way", never redesigned. Each in its own git worktree; fan-out only explicit, and only when a committed contract (OpenAPI or JSON schema) exists between layers.
3. **Mechanics (Sonnet; Haiku for trivia).** Test and gate runs, one-line fixes, doc-only touch-ups. Never whole features.

Plus a **reviewer gate on the session model (Fable)**, read-only: constitution, secrets, test coverage, migration safety. Deliberately without a model pin, because it catches the most expensive mistakes at a third to a half of implementation cost. Merge is always a human.

## How it came about, with dates

- Before 2026-08-02: background agents silently inherited the session model; limits burned out 3–4 times a day.
- rev.1, 2026-08-02: implementation on Sonnet, brain and reviewer on Fable, detailed briefs as the carrier of design.
- Same day, T20 (state machine, ~1.2k lines): a Sonnet sub-agent authored both the spec kit and the implementation and declared 13 design deviations in its report, i.e. decisions the implementer should not have been making at all. The owner rolled the attempt back before review. This is not "Sonnet is weak" but "the wrong tier made the decisions".
- rev.2, 2026-08-03 00:55: the spec kit moved to the brain, implementation moved to Opus 5. First run under rev.2: Opus produced zero deviations from the contract and 26 implementation notes exactly where the contract left gaps. The reviewer found one real bug (stale-reply race) and four contract-text corrections, which the brain fixed.
- The rule lives in CLAUDE.md §"Sub-agent model policy", in the agents' frontmatter, and in an explicit `model` on every ad-hoc launch. The owner deliberately did not enable a hook to enforce it.

## Why it works (thesis for the piece)

- Design and code are separated not by a document but by model tier: the most expensive model thinks once, the cheaper one executes faithfully, the cheapest runs the gates.
- Briefs and contracts carry the design, so the implementer has a single quality criterion: "filled the gap" vs "quietly redesigned". That is exactly what the reviewer checks separately.
- Gates are the same for everyone: pytest, ruff ×2, mypy --strict, the provider-SDK import guard, pre-commit. Reviewer on top of gates, human on top of the reviewer.

## What today's experiment added

- Stage 2 confirmed that with the same implementer (Opus) the difference between arms is exactly the form in which the brain hands over intent: full spec (+128 after review) vs rules file (+239) vs CLAUDE.md only (+513).
- A rules file can encode a mistake as well as a rule (arm B: "retry once" vs the documented "up to twice"), and Opus will execute it. The spec with clarify surfaced the contradiction to the owner as a decision.
- Converge returned Converged only where the spec preceded the code.

## Care in the piece (owner's instruction)

The "Sonnet implements" policy lived less than a day, so write "an attempt to have the junior tier execute a whole feature", not "a model failure". Accompany the T20 numbers (13 → 0 deviations) with the note that the 13 were self-declared and that 8 of them were accepted into the contract.
