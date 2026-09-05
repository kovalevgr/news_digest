```yaml
platform: linkedin
chars: 1587         # plain text incl. link line + hashtags, take marker stripped
playbook_checklist: pass (owner's call: link position; 3 hashtags; the take is a proposal)
sources: pieces/coding-models-sept-2026-linkedin/sources/ (17 files; every number below traces to one of them)
```
Three frontier coding models shipped in three days. The rank on the leaderboard is the least useful number in any of the three announcements.

Sept 1: Claude Fable 5.1, $10 in / $50 out per million tokens, cache reads cut to $0.25.
Sept 2: Gemini 3.8 Flash, $0.75 / $3.75 (intro price until Dec 31).
Sept 3: GPT-6 Astra, $10 / $50.

That is a 13x spread in list price between models sitting within two points of each other on Terminal-Bench 2.1: 91.4 and 89.9 in Artificial Analysis' independent runs for Fable 5.1 and Astra, 89.4 self-reported for 3.8 Flash.

Three things now move the result more than the rank does.

Effort. Same Fable 5.1, same prompt: $0.01 at low effort, $3.30 at max, 24 seconds vs 14 minutes (Simon Willison's pelican test). On the same test, Astra at low effort beat every GPT-5.6 Sol setting for under 10 cents.

Harness. NVIDIA's AVO took Claude Opus 5 from 30% to a perfect 100 on ARC-AGI-3 without changing a single weight. Harness-Bench shows a 24-point spread for one model across harnesses.

Open weights. DeepSeek V4-Pro (MIT) reports 87.9 on Terminal-Bench 2.1, Ornith-1.5 86.1, Tencent Hy4 85.4. Self-reported, but a few points behind the closed leaders. And a 27B Qwen3.8 scores 73 while running at full context on a single RTX 5090.

[proposed take: Picking a coding model in September 2026 is picking a price tier, an effort default and a harness. The leaderboard rank is the entry ticket, not the decision.]

What decides it for you: cost per task, or the ceiling at max effort?

[link → first comment or keep here, owner's call]: https://artificialanalysis.ai/evaluations/terminalbench-v2-1

#LLM #AIAgents #Coding
