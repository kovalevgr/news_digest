---
kind: source
title: "Introducing Claude Fable 5.1 and Claude Mythos 5.1 (official) + What's new in Claude Fable 5.1 (platform docs)"
url: https://www.anthropic.com/claude-fable-and-mythos-5-1
url2: https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1
fetched: 2026-09-05
note: WebFetch-verified 2026-09-05
---

Released 2026-09-01. Fable 5.1 GA on Claude API, AWS Bedrock, Google Cloud, Microsoft Foundry (model id `claude-fable-5-1`). Mythos 5.1 = same underlying model, Project Glasswing participants only.

## Benchmarks (max effort)
- Terminal-Bench 4.0 (agentic coding): Fable 5.1 55.8%, Mythos 5.1 60.9%, Fable 5 42.0%, Opus 5 52.3%, GPT-5.6 Sol 37.3%
- Terminal-Bench-Science 0.1: Fable 5.1 52.6%, Fable 5 24.7%, Opus 5 29.0%, GPT-5.6 Sol 22.4%
- CursorBench 3.2.0: Fable 5.1 73.4%, Fable 5 70.5%, Opus 5 70.0%, GPT-5.6 Sol 67.2%
- Humanity's Last Exam: 60.9% no tools / 65.0% with tools (Fable 5: 57.8 / 63.8)

## Pricing (USD per MTok)
- Input $10, output $50 (same as Fable 5); cache reads $0.25 (0.025× base; other Claude models 0.1×); 5m cache write $12.50, 1h $20; batch $5 / $25.
- "For typical workloads, costs are reduced by around 25% relative to Fable 5. For complex coding and highly agentic tasks, the savings could be up to around 45%."

## Specs (platform docs)
- 1M token context (default and max), 128k max output; adaptive thinking always on; `effort` parameter controls depth, default `high`; per-message effort change mid-conversation (beta) without invalidating the prompt cache.
- Breaking: forced tool use unsupported; thinking blocks bound to the model; editing earlier turns invalidates thinking blocks.
- Behaviour changes vs Fable 5: parallel tool calling more variable (may issue one tool call per turn), fewer progress updates, answers from memory more at `low` effort, whole-file rewrites for small edits more likely.
- Tokenizer same as Fable 5; vs models older than Opus 4.7 the same text produces ~30% more tokens.
- Text output carries Anthropic's statistical watermark.
