---
kind: owner
title: "Spec Kit 1.0 — stage 1 (converge vs a 13-deviation implementation) + stage 2 (one feature three ways) — TechScreen, 2026-09-06"
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

_Owner (Ihor), 2026-09-06, via the news_digest session:_

> Апгрейд не змінив нічого в щоденній роботі, а converge за 5 хвилин зробив рев'ю, якого відкочена спроба ніколи не отримала, і знайшов 7 багів, про які імплементер змовчав.

EN: The upgrade changed nothing in day-to-day work; converge did, in five minutes, the review the rolled-back attempt never got, and found 7 bugs the implementer had not declared.

Context the owner gave while reading the results: after running the protocol he "honestly did not see the difference" between 0.7.4 and 1.0.4 in daily use — which is accurate: the only visible change is the new `converge` step after `implement`; the rest of the workflow is unchanged. Keep converge on: yes.

## H. Stage 2 setup (feature, base commit, prompt text, arm definitions, agent.md content)

**Feature: T24 — Pre-Interview Planner agent wrapper** (`app/backend/agents/planner.py` + `tests/agents/test_planner.py` + one mock fixture). Why: next in the Tier-4 backlog; no DB, no cloud, offline against the mock Vertex backend; two committed siblings with the same pattern (Interviewer 256 lines, Assessor 399) so the "nothing" arm has a fair template and the Spec Kit arm has real things to clarify; prompt and schema already committed; T18-class size (the T18 spec was 79 lines). Genuine forks the task text leaves open: retry policy, structural validation against the rubric subset, version lockstep, how to obtain the fixture SHA, whether to append the Interviewer's level guide.

**Base commit:** `770bba1` (tip of `036-speckit-1x-converge` after §G — includes Spec Kit 1.0.4 and stage-1 results). Three worktrees `036-arm-{A,B,C}` on branches of the same name; arm B additionally carries one commit `d035e86` adding `agent.md`. No arm can see another (sub-agents instructed never to read other worktrees or branches; each worktree has its own branch).

**Implementer model:** `opus` in all three arms (CLAUDE.md model policy). **Design-model note:** in arm A the spec kit (spec/clarify/plan/tasks) was authored by the main loop (Fable 5.1) with the owner answering questions — exactly rev.2 practice; arm B's `agent.md` was also authored by Fable; arm C gets only CLAUDE.md. So the implementer is constant and what differs is the *form* in which the brain's intent reaches it: full spec kit (A), a standing rules file (B), the generic project file (C). Recorded in §K as a deliberate choice, not a confound to hide.

**Shared setup for every arm (baseline):** "First read `<worktree>/CLAUDE.md` in full" (sub-agents launch from another cwd, so the project file would not auto-load); run tooling from the worktree root through the shared venv (`UV_PROJECT_ENVIRONMENT=…/.venv uv run …`); never install dependencies; commit on the arm branch; do not push; record start and first-all-green timestamps. Gates identical: `pytest app/backend/tests -q`, `ruff check`, `ruff format --check`, `mypy --strict`, `check-no-provider-sdk-imports.sh`.

**Exact feature prompt (identical in all three arms):**

```text
Implement T24 from docs/engineering/implementation-plan.md — the Pre-Interview Planner agent wrapper.

What: add `app/backend/agents/planner.py`, a thin typed adapter around `app.backend.llm.call_model` for the Planner, in the same shape as the existing Interviewer (`app/backend/agents/interviewer.py`) and Assessor (`app/backend/agents/assessor.py`) wrappers. The prompt already exists and is pinned: `prompts/planner/v0001/` (`system.md` describes the inputs in §3 and the output contract in §4; `schema.json` is the committed output schema; `configs/models.yaml` carries the planner model config). The wrapper takes the §3 inputs as typed models, assembles the system prompt from the version directory, makes the model call with the committed schema, and returns the plan as a typed output mirroring `schema.json`. Session id is needed for cost attribution and tracing, as in the siblings.

Acceptance (from the implementation plan): a schema-valid plan is generated for a dummy position template against the mock Vertex backend (`LLM_BACKEND=mock`; fixtures live under `app/backend/tests/fixtures/llm_responses/` — read its README and `app/backend/llm/_mock_backend.py`). Plus a unit suite `app/backend/tests/agents/test_planner.py` in the style of the sibling suites (they monkeypatch `call_model` at the module boundary).

Constraints: purely additive — do not modify `prompts/**`, `app/backend/llm/**`, `configs/**`, or the existing agent modules. No DB access in the wrapper. No new dependencies.

Gates, all green before you stop: `uv run pytest app/backend/tests -q`, `uv run ruff check app/backend`, `uv run ruff format --check app/backend`, `uv run mypy --strict app/backend`, `bash scripts/check-no-provider-sdk-imports.sh`. When green, commit on your branch (do not push) and report: what you built, every decision you made where the inputs left a choice, and the gate output.
```

**Arm wrappers (the only difference between arms):**

- **A — Spec Kit 1.0.4.** Main loop ran `speckit-specify` (with its own ≤3-question round), `speckit-clarify` (3 of max 5 questions asked), `speckit-plan` (plan.md, research.md, data-model.md, quickstart.md), `speckit-tasks` (18 tasks in 6 phases) — all committed on the arm branch; then an opus sub-agent was told to read CLAUDE.md and execute `.claude/skills/speckit-implement/SKILL.md` verbatim; then `speckit-converge` on the session model. Process warts observed: the core `create-new-feature.sh` created `specs/037-…`, and the git extension's script — run afterwards as the `before_specify` hook prescribes — numbered the branch `038-planner-agent-wrapper` (the skill says branch and directory numbering are independent; they were).
- **B — `agent.md` only.** Prompt prefixed with "Read `agent.md` at the repo root first and follow it", plus "Do NOT use the Spec Kit skills and do NOT write anything under `specs/`". The file (43 lines, below) was written by the main loop from `docs/engineering/coding-conventions.md`, the CLAUDE.md invariants and the anti-patterns list, in Sanglard's spirit: terse imperative rules.
- **C — nothing.** Prompt plus "Do NOT use the Spec Kit skills and do NOT write anything under `specs/`; implement directly".

**Questions the owner answered in arm A (the interactive part):**

| Step | Question | Answer |
| --- | --- | --- |
| specify Q1 | Which semantic guardrails beyond the JSON schema? (none / structural / structural+numeric) | **B — structural only**: node ids exist in the input subset; every required competency appears |
| specify Q2 | Input typing: reuse `RubricSnapshot`/`PositionTemplateRead` or wrapper-local §3 models? | **B — wrapper-local models**; T25/T27 convert |
| clarify Q1 | Return the plan alone, or plan + call metadata for T25's `generated_by`? | **A — plan alone** (recommended) |
| clarify Q2 | Retry budget: once (siblings) vs "up to twice" (`vertex-integration.md`) vs twice + wrapper-side fallback | **B — three attempts, fallback is the caller's** (recommended) |
| clarify Q3 | Append the Interviewer's level guide to the Planner prompt? | **A — no**, `system.md` + anchors only (recommended) |

Clarify Q2 is the interesting one: the repo's own docs say the Planner retries up to twice, while both siblings retry once — a contradiction the spec author (Fable) had missed in the first draft and only surfaced because arm C's report cited the doc. The owner picked the documented policy.

**`agent.md` content (arm B, verbatim):**

```markdown
# agent.md — standing rules for working in this backend

Read this before writing any code. Rules, not preferences. When the codebase and this file disagree, this file wins.

## The floor
- LLMs produce content, never routing decisions. No `if` on model prose anywhere. (constitution §2)
- Every model call goes through `app.backend.llm.call_model`. Never import a provider SDK outside `app/backend/llm/`.
- Prompts are versioned directories under `prompts/<agent>/<vNNNN>/`. Never edit one in place; never read one you did not pin by version.
- Hard caps on every call: 30 s timeout, 4096 output tokens max, cost tracked per session. The wrapper enforces them; you do not relax them.
- No secret in source, tests, logs, fixtures, or prompts. `.env` locally, Secret Manager in prod.
- Append-only audit tables: never `UPDATE`/`DELETE` them. Corrections are new rows.
- Configs as code: model names, thresholds, prompt versions live in `configs/*.yaml`, never in Python literals.

## Shape of an agent wrapper
- One module in `app/backend/agents/`, one public `async def run_<agent>_<unit>(...)`. It executes; it does not decide.
- Pin `PROMPT_VERSION` as a module constant; it must match `configs/models.yaml` and `prompts/<agent>/active.txt`. Test the lockstep.
- Assemble the system prompt at runtime from the version directory exactly as the prompt's own §§ declare (appendices included). Cache the read; never cache mutable dicts you hand to callers — deep-copy.
- Typed inputs and outputs are frozen pydantic models. Outputs mirror `schema.json` with `extra="forbid"` and the same field constraints, so "passes pydantic" means "satisfies the committed contract".
- Serialize the user payload deterministically: `sort_keys=True`, `ensure_ascii=False`, total over legal inputs (`mode="json"`, `fallback=str`). Byte-stable payloads are what the mock backend's SHA-keyed fixtures depend on.
- Retry policy is per agent, explicit, and bounded: retry ONCE on a schema-class failure, then raise a typed `<Agent>OutputInvalid` chaining the cause. Every other wrapper error propagates untouched. Never loop until success.
- Validate what the schema cannot: ids must exist in the inputs they reference; enums echo back what was asked. A semantic mismatch is a contract failure, not a warning.
- No DB access, no filesystem writes, no side effects beyond what `call_model` performs through its injected sink/ledger.

## Python
- 3.12, `mypy --strict`, `ruff` + `ruff format`. Every parameter and return annotated. No bare `dict`/`list`.
- f-strings only. `logging` with structured `extra=`; never `print()`.
- Specific exception classes; never bare `except:`; never swallow.
- `async def` for anything that awaits; never block the loop.
- Layering: `api → services → repositories / llm / orchestrator → domain / config / utils`. Agents sit beside `llm`; they import from `llm`, never from `api` or `services`.

## Tests
- `pytest` + `pytest-asyncio`. Test file mirrors the module: `tests/agents/test_planner.py` for `agents/planner.py`.
- Mock only the LLM boundary (`call_model` monkeypatched at the module you test). Never mock the database; DB tests skip without `DATABASE_URL`.
- Every branch of the retry policy has a test. Every boundary in the schema (min/max, enum edge) has a test. The lockstep of version pins has a test.
- A test that passes because of a real side effect is a bug. Fixtures are deterministic files, checked in.
- Never disable a failing test. If it is wrong, delete it and say why in the commit body.

## Process
- Read before writing: the sibling modules, the prompt's `system.md`, the schema, the mock backend's fixture format.
- Purely additive changes unless the task says otherwise. Do not touch prompts, the llm package, or configs.
- Where the inputs leave a choice, choose the simplest reading consistent with the siblings, and list every such choice in your final report. Do not redesign.
- Gates before you stop: `pytest`, `ruff check`, `ruff format --check`, `mypy --strict`, the provider-SDK import guard. All green or you are not done.
- Commit with an imperative, lower-case subject ≤ 72 chars; reference the task in the body. Do not push.
```

**Blind review:** three separate reviewer sub-agents on the session model, identical prompt, each given one worktree as "candidate X / Y / Z" (X = arm B, Y = arm C, Z = arm A), told to follow `.claude/agents/reviewer.md`, review only `git diff 770bba1...HEAD -- app/`, and never read `specs/`, `agent.md`, or git log. Then a fix-round in each arm by the same implementer agent (same model, same context), and a second measurement.

**Timeline:** worktrees created 18:16:04; arms B and C launched 18:16; arm A specify started 18:17:27.

## I. Per-arm logs (turns, gate runs, reviewer output) — A, B, C

Reviewer identity per candidate: X = arm B, Y = arm C, Z = arm A. Fix-rounds were run by a **fresh** opus sub-agent per arm (the harness cannot resume a finished sub-agent in this session), given the same wrapper rules plus the reviewer report verbatim; same handicap for all three.

### Arm A — Spec Kit 1.0.4 (worktree `036-arm-A`, branch `038-planner-agent-wrapper`, base `770bba1`)

Process timeline (main loop = Fable 5.1, owner interactive): specify hook + spec draft 18:17:27–18:19:32 (2 specify questions → owner answered 18:2x); clarify 3 questions (owner answered; committed 18:37:26); plan + research + data-model + quickstart committed 18:39:18; tasks (18) committed 18:40:24. Spec-kit artifacts: 485 lines across 7 files. Owner turnaround included, brain-side wall clock ≈ 23 min (18:17 → 18:40).

Implementer: opus (general-purpose sub-agent executing `speckit-implement` SKILL.md verbatim). 47 tool uses; 169,388 tokens; started 18:40:49, gates first all green 18:49:01 (8 min 12 s); total agent duration 9 min 24 s. Commit `387e847` "add the pre-interview planner agent wrapper (T24)".

Report, verbatim:

> **Extension Hooks:** Optional Hook `git` / `/speckit-git-commit` ("Commit implementation changes?") — not executed, `auto_commit: false`; committed by hand.
>
> **Checklist status (read-only gate):** `requirements.md` 16/16 checked → PASS; implementation proceeded automatically.
>
> **Tasks completed:** all 18 in `specs/037-planner-agent-wrapper/tasks.md` now `[x]`.
>
> **What was built:** `app/backend/agents/planner.py` (~390 lines) — public API `PROMPT_VERSION`, `PlannerOutputInvalid`, `PlannerPlanMismatch`, `CandidateProfile`, `PositionSpec`, `RubricNode`, `PlannerInputs`, `DepthProbe`, `SeedQuestion`, `CompetencyPlan`, `PlannerOutput`, `async run_planner(inputs, *, sink, ledger, settings) -> PlannerOutput`; private loaders/serializer/validator. `app/backend/tests/agents/test_planner.py` — 38 tests (unit + offline acceptance). Fixture `…/planner/46e97ce2…1f29.json` — hand-authored Ukrainian plan (2 competencies, 3 seeds, 4 probes) via the `_unrecorded/` promotion flow. Diff purely additive apart from tasks.md checkboxes.
>
> **Choices the artifacts left open:**
> 1. `CompetencyPlan` vs `PlanCompetency` — spec.md says one, data-model.md/tasks.md the other; took the two-against-one name `CompetencyPlan`.
> 2. Added `_AGENT_NAME: Final[str] = "planner"` (assessor has it, interviewer does not).
> 3. `RubricNode.level_descriptors` left as plain `dict[str, str]` (data-model: no construction-time validation beyond field constraints).
> 4. Retry loop as a single `for _attempt in range(3)` with `last_failure` (plan §3 prescribes it) rather than the siblings' unrolled try-blocks.
> 5. Guardrail messages name node ids (not PII; assessor precedent); `PlannerOutputInvalid` stays PII-free.
> 6. `_MAX_ATTEMPTS: Final[int] = 3` named constant.
> 7. Prompt-assembly join in the interviewer's form (closer shape).
> 8. Level-guide-absence test reads the guide's first heading rather than hard-coding a marker.
> 9. Acceptance test reuses the shared `test_settings` conftest fixture (T011 allowed "the way existing mock-backend tests do").
> 10. Only the no-`DATABASE_URL` pytest mode was runnable (155 skips = DB suites); the feature adds no DB tests.
>
> **Gate output:** pytest → 421 passed, 155 skipped in 8.02 s · ruff check → All checks passed! · ruff format --check → 127 files already formatted · mypy --strict → Success: no issues found in 127 source files · provider guard → exit 0. `git status --porcelain` empty after commit. All 28 pre-commit hooks passed. Not pushed.

#### `speckit-converge` on arm A (Fable 5.1; 19 tool uses; 145,658 tokens; 18:51:10 → 18:54:25, 3 min 15 s)

> Prerequisite script: `{"FEATURE_DIR":".../specs/037-planner-agent-wrapper","AVAILABLE_DOCS":["research.md","data-model.md","quickstart.md","tasks.md"]}`. Hooks: none. Read all seven feature artefacts, the full module and test file, the fixture, the prompt assets, the sibling wrappers and the llm/conftest references. No gates run, no git history.
>
> **Convergence Findings:** empty table — "No gaps found. Every FR, SC, acceptance scenario, edge case, plan decision, and applicable constitution principle in the intent inventory is satisfied by the present code", with an evidence line per inventory item (FR-001…FR-010, SC-001…SC-004, US1–US3 acceptance scenarios, five edge cases, research D1–D6, plan design items 1–5, tasks T001–T018 all `[x]` and present).
>
> **Summary metrics:** 28 requirements/acceptance criteria checked; 11 plan decisions; 8 applicable constitution principles (§2, §5, §11, §12, §14, §15, §16, §17 — all PASS; §9 N/A per plan); findings 0/0/0/0.
>
> Observation (not a finding, out of additive scope): `vertex-integration.md:129` still lacks the "see planner.py; fallback is the caller's" note the Assessor/Interviewer lines carry.
>
> **Outcome: `converged`** — "✅ Converged — the implementation satisfies the spec, plan, and tasks." tasks.md byte-for-byte unchanged; `git status --short` empty.

First `converged` result in the whole experiment (stage 1's control run had found a stale docstring). The spec here was written before the code and the code was written to it, which is the case converge is built for.

#### Reviewer report — candidate Z (= arm A), blind, Fable 5.1, 22 tool uses, 145,515 tokens, 18:50:58–18:54:06

> **Status:** ⚠️ warnings
>
> **Blocks:** none.
>
> **Warnings**
> - [planner.py:38–44, 404–415] Documented policy deviation: `vertex-integration.md` §JSON mode says "retry up to twice; on repeated failure, fall back to the previous rubric version's default plan template." The wrapper implements the two retries but on exhaustion raises `PlannerOutputInvalid` and delegates the fallback to "the caller (T25/T27)". Justification (no DB access) is sound and stated, but doc and code disagree on where the fallback lives; amend the doc in a follow-up and name the owning task.
> - [planner.py:144–146, 204–210] Wrapper-invented input bounds not in the pinned §3 contract: `prior_role_notes` `max_length=600`, `expected_minutes` 10–90, `per_competency_minute_budget` 3–20 (the latter two copied from the *output* schema). A 25-minute per-competency budget or a 700-char note is rejected before any call. Defensible as "never spend tokens on an unanswerable request", but it narrows §3 — confirm against the T25/T27 conversion or relax.
>
> **Notes** (10): prompt-contract fidelity otherwise exact (schema mirrored field-for-field, deep-copied schema, §7.1/§8.1 guardrails enforced, §12 caps asserted, `session_id` attached, level guide deliberately excluded per §5 wording) · `required_competencies` read as node ids — if a caller passes labels every plan fails guardrail (b) and burns three Pro calls; worth a sentence in the T25/T27 conversion contract · `target_level` capped at 4 vs glossary's ranks 1–5 (prompt-level scale question, not a wrapper defect) · implementation-plan's `must_cover`/`nice_to_have` drift (schema is the source of truth) · docstrings cite "research D1/D2/D3", "owner decision 2026-09-06" without a path · `PlannerPlanMismatch(ValueError)` vs `AssessorEchoMismatch(Exception)` — small shape drift · exceptions module-local like siblings · `plan_version_seed` literal lockstep tested · 38 tests pass in 0.8 s, wider agents+llm run 185 passed / 25 skipped; acceptance unpatched through the mock; `_unrecorded/` clean; ruff/format/mypy clean; test file 1028 lines vs siblings 553/737 · §17 unverifiable blind, though tests reference FR-010 / SC-001 / User Stories 1–3.
>
> **Checked:** Constitution ✓ (§2, §5, §11, §12, §15, §16) · Secrets ✓ (gitleaks no leaks) · Tests ✓ (38) · Migrations n/a · Prompts n/a · Contract ✓ · Design / Visual n/a.
>
> COUNTS: blocks=0 warnings=2 notes=10

Blindness leak: the reviewer noticed tests reference FR/SC/User-Story ids ("indicates a spec exists"). It did not name the process.

**Owner adjudication before the fix-round (rev.2: contract text is the brain's):** warning 2 touched `data-model.md`, so the main loop amended it (keep the two schema-mirrored bounds with rationale; relax the notes cap to 2000) and added a Clarifications line naming T25/T27 as the fallback owner — commit `5e8e730`, ~2 min. The fix-round agent was told the resolutions, not asked to decide.

#### Arm A fix-round (fresh opus agent, spec artifacts amended by the owner first — commit `5e8e730`; 44 tool uses; 109,825 tokens; 18:56:36 → gates green 19:01:08, 4 min 32 s). Commit `a1ed081`; `git diff --stat HEAD~1..HEAD` → planner.py +81ish, test_planner.py +68ish; **2 files, +128/−21**. Tests 38 → 42.

> **Warning 1 (fallback ownership):** owner marker at the `PlannerOutputInvalid` raise site in the repo's TODO convention — `# TODO(@T25/T27, docs/engineering/implementation-plan.md): the default-plan-template fallback … is owned by the session-start caller … NOT by this wrapper …`; the module docstring's retry bullet points at it. Only TODO marker in `app/backend`.
> **Warning 2 (input bounds):** kept 10–90 and 3–20 with the adjudicated rationale in the module docstring, both field docstrings and a header comment ("CONTRACT MIRRORS, not policy"); relaxed `prior_role_notes` to 2000 as a sanity ceiling. Four new tests, incl. `test_input_minute_bounds_mirror_the_committed_output_schema`, which reads `schema.json` and asserts the input bounds equal the output bounds — "turns 'they are mirrors' into an executable claim".
> **Notes:** caller warning on `required_competencies` (ids, not labels); citations now carry `specs/037-planner-agent-wrapper/<file>` paths; `PlannerPlanMismatch(ValueError)` kept with a reason; the rest left.
> Gates: 425 passed, 155 skipped in 7.55 s; ruff, format, mypy --strict, guard clean.

### Arm B — `agent.md` only (worktree `036-arm-B`, base `770bba1` + `d035e86` agent.md)

Implementer: opus (general-purpose sub-agent). 40 tool uses; 163,321 tokens; started 18:16:21, gates first all green 18:25:28 (9 min 7 s); total agent duration 9 min 57 s. Commit `7dc2511` "add planner agent wrapper".

Report, verbatim:

> **What I built (3 new files, purely additive)**
> - `app/backend/agents/planner.py` — `run_planner_plan(inputs, *, sink, ledger, settings) -> PlannerOutput`. Pins `PROMPT_VERSION = "v0001"`; assembles the system prompt (cached `lru_cache`) from `prompts/planner/v0001/system.md` + `prompts/shared/ukrainian-anchors.md`; deep-copies the committed `schema.json` into `ModelCallRequest.json_schema`; serializes the §3 inputs with `model_dump(mode="json", exclude={"session_id"}, fallback=str)` + `json.dumps(sort_keys=True, ensure_ascii=False, default=str)`; §12 caps untouched. Typed inputs `PlannerInputs` (`CandidateProfile`, `PositionSpec`, permissive `rubric_snapshot` dicts, `expected_minutes`, `per_competency_minute_budget`); typed output `PlannerOutput` / `CompetencyPlan` / `SeedQuestion` / `DepthProbe`, all `frozen` + `extra="forbid"` mirroring `schema.json` (const, enums, `^q[0-9]+$`, all length/range bounds). Retry-once policy over `(VertexSchemaError, ValidationError, PlannerPlanMismatch)` → `PlannerOutputInvalid` chaining the second cause; everything else propagates. No DB, no writes.
> - `app/backend/tests/agents/test_planner.py` — 52 tests, sibling style (`call_model` monkeypatched at the module boundary), plus the T24 acceptance test driving the **real** `call_model` with `LLM_BACKEND=mock`.
> - `app/backend/tests/fixtures/llm_responses/planner/3869322…f7b.json` — the acceptance fixture, produced via the README's `_unrecorded/` promotion flow.
>
> **Decisions where the inputs left a choice**
> 1. Prompt assembly = `system.md` + shared Ukrainian anchors only. Planner §6 binds all plan text to the anchors, so it is appended. §5's pointer at `prompts/interviewer/v0001/level-guide.md` is a cross-agent "see … for examples" reference — unlike the Interviewer's own §5 ("Pulled in as an appended section at runtime") — and §5 already carries the L1–L4 mapping inline, so I did not reach into another agent's version directory (that would also mean pinning a second agent's prompt version). A test asserts the guide is *not* inlined, so the choice is visible if you want it reversed.
> 2. Function name `run_planner_plan` — literal `run_<agent>_<unit>` per agent.md; the Planner's unit is the plan.
> 3. Semantic checks limited to three (`PlannerPlanMismatch`): unknown `rubric_node_id`, uncovered required competency, `expected_minutes` echo. Not enforced: §8 forbidden #2 (seed level ≤ target+1) or §7 guardrail #6 (±20% total minutes) — calibration-quality signals per the prompt's `notes.md`; making them hard failures would be a policy call beyond "ids exist / enums echo".
> 4. `PositionSpec.required_competencies` holds rubric node ids, not labels — the only reading that makes the coverage check well-defined. Documented on the field.
> 5. `rubric_snapshot` stays `tuple[dict[str, Any], ...]` (matching the Assessor's permissive `rubric_snapshot_subset`); the node-id check reads the `id` key §3 declares, ignores nodes without a string `id`. Did not validate `required_competencies ⊆ snapshot ids` at input construction (caller hygiene, not a model contract).
> 6. Input bounds mirror the output schema (`expected_minutes` 10–90, `per_competency_minute_budget` 3–20) so an out-of-contract request is rejected before tokens are spent. `years_experience: int | None, ge=0`.
> 7. Collection types follow the closest sibling: `tuple` in inputs, `list` in outputs.
> 8. `plan_version_seed` is a static `Literal["planner-v0001"]`; a test asserts it equals `f"planner-{PROMPT_VERSION}"` and the schema's `const`.
> 9. Fixture content is hand-written, deliberately not a copy of the unit-test payload (three seeds, three probes across two competencies) so the acceptance test is not tautological. Token counts are plausible placeholders.
> 10. Retry flow uses the Assessor's nested `try` rather than the Interviewer's sequential form, because the failure message names both misses.
>
> **Gate output**
> ```
> uv run pytest app/backend/tests -q      → 435 passed, 155 skipped in 7.75s   (52 new)
> uv run ruff check app/backend           → All checks passed!
> uv run ruff format --check app/backend  → 127 files already formatted
> uv run mypy --strict app/backend        → Success: no issues found in 127 source files
> bash scripts/check-no-provider-sdk-imports.sh → exit 0
> ```
> Commit `7dc2511` "add planner agent wrapper" (pre-commit hooks all passed). Nothing pushed; `prompts/**`, `app/backend/llm/**`, `configs/**`, and the existing agent modules are untouched.

#### Reviewer report — candidate X (= arm B), blind, Fable 5.1, 20 tool uses, 150,706 tokens, 18:41:35–18:44:30

> **Status:** ⚠️ warnings
>
> **Blocks:** none.
>
> **Warnings**
> - [planner.py:33–36, 417–429] Retry policy deviates from the documented per-agent Planner policy. `docs/engineering/vertex-integration.md:129` says "retry up to twice; on repeated failure, fall back to the previous rubric version's default plan template." The wrapper retries exactly once (mirroring the siblings) and raises `PlannerOutputInvalid` with no fallback. Defensible under "no DB access / purely additive", but the docstring presents "retry ONCE" as *the* policy without acknowledging the documented one. Cite the deviation (and who owns the fallback) or align the doc.
> - [planner.py:329–352] Semantic enforcement is partial relative to the pinned prompt contract: enforces §8 #1 (no invented node ids), §7 #1 (required coverage) and an `expected_minutes` echo, but skips §8 #2 / §7 #2 (`seed_questions[].level` ≤ `target_level + 1`) and the per-competency `target_level` echo against the snapshot node (the Assessor does the analogous echo check, `assessor.py:386–398`). Add both to `_check_plan_against_inputs` or document why they are left to calibration.
>
> **Notes**
> - Committed fixture's budgets sum to 15 min against `expected_minutes: 30` — outside §7 #6 (±20 %); passes because the wrapper doesn't enforce §7 #6, but the "known-good" artefact should model the prompt's rules.
> - Neither schema nor model rejects duplicate `rubric_node_id` / duplicate seed ids; flagged for the T25/orchestrator owner.
> - A pre-existing planner fixture from the base commit (`11c0…e21e.json`, T04-era placeholder) is now dead weight.
> - Constitution §17 (spec reference for > 50 lines) not verifiable under blind rules.
> - Test-run hygiene clean (`_unrecorded/` empty, `git status` clean after the suite).
> - Verification: `test_planner.py` → 52 passed in 3.82 s; ruff, ruff format, mypy --strict clean.
>
> **Checked:** Constitution ✓ (§2, §5, §11, §12, §15, §16; §17 unverifiable) · Secrets ✓ (gitleaks on the diff: no leaks) · Tests ✓ (adjacent suite, sibling style, covers assembly, lockstep, caps, payload, every schema bound, all three semantic checks, retry paths, non-schema propagation, input rejection, acceptance through real `call_model` + mock) · Migrations n/a · Prompts n/a (nothing under `prompts/**` touched; level guide deliberately not appended, documented + tested) · Contract ✓ (`PlannerOutput` mirrors schema field-for-field) · Additivity ✓ ("three new files under `app/` — plus a root `agent.md`, not read") · Design / Visual n/a.
>
> COUNTS: blocks=0 warnings=2 notes=6

Blindness leak: the reviewer ran `git diff --name-status` without the `app/` filter and saw that a root `agent.md` exists (it says it did not read it). It did not name the process in its report.

#### Arm B fix-round (fresh opus agent, same wrapper rules; 34 tool uses; 119,846 tokens; 18:46:31 → gates green 18:52:27, 5 min 56 s). Commit `8d72e14`; `git diff --stat HEAD~1..HEAD` → planner.py +123/−10ish, test_planner.py +124, fixture 2 lines; **3 files, +239/−10**. Tests 52 → 58.

> **Warning 1 (retry policy):** resolved on the docstring side; **retry-once kept deliberately** — the documented fallback is stored state (rubric-version lookup + template read) that a pure wrapper cannot own; T25 catches `PlannerOutputInvalid` and owns escalation; adopting only the "up to twice" half "would spend a third call on the same missed contract while breaking the single bounded-retry shape every wrapper shares". Docs-side reconciliation named as out of additive scope.
> **Warning 2 (partial semantics):** both checks added to `_check_plan_against_inputs` on the `PlannerPlanMismatch` path — `target_level` echo against the snapshot node (nodes without an int `target_level` are skipped, not guessed; documented + tested) and seed-level ceiling `≤ target_level + 1`. Six new tests incl. boundary-valid params and retry recovery.
> **Notes:** fixture budgets rebalanced 8+7 → 15+12 (within ±20 %; SHA unchanged since it keys on the request) and the acceptance test now asserts §7 #6 and the ceiling; duplicates left alone and recorded as out of scope in the docstring; T04 placeholder fixture untouched; §17 nothing to do.
> Gates: 441 passed, 155 skipped in 7.53 s; ruff, format, mypy --strict, sdk guard all clean.

### Arm C — nothing (worktree `036-arm-C`, base `770bba1`)

Implementer: opus (general-purpose sub-agent). 40 tool uses; 169,251 tokens; started 18:16:34, gates first all green 18:25:26 (8 min 52 s); total agent duration 9 min 51 s. Commit `9a66315`.

Report, verbatim:

> **What I built (purely additive — 3 new files, nothing modified)**
> - `app/backend/agents/planner.py`: `load_system_prompt()` (lru_cached), `load_output_schema()` (cached read + deepcopy per call, like the Interviewer). Typed §3 inputs: `PlannerInputs` (session_id, candidate_profile, position, rubric_snapshot, expected_minutes, per_competency_minute_budget) with `CandidateProfile` / `PositionSpec` sub-models and `to_user_payload()`. Typed output mirroring `schema.json`: `PlannerOutput` → `CompetencyPlan` → `SeedQuestion` → `DepthProbe`, all `frozen` + `extra="forbid"`, encoding the const, the 1–4 level enums, the `^q[0-9]+$` id pattern, and every length/range/cardinality bound. `run_planner(inputs, *, sink, ledger, settings)` + typed `PlannerOutputInvalid`.
> - `app/backend/tests/agents/test_planner.py` — 39 tests in the sibling style (`call_model` monkeypatched), plus the T24 acceptance test which does *not* patch: it runs the real `call_model` against `LLM_BACKEND=mock` and asserts a schema-valid plan, one trace record (agent=planner, model=gemini-2.5-pro) and a non-zero ledger charge.
> - `app/backend/tests/fixtures/llm_responses/planner/47d34a68…7505.json` — recorded through the documented `_unrecorded/` promotion flow (capture file deleted afterwards).
>
> **Decisions where the inputs left a choice**
> 1. Prompt assembly = `system.md` + `prompts/shared/ukrainian-anchors.md`; the Interviewer level-guide is *not* inlined. §6 makes the anchors binding; §5 only says "See … for examples", already inlines its own L1–L4 mapping, and that guide is written against `current_competency.target_level` — an input the Planner never receives. A test pins this choice.
> 2. **Retry budget = 3 attempts (retry up to twice), not the siblings' retry-once.** `docs/engineering/vertex-integration.md` § "JSON mode" states the per-agent policy explicitly: *"Planner: retry up to twice; on repeated failure, fall back to the previous rubric version's default plan template."*
> 3. The documented fallback (previous rubric version's default plan template) is left to the caller — no such template exists in the repo and selecting one needs rubric/DB access. The wrapper raises `PlannerOutputInvalid` so T25's plan-generation service owns the escalation.
> 4. `rubric_snapshot` stays a permissive `tuple[dict[str, Any], ...]` (min 1 node). §3's shape is a per-session *selection* and is **not** the repo's `RubricSnapshot`; typing it here would fork a contract T25 owns.
> 5. Input bounds mirror the pinned output contract: `expected_minutes` 10–90, `per_competency_minute_budget` 3–20. Side effect noted: v0001 caps levels at 4, so a rubric node targeting level 5 is unrepresentable in this prompt version.
> 6. **No semantic plan↔rubric cross-checks** (required-competency coverage §7.1, unknown `rubric_node_id` §8.1). With `rubric_snapshot` permissive, enforcing them would mean guessing a wire key name. Deferred to T25; documented on `CompetencyPlan.rubric_node_id`.
> 7. Small tightening over `schema.json`: `rubric_node_id` gets `min_length=1`; absent `depth_probes` normalises to `[]`; absent optional profile fields serialize as explicit `null`.
> 8. Naming: `run_planner` (not `run_planner_turn`) — the Planner runs once per session.
>
> Observation, out of scope: `prompts/planner/v0001/schema.json` and the orchestrator's `PlanSnapshot` are different shapes (`rubric_node_id`/`minute_budget`/`seed_questions[]` vs `node_id`/`minutes`/`seed_questions_uk`, target_level 1–4 vs 1–5). Translating is T25's job; noted in the module docstring.
>
> **Gate output (all green)**
> ```
> pytest → 422 passed, 155 skipped in 8.49s
> ruff check → All checks passed!  ruff format → 127 files already formatted
> mypy --strict → Success: no issues found in 127 source files
> sdk guard → OK
> ```
> Pre-commit hooks all passed on commit. Nothing pushed.

#### Reviewer report — candidate Y (= arm C), blind, Fable 5.1, 31 tool uses, 159,214 tokens, 18:41:44–18:44:40

> **Status:** ⚠️ warnings
>
> **Blocks:** none.
>
> **Warnings**
> - [planner.py:310–319, 322–340] Prompt guardrails are not enforced at the wrapper even though every operand is in hand: §7.1 (every required competency must appear), §8.1 (only ids from `rubric_snapshot`), §7.2/§8.2 (no seed above `target_level + 1`) are relational checks `schema.json` cannot express; `PlannerOutput` only checks `rubric_node_id` non-emptiness. The Assessor enforces the analogous integrity check in-wrapper (`assessor.py:367–399`). The candidate defers to T25 by docstring. Enforce on the retry-then-raise path or have the owner confirm the deferral — a hallucinated `rubric_node_id` reaching plan review/freeze is the risk.
> - [planner.py:22–30, 398–402] `vertex-integration.md` §JSON mode: "Planner: retry up to twice; on repeated failure, fall back to the previous rubric version's default plan template." Retry count matches (`_MAX_ATTEMPTS = 3`), the fallback half is deferred to T25 by docstring only; nothing records it as a follow-up. Add a tracked marker or amend the doc.
>
> **Notes** (10): §17 unverifiable blind · `implementation-plan.md:531` describes T24 output with `must_cover`/`nice_to_have` that the pinned schema lacks (doc drift, not a defect) · `_MAX_ATTEMPTS` docstring says "stricter" where it is more lenient (wording) · level guide deliberately not appended, documented and pinned by test; a prompt-engineer should confirm intent · `PlannerOutputInvalid` in-module rather than `app/backend/exceptions.py` (file does not exist; siblings identical) · no wrapper-level language check on `text_uk` (siblings identical) · `prior_role_notes` uncapped vs "1–3 sentences" · public `load_*` names mirror the Assessor · verification: 39 passed in 0.91 s, ruff/format/mypy clean, gitleaks no leaks, `_unrecorded/` clean, fixture within all schema bounds (q2 at level 2 ≤ target 3+1), acceptance exercises real `call_model` → mock → SHA fixture · purely additive; §12 defaults asserted; `session_id` set; lockstep tested. `[escalation-candidate]`: none.
>
> **Checked:** Constitution ⚠ (§17 unverifiable; §2/§3/§5/§11/§12/§15/§16 ✓) · Secrets ✓ · Tests ✓ (39) · Migrations n/a · Prompts n/a · Contract ✓ (`json_schema` equals committed schema byte-for-byte per test) · Design / Visual n/a.
>
> COUNTS: blocks=0 warnings=2 notes=10

#### Arm C fix-round (fresh opus agent, same wrapper rules; 30 tool uses; 117,353 tokens; 18:46:46 → gates green 18:53:24, 6 min 38 s). Commit `7689e7e`; `git diff --stat HEAD~1..HEAD` → planner.py +225ish, test_planner.py +317ish; **2 files, +513/−29**. Tests 39 → 50.

> **Warning 1 (guardrails):** added `_check_guardrails(plan, inputs)` inside the retry loop — §8.1 unknown node id (checked first), §7.1 required coverage, §7.2/§8.2 seed level ≤ `target_level + 1` using the **frozen snapshot's** `target_level` as authority (echoed level only as fallback for permissive nodes). New `PlannerGuardrailViolation` on the contract-miss path; PII-free messages. Also a `model_validator` on `PlannerInputs` rejecting a required competency absent from the snapshot ("§7.1 and §8.1 are in direct conflict there — no legal plan exists; without it the wrapper would burn three Pro calls and blame the model for a caller bug").
> **Warning 2 (fallback deferral):** explicit `TODO(T25, owner: backend-engineer, tracked as task T25 in docs/engineering/implementation-plan.md …)` at the raise site, per coding-conventions' "no TODO without owner and link" (no issue tracker wired). Docs untouched.
> **Notes:** "stricter" wording fixed to "more lenient"; `prior_role_notes` capped at 1000 chars (tested 1000/1001); the rest left as no-ops per the reviewer's reading.
> Tests: `_VALID_PARSED` now covers both required competencies; 11 new cases; acceptance fixture SHA intact.
> Gates: 432 passed, 155 skipped in 7.55 s; ruff, format, mypy --strict, sdk guard clean; 27 pre-commit hooks passed.

## J. Scorecard table (the metrics above, one column per arm)

| Metric | A — Spec Kit 1.0.4 | B — `agent.md` | C — nothing |
| --- | --- | --- | --- |
| Implementer tool uses to first green gates | 47 (+ main loop: ~12 tool calls and 5 owner answers to author the spec kit) | 40 | 40 |
| Implementer tokens, build | 169,388 | 163,321 | 169,251 |
| Reviewer findings (blocks / warnings / notes) | 0 / 2 / 10 | 0 / 2 / 6 | 0 / 2 / 10 |
| Reviewer verdict | ⚠️ warnings | ⚠️ warnings | ⚠️ warnings |
| Fix-round tool uses / tokens | 44 / 109,825 | 34 / 119,846 | 30 / 117,353 |
| **Lines changed after review** (`app/` diff, first green → post-review) | **+128 / −21** (2 files) | **+239 / −10** (3 files) | **+513 / −29** (2 files) |
| Diff at first green (`app/`) | +1,451 (3 files) | +1,355 (3 files) | +1,174 (3 files) |
| Diff at post-review (`app/`) | +1,558 | +1,584 | +1,658 |
| `planner.py` / `test_planner.py` lines at end | 471 / 1,080 | 534 / 1,043 | 586 / 1,065 |
| Tests at first green → end | 38 → 42 | 52 → 58 | 39 → 49 |
| Tokens, implementer total (build + fix) | 279,213 | 283,167 | 286,604 |
| Tokens, process extras | converge 145,658 (+ main-loop spec-kit authoring, not metered by the harness) | 0 | 0 |
| Tokens, reviewer (identical role, not an arm cost) | 145,515 | 150,706 | 159,214 |
| Wall clock, active (build + review + fix; A adds spec-kit authoring incl. owner turnaround, converge ran parallel to review) | ≈ 39 min (23 + 8:12 + 3:08 + 4:32) | ≈ 18 min (9:07 + 2:55 + 5:56) | ≈ 18 min (8:52 + 2:56 + 6:38) |
| Wall clock, start → post-review green (incl. orchestration waits) | 18:17:27 → 19:01:08 = 43 min 41 s | 18:16:21 → 18:52:27 = 36 min 6 s | 18:16:34 → 18:53:24 = 36 min 50 s |
| Spec / process artifact lines | 488 (7 files: spec 121, plan 89, research 31, data-model 63, quickstart 30, tasks 119, checklist 35) | 43 (`agent.md`) | 0 |
| Converge result | ✅ Converged (0 findings) | not applicable | not applicable |
| Retry policy shipped at first green | 3 attempts (from clarify Q2 → `vertex-integration.md`) | retry once (from `agent.md`) — kept after review, defended | 3 attempts (found `vertex-integration.md` unprompted) |
| Semantic guardrails at first green | node ids + required coverage (spec) | node ids + required coverage + `expected_minutes` echo (`agent.md` "validate what the schema cannot") | none (deferred to T25 by docstring) |
| What the fix-round had to add | docstrings, an owner marker, one relaxed cap, 4 tests | `target_level` echo + seed-level ceiling, fixture rebalance, 6 tests | all three guardrails + input validator + owner marker + notes cap, 11 tests |
| Owner's subjective note (2–3 lines per arm) | _owner_ | _owner_ | _owner_ |

**Main-loop observations (data, not the owner's verdict):**

- All three arms reached mergeable code: zero blocks anywhere, and each reviewer raised exactly two warnings on the same two topics — the retry policy vs `vertex-integration.md`, and how much of the prompt's §7/§8 guardrails the wrapper enforces. The reviewer gate, not the process, is what equalised the arms.
- The arms differ in **when** the design decisions got made. A made five of them before code (owner answered five questions), B carried three of them in a rules file (one of them wrong for this agent: `agent.md` says "retry ONCE", the repo doc says "up to twice" for the Planner, and the B agent obeyed the rules file, then defended it in the fix-round), C made none up front and discovered one on its own (it read the doc that the spec author had missed). Post-review churn follows that order exactly: +128 / +239 / +513.
- The one thing only Spec Kit did: **clarify surfaced a contradiction inside the repo** (siblings retry once; the doc says the Planner retries twice) as an owner decision. Honest footnote: the spec author (Fable) noticed it only after arm C's report cited the doc; without the parallel arms the clarify round might have shipped FR-005 as "retry once".
- Blind review leaked in small ways: reviewer X saw a root `agent.md` in an unfiltered `--name-status`; reviewer Z inferred a spec from FR/SC ids in test names. Neither named the process; none of the reports reads as biased.
- Converge on A returned **Converged** — its first clean result in this experiment — because here the spec preceded the code, which is the case the tool is built for.
- Cost: implementer tokens are flat across arms (~280 k each incl. fix-round). Spec Kit's extra cost is the brain's authoring (unmetered; ~23 min of wall clock including the owner's five answers) plus converge (146 k). The rules file cost 43 lines once and nothing per feature.
- Threshold reading for this T18-sized feature: B and C ended within one review round of A's quality at roughly half the wall clock; A bought lower post-review churn and a decision record (spec Clarifications) with the owner's attention. Where the feature has more than a handful of real forks, or the forks are ones the reviewer would not catch, that trade flips; here it did not, because the reviewer caught every fork in every arm.

## K. Owner's notes (which arm you'd actually ship; where the threshold seems to be)

_owner writes this_

## Appendix — evidence locations (all local, nothing pushed)

- Branch `036-speckit-1x-converge`: §A/§B commits, the upgrade commit `c04b19f`, this file.
- Run worktrees under `.claude/worktrees/036-run-{control,attempt-v12,attempt-v10}` on
  branches `036-run-*`; each has one final commit with converge's Phase 8 append to
  `specs/032-t20-state-machine/tasks.md` (diff = exactly the blocks quoted above).
- Local tag `archive/032-t20-sonnet-attempt` → `d464a9a` (the attempt's four commits).
- Scratch trial clone of the upgrade: session scratchpad only, disposable.
- Stage 2 arms: worktrees `.claude/worktrees/036-arm-{A,B,C}` on branches `036-arm-A` → `038-planner-agent-wrapper` (A's git hook renamed it), `036-arm-B`, `036-arm-C`; base `770bba1`. Each holds its build commit, review fix-round commit, and (A) the spec-kit commits.
