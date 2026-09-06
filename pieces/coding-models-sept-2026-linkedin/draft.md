```yaml
platform: linkedin
chars: 1893          # plain text incl. hashtags; no links in the body (owner's call 2026-09-05)
playbook_checklist: pass — 0 links in body, 5 hashtags (owner's call, above the playbook's 0–3), take accepted by owner, carousel PDF to attach as a document post
first_comment_links:   # owner posts these as the first comment, by hand
  - Fable 5.1: https://www.anthropic.com/claude-fable-and-mythos-5-1
  - Gemini 3.8 Flash: https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/
  - GPT-6 Astra: https://openai.com/index/gpt-6-astra/
  - Terminal-Bench 2.1 independent runs: https://artificialanalysis.ai/evaluations/terminalbench-v2-1
  - Effort test: https://simonwillison.net/2026/Sep/1/claude-fable-5-1/
  - AVO: https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/
sources: pieces/coding-models-sept-2026-linkedin/sources/ (17 files; every number below traces to one of them)
```
Three coding model launches in three days. I read all of them. The leaderboard rank was the least useful number in every one.

If you ship code with an agent, here is the part that actually touches your bill.

Sept 1, Claude Fable 5.1: $10 in / $50 out per million tokens. Cache reads dropped to $0.25, which is the number that matters if your agent re-reads the same repo for hours.
Sept 2, Gemini 3.8 Flash: $0.75 / $3.75, and that intro price runs out on Dec 31.
Sept 3, GPT-6 Astra: $10 / $50.

Same job, 13x apart on price. On Terminal-Bench 2.1 they sit within two points of each other (91.4 and 89.9 in Artificial Analysis' own runs, 89.4 self-reported for Flash). So the rank tells you almost nothing. Three other dials do.

Dial 1: effort. Simon Willison ran one prompt through Fable 5.1 at every effort level: 1 cent and 24 seconds at low, $3.30 and 14 minutes at max. Same model. And Astra at its lowest setting beat every GPT-5.6 Sol setting on his test for under 10 cents. Your default effort level is now a line item.

Dial 2: the harness. NVIDIA's AVO wrapped Claude Opus 5 in a better agent loop and went from 30% to a perfect 100 on ARC-AGI-3. Not one weight changed. Harness-Bench shows a 24-point spread for a single model depending on who wrote the loop around it.

Dial 3: open weights. DeepSeek V4-Pro (MIT) reports 87.9 on the same Terminal-Bench, Ornith-1.5 86.1, Tencent Hy4 85.4. Vendor numbers, sure, but that is a few points, not a generation. And a 27B Qwen3.8 scores 73 on its own card and fits, at full context, on one RTX 5090 under your desk.

Choosing a coding model in September 2026 means choosing a price tier, an effort default and a harness. The leaderboard is the entry ticket. The decision happens on the other three.

Which of the three dials would you turn first: effort, harness, or going open?

[attach as a LinkedIn document post: assets/carousel.pdf, 6 slides 1080×1350 — hook / prices / effort chart / harness / open-weights chart / the decision. Rebuild with assets/carousel_build.py (headless Chrome). The two standalone charts stay in assets/ as fallback.]

#LLM #AIAgents #AIEngineering #LocalLLM #OpenSourceAI
