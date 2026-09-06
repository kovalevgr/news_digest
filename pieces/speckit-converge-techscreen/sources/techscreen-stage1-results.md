---
kind: owner
title: "Spec Kit 1.0 /speckit.converge vs a 13-deviation implementation — TechScreen, 2026-09"
date: 2026-09-06
---

Stage 1 of the protocol in `news_digest/news/research/2026-09-06-speckit-converge-protocol.md`.
Branch `036-speckit-1x-converge` off `main` @ `75d1006`. Nothing merged, nothing pushed.
Product identity: "an internal AI interview system"; client name stripped.

## A. The 13 deviations (verbatim list + where they were documented)

### Where they are documented

1. **Primary source — the implementer's own final report.** The 13 items are the Sonnet
   sub-agent's self-declared "Deviations, each with one-line rationale" section in its
   task-completion report (Claude Code session `5842b161-…`, agent task `a867fec511abbf33d`,
   report timestamp 2026-08-02 22:47 UTC; 196 tool uses, 359,821 sub-agent tokens, 58 min).
   The list below is copied verbatim from that report.
2. **The attempt's own spec kit** — `specs/032-t20-state-machine/spec.md` at commit `d464a9a`
   (`## Clarifications › Session 2026-08-03`) restates the same 13 as Q→A pairs, in the same
   order, plus the 21-edge test mapping.
3. **The adjudication** — contract `docs/contracts/state-machine.md` §Amendments v1.1
   (commit `f9cc0cd`): "folded accepted refinements from the discarded first implementation
   round … the discarded round's remaining deviations were rejected or made moot"; PR #33
   body "Provenance note": "its 8 acceptable design refinements were folded into contract
   v1.1 … the rest rejected"; final spec.md Clarification 1 names the two rejected readings
   (two-round-trip advances; a separate no-op `ScheduleNothing` command).
4. **Memory / policy** — `CLAUDE.md` §Sub-agent model policy rev. 2 (commit `687edaf`) and the
   session memory file `techscreen-progress.md`: "opus implemented with ZERO contract
   deviations (26 gap-fill notes) vs sonnet's discarded round (13 design deviations)".

**Important nuance for the article:** no reviewer gate ever ran on the Sonnet attempt. The
owner read the implementer's report, judged that an implementer should not have been making
13 design decisions at all, and rolled the round back on process grounds (2026-08-03 00:52
local) before review. "13 deviations" is therefore the implementer's *own* count against
contract v1.0 (`6079df2`), not an independent audit. Eight of the thirteen were then
*accepted into* the contract (v1.1), so measured against the contract on `main` today (v1.2)
only a subset remain deviations by construction — see § E for the per-item status.

### The list (verbatim, from the implementer's report)

> 1. `awaiting` promoted to a top-level `SessionState` field instead of nested in `TechState` (contract §4's literal pseudocode) — the same turn-taking concept applies uniformly across INTRO/TECH/QA/CLOSE, not just TECH; one field avoids desync.
> 2. Edge 3's `ScheduleNothing` is represented by omission (no `RunAssessor` in the command tuple), not a distinct no-op `Command` variant.
> 3. CLOSE modeled as a real, separately-persisted phase; edge 17 mirrors edge 4's `awaiting=="interviewer"` guard shape. The contract's "`InterviewerReplyReady` / immediate" is read as a shell-level optimization, not a second core code path.
> 4. Edges 10/12 (advance to next competency) issue **one** `RunInterviewer(move="ask_seed", ...)` call with the prior-competency acknowledge/close framing folded into `context["transition_note"]`, since `InterviewerMove` allows exactly one move per call and the machine has one outstanding call at a time.
> 5. Only `seed_questions_uk[0]` is consumed per competency by the T20 loop; index 1+ is accepted for forward Planner-shape compatibility but not driven by T20 — all follow-up goes through the `depth_probe` budget.
> 6. Command `turn_id`s are derived via `uuid.uuid5(session_id, structural counters)`, never `uuid4()` — satisfies "no randomness" and makes edge 21 reissue idempotent by construction, not just by caching.
> 7. `_adjudicate()` evaluation order settled explicitly: ANSWERED → `latest_level==0` short-circuit → budget-exhausted-or-not-assessable → else CLARIFY. `proceed_planned` (§6.1) falls out of this same table with zero/partial data rather than being a separate branch.
> 8. `CoverageCell` tracks `best_*` (max level, ties take latest) separately from `latest_*` (most-recently-completed) since §5 uses different aggregations for ANSWERED vs. the level-0 NONE trigger; `assessed_turn_ids` and `empty_assessment_seen` are mutually exclusive per turn so `gap_not_assessable`/`assessment_failed`/`gap_budget_exhausted` are distinguishable.
> 9. TimerTick priority: candidate-timeout (edge 18) checked before session/QA budget (edges 14/16) — silence is treated as the stronger signal.
> 10. Forced QA/CLOSE on TimerTick implemented only for TECH/QA phases (literal table scope); INTRO/CLOSE get no speculative equivalent.
> 11. `AssessmentCompleted`/`AssessmentFailed` generalized beyond literal "TECH/any" to "any non-terminal phase, `tech` populated, turn_id still pending" — needed for late-arriving data to update coverage even after the phase has moved on (§6.1).
> 12. Rubric-snapshot cross-check on `PlanCompetency.node_id` deliberately deferred to a future session-start service (explicitly flagged in the brief as T22-time).
> 13. No feature flag added — contract §11 places the dark-launch flag at T22/T29's exposure point; `state_machine.py` has no caller outside tests today.

The report also raised 4 open questions for the reviewer (one-call vs two-round-trip advance;
tick priority; persist-ordering being the shell's job; migration verified offline only — no
Docker in the sandbox).

### Commits

| What | Commits | Reachability |
| --- | --- | --- |
| Sonnet attempt (rolled back) | `6079df2` contract v1.0 → `6aff960` core + persistence → `283e773` tests → `d464a9a` spec kit (all 2026-08-03 00:20–00:46 local, based on `main` @ `f8661b5`) | Were dangling (branch `worktree-agent-a867fec511abbf33d` deleted in the rollback). Pinned today with the local tag `archive/032-t20-sonnet-attempt` (not pushed). |
| Final (Opus, merged as PR #33) | `687edaf` policy rev. 2 → `f9cc0cd` contract v1.1 → `4490cc0` spec kit (main-loop authored) → `2acb104` core → `54c6852` persistence → `d8f0820` tests → `4c00996` contract v1.2 → `3618fb1` reviewer fix round → merge `232ae28` | On `main`. |

Attempt vs final, implementation scope only (`app/backend/orchestrator`, tests, migration,
model mapping, `configs/orchestrator.yaml`): 25 files, +4014/−2638 — the final is a rewrite,
not a patch. The attempt's core was 1,175 lines; the final's 1,395 (+26 fix round).

## B. Upgrade log (versions, file diff summary, breakages, minutes)

_Before state recorded 2026-09-06 11:39 local; the upgrade itself is pending the owner's go
(the integration upgrade rewrites every `.claude/skills/speckit-*/SKILL.md`)._

**Before:** Spec Kit `0.7.4.dev0` (init 2026-04-19, `--ai claude --ai_skills`, skills mode,
`script: sh`), `specify integration status` → OK, 0 modified / 0 missing managed files,
git extension v1.0.0 with `auto_commit: default: false`. No persistent `specify` binary on
the machine — the project has always used ephemeral `uvx --from git+…`.
Upstream: v1.0.4 released 2026-09-02 (1.0.0 on 2026-08-21); `main` reports `1.0.5.dev0`.
Upgrade path per upstream `docs/upgrade.md`: `specify integration upgrade claude` (manifest-
aware; blocks on locally-modified managed files) then `specify extension update`; the old
`specify init --here --force` is now the documented fallback only.

**Trial run on a throwaway clone** (`uvx --from git+…@v1.0.4 specify integration upgrade claude`,
1 s wall clock): 27 tracked files modified, 4 new — 14 `SKILL.md` rewrites (content, not
mode-only; +1,530/−706 across everything incl. scripts), new `.claude/skills/speckit-converge/SKILL.md`
(279 lines), scripts `common.sh` (+893 lines diff), `check-prerequisites.sh` (gains
`--require-spec`), `create-new-feature.sh`, `setup-plan.sh`, new `resolve-template.sh` and
`setup-tasks.sh`, 4 templates, manifests + `init-options.json` + `integration.json`
(new `integration_state_schema: 1`), extension registry re-registers the 5 git skills, and a
new `.specify/.gitignore` that untracks `feature.json` (currently committed). The CLI printed
"9 shared infrastructure path(s) already exist and were not updated" yet those exact files
show content diffs — misleading message, observed result recorded here. `specify extension
update` → "All extensions are up to date" (git v1.0.0; no `before_converge`/`after_converge`
hooks added to `extensions.yml`). Untouched: constitution, `specs/`, `extensions.yml`,
`git-config.yml` (`auto_commit` stays off), `CLAUDE.md`.

**Real run (owner's go, 2026-09-06 11:56:58 local):** `uvx --from git+https://github.com/github/spec-kit.git@v1.0.4 specify integration upgrade claude`
→ 3 s wall clock, identical result to the trial (31 paths: 27 modified, 4 new; +1,530/−706).
`specify extension update` → "All extensions are up to date". `specify integration status` →
OK, `Multi-install safe: yes`, 0 modified / 0 missing managed files. Every `speckit-*` skill
still parses (`name:` frontmatter present; the git-extension skills use unquoted values,
unchanged from 0.7.4). Committed as one commit `c04b19f` on `036-speckit-1x-converge`;
TechScreen's own pre-commit hooks (shellcheck, gitleaks, secrets scans) passed on the upstream
scripts. **Skills-not-slash-commands setup survived** (`integration_settings.claude.invoke_separator: "-"`).

**After:** Spec Kit `1.0.4`. New in the workflow: `speckit-converge` (append-only: its only
write is a `## Phase N: Convergence` section in tasks.md); `check-prerequisites.sh --require-spec`;
feature resolution now via `SPECIFY_FEATURE_DIRECTORY` env or `.specify/feature.json`
(persisted on every run, now gitignored — the tracked copy stays tracked until someone
`git rm --cached`s it). Behavioural changes in the rewritten skills worth knowing before
keeping the upgrade: `speckit-implement` now treats checklists as a read-only gate and reads
the constitution; `speckit-clarify` (+102 lines) and `speckit-specify` (+140 lines) grew
noticeably — the interactive flow will feel different; hook blocks now say the agent MUST
actually invoke a mandatory hook (moot here: no mandatory hooks, `auto_commit` off).

**Breakages:** none found. **Doc drift:** `CLAUDE.md` still says "Spec Kit `0.7.4`" and the
workflow list lacks `speckit-converge` — a one-line owner edit if the upgrade is kept.

**Minutes:** ~25 min total for step 2 — 1 s + 3 s of CLI time; the rest was reading the
upstream upgrade guide/changelog, the trial run on a scratch clone, and the diff review.

### Run setup for §C–§D

- Three git worktrees off the upgraded commit `c04b19f`, one per run, each with
  `.specify/feature.json → specs/032-t20-state-machine` committed so the only diff a run can
  produce is its own tasks.md append:
  - **C control** — branch `036-run-control` @ `2b18bb2`: `main`'s T20 exactly.
  - **D attempt/v1.2** — branch `036-run-attempt-v12` @ `e1aa555`: the Sonnet attempt's
    implementation files (`app/backend/orchestrator/**`, `app/backend/tests/orchestrator/**`,
    migration 0006, `configs/orchestrator.yaml`; the final's `tests/db/test_session_state_persistence.py`
    removed) swapped in from `283e773`; `spec.md`/`plan.md`/`tasks.md` and the contract (v1.2)
    exactly as on `main`. `interview.py` kept from main (both versions add the same
    `session_state` column; main's also carries T21's `dev_transcript`). Note the T21/T22 shell
    on main imports the *final* orchestrator's names — with the attempt's package swapped in,
    the shell would not import; converge is told not to run tests, and this is outside the
    032 scope map, but any finding citing it is noted in §E.
  - **D′ attempt/v1.0** — branch `036-run-attempt-v10` @ `fb548b9`: as D, plus
    `docs/contracts/state-machine.md` reverted to v1.0 (`6079df2`) — the text the attempt was
    actually written against, so the 8 folded-in refinements are visible as deviations.
- Each run = one background sub-agent on the session model (Fable 5.1; the reviewer-gate tier
  per CLAUDE.md model policy), told to read and execute
  `.claude/skills/speckit-converge/SKILL.md` verbatim, empty `$ARGUMENTS`, present-state only
  (no git history, no tests/gates, no other worktrees), report the full prescribed output.
- One interpretation note given to all three runs (recorded because it matters): spec.md
  says the contract is normative and "this spec does not restate it", so the contract is
  treated as incorporated by reference into the intent inventory. Without that note a
  literal converge (spec/plan/tasks as the "sole source of intent") would have almost nothing
  to check T20's logic against.
- All three launched in parallel at ~12:05 local.

## C. Converge on the final implementation (control) — full output, then 3-line summary

Worktree `036-run-control` @ `2b18bb2` — `main`'s T20 (final Opus implementation + reviewer fix round), contract v1.2.

Sub-agent report, verbatim (model Fable 5.1; 27 tool uses; 202,741 tokens; 11:59:53 → 12:05:11, 5 min 18 s):

> **Prerequisite script:** `{"FEATURE_DIR":".../036-run-control/specs/032-t20-state-machine","AVAILABLE_DOCS":["tasks.md"]}`. SPEC/PLAN/TASKS present (`AVAILABLE_DOCS` only enumerates optional docs). Constitution present, filled (v1.1) → checks applied. Pre-execution hook check: no `hooks.before_converge` → skipped silently. `$ARGUMENTS` empty.
>
> **Files read:** skill, extensions.yml, feature.json, constitution; spec/plan/tasks; contract v1.2; `orchestrator/{__init__,state_machine (full, 1421 lines),plan,config,persistence}.py`; `configs/orchestrator.yaml`; migrations 0006 + 0007 header; `db/models/interview.py` L100–150; `llm/models_config.py` L1–80 (the loader `config.py` must mirror); `agents/interviewer.py` (`InterviewerMove`, `InterviewerOutput`), `agents/assessor.py` (`AssessorOutput` etc.); `scripts/check-no-provider-sdk-imports.sh` (existence); `prompts/shared/candidate-facing/` listing; all 11 files under `tests/orchestrator/`; `tests/db/test_session_state_persistence.py`; `tests/conftest.py` (grep for the `DATABASE_URL` skip gate).
>
> **Interpretation note:** acknowledged and applied — contract §2–§9 shapes/policies, §10 edges 1–21, §11 hooks in the intent inventory alongside FR-032-1..10, SC-1..5, the 26 Clarifications/notes, plan.md, tasks.md.
>
> ### Convergence Findings
>
> | ID | Gap Type | Severity | Source | Evidence | Remaining Work |
> |----|----------|----------|--------|----------|----------------|
> | F1 | partial | LOW | spec Clarification 26 / contract §Amendments v1.2 (spec header: contract is normative) | `app/backend/orchestrator/state_machine.py:3` declares "Normative design: `docs/contracts/state-machine.md` **v1.1**" and `app/backend/orchestrator/__init__.py:5` cites "(v1.1), which is normative", while the contract's §Amendments records v1.2 (2026-08-03, reviewer gate) as current and spec Clarification 26 states v1.2 made notes 8/9/15 normative. Code behaviour already matches v1.2 (verified: edge 14 split at `_on_timer_tick` lines 1335–1339, inclusive budget guards `>=` at lines 947/955, §6.9a stale-reply guard `_answers_pending_command` at lines 623–640 gating both reply and failure handlers, `PersistState` emitted exactly per table). Only the cited normative version is stale. | Update the two docstrings to cite contract v1.2 |
>
> **Summary metrics:**
> - Requirements / acceptance criteria checked: 10 FRs + 5 SCs + 39 contract items by reference (§2 phases, §3 nine events, §4 state shape, §5 adjudication table, §6.1–§6.9a ten policies, §7 plan shape, §8 config, §9 persistence, §10 edges 1–21 each individually, §11 hooks) + 26 Clarifications/implementation notes. SC-1 and SC-2 verified by inspection (named `test_edge_01…21` fixtures all present; the ANSWERED/CLARIFY/NONE × present/pending/failed matrix complete in `test_adjudication.py` L56–157 incl. the `confidence == confidence_min` boundary and probe-exhaustion cases; determinism and JSON round-trip in `test_determinism.py`). SC-3/4/5 are gate-run/diff outcomes not verifiable statically under this run's no-git/no-test rules; no code gap observed for them.
> - Plan decisions checked: 8 — Phase 3 core files, Phase 4 persistence (migration `0006` in chain, nullable JSONB mapping, `StateSchemaVersionError`), Phase 5 test suites, source-tree layout, gate plan, state-schema-evolution risk, `agent:`/`parallel:` labels (§18), contract-first (§14). Plus T001–T021 verified against present code (T017 stale-reply guard + `test_stale_replies.py`; T018 hardened purity guards incl. attribute-form scan, `import uuid` ban, `ast.Match`, `description_en`/`manual_review_reason_en`; T019 `plan.py` cites Clarification 11).
> - Constitution principles checked: 20 reviewed; 12 with buildable obligations assessed (§2, §3, §5, §9, §10, §11, §14, §15, §16, §17, §18, §19) — **0 violations**; 8 not applicable.
> - Findings by gap type: missing 0 / partial 1 / contradicts 0 / unrequested 0.
> - Findings by severity: CRITICAL 0 / HIGH 0 / MEDIUM 0 / LOW 1.
>
> **Outcome:** `tasks_appended`
>
> **Next Actions (handoff):** 1 task (T022) appended under `## Phase 8: Convergence`. Run `/speckit-implement` to complete it (two docstring edits, no behavioural change). A follow-up converge should then find no remaining items.
>
> **Extension Hooks:** none registered.
>
> **Observations recorded but deliberately NOT raised as findings:**
> - §6.5 references an undefined threshold `qa_minutes_min` that appears in neither §7 (plan) nor §8 (config). The code follows the normative §10 edge 14 (v1.2 split): after `session_max` is reached the next tick in QA goes to CLOSE, so post-budget Q&A is effectively one tick. A contract-internal inconsistency in a spec-by-reference document; converge may not edit spec artifacts, so no task was emitted.
> - Resume re-issues only `pending_command` (`RunInterviewer`/`DeliverUtterance`/`EmitScripted*`), never a `RunAssessor` that a crash may have prevented the shell from dispatching. §9 and edge 21 say "the pending command" (singular), so the requirement as written is met; a lost assessment degrades gracefully to a `gap_budget_exhausted` reviewer gap via `proceed_planned`. Surfaced for the contract owner, not tasked.
> - `InterviewSession.dev_transcript` and migration `0007` are T21's; outside this feature's bounded scope, not classified as `unrequested`.
>
> **Appended to tasks.md (verbatim):**
>
> ```markdown
> ## Phase 8: Convergence
>
> - [ ] T022 Update the contract version cited as normative in app/backend/orchestrator/state_machine.py (module docstring, "**v1.1**") and app/backend/orchestrator/__init__.py ("(v1.1), which is normative") to v1.2, matching docs/contracts/state-machine.md §Amendments — code behaviour already matches v1.2, only the cited version is stale — per spec Clarification 26 / contract §Amendments v1.2 (partial)
> ```
>
> `git status --short` → ` M specs/032-t20-state-machine/tasks.md` only.

**3-line summary (C):** On code that passed the human-plus-Fable reviewer gate, converge found exactly one LOW item — two docstrings still cite contract v1.1 — and 0 contract, plan or constitution gaps; it independently re-verified the reviewer's two fixes (stale-reply guard, hardened purity guards) as present. It did not go clean ("Converged") because a docstring counts as `partial`; the outcome was still `tasks_appended`. Its two un-tasked observations (undefined `qa_minutes_min` in §6.5; resume never re-issues a lost `RunAssessor`) are contract-owner questions the reviewer gate did not raise either.


## D. Converge on the Sonnet attempt — full output, then 3-line summary

### D.1 Run D — attempt code, contract v1.2, `main`'s spec kit (worktree `036-run-attempt-v12` @ `e1aa555`)

Sub-agent report, verbatim (model Fable 5.1; 22 tool uses; 172,268 tokens; 12:00:06 → 12:04:47, 4 min 41 s):

> **Prerequisite script:** `{"FEATURE_DIR":".../036-run-attempt-v12/specs/032-t20-state-machine","AVAILABLE_DOCS":["tasks.md"]}`. Pre-execution hook check: `.specify/extensions.yml` exists; no `hooks.before_converge` / `hooks.after_converge` → skipped silently.
>
> **Files read:** the converge SKILL.md, extensions.yml, feature.json, constitution; spec.md, plan.md, tasks.md; `docs/contracts/state-machine.md`; `app/backend/orchestrator/{__init__,state_machine (full, 1175 lines),plan,config,persistence}.py`; `configs/orchestrator.yaml`; migration 0006 (+ `down_revision` grep); `db/models/interview.py` L100–145; `services/dev_session.py` L90–105 (import block only); all 11 files under `tests/orchestrator/`; directory listings. No git history commands; no tests/gates executed.
>
> **Interpretation note:** acknowledged and applied — contract §1–§11 inventoried as spec requirements alongside FR-032-1…10, SC-1…5, Clarifications 1–7, notes 8–26, plan/tasks.
>
> ### Convergence Findings
>
> | ID | Gap Type | Severity | Source | Evidence | Remaining Work |
> |----|----------|----------|--------|----------|----------------|
> | F1 | contradicts | HIGH | Clarification 2; contract §10 edges 10 & 12; §4 ("bare `ask_seed` only for the very first seed after INTRO") | `state_machine.py` `_advance_to_next_competency` (~L726–767) issues `RunInterviewer(move="ask_seed")` with a `context["transition_note"]` string on every competency advance instead of `acknowledge_and_transition` (ANSWERED) / `close_competency` (NONE) with the next seed in `move_context`; it also sets `tech.last_issued_move="ask_seed"`, so an Interviewer that correctly executes the transition move is counted as drift (§6.4). `test_transition_table_adjudication.py::test_edge_10_...` asserts `move == "ask_seed"`, codifying the deviation | Emit the contract move vocabulary on edges 10/12 with the next seed in `move_context`; set `last_issued_move` accordingly; fix edge 10/12 tests |
> | F2 | missing | HIGH | contract §4 multi-seed rule (v1.1); Clarification 2; T012 "multi-seed iteration" | On ANSWERED the core always advances to the next competency; no branch checks `seed_questions_uk[k+1]` + competency time remaining. `TechState` has `seeds_asked`, no `seed_index`; `_seed_context` always reads `seed_questions_uk[0]`; `plan.py` docstring states multi-seed is "not consumed by the T20 loop". No test exercises a second seed | Implement the per-competency seed loop and add the multi-seed iteration test |
> | F3 | missing | HIGH | contract §6.9a; spec note 23; T017 | No `_answers_pending_command` guard exists (grep: 0 hits). `_handle_interviewer_reply_ready` (L855–862) and `_handle_interviewer_failed` (L910–939) never compare `event.turn_id` to `state.pending_work.turn_id`. `test_stale_replies.py` does not exist. Consequence: after edge 14 preempts an in-flight probe, the stale reply is delivered, `awaiting` flips to candidate, and the real ack reply is then dropped by `_unchanged` | Add the stale-reply no-op guard to both handlers (CLOSE included) and the `test_stale_replies.py` suite |
> | F4 | partial | HIGH | FR-032-10; spec note 24; T018 | `test_static_guards.py` has only: `import random` ban, `uuid4()` call ban, `.now()`/`time.time()` bans, `.text`/`should_*` attribute bans, 4 I/O substrings. Absent: attribute-form randomness scan (`random.*`, `secrets.*`), `import uuid` ban (and `state_machine.py:41` does `import uuid`, the form note 24 bans), `ast.Match`/`case`-guard inspection, prose-attribute set (`description_en`, `manual_review_reason_en`, `rationale_en`, `evidence_*`). T018 is checked in tasks.md but the work is not present | Harden the guards per note 24; switch the core to `from uuid import UUID, uuid5`; verify each predicate against a planted violation |
> | F5 | partial | MEDIUM | contract §10 edge 17 ("InterviewerReplyReady / immediate"); spec note 23 ("its 'immediate' `TimerTick` path") | `_handle_timer_tick` (L1043–1071) has no CLOSE branch; CLOSE exits only via a shell-synthesised `InterviewerReplyReady` (the closing is scripted — no LLM call produces one). Otherwise the only exit is edge 18's `candidate_timeout` abort, and `_close_session` (L835–849) does not refresh `last_candidate_activity_at`, so a finished interview would be recorded `ABORTED(candidate_timeout)` | Add the immediate/`TimerTick` completion path for CLOSE and a test; ensure CLOSE cannot fall into candidate-timeout abort |
> | F6 | contradicts | MEDIUM | spec note 16; Handoff T21 (`ABORTED(cost_ceiling)` hook) | `OperatorAbort.reason: str` (free text, L308–313); `_handle_operator_abort` does `del event` and hard-codes `abort_reason="operator_abort"` (L1093–1098). `ABORTED(cost_ceiling)` is unreachable through the event alphabet | Type `OperatorAbort.reason` as the §2 abort set, copy it onto `abort_reason`; add a test reaching `cost_ceiling` |
> | F7 | contradicts | MEDIUM | spec note 11 ("Unknown extra keys are tolerated") | `plan.py`: `PlanCompetency` and `PlanSnapshot` both declare `extra="forbid"`; `test_plan.py::test_plan_snapshot_rejects_unknown_top_level_fields` asserts rejection | Tolerate extra keys per note 11 and invert the test |
> | F8 | partial | MEDIUM | FR-032-9; SC-1; T012 adjudication matrix | Covered: ANSWERED×present (edge 10), CLARIFY×present (11), NONE×present (12), CLARIFY×pending (07), CLARIFY×failed (07). Absent: NONE×pending, NONE×failed (no test produces the `assessment_failed` outcome of `_finalize_gap_outcome`, L1171–1172), ANSWERED×pending/failed | Add the missing matrix cells as named tests |
> | F9 | partial | MEDIUM | spec note 20 (`confidence_min` capped at 0.99) | `AdjudicationConfig.confidence_min = Field(ge=0.0, le=1.0)` (L464); `confidence_min: 1.0` loads and makes ANSWERED unreachable mid-interview. `test_config.py` only checks 1.5 | Cap at 0.99 and add a loader test at 1.0 |
> | F10 | contradicts | LOW | contract §6.6; spec note 15 (strict `>`) | `_candidate_timed_out` uses `elapsed >= timedelta(...)` (L1078). `test_edge_18_*` uses 11 min, not the boundary | Change to strict `>`; add a boundary test |
> | F11 | partial | LOW | contract §4 (top-level `last_issued_move`, `seed_index`, `pending_assessments: [turn_id]`); spec notes 10 (`plan_input`), 13 (`assessment_focus`) | `SessionState` has `plan_raw`; `last_issued_move` nested in `TechState`; `seeds_asked` instead of `seed_index`; `pending_assessments` is `dict[turn_id, node_id]` (L184–226). Persisted `state_schema_version=1` JSON diverges from §4 | Align the shape with §4 / notes 10, 13 (or record the deviation), keeping round-trip tests green |
> | F12 | missing | LOW | spec note 19 | grep for `OPENING_SCRIPT_PATH` / `CLOSING_SCRIPT_PATH` under `app/` returns nothing | Add the two path constants (reference only) |
> | F13 | partial | LOW | spec note 12 | `ReissuePendingCommand` is flattened with `label ∈ {run_interviewer, emit_scripted, deliver_utterance}` (L414–426); cannot distinguish `EmitScriptedOpening` from `EmitScriptedClosing` | Carry the outstanding command or an opening/closing discriminator |
> | F14 | partial | LOW | contract §5 (`needs_manual_review` "recorded in coverage + session flags") | Recorded only on `CoverageCell.had_manual_review_flag` (L968, L985); no session-level flag on `SessionState` | Add a session-level manual-review flag |
> | F15 | partial | LOW | spec note 8; contract §10 edges 14, 15 | Edge 15 (L826–832) emits `PersistState` where the table has none; edge 14 TECH→QA (L1069–1070) emits `RecordGap`+`PersistState` beyond "as #13". Advisory per §9 v1.2, but note 8 claims verbatim | Make tuples literal or amend note 8 |
>
> **Summary metrics:**
> - Requirements / acceptance criteria checked: FR-032-1…10 (10); SC-1…5 (5 — SC-3/4/5 not statically assessable without running gates or git; artefact presence only); Clarifications/notes 1–26 (26); contract §10 edges 1–21 (21; every edge has a `test_edge_NN_*` fixture); §6 policies 1–9 + 9a (10); §4/§5/§7/§8/§9 shapes (5)
> - Plan decisions checked: 7 (phases 1–5, source tree, `state_schema_version` risk)
> - Constitution principles checked: 8 (§2, §3, §4, §5, §9, §11, §16, §17) — no MUST violation observed; §3 respected (`persistence.py` UPDATEs only `interview_session`, outside the append-only set); migration chain intact (0007 revises 0006); `InterviewSession.session_state` mapped as nullable JSONB
> - Findings by gap type: missing 3 / partial 8 / contradicts 4 / unrequested 0
> - Findings by severity: CRITICAL 0 / HIGH 4 / MEDIUM 5 / LOW 6
>
> **Outcome:** `tasks_appended`
>
> **Next Actions (handoff):** 15 tasks (T022–T036) were appended under `## Phase 8: Convergence` in `specs/032-t20-state-machine/tasks.md`, HIGH first. Run `/speckit-implement` to complete them; a follow-up `/speckit-converge` run should then find fewer or no remaining items. Note that three tasks already checked `[x]` in Phase 5/7 (T012 multi-seed, T017 stale-reply guard, T018 hardened purity guards) do not have their work present in the code — the new tasks re-open that work without touching the old entries.
>
> **Extension Hooks:** none — `.specify/extensions.yml` has no `hooks.after_converge` entry.
>
> **Out-of-scope observation (not a finding row):** `app/backend/services/dev_session.py` imports `InterviewSessionNotFound`, `encode_session_state` from `orchestrator.persistence` and `PlannedCompetency`, `plan_payload` from `orchestrator.plan`, none of which exist in the present orchestrator code, and calls `save_session_state` with three arguments vs. the two-argument signature in `persistence.py`. That module is T21/T22/T23 work and outside this feature's artifacts, so per the skill's scope bound I did not emit a task for it — but it will fail at import time in the present tree.
>
> **Appended to tasks.md (verbatim):**
>
> ```markdown
> ## Phase 8: Convergence
>
> - [ ] T022 Issue the contract move vocabulary on competency advances: `acknowledge_and_transition` (ANSWERED) / `close_competency` (NONE) with the next seed in `move_context`, set `last_issued_move` accordingly, and fix `test_edge_10_*`/`test_edge_12_*` per Clarification 2 / contract §10 edges 10, 12 (contradicts)
> - [ ] T023 Implement the per-competency multi-seed loop (`seed_index`; on ANSWERED go to `seed_questions_uk[k+1]` when it exists and competency time remains, else advance) and add the multi-seed iteration test per contract §4 / T012 (missing)
> - [ ] T024 Add the stale-reply no-op guard (`_answers_pending_command`) to `_handle_interviewer_reply_ready` and `_handle_interviewer_failed` (CLOSE included) and create `app/backend/tests/orchestrator/test_stale_replies.py` covering the preempted-probe race, failure ladder, edge-15 QA path and CLOSE per contract §6.9a / spec note 23 / T017 (missing)
> - [ ] T025 Harden `test_static_guards.py`: attribute-form randomness scan (`random.*`, `secrets.*`, `uuid.uuid4`), ban `import uuid` in the pure modules (switch `state_machine.py` to `from uuid import UUID, uuid5`), inspect `ast.Match` subjects and `case` guards, add `description_en` / `manual_review_reason_en` / `rationale_en` / `evidence_*` to the prose-branch set; verify each predicate against a planted violation per FR-032-10 / spec note 24 / T018 (partial)
> - [ ] T026 Add the immediate/`TimerTick` completion path for CLOSE (edge 17) so a scripted closing reaches COMPLETED without a synthesised `InterviewerReplyReady`, ensure CLOSE cannot fall into the candidate-timeout abort, and add a named test per contract §10 edge 17 / spec note 23 (partial)
> - [ ] T027 Type `OperatorAbort.reason` as the §2 abort set (default `operator_abort`), copy it onto `SessionState.abort_reason`, keep `RecordDecision(operator)`, and add a test reaching `ABORTED(cost_ceiling)` per spec note 16 / Handoff T21 (contradicts)
> - [ ] T028 Tolerate unknown extra keys on `PlanSnapshot` / `PlanCompetency` (replace `extra="forbid"`) and invert `test_plan_snapshot_rejects_unknown_top_level_fields` per spec note 11 (contradicts)
> - [ ] T029 Complete the adjudication matrix tests: NONE x pending (budget exhausted, no assessment), NONE x failed (produces the `assessment_failed` coverage outcome), ANSWERED x pending/failed (prior ANSWERED evidence plus a later failed/pending turn) per FR-032-9 / SC-1 / T012 (partial)
> - [ ] T030 Cap `AdjudicationConfig.confidence_min` at 0.99 in the loader/model and add a `test_config.py` case rejecting 1.0 per spec note 20 (partial)
> - [ ] T031 Make the candidate-timeout guard strict (`>`) in `_candidate_timed_out` and add a boundary test at exactly `candidate_timeout_minutes` per contract §6.6 / spec note 15 (contradicts)
> - [ ] T032 Align `SessionState` with contract §4 / spec notes 10 and 13: `plan_input` naming, top-level `last_issued_move`, `seed_index`, `pending_assessments` as a bare turn-id list plus a separate `assessment_focus` map (or record the deviation explicitly in spec.md Clarifications), keeping JSON round-trip tests green per contract §4 (partial)
> - [ ] T033 Add `OPENING_SCRIPT_PATH` / `CLOSING_SCRIPT_PATH` path constants to the core referencing `prompts/shared/candidate-facing/{opening,closing}.md` (reference only, no file reads) per spec note 19 (missing)
> - [ ] T034 Make `ReissuePendingCommand` carry the outstanding command (or an opening/closing discriminator) so the shell can distinguish `EmitScriptedOpening` from `EmitScriptedClosing` per spec note 12 (partial)
> - [ ] T035 Add a session-level manual-review flag on `SessionState` set from `AssessorOutput.needs_manual_review` alongside the coverage-cell marker per contract §5 (partial)
> - [ ] T036 Make edge 15 and edge 14 (TECH->QA) command tuples literal to contract §10 (drop the extra `PersistState` on edge 15; drop or justify `RecordGap`+`PersistState` on edge 14) or amend spec note 8 to record the additions per spec note 8 / contract §10 (partial)
> ```
>
> `git status --short` → ` M specs/032-t20-state-machine/tasks.md` only.

**3-line summary (D):** 15 findings, 0 CRITICAL / 4 HIGH / 5 MEDIUM / 6 LOW; outcome `tasks_appended` (T022–T036). The two genuinely rejected readings from the attempt (`ask_seed`+`transition_note`; single-seed loop) are F1 and F2, both HIGH. Nine of the fifteen (F3–F7, F9, F12, F13, F15) cite the final's implementation notes 8–26 or contract v1.2 — intent written *after* the attempt — so they measure "is this the merged design?" rather than "does this violate the design it was given"; see §E.

### D.2 Run D′ — attempt code, contract reverted to v1.0, `main`'s spec kit (worktree `036-run-attempt-v10` @ `fb548b9`)

Sub-agent report, verbatim (model Fable 5.1; 27 tool uses; 179,161 tokens; 12:00:15 → 12:05:40, 5 min 25 s). Same prompt as D plus one sentence: "Where spec.md and the contract text disagree, report the disagreement as a finding rather than silently picking one."

> **Prerequisite script:** `{"FEATURE_DIR":".../036-run-attempt-v10/specs/032-t20-state-machine","AVAILABLE_DOCS":["tasks.md"]}`, exit 0. Hook check: no `before_converge`/`after_converge` → skipped.
>
> **Files read:** skill, extensions.yml, feature.json, constitution; spec/plan/tasks; contract (v1.0 text); `orchestrator/*.py` (5); `configs/orchestrator.yaml`; migration 0006; `db/models/interview.py` (grep context); `llm/models_config.py`; `agents/interviewer.py` L55–70, `agents/assessor.py` (grep); `scripts/check-no-provider-sdk-imports.sh` (header); `prompts/shared/candidate-facing/{opening,closing}.md` (heads); all 12 files under `tests/orchestrator/`. No git history, no other worktrees, no tests/gates.
>
> **Interpretation note:** acknowledged and applied; where spec.md and the contract text disagree, reported as finding F1.
>
> ### Convergence Findings
>
> | ID | Gap Type | Severity | Source | Evidence | Remaining Work |
> |----|----------|----------|--------|----------|----------------|
> | F1 | contradicts | HIGH | spec.md Contract header (v1.1) + FR-032-4/5/8 + fix-round note 26 (v1.2) vs `docs/contracts/state-machine.md` | The contract file in the worktree reads `Status: v1` and `*Amendments: none yet.*`; §6 has only items 1–6. spec.md cites §6.7 (tick priority), §6.8 (late assessments), §6.9 (uuid5 ids), §6.9a (stale replies), a §Amendments section, a §9 "PersistState is advisory" statement, a split edge-14 cell and normative evaluation order / inclusive guards — none of which exist in the file. | Bring the contract to the v1.2 text spec.md cites (or the owner corrects spec.md — converge cannot). |
> | F2 | missing | HIGH | fix-round note 23 / T017 (§6.9a) | No `_answers_pending_command` anywhere. `_handle_interviewer_reply_ready` (`state_machine.py:855–862`) and `_handle_interviewer_failed` (`910–939`) never compare `event.turn_id` to `state.pending_work.turn_id`: a stale reply after edge 14 preempts an in-flight `depth_probe` is delivered, flips `awaiting`, and counts drift. `test_stale_replies.py` and `_builders.py` do not exist. `test_edge_17` passes a random `closing_turn_id` and still completes. | Implement the turn_id guard in both handlers (edge 17 answers only the outstanding closing turn); add `test_stale_replies.py` with the four named scenarios. |
> | F3 | contradicts | HIGH | spec Clarification 2 (advance-move vocabulary) | `_advance_to_next_competency` (`state_machine.py:726–767`) emits `RunInterviewer(move="ask_seed", context={..., "transition_note": "acknowledge_and_transition"\|"close_competency"})` and sets `last_issued_move="ask_seed"`; `test_edge_10_answered_verdict_advances_to_next_competency` asserts `move == "ask_seed"`. Clarification 2 fixes the inverse. | Swap move vs. context on edges 10/12, fix `last_issued_move` (drift accounting), update edge 10/12 tests. |
> | F4 | contradicts | MEDIUM | implementation note 11 / FR-032-6 | `PlanSnapshot` and `PlanCompetency` use `extra="forbid"` (`plan.py:33,60`); `test_plan_snapshot_rejects_unknown_top_level_fields` asserts rejection. Note 11: unknown extra keys are tolerated. | `extra="ignore"` on both models; invert the test. |
> | F5 | contradicts | MEDIUM | implementation note 16 / T21 handoff (`ABORTED(cost_ceiling)` hook) | `OperatorAbort.reason: str` (`state_machine.py:312`); `_handle_operator_abort` (`1093–1098`) does `del event` and hardcodes `abort_reason="operator_abort"` + `RecordDecision("operator")`. `cost_ceiling` in `AbortReason`/`DecisionReason` is unreachable; test_edge_19 passes free text. | Type `reason` as `AbortReason` (default `operator_abort`), copy it onto the state, add a `cost_ceiling` edge-19 test. |
> | F6 | contradicts | MEDIUM | implementation note 20 / FR-032-7 | `AdjudicationConfig.confidence_min = Field(ge=0.0, le=1.0)` (`state_machine.py:464`); `AssessmentItem.confidence` is `le=0.99` (`assessor.py:253`), so `confidence_min: 1.0` loads fine and makes ANSWERED unreachable mid-interview. No loader test above 0.99. | `le=0.99` + a `test_config.py` case. |
> | F7 | partial | MEDIUM | FR-032-9 / SC-1 / T012 (matrix "complete") | Covered: ANSWERED×present, CLARIFY×present, NONE×present (level-0, probe budget, time budget, not-assessable), CLARIFY×pending, CLARIFY×failed. Not covered: NONE×pending, NONE×failed (the `assessment_failed` outcome from `_finalize_gap_outcome` `1171–1172` is never asserted anywhere), ANSWERED×pending, ANSWERED×failed. No multi-seed iteration test although T012 lists it. | Add the missing cells + multi-seed test. |
> | F8 | partial | MEDIUM | contract §4 ("`ask_seed` (up to plan's seeds)"), §7 (`seed_questions_uk ≥1`), T012 | `_seed_context` (`state_machine.py:643–647`) only ever uses `seed_questions_uk[0]`; `seeds_asked` is set to 1 and never incremented. `plan.py:57–62` docstring says multi-seed is "not consumed by the T20 loop — see spec Clarifications", but no such Clarification exists in spec.md. | Implement seed iteration or obtain/record an owner Clarification for the single-seed reading. |
> | F9 | partial | MEDIUM | fix-round note 24 / T018 / FR-032-10 | `state_machine.py:41` is `import uuid` — the form note 24 bans. `test_static_guards.py` has no `import uuid` ban, no attribute-form `random.*`/`secrets.*` scan, no `match`/`case`-guard inspection, and its only prose-attribute ban is `.text`; it scans `state_machine.py` only, not `plan.py`. FR-032-10's base guards are present. | Rewrite the import; add the hardened guards over both pure modules. |
> | F10 | contradicts | LOW | implementation note 13 / contract §4 | `TechState.pending_assessments: dict[uuid.UUID, str]` (`state_machine.py:191`) — §4's `[turn_id]` shape is not kept and there is no `assessment_focus` field. | Split into list + `assessment_focus` map, or record the deviation. |
> | F11 | contradicts | LOW | implementation note 8 (command tuples literal) / contract §10 | Edge 15 emits `RunInterviewer, PersistState` (`826–832`) though the table lists only `RunInterviewer`; the edge-14 TECH branch emits `RecordGap, RunInterviewer, PersistState` (`1069–1070`) though the table says "as #13". Harmless if `PersistState` is advisory, but `RecordGap` on edge 14 is untabulated. | Align tuples/tests or amend note 8. |
> | F12 | contradicts | LOW | implementation note 15 / contract §6.6 (strict `>`) | `_candidate_timed_out` uses `elapsed >= timedelta(...)` (`state_machine.py:1078`). | Use `>`; add an at-boundary test. |
> | F13 | missing | LOW | implementation note 19 | No `OPENING_SCRIPT_PATH` / `CLOSING_SCRIPT_PATH` constant anywhere in `app/backend/orchestrator/`; the prompt files exist. | Add the constants (never read by the core). |
> | F14 | partial | LOW | implementation note 12 / contract §9 | `ReissuePendingCommand` (`state_machine.py:414–426`) is a flattened label/move/context/utterance variant, not a `Command` variant *wrapping* the outstanding command as note 12 states. Functionally equivalent for the shell. | Wrap, or record the flattened shape as accepted. |
> | F15 | partial | LOW | implementation notes 10, 23, 25, 26 / T019 | Identifiers spec.md names do not exist in code: `SessionState.plan_input` (code `plan_raw`), `_on_interviewer_reply`/`_on_interviewer_failed` (code `_handle_*`), `_builders.py` with `tech_with_coverage`/`drive_to_qa`, `test_transition_table.py`. Note 26 says `plan.py` cites "Clarification 11" — it cites no number; both `plan.py:61` and `TechState`'s docstring cite Clarifications absent from spec.md. T019 cannot be verified as done. | Rename in code or correct the notes. |
>
> **Summary metrics:**
> - Requirements / acceptance criteria checked: **71** — FR-032-1…10 (10), SC-1…5 (5), Clarifications 1–7 (7), notes 8–26 (19), contract §10 edges 1–21 (21) and §1–§9/§11 obligations (9). All 21 edges have a named `test_edge_NN_*` test.
> - Plan decisions checked: **9** — all present.
> - Constitution principles checked: **20**; buildable obligations assessed §2, §3, §4, §5, §9, §10, §11, §14, §16, §17, §18 — **0 violations**.
> - Findings by gap type: missing **2** (F2, F13) / partial **5** (F7, F8, F9, F14, F15) / contradicts **8** (F1, F3, F4, F5, F6, F10, F11, F12) / unrequested **0**.
> - Findings by severity: CRITICAL **0** / HIGH **3** / MEDIUM **6** / LOW **6**.
>
> **Outcome:** `tasks_appended` — 15 tasks (T022–T036) under `## Phase 8: Convergence`, HIGH → MEDIUM → LOW. Note for the owner: T022 (contract text), T029 (single- vs multi-seed) and T036 (spec-note identifiers) may resolve by correcting spec/contract prose rather than code — converge cannot edit spec.md, so those decisions are surfaced as tasks.
>
> **Extension Hooks:** none.
>
> **Appended to tasks.md (verbatim):**
>
> ```markdown
> ## Phase 8: Convergence
>
> - [ ] T022 Bring `docs/contracts/state-machine.md` up to the v1.2 text that spec.md cites: add §6.7 (tick priority), §6.8 (late assessments in any non-terminal phase), §6.9 (uuid5 idempotent ids), §6.9a (stale agent replies), the §Amendments section, the §9 statement that `PersistState` is an advisory marker, the split edge-14 command cell, the inclusive budget guards and the §5 evaluation order — the file currently reads "Status: v1" / "Amendments: none yet" and §6 stops at item 6, so FR-032-4/5/8 and notes 23–26 reference sections that do not exist per spec.md Contract header + FR-032-4/FR-032-5/FR-032-8 + fix-round note 26 (contradicts)
> - [ ] T023 Implement the §6.9a stale-reply guard: in `app/backend/orchestrator/state_machine.py` make `_handle_interviewer_reply_ready` and `_handle_interviewer_failed` a no-op (same state, no commands, no drift step, no failure-ladder step) when `event.turn_id != state.pending_work.turn_id`, edge 17 answering only the outstanding closing turn; add `app/backend/tests/orchestrator/test_stale_replies.py` covering the edge-14-preempts-`depth_probe` race, the failure ladder, the edge-15 QA path and CLOSE per fix-round note 23 / T017 (missing)
> - [ ] T024 Switch competency advances to the Clarification-2 move vocabulary: in `_advance_to_next_competency` issue `RunInterviewer(move="acknowledge_and_transition")` on the ANSWERED path and `RunInterviewer(move="close_competency")` on the NONE path with the next seed carried in `context`, set `last_issued_move` accordingly, and keep bare `ask_seed` only for the first seed after INTRO; update `test_edge_10_*` / `test_edge_12_*` which currently assert `move == "ask_seed"` per spec Clarification 2 (contradicts)
> - [ ] T025 Tolerate unknown extra keys in the plan shape: change `PlanSnapshot` and `PlanCompetency` in `app/backend/orchestrator/plan.py` from `extra="forbid"` to `extra="ignore"` and invert `test_plan_snapshot_rejects_unknown_top_level_fields` in `test_plan.py` to assert acceptance per implementation note 11 / FR-032-6 (contradicts)
> - [ ] T026 Make `ABORTED(cost_ceiling)` reachable: type `OperatorAbort.reason` as `AbortReason` (default `operator_abort`), copy it onto `SessionState.abort_reason` in `_handle_operator_abort` instead of `del event` + hardcoded `operator_abort`, keep `RecordDecision(reason="operator")`, and add an edge-19 test for `reason="cost_ceiling"` per implementation note 16 / T21 handoff (contradicts)
> - [ ] T027 Cap `confidence_min` at the assessor confidence ceiling: change `AdjudicationConfig.confidence_min` in `state_machine.py` from `le=1.0` to `le=0.99` and add a `test_config.py` case that `confidence_min: 0.995` raises `OrchestratorConfigError` per implementation note 20 / FR-032-7 (contradicts)
> - [ ] T028 Complete the adjudication matrix in `test_transition_table_adjudication.py`: add NONE×pending (probe budget exhausted with no completed assessment), NONE×failed (only failed turns + budget exhausted → `assessment_failed` finalized outcome, currently never asserted), ANSWERED×pending and ANSWERED×failed (prior ANSWERED evidence plus a later pending/failed turn), and a multi-seed iteration test per FR-032-9 / SC-1 / T012 (partial)
> - [ ] T029 Implement contract §4's per-competency seed loop ("`ask_seed` (up to plan's seeds)"): ask `seed_questions_uk[k]` for k ≥ 1 and increment `seeds_asked` before the competency exits, or obtain and record an owner Clarification for the single-seed reading — `_seed_context` only ever uses `seed_questions_uk[0]`, `seeds_asked` is fixed at 1, and `plan.py` cites a spec Clarification for this allowance that spec.md does not contain per contract §4 / §7 / T012 (partial)
> - [ ] T030 Harden the static purity guards per note 24: replace `import uuid` in `state_machine.py` with `from uuid import UUID, uuid5`; in `test_static_guards.py` ban `import uuid` in the pure modules (`state_machine.py` and `plan.py`), scan attribute-form `uuid.uuid4`/`random.*`/`secrets.*`, inspect `match` subjects and `case` guards alongside `if`/`while`/conditional expressions/comparisons, and add `description_en` / `manual_review_reason_en` to the banned prose-attribute set (currently only `.text` is banned) per fix-round note 24 / T018 / FR-032-10 (partial)
> - [ ] T031 Restore contract §4's `pending_assessments: [turn_id]` shape and add the separate `TechState.assessment_focus` (`turn_id → node_id`) map dropped together with the pending id, replacing the current `pending_assessments: dict[uuid.UUID, str]` per implementation note 13 / contract §4 (contradicts)
> - [ ] T032 Make the edge-14 and edge-15 command tuples literal per note 8: edge 15 currently emits `RunInterviewer, PersistState` (table lists `RunInterviewer` only) and the edge-14 TECH branch emits `RecordGap, RunInterviewer, PersistState` (table says "as #13"); align the tuples and their tests, or amend note 8 to record the deviation per implementation note 8 / contract §10 (contradicts)
> - [ ] T033 Change `_candidate_timed_out` in `state_machine.py` from `>=` to the strict `>` the contract writes and add a boundary test at exactly `candidate_timeout_minutes` (must NOT abort) per implementation note 15 / contract §6.6 (contradicts)
> - [ ] T034 Add the `OPENING_SCRIPT_PATH` and `CLOSING_SCRIPT_PATH` path constants (pointing at `prompts/shared/candidate-facing/opening.md` / `closing.md`, never read by the core) to `state_machine.py` per implementation note 19 (missing)
> - [ ] T035 Make `ReissuePendingCommand` wrap the outstanding `RunInterviewer` / `DeliverUtterance` / `EmitScriptedOpening` / `EmitScriptedClosing` command (or record the flattened shape as the accepted reading) — it is currently a flattened label/move/context/utterance variant per implementation note 12 / contract §9 (partial)
> - [ ] T036 Reconcile identifiers that spec.md names with the code: `SessionState.plan_input` (code: `plan_raw`), `_on_interviewer_reply` / `_on_interviewer_failed` (code: `_handle_*`), `_builders.py` with `tech_with_coverage` / `drive_to_qa` and `test_transition_table.py` (code: `_helpers.py` and four `test_transition_table_*.py`), the "Clarification 11" citation note 26 says `plan.py` carries (it cites no number), and the `awaiting`-promoted-to-top-level Clarification `TechState`'s docstring cites (absent from spec.md) — rename in code or correct the notes per implementation notes 10, 23, 25, 26 / T019 (partial)
> ```
>
> ID/phase derivation: max existing T021 → T022–T036; highest phase 7 → Phase 8. Existing content is a byte-prefix of the new file (md5 before `8f1b1727…`, after `a87fc8e4…`). `git status --short` → ` M specs/032-t20-state-machine/tasks.md` only.

**3-line summary (D′):** Same 15-finding count as D, 13 of them the same items. Reverting the contract to v1.0 did **not** make the 8 folded-in refinements reappear as deviations — converge treats `spec.md` (which endorses them via Clarifications and notes) as the higher authority and instead filed one HIGH finding that the contract file is stale relative to spec.md (F1), which is exactly right for what the worktree contained. Net vs D: gained F1 (contract drift) and F15 (identifier mismatches), lost D's F5 (CLOSE immediate path) and F14 (session-level manual-review flag); single-seed dropped from HIGH/missing to MEDIUM/partial because v1.0 §4 only says "up to plan's seeds".


## E. Scorecard

Scoring done by the main loop (Fable 5.1) with the attempt's code open, against the contract
text of each run plus the v1.0 text the attempt was written against. "Status vs `main`"
says what the deviation *is* today, because 8 of the 13 stopped being deviations when the
contract owner folded them into v1.1.

### E.1 The 13 deviations × converge on the attempt

| # | Deviation (short) | Status vs `main` (contract v1.2 + spec) | Run D (v1.2) | Run D′ (v1.0) | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | `awaiting` top-level, not in `TechState` | **accepted** (v1.1 §4) | n/a — correctly not flagged; residual flagged: `last_issued_move` still nested, `seeds_asked` vs `seed_index` (F11, LOW) | n/a — not flagged | v1.1 moved *both* `awaiting` and `last_issued_move` top-level; the attempt moved only one. Converge caught the half-done shape. |
| 2 | `ScheduleNothing` by omission | **accepted** (v1.1 §10 note) | n/a — not flagged | n/a — not flagged | Correct on both. |
| 3 | CLOSE as real phase; edge 17 "immediate" read as shell-only | **rejected in substance** — final implements both the reply path and the immediate `TimerTick` path (note 23) | **found** — F5, MEDIUM: no CLOSE branch in `_handle_timer_tick`; a finished interview can end as `ABORTED(candidate_timeout)` | **missed** | v1.0 edge 17 already said "InterviewerReplyReady / immediate". D′ read the same text and did not flag it. |
| 4 | Advance = `ask_seed` + `context["transition_note"]` | **rejected** (v1.1: `acknowledge_and_transition` / `close_competency`, seed in `move_context`) | **found** — F1, HIGH (contradicts) | **found** — F3, HIGH (contradicts) | The one deviation the owner called out explicitly as "sonnet invented a vocabulary". Both runs also spotted the knock-on: `last_issued_move="ask_seed"` makes correct interviewer behaviour count as drift. |
| 5 | Only `seed_questions_uk[0]` consumed | **rejected** (v1.1 §4 multi-seed iteration rule) | **found** — F2, HIGH (missing) | **partially** — F8, MEDIUM (partial): "implement or obtain an owner Clarification" | Against v1.0's softer "up to plan's seeds" converge downgraded it and offered the escape hatch. Correct calibration. |
| 6 | uuid5 command ids | **accepted** (v1.1 §6.9) | n/a — not flagged (the `import uuid` *form* is F4, a note-24 hardening item, not this deviation) | n/a | Correct. |
| 7 | Adjudication evaluation order | **accepted** (v1.2 made it normative) | n/a — not flagged | n/a | Correct; converge read `_adjudicate` and did not object. |
| 8 | `CoverageCell` best/latest split | **accepted** (v1.1 §4) | n/a — not flagged | n/a | Correct. |
| 9 | Candidate-timeout before budget on one tick | **accepted** (v1.1 §6.7) | n/a — not flagged | n/a | Correct. |
| 10 | Forced QA/CLOSE only from TECH/QA | **moot** (table scope unchanged) | n/a — not flagged | n/a | Correct. |
| 11 | Late assessments accepted in any non-terminal phase | **accepted** (v1.1 §6.8) | n/a — not flagged | n/a | Correct. |
| 12 | Rubric-snapshot cross-check deferred to T22 | **accepted** (spec Clarification 7) | n/a — not flagged | n/a | Correct. |
| 13 | No feature flag in T20 | **accepted** (spec Clarification 5) | n/a — constitution §9 checked, Clarification 5 cited, no finding | n/a — same | Correct; converge did the constitution check and reached the owner's conclusion. |

**Tally.** Of the 13, three are still deviations against the design on `main` (#3, #4, #5).
Run D found **3/3** (2 HIGH, 1 MEDIUM). Run D′ found **1 + 1 partial** of 3 and missed #3.
On the ten items the contract owner had accepted, **neither run produced a false positive** —
converge did not re-litigate a single folded-in refinement, because `spec.md`/contract now
state them. Against the *original* v1.0 text all 13 were deviations by the implementer's own
account; converge did not surface them that way in D′ because it ranks `spec.md` above the
contract when they disagree (and said so, as F1). That is the single most important thing to
know about the tool: **it validates against the artifacts as they stand, not against the
artifacts the implementer was given.**

### E.2 Converge findings → verdict

Verdict vocabulary: **true** = the code deviates from a design statement that existed when
the attempt was written (contract v1.0) or from `main`'s contract; **true (post-attempt
intent)** = a real gap, but the requirement was written into the spec *after* the attempt
(the final's implementation notes 8–26 / fix-round notes / contract v1.2) — converge is
reading the answer key; **style** = naming/docstring/shape with no behavioural difference;
**false-positive** = not a gap; **experiment artifact** = caused by the run setup.

Run D (attempt, contract v1.2) — 15 findings:

| Converge finding (D) | Verdict | Why |
| --- | --- | --- |
| F1 `ask_seed`+`transition_note` on edges 10/12 (HIGH) | **true** | Deviation #4; v1.0 edge 10 already listed `acknowledge_and_transition`. Also the real drift-accounting bug. |
| F2 single-seed loop (HIGH) | **true** | Deviation #5; v1.0 §4 "up to plan's seeds". |
| F3 no stale-reply guard §6.9a (HIGH) | **true (post-attempt intent)** — and a real race | §6.9a is v1.2 text; but the reviewer gate found this exact race on the *final* code and it is present in the attempt too. The attempt did not self-declare it. |
| F4 purity guards not hardened; `import uuid` (HIGH) | **true (post-attempt intent)**, test-hardening | Note 24 is fix-round text. Base FR-032-10 guards are present; converge said so. Severity HIGH is generous. |
| F5 CLOSE has no immediate/`TimerTick` path (MEDIUM) | **true** | v1.0 edge 17 "/ immediate"; deviation #3. The `candidate_timeout`-after-CLOSE consequence is converge's own observation, not in any spec text. |
| F6 `OperatorAbort.reason` free text; `cost_ceiling` unreachable (MEDIUM) | **true** | v1.0 §11: "the machine only exposes `ABORTED(cost_ceiling)` … hooks"; the attempt made the hook unreachable. Not self-declared. |
| F7 plan `extra="forbid"` vs note 11 (MEDIUM) | **true (post-attempt intent)** | Note 11 is the final implementer's reading; v1.0 §7 is silent. Reasonable people differ; the attempt even tests the opposite. |
| F8 adjudication matrix cells missing (MEDIUM) | **true** | FR-032-9 and the attempt's own brief required the full 3×3; the attempt's report claimed "full matrix" — converge disproved the claim by reading the tests. |
| F9 `confidence_min` not capped at 0.99 (MEDIUM) | **true (post-attempt intent)** — real footgun | Note 20 postdates; but the assessor's 0.99 ceiling existed and `confidence_min: 1.0` silently kills ANSWERED. |
| F10 candidate timeout `>=` vs `>` (LOW) | **true** | v1.0 §6.6 writes `>`. Not self-declared. |
| F11 state shape: `last_issued_move` nested, `seeds_asked`, `plan_raw`, `pending_assessments` as dict (LOW) | **true** (v1.1 §4 shape) + **style** (`plan_input`/`assessment_focus` names from notes 10/13) | Half of deviation #1 undone; the rest is naming. |
| F12 `OPENING_SCRIPT_PATH`/`CLOSING_SCRIPT_PATH` constants (LOW) | **style** (post-attempt note 19) | Reference-only constants. |
| F13 `ReissuePendingCommand` flattened vs wrapping (LOW) | **style** (post-attempt note 12) | D′ itself called it functionally equivalent. |
| F14 no session-level manual-review flag (LOW) | **true** | v1.0 §5: "recorded in coverage + session flags". Not self-declared. |
| F15 edge 15 extra `PersistState`, edge 14 untabulated `RecordGap` (LOW) | **true** but harmless for `PersistState` (advisory per v1.2 §9); `RecordGap` on edge 14 is a genuine untabulated command | Not self-declared. |

D verdict counts: **true 9** (F1, F2, F5, F6, F8, F10, F11-part, F14, F15) · **true, post-attempt intent 4** (F3, F4, F7, F9) · **style 3** (F11-part, F12, F13) · **false-positive 0**.

Run D′ (attempt, contract v1.0) — 15 findings, 13 shared with D:

| Converge finding (D′) | Maps to D | Verdict | Why |
| --- | --- | --- | --- |
| F1 contract file stale vs spec.md (HIGH) | — | **experiment artifact, correctly detected** | We reverted the contract; converge noticed spec.md cites sections that don't exist and refused to pick silently. |
| F2 stale-reply guard (HIGH) | D.F3 | true (post-attempt intent), real race | same |
| F3 advance vocabulary (HIGH) | D.F1 | true | same |
| F4 plan extra keys (MEDIUM) | D.F7 | true (post-attempt intent) | same |
| F5 `OperatorAbort` untyped (MEDIUM) | D.F6 | true | same |
| F6 `confidence_min` cap (MEDIUM) | D.F9 | true (post-attempt intent) | same |
| F7 matrix cells + multi-seed test (MEDIUM) | D.F8 (+F2's test) | true | same |
| F8 single-seed loop (MEDIUM, partial) | D.F2 | true, correctly softened for v1.0 wording | offers the Clarification escape hatch |
| F9 purity guards / `import uuid` (MEDIUM) | D.F4 | true (post-attempt intent), test-hardening | D′ rated it MEDIUM, D rated HIGH — same evidence |
| F10 `pending_assessments` dict shape (LOW) | D.F11-part | true (v1.1 shape) / style | same |
| F11 edge 14/15 tuples (LOW) | D.F15 | true, mostly harmless | same |
| F12 timeout `>=` (LOW) | D.F10 | true | same |
| F13 script-path constants (LOW) | D.F12 | style | same |
| F14 `ReissuePendingCommand` shape (LOW) | D.F13 | style | same |
| F15 identifiers named in spec notes absent from code (LOW) | — | **style / answer-key leak** | The clearest symptom that the final's implementation notes were being used as intent: converge asks the attempt to rename `_handle_*` to `_on_*` because note 23 says so. |

D′ missed vs D: CLOSE immediate path (D.F5) and the session-level manual-review flag (D.F14) — both present in v1.0 text, so these are run-to-run variance, not a contract-version effect.

### E.3 What converge flagged that the humans did not

- **vs the implementer's self-report (the only "review" the attempt ever had):** 7 substantive
  items the Sonnet agent did not declare — the stale-reply race (F3), `cost_ceiling`
  unreachable (F6), the adjudication matrix being incomplete despite a "full matrix" claim
  (F8), timeout boundary (F10), the half-migrated state shape (F11), missing session-level
  manual-review flag (F14), untabulated `RecordGap` on edge 14 (F15).
- **vs the reviewer gate on the final code (run C):** converge re-verified both reviewer
  fixes as present and raised two contract-owner questions the reviewer gate did not:
  §6.5 references a `qa_minutes_min` threshold that exists in neither §7 nor §8, and resume
  (edge 21) never re-issues a `RunAssessor` lost to a crash. Neither became a task (converge
  cannot edit spec artifacts and judged the second as "requirement as written is met").
- **What the reviewer found that converge on the attempt did not phrase as a bug:** nothing
  material — the reviewer's finding 1 (stale replies) is D.F3/D′.F2; its finding 5 (purity
  hardening) is D.F4/D′.F9. The reviewer's other findings were contract-text corrections,
  which converge is forbidden to make.

### E.4 Calibration notes

- Severity is mostly sane but noisy across runs: the same purity-guard evidence was HIGH in
  D and MEDIUM in D′; the same single-seed evidence was HIGH/missing vs MEDIUM/partial
  (defensible, since the contract wording differed).
- Converge never produced a `converged` result, even on the reviewed code: a stale docstring
  is a `partial` gap. Expect a Phase N append on almost every run.
- Zero false positives in 31 finding rows across three runs; 3 style-only rows in D, 3 in D′.
  The "answer-key leak" (post-attempt implementation notes read as intent) accounts for 4 of
  D's 15 rows and inflates the count, but none of those four is wrong about the code.
- Converge honoured every operating constraint: no code edits, no spec edits, append-only
  tasks.md, no commits, and it declined to task the out-of-scope T21/T22 shell import
  breakage while reporting it.
- The interpretation note mattered. Without "treat the contract as spec by reference" the
  skill's literal "spec/plan/tasks as the sole source of intent" would have left a 12-line
  FR list to check 1,175 lines of state machine against.

## F. Cost + time per run

| Run | State | Findings | Sub-agent tokens (harness-reported) | Tool uses | Wall clock |
| --- | --- | --- | --- | --- | --- |
| C control | final code, contract v1.2 | 1 (LOW) | 202,741 | 27 | 5 min 18 s (11:59:53–12:05:11) |
| D attempt | attempt code, contract v1.2 | 15 (4 H / 5 M / 6 L) | 172,268 | 22 | 4 min 41 s (12:00:06–12:04:47) |
| D′ attempt | attempt code, contract v1.0 | 15 (3 H / 6 M / 6 L) | 179,161 | 27 | 5 min 25 s (12:00:15–12:05:40) |
| **Total** | | 31 rows | **554,170** | 76 | ~5.5 min (parallel) |

Model: Fable 5.1 for all three (the reviewer-gate tier per CLAUDE.md model policy; the thing
under test is a review, so it got the review model). Tokens are the harness's per-sub-agent
total; no dollar conversion attempted. For comparison, the Sonnet attempt's *implementation*
run consumed 359,821 tokens over 58 min — one converge run costs roughly half an
implementation run in tokens and a tenth of the wall clock.

Stage-1 wall clock overall: 11:20 → 12:35 local (~75 min), of which the CLI upgrade was 3 s,
the three converge runs 5.5 min in parallel, and the rest archaeology (locating the attempt in
dangling commits, the deviation list in a session transcript) plus this write-up.

**Step 7 (optional `/speckit-analyze` / `/speckit-checklist`)** — not run. 1.0.4's `analyze`
is a spec↔plan↔tasks consistency pass (no code), so it would not add to §C/§D; skipped as
"not cheap enough to matter". Easy to add later on the same worktrees.

## G. Owner's notes (what surprised, what was annoying, would you keep converge on?)

_owner writes this_

## Appendix — evidence locations (all local, nothing pushed)

- Branch `036-speckit-1x-converge`: §A/§B commits, the upgrade commit `c04b19f`, this file.
- Run worktrees under `.claude/worktrees/036-run-{control,attempt-v12,attempt-v10}` on
  branches `036-run-*`; each has one final commit with converge's Phase 8 append to
  `specs/032-t20-state-machine/tasks.md` (diff = exactly the blocks quoted above).
- Local tag `archive/032-t20-sonnet-attempt` → `d464a9a` (the attempt's four commits).
- Scratch trial clone of the upgrade: session scratchpad only, disposable.
