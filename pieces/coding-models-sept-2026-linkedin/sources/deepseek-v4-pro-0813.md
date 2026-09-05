---
kind: source
title: "DeepSeek-V4-Pro-0813 model card (Hugging Face)"
url: https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813
fetched: 2026-09-05
note: WebFetch-verified 2026-09-05; release 2026-08-13 (the "0813" suffix)
---

- 1.7T-parameter MoE, MIT license, million-token context, DSpark speculative decoding "enabled with a single flag".
- Code-agent evals run in "the minimal mode of DeepSeek Harness" (open-sourced as `deepseek-harness`, MIT) with reasoning effort low/high/max.

| Benchmark | V4-Pro-0813 | V4-Pro Preview |
| --- | --- | --- |
| Terminal-Bench 2.1 | 87.9 | 72.1 |
| DeepSWE | 62.7 | 12.8 |
| NL2Repo | 61.5 | 38.5 |
| Toolathlon-Verified | 74.1 | 55.9 |
| CyberGym | 83.3 | 52.7 |

API pricing not on the card (DeepSeek pricing page not fetchable in this env).
