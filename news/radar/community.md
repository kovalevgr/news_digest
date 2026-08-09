---
category: community
updated: 2026-08-09
---

# Radar: community

Technical-radar items for this category (sources in [`config/radar.json`](../config/radar.json)).
Appended by the daily routine under weekly headings; format matches topics files.

## 2026-W32

- **2026-08-09** — [ds4 flash 0731 UD-IQ2_M wrote a custom Metal kernel for Kimi K2 IQ1_0 in about 50 minutes](https://www.reddit.com/r/LocalLLaMA/comments/1vje00y/ds4_flash_0731_udiq2_m_wrote_a_custom_metal/) — A local DeepSeek-4 Flash agent autonomously wrote a custom Metal kernel for a Kimi K2 IQ1_0 quant on a Mac Studio in ~50 minutes; modest throughput (~4 t/s decode, ~20 t/s prefill) but no pre-existing kernel was available.
- **2026-08-08** — [Kimi K3 (Unsloth) IQ2-XXS from 711GB down to 478GB](https://www.reddit.com/r/LocalLLaMA/comments/1vjanps/kimi_k3_unsloth_iq2xxs_from_711gb_down_to_478gb/) — Unsloth shrank a Kimi K3 IQ2-XXS quant from 711GB to 478GB by stripping multilingual weights while keeping English-language capability intact.
- **2026-08-09** — [No wonder Qwen and Gemma are so different](https://www.reddit.com/r/LocalLLaMA/comments/1vjb15v/no_wonder_qwen_and_gemma_are_so_different/) — Side-by-side tokenization of the same 330-line code snippet: Qwen 35B A3B tokenized to 1609 tokens vs Gemma 26B A4B to 4258 tokens, offered as a partial explanation for Qwen's coding edge over Gemma.
- **2026-08-09** — [google/skills](https://github.com/google/skills) — Google published an official Agent Skills repo for Google Cloud products/technologies, installable via `npx skills add google/skills`, letting agents pull in Cloud-specific skills on demand.
- **2026-08-09** — [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) — Multi-agent LLM trading framework shipped v0.3.1 with graph-router crash-safety, checkpoint-aware resume, a configurable LLM retry budget, and Claude Sonnet 5/Fable 5 support — orchestration patterns of interest beyond the finance use case.
