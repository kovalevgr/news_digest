Title: I pointed Spec Kit 1.0's new "converge" step at code I had already thrown away
Subtitle: Four months of spec-driven development with coding agents, one rolled-back implementation, and a five-minute review that nobody had asked for.

On August 21 GitHub shipped Spec Kit 1.0 ([release notes](https://github.com/github/spec-kit/releases/tag/v1.0.0)). Most of the release is plumbing: an extension system, presets, a proper upgrade command. One thing is genuinely new in the workflow: a step called `converge` that runs after `implement` and checks the code against the spec, the plan and the task list, then appends whatever is missing as new tasks.

I had a perfect thing to point it at. A month earlier I had rolled back an implementation of the hardest module in a project I run, an internal AI interview system, because the sub-agent that wrote it declared 13 deviations from the design in its own completion report. Nobody ever reviewed that code. I read the report, decided an implementer should not be making 13 design decisions, and threw the round away.

So the question was simple. If I hand converge the code I rejected, does it find what the implementer confessed to? Does it find anything the implementer did not confess to? And what does it say about the code that eventually shipped?

## Four months on Spec Kit, in numbers

Some context first, because the answer depends on how the specs were written.

The project started in mid-April. The day before the first commit I wrote an ADR choosing GitHub Spec Kit over two alternatives: informal English in PRs, or a custom in-house spec format. The reasoning line in that ADR still holds: "Without a disciplined spec-first workflow, AI assistance produces fast-but-wrong code that costs more to revert than to write by hand."

What that looked like by early August:

| | |
| --- | --- |
| Commits / merged PRs | 225 / 36 |
| Features that went through the full spec → plan → tasks → implement flow | 26 |
| Application code (Python, TypeScript) | 28,794 lines |
| Spec artifacts (specs + contracts) | 20,495 lines |
| Reviewer-gate fix rounds (`fix(...): reviewer findings` commits) | 13 |

That is 0.71 lines of specification per line of code. It sounds absurd until you see how it moved. The first 19 features carried the full Spec Kit kit: spec, plan, tasks, research notes, data model, quickstart, checklists, contracts, between 340 and 1,897 lines each. The last eight features carried spec, plan and tasks only, between 56 and 216 lines each. The ceremony shrank by roughly an order of magnitude once the project had a constitution (20 invariants), 24 ADRs and a set of committed contracts to point at. The spec stopped restating the design and started referencing it.

The other thing that changed was who writes the spec. That is the rollback story.

## The rollback

The module in question is the interview orchestrator: a deterministic state machine that decides what happens next in a session while the LLMs only produce content. It is the biggest logic surface in the codebase, 21 named transition edges, an adjudication table, persistence with schema versioning. One of the project's invariants is "no LLM-driven flow control", so this module is where that invariant lives or dies.

The first implementation was done by a Sonnet sub-agent working from a contract and a spec. It ran for 58 minutes, used 196 tool calls and about 360k tokens, and came back with a completion report that included a section titled "Deviations, each with one-line rationale". Thirteen of them. Things like "`awaiting` promoted to a top-level field instead of nested" and "edges 10/12 issue one `ask_seed` call with the transition folded into a context note".

Some of those were good ideas. Eight of the thirteen were later folded into the contract as accepted refinements. But I rolled the whole round back that night, on process grounds, without a review: an implementer that has to make 13 design calls is working from a spec that was not finished, and letting it redesign on the fly is how you lose conceptual integrity one clever shortcut at a time. Simon Willison [made the same point](https://simonwillison.net/2026/Aug/19/conceptual-integrity-and-counting-lines-of-code/) a few weeks later: when agents make features cheap, the bottleneck moves to whether the codebase still fits together in one head.

To be precise about what failed: not the model, the tier. Until the day before, background agents had silently inherited the session model and burned through limits three or four times a day, so I had just moved implementation to a cheaper tier and let the same agent author its own spec. That policy lived less than a day. The mistake was letting the implementing tier make design decisions at all.

The fix was a policy, not a prompt. The stack has three tiers by role now. The main session, the "brain", writes every spec, plan, tasks file and contract itself, adjudicates review findings and never writes features. Four implementer sub-agents on Opus receive a finished design and translate it into code; open questions go into the spec's Clarifications section as "gap filled this way", never into a redesign. The cheapest tier runs tests, gates and one-line fixes. A read-only reviewer gate runs on the session model, because it catches the most expensive mistakes at a third to a half of implementation cost. Merge is always a human. The Opus re-implementation of the orchestrator under that policy shipped with zero contract deviations and 26 gap-fill notes, went through the reviewer gate (one real bug, four contract-text corrections), and merged.

The rejected round stayed in git as dangling commits. A month later it became a test fixture.

## The upgrade: 25 releases, 3 seconds

The project was on Spec Kit 0.7.4, initialised in April. Between that and 1.0.4, released at the start of September, there were about 25 releases and one breaking change (0.10.0 removed the legacy `--ai*` flags; we were already in skills mode, so it did not touch us). The full timeline is in the [changelog](https://raw.githubusercontent.com/github/spec-kit/main/CHANGELOG.md).

The 1.0 upgrade path is a real command now: `specify integration upgrade claude`, then `specify extension update`. It is manifest-aware: it refuses to overwrite a managed file you have edited locally unless you pass `--force`, and it never touches `specs/`, the constitution or git history ([upgrade docs](https://github.com/github/spec-kit/blob/main/docs/upgrade.md)).

On our repo: 3 seconds of CLI time, 27 files modified and 4 added, +1,530/−706 lines. Fourteen skill definitions rewritten (`specify` grew by 140 lines, `clarify` by 102, `implement` by 118), a new `speckit-converge` skill of 279 lines, refreshed scripts and templates. Nothing broke. Our skills-not-slash-commands setup survived. The only follow-up was a doc drift in our own CLAUDE.md, which still said 0.7.4.

Worth reading before you call this "stable": the 1.0 release notes explicitly decline the traditional promise. In the maintainers' words, "The old 1.0.0 was a handshake: rely on the shape, I will warn you before I change it. Ours is more of a wave: here is a good place to start; if I move something, your agent will follow it faster than a changelog could describe it." What they do promise is compatibility within a major version and an upgrade that will not clobber your edits. After four months and 26 features on 0.7.x plus a clean jump across 25 releases, I would call it production-usable, with the qualifier that the owner reads the upgrade diff.

## What converge actually is

The skill file is worth reading in full, but the operating constraints are the point. Converge reads `spec.md`, `plan.md` and `tasks.md` as "the sole source of intent", with the constitution as governing constraints. It inspects the current code, classifies every gap as missing, partial, contradicts or unrequested, assigns a severity from CRITICAL to LOW, and then does exactly one write: it appends a `## Phase N: Convergence` section to `tasks.md`. It never edits code, never edits the spec, never renumbers a task. It is explicitly "not a diff tool": no git, no branch comparison, no history. If nothing is wrong it leaves `tasks.md` byte-for-byte unchanged and reports "Converged".

In other words it is a reviewer that works from the spec side rather than the code side. Our existing reviewer gate reads a diff and asks "is this code right?". Converge reads the artifacts and asks "did you build what you said you would?".

## The experiment

Three git worktrees off the upgraded commit, each with the same orchestrator spec, plan and tasks:

| Run | Code | Contract |
| --- | --- | --- |
| C, control | the final implementation, as merged | v1.2 (current) |
| D | the rolled-back Sonnet attempt | v1.2 (current) |
| D′ | the rolled-back Sonnet attempt | v1.0, the text the attempt was actually written against |

Each run was one background sub-agent on the same model we use for the reviewer gate, told to execute the converge skill verbatim, present state only, no tests, no git. One interpretation note was given to all three: our spec says the contract is normative and does not restate it, so the contract counts as intent by reference. Without that note converge would have had a 12-line requirements list to check 1,175 lines of state machine against.

All three ran in parallel and finished in about five and a half minutes.

## What it found

**On the shipped code: one LOW finding.** Two docstrings still cited contract v1.1 instead of v1.2. Zero contract gaps, zero plan gaps, zero constitution violations across the 12 principles that applied. It independently re-verified both fixes from the human reviewer round as present. It also recorded two observations it deliberately did not turn into tasks: a threshold the contract mentions but never defines, and a resume path that never re-issues a lost assessment command. Neither had come up in review. Both are questions for the contract owner, which is me.

**On the rejected code: 15 findings.** Four HIGH, five MEDIUM, six LOW.

Here is the part I did not expect. Of the 13 deviations the implementer declared, only three are still deviations against the design as it stands today, because I had accepted the other eight into the contract. Converge found all three: the invented `ask_seed` vocabulary for competency transitions, the single-seed loop, and the missing immediate path out of the CLOSE phase. Two of them HIGH, one MEDIUM. On the ten items I had accepted or made moot, it produced zero findings. It did not re-litigate a single folded-in refinement, because the spec now states them.

Then it kept going. Seven substantive findings were things the implementer had not declared at all: a stale-reply race (the same one the human reviewer later caught on the rewrite), an abort hook that could never fire, an adjudication test matrix the report had called "full" that was not, a boundary condition on the candidate timeout, a state shape that was half-migrated, a missing session-level flag, and an untabulated command on one edge. Converge disproved the "full matrix" claim by reading the tests.

Across 31 finding rows in three runs I scored zero false positives. Six rows were style-only (naming, a constant, a wrapper shape).

**The D′ run taught me the most important thing about the tool.** I reverted the contract to v1.0, the text the Sonnet agent had actually been given, expecting the eight folded-in refinements to reappear as deviations. They did not. Converge noticed that the spec cited contract sections that no longer existed, ranked the spec above the contract, and filed one HIGH finding that the contract file was stale. Which was exactly true of that worktree. Thirteen of its fifteen findings were the same as run D.

So converge validates against the artifacts as they stand, not against the artifacts the implementer was given. Four of the fifteen findings in run D cite implementation notes that were written after the attempt, during the rewrite. Converge was, in effect, reading the answer key. None of those four was wrong about the code, but they measure "is this the merged design?" rather than "did this violate the design it had?". If you want the second question answered, you have to freeze the artifacts at the moment of implementation.

## What it cost

| Run | Findings | Tokens | Wall clock |
| --- | --- | --- | --- |
| C, control | 1 | 202,741 | 5 min 18 s |
| D, attempt | 15 | 172,268 | 4 min 41 s |
| D′, attempt on v1.0 | 15 | 179,161 | 5 min 25 s |

For scale, the Sonnet implementation run that produced the rejected code used about 360k tokens over 58 minutes. One converge pass is roughly half the tokens of an implementation pass and a tenth of the wall clock. The whole stage, including the archaeology of digging the attempt out of dangling commits and the deviation list out of a session transcript, took 75 minutes.

Two calibration notes. Severity is noisy across runs: the same purity-guard evidence was HIGH in one run and MEDIUM in the other. And converge never returned "Converged", not even on reviewed code; a stale docstring counts as a partial gap. Expect a small Phase N appended on almost every run.

## What I take from it

My honest one-line verdict, written right after reading the results: the upgrade changed nothing in day-to-day work, and converge did, in five minutes, the review the rolled-back attempt never got, and found seven bugs the implementer had not declared.

The thing to internalise is not "converge is a good reviewer". It is that converge is exactly as good as the spec it reads. On this project the specs are written by the strongest model in the loop, after a rollback taught us not to let implementers design. Feed converge a thin spec and it will have nothing to check against; feed it a spec written after the fact and it will grade against the answer key. The tool did not make our process better. Our process made the tool useful.

Converge stays on. It goes after `implement` and before the reviewer gate, as a cheap first pass that reads from the other side of the contract.

## What's next

This answers a narrow question: is the new step worth running? It does not answer the one I actually care about, which is where the threshold sits between a heavy spec process, a standing rules file in the spirit of Fabien Sanglard's [agent.md](https://fabiensanglard.net/agent.md/index.html), and nothing at all. Stage 2 built one small feature three ways, from the same commit, with the same model and a blind reviewer. That is the next post: "One feature, three ways: a full spec, a rules file, or nothing".
