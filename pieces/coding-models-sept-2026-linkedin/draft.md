```yaml
platform: linkedin
chars: 1814 body + 556 sources block = 2370 (limit 3000; playbook range exceeded on purpose per owner: links + livelier tone)
playbook_checklist: needs owner call — 6 links in body (playbook default is 1; reach trade-off), length above the 900–1,600 range; 2 images to attach; 3 hashtags ok; no Markdown leaks
sources: pieces/coding-models-sept-2026-linkedin/sources/ (17 files; every number below traces to one of them)
```
I spent this week reading three frontier coding model launches back to back. If you ship code with an agent, here is the part that actually touches your bill, with the leaderboard rank left out on purpose.

Sept 1, Claude Fable 5.1: $10 in / $50 out per million tokens. Cache reads dropped to $0.25, which is the number that matters if your agent re-reads the same repo for hours.
Sept 2, Gemini 3.8 Flash: $0.75 / $3.75, and that intro price runs out on Dec 31.
Sept 3, GPT-6 Astra: $10 / $50.

Same job, 13x apart on price. On Terminal-Bench 2.1 they sit within two points of each other (91.4 and 89.9 in Artificial Analysis' own runs, 89.4 self-reported for Flash). So the rank tells you almost nothing. Three other dials do.

1. The effort dial. Simon Willison ran one prompt through Fable 5.1 at every effort level: 1 cent and 24 seconds at low, $3.30 and 14 minutes at max. Same model. And Astra at its lowest setting beat every GPT-5.6 Sol setting on his test for under 10 cents. Your default effort level is now a line item.

2. The harness. NVIDIA's AVO wrapped Claude Opus 5 in a better agent loop and went from 30% to a perfect 100 on ARC-AGI-3. Not one weight changed. Harness-Bench shows a 24-point spread for a single model depending on who wrote the loop around it.

3. Open weights. DeepSeek V4-Pro (MIT) reports 87.9 on the same Terminal-Bench, Ornith-1.5 86.1, Tencent Hy4 85.4. Vendor numbers, sure, but that is a few points, not a generation. And a 27B Qwen3.8 does 73 while running at full context on one RTX 5090 under your desk.

[proposed take: Choosing a coding model in September 2026 means choosing a price tier, an effort default and a harness. The leaderboard is the entry ticket. The decision happens on the other three.]

Which of the three dials would you turn first: effort, harness, or going open?

[image 1: chart, Terminal-Bench 2.1 scores, open vs closed weights, independent runs hatched, list price on the closed models. File: assets/01-terminal-bench-open-vs-closed.png]
[image 2: chart, Fable 5.1 cost per run at five effort levels on a log scale, 330x spread. File: assets/02-effort-cost-fable-5-1.png]

Sources [owner's call: keep here, or move to the first comment for reach]
Fable 5.1: anthropic.com/claude-fable-and-mythos-5-1
Gemini 3.8 Flash: blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/
GPT-6 Astra: openai.com/index/gpt-6-astra/
Independent Terminal-Bench 2.1 runs: artificialanalysis.ai/evaluations/terminalbench-v2-1
Effort test: simonwillison.net/2026/Sep/1/claude-fable-5-1/
AVO: developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/

#LLM #AIAgents #Coding
