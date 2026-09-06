---
kind: source
title: "Ornith-1.5-397B model card (Hugging Face, ornith-ai)"
url: https://huggingface.co/ornith-ai/Ornith-1.5-397B
fetched: 2026-09-05
note: WebFetch-verified 2026-09-05; family also has 35B-A3B and 9B; maker named as DeepReinforce only in secondary coverage
---

- 397B MoE (~800 GB bf16), MIT license, 262,144-token context; FP8 / NVFP4 / GGUF variants published.
- Trained with a self-improving RL loop that jointly optimises task generation, scaffold construction and solution rollouts.

| Benchmark | Ornith-1.5-397B | Claude Opus 4.8 | DeepSeek-V4-Flash | GLM-5.2 |
| --- | --- | --- | --- | --- |
| Terminal-Bench 2.1 (Terminus-2) | 86.1 | 85.0 | 82.7 | 81.0 |
| DeepSWE | 56.0 | 59.0 | 54.4 | 46.2 |
| SWE-bench Verified | 86.0 | 85.8 | 81.6 | 83.0 |
| GPQA Diamond | 92.8 | 93.6 | 91.4 | 91.2 |

Card's own claim: "on par with Claude Opus 4.8".
