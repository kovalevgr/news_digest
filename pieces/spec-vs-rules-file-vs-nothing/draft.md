Title: One feature, three ways: a full spec, a rules file, or nothing
Subtitle: Same commit, same implementer model, same blind reviewer. The only thing that changed was how my intent reached the agent. The post-review diff went +128, +239, +513.

There is a debate running through coding-agent land about how much process to put in front of the model. GitHub Spec Kit hit 1.0 in August with a full spec → plan → tasks → implement → converge pipeline ([release notes](https://github.com/github/spec-kit/releases/tag/v1.0.0)). Fabien Sanglard argued the opposite corner the same week: one terse `agent.md` of standing rules, loaded at session start, and stop repeating yourself ([his post](https://fabiensanglard.net/agent.md/index.html)). And plenty of people ship with neither, just a project file and a prompt.

I have been on Spec Kit for four months in an internal AI interview system, 26 features through the full flow. I wanted to know what the process actually buys on a feature that does not obviously need it. So I built the same feature three times.

## The setup

**The feature.** T24, a Pre-Interview Planner agent wrapper: a thin typed adapter around our single `call_model` boundary, in the same shape as two existing sibling wrappers (Interviewer, 256 lines; Assessor, 399). The prompt and output schema were already committed. No database, no cloud, runs offline against a mock backend. About the size of an early Tier-1 feature whose spec was 79 lines. It has genuine forks the task text leaves open: retry policy, how much semantic validation the wrapper does against the rubric, version lockstep, whether to append another agent's level guide.

**The fairness rules.** One base commit. Three git worktrees; no arm can see another. One implementer model, Opus, in all three. One feature prompt, byte-identical across arms, ending with the same five gates: `pytest`, `ruff check`, `ruff format --check`, `mypy --strict`, a provider-SDK import guard. Then one blind reviewer per arm, on our usual reviewer model, given the worktree as "candidate X / Y / Z", told to review only the `app/` diff and never to read `specs/`, `agent.md` or the git log. Then one fix-round per arm by a fresh implementer agent with the reviewer report.

**The three arms.**

- **A. Spec Kit 1.0.4.** I answered the questions: `specify` asked two, `clarify` asked three. The "brain" (the session model, which owns all design artifacts on this project) wrote spec, plan, research, data model, quickstart and 18 tasks, 488 lines across seven files. Then `implement`, then `converge`.
- **B. A rules file.** One `agent.md` of 43 lines, written in Sanglard's spirit from our coding conventions and constitution: the floor (LLMs never route, every call through `call_model`, hard caps), the shape of an agent wrapper (frozen pydantic models mirroring the schema, deterministic payload serialisation, "retry ONCE on a schema-class failure, then raise"), Python rules, test rules, process rules. The prompt said: read this first, follow it, do not touch Spec Kit.
- **C. Nothing.** The prompt and the project's CLAUDE.md, which every arm loads anyway.

One thing I chose not to hide: in arms A and B the brain wrote the spec and the rules file. The implementer is the constant; what differs is the form in which the brain's intent reaches it.

## The scorecard

| | A, Spec Kit | B, `agent.md` | C, nothing |
| --- | --- | --- | --- |
| Reviewer verdict | warnings | warnings | warnings |
| Blocks / warnings / notes | 0 / 2 / 10 | 0 / 2 / 6 | 0 / 2 / 10 |
| Lines changed after review | **+128 / −21** | **+239 / −10** | **+513 / −29** |
| Tests at first green → after fix | 38 → 42 | 52 → 58 | 39 → 49 |
| Implementer tokens, build + fix | 279k | 283k | 287k |
| Process artifacts | 488 lines, 7 files | 43 lines, 1 file | 0 |
| Wall clock, start → post-review green | 43 min 41 s | 36 min 6 s | 36 min 50 s |
| Converge | Converged, 0 findings | n/a | n/a |

Three things jump out of that table, and one of them is not in it.

## All three reached mergeable code

Zero blocks anywhere. And each of the three blind reviewers raised exactly two warnings, on the same two topics: whether the wrapper's retry policy matches the one documented in our integration guide, and how many of the prompt's semantic guardrails (required competencies covered, no invented rubric node ids, no seed question above the target level plus one) the wrapper enforces itself rather than deferring to the caller.

That deserves a pause. The reviewer gate, not the process, is what equalised the arms. Whatever each arm got wrong up front, the same reader caught it in the same place. If your project has a serious review step, the choice between spec and no spec is not a choice between correct and incorrect code. It is a choice about when decisions get made and how much churn follows.

## The decisions moved, they did not disappear

The post-review diff is the tell: +128, +239, +513. That order is exactly the order in which design decisions were made before code.

Arm A made five of them before a line was written, because I answered five questions. Arm B carried three of them in the rules file. Arm C made none up front and discovered one on its own.

And arm B is the most instructive one, because its rules file was wrong for this agent. `agent.md` said "retry ONCE on a schema-class failure", which is what both sibling wrappers do. Our own integration guide says the Planner specifically should "retry up to twice; on repeated failure, fall back to the previous rubric version's default plan template". The implementer obeyed the file. The blind reviewer flagged it. The fix-round agent kept retry-once and defended it, coherently: the documented fallback needs stored state a pure wrapper cannot own, and spending a third call on the same missed contract breaks the shape every wrapper shares. A defensible position, reached by following a rule I had written without checking it against the doc.

Arm C, with no rules to obey, went and read the integration guide and shipped three attempts. Arm A shipped three attempts because `clarify` had asked me and I picked the documented policy. Same answer, three different routes, and only one of them involved me before the code existed.

A rules file carries rules. It does not carry per-feature decisions. When it tries to, it can encode a mistake as faithfully as it encodes a principle, and a good implementer will execute the mistake.

## The one thing only Spec Kit did

`clarify` surfaced a contradiction inside my own repo, siblings retry once versus the guide saying the Planner retries twice, as a question for me to answer. That is the whole value of the round: five decisions made by the person who owns the design, before anyone paid tokens for code, recorded in the spec's Clarifications section where the next person can find them.

An honest footnote from the results log. The spec author noticed the contradiction only after arm C's implementer report cited the guide. Without the parallel arms, the clarify round might well have shipped "retry once" as a functional requirement. The process gave me the venue for the decision; it did not guarantee I would see the fork.

Converge, run on arm A after implement, returned "Converged" with zero findings: 28 requirements checked, 11 plan decisions, 8 applicable constitution principles, nothing missing. It was the first clean converge result across both stages of this experiment, and it came in the one case the tool is built for: the spec preceded the code and the code was written to it. (Stage 1, where I pointed converge at code I had already thrown away, is its own post [owner: link].)

## What it cost

Implementer tokens were flat: roughly 280k per arm including the fix round. Spec Kit's extra cost was my attention, about 23 minutes of wall clock across the specify and clarify questions and the brain's authoring, plus 146k tokens for converge. The rules file cost 43 lines once and nothing per feature. Arms B and C finished in 36 minutes to A's 44.

Two leaks in the blind review, for the record: reviewer X ran an unfiltered `git diff --name-status` and saw that a root `agent.md` existed (it says it did not read it); reviewer Z inferred a spec from FR and SC ids in test names. Neither named the process, and none of the three reports reads as biased.

## Where the threshold is

My own note, written right after the runs: for a feature this size I would merge any of the three after review. Spec Kit paid for itself not in code quality but by making me answer five questions before anyone wrote a line, and one of them turned out to be a contradiction in my own docs. `agent.md` carries rules, not per-feature decisions. The threshold as I see it now: a spec is needed where there are forks the reviewer will not see in the diff.

[proposed take: The usual framing, process versus speed, is the wrong axis. All three arms were fast and all three were correct after review. The real axis is who makes the design calls and when. A full spec puts them with the owner, before code. A rules file puts them with whoever wrote the rules, possibly months ago and for a different agent. Nothing puts them with the implementer, who will make them well and tell you afterwards. Pick by how expensive it is to discover a wrong call at review time, not by how heavy the process feels.]

The stack this ran on matters for reading the numbers. Design and code are separated here by model tier, not just by document: the most capable model in the loop writes every spec, contract and rules file and never writes features; Opus implements from a finished design and records gaps rather than redesigning; the cheapest tier runs gates; a read-only reviewer on the top model sits on top; a human merges. Under that policy the implementer has one quality criterion, "filled the gap" or "quietly redesigned", and that is what the reviewer reads for. Stage 2 is really a measurement of how much of the brain's intent survives the trip to the implementer in each container. Most of it survived in all three. The spec just kept me in the room for the part that mattered.

[owner: the full results write-up (three implementer reports, three blind reviewer reports, three fix-round reports, verbatim) is in the project repo. Same decision as the stage-1 post: gist and link, or keep private.]
