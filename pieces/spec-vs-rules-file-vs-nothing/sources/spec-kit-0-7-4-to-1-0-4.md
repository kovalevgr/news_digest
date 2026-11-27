---
kind: source
title: "GitHub Spec Kit 0.7.4 → 1.0.4: what changed (CHANGELOG, v1.0.0 release notes, docs/upgrade.md, the converge skill) — fetched 2026-09-06"
url: https://raw.githubusercontent.com/github/spec-kit/main/CHANGELOG.md
url2: https://github.com/github/spec-kit/releases/tag/v1.0.0
url3: https://github.com/github/spec-kit/blob/main/docs/upgrade.md
url4: (local) TechScreen .claude/skills/speckit-converge/SKILL.md after the upgrade, commit c04b19f
---

## Timeline 0.7.4 → 1.0.4 (CHANGELOG, dates as listed)

TechScreen initialised on 0.7.4 (2026-04-21 release; project init 2026-04-19 on the dev build). Between that and 1.0.4 there were ~25 releases in four and a half months.

| Version | Date | What matters |
| --- | --- | --- |
| 0.7.5 | 2026-04-22 | `specify self check` / `self upgrade` stubs; skill placeholder fixes |
| 0.8.0 | 2026-04-23 | Preset composition (prepend/append/wrap) for templates, commands, scripts; skills-based scaffolding via `--integration-options="--skills"` |
| 0.9.0 | 2026-06-01 | agent-context extracted into a bundled extension; native Cline integration |
| 0.9.4 | 2026-06-04 | JSON output for `workflow run/resume`; headless CLI dispatch for Cursor; `specify workflow run` on bare YAML |
| **0.10.0** | 2026-06-09 | **BREAKING:** legacy `--ai`, `--ai-commands-dir`, `--ai-skills` flags removed; git extension opt-in, `--no-git` removed |
| 0.11.0 | 2026-06-16 | Workflow step catalog (community-installable step types); Zed integration; integration scaffolder |
| 0.11.2 | 2026-06-18 | `specify bundle`; **bug-assess agentic workflow**; `from_json` filter; init workflow step |
| 0.11.3 | 2026-06-19 | `/analyze` forked to a subagent for long-session stability |
| 0.12.0 | 2026-06-29 | agent-context extension fully opt-in; Firebender (Android Studio/IntelliJ); create-new-feature and related scripts ported to Python |
| 0.12.3 | 2026-07-01 | Warning before the skills default rollout; Roo Code and Windsurf integrations retired |
| 0.13.0 | 2026-07-17 | **Idea-assessment pipeline extension** |
| 0.14.0 | 2026-07-23 | `invoke_separator` handling; reproducible builds; Factory Droid CLI; Python script type |
| 0.15.0 | 2026-07-30 | First-class agent-native runtime hooks for integrations |
| 0.16.0 | 2026-08-05 | Context injection for OpenCode; JSON-envelope agent hooks; Copilot defaults to skills; stdin capped at 1 MiB |
| 0.16.2 | 2026-08-10 | Command Code integration; **manifest-aware template resolution** for presets |
| 0.16.5 | 2026-08-19 | **feature-assess agentic workflow**; Docker Agent integration |
| **1.0.0** | 2026-08-21 | Stable 1.0 with integrated extension / preset / workflow systems; Security Review extension v2.0.0 |
| 1.0.1 | 2026-08-21 | Docs refresh; workflow quickstarts; brand consolidated as "Spec Kit" |
| 1.0.2 | 2026-08-31 | Community catalog expansion; extension manifest validation hardening |
| 1.0.3 | 2026-09-01 | Config validation; workflow config fixes |
| 1.0.4 | 2026-09-02 | Workflow composition fixes; DeepSeek Harness integration; error handling for corrupted state files |

Note: the CHANGELOG does not list `converge` as a line item; it arrives with the 1.0 command set (the skill file is `templates/commands/converge.md`, installed as `speckit-converge` on upgrade — verified locally, 279 lines, commit `c04b19f`).

## What "1.0" means, in the maintainers' own words (release notes, 2026-08-21)

> "The old 1.0.0 was a handshake: rely on the shape, I will warn you before I change it. Ours is more of a wave: here is a good place to start; if I move something, your agent will follow it faster than a changelog could describe it."

> "The migration guide is no longer something you consume; it is something your agent consumes for you."

So 1.0 is explicitly NOT a traditional stability promise. What IS promised (docs/upgrade.md): "Spec Kit follows semantic versioning for major releases. The CLI and project files are designed to be compatible within the same major version." Plus a manifest-aware upgrade: `specify integration upgrade <key>` stops on locally-modified managed files unless `--force`; `specs/`, source, git history and the constitution are "never modified during upgrades".

## Practical differences for a project that was on 0.7.4 (what the TechScreen upgrade showed, stage-1 §B)

- Upgrade is now a supported, manifest-aware command (`specify integration upgrade claude` + `specify extension update`) instead of `init --here --force`. On TechScreen: 3 s CLI, 27 files modified + 4 new, +1,530/−706 lines, zero breakages, skills-mode setup survived, constitution/specs/extensions/git-config untouched.
- 14 `SKILL.md` rewrites: `speckit-specify` +140 lines, `speckit-clarify` +102, `speckit-implement` +118 (now treats checklists as a read-only gate, reads the constitution before implementing, mandatory hooks must actually be invoked), `speckit-plan` +91, `speckit-tasks` +99.
- New `speckit-converge`: append-only; its only write is a `## Phase N: Convergence` section in `tasks.md`; reads spec/plan/tasks as the "sole source of intent" with the constitution as governing constraints; classifies gaps as missing / partial / contradicts / unrequested with CRITICAL–LOW severity; "not a diff tool … no git, no branch comparison, no history"; must run after `implement`; reports `converged` (tasks.md byte-for-byte unchanged) or `tasks_appended`.
- New scripts `resolve-template.sh`, `setup-tasks.sh`; `check-prerequisites.sh --require-spec`; feature resolution via `SPECIFY_FEATURE_DIRECTORY` or `.specify/feature.json` (now gitignored).
- New workflows available as extensions: bug-assess (assess → fix → test), idea/feature assessment (intake → research → define → shape → decide).
- Doc drift to fix if the upgrade is kept: TechScreen `CLAUDE.md` still says 0.7.4 and omits `speckit-converge`.

## "Can it be used in production?" — the honest framing for the piece

Evidence FOR: four months / 26 features / 36 PRs on 0.7.x in a real internal project; a clean in-place upgrade across 25 releases and one breaking change (0.10.0's removed flags did not affect a skills-mode project); manifest-aware upgrades that refuse to clobber local edits; semver compatibility within the major. Evidence AGAINST a blanket claim: the maintainers themselves decline the traditional 1.0 stability handshake; converge's severity was noisy across runs (same evidence rated HIGH vs MEDIUM); converge never returned `converged` even on reviewed code. Proposed wording: "production-usable with an owner who reads the diff", not "stable".
