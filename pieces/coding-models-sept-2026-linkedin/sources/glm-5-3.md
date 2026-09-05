---
kind: source
title: "GLM-5.3 model card (Hugging Face, zai-org) + Interconnects analysis"
url: https://huggingface.co/zai-org/GLM-5.3
url2: https://www.interconnects.ai/p/glm-53-how-chinese-labs-keep-stride
fetched: 2026-09-05
note: both WebFetch-verified 2026-09-05; announced 2026-08-14, open weights ~2 weeks later
---

- 753B MoE, same base as GLM-5.2 — "every gain comes from post-training" / Z.ai: "Scaling post-training is all we did for GLM-5.3". Text-only. License: GLM-5.3 (custom).

| Benchmark | GLM-5.3 | GLM-5.2 | Kimi K3 | Opus 4.8 | GPT-5.6 Sol |
| --- | --- | --- | --- | --- | --- |
| Terminal-Bench 3.0 | 28.3 | 4.6 | 17.4 | 85.0* | 34.6 |
| DeepSWE v1.1 | 66.9 | 46.2 | 67.5 | 58.0 | 72.7 |
| CyberGym | 84.5 | 77.2 | 80.0 | 78.1 | 83.6 |
| FrontierSWE | 78.1 | 67.5 | — | 66.5 | 88.2 |

\* the Opus 4.8 Terminal-Bench figure in the card's row is almost certainly a 2.1 number mixed into a 3.0 column [owner to check before quoting].

Interconnects (Nathan Lambert): GLM-5.3 beats Kimi K3 despite being ~a third its size on post-training execution, not distillation ("One does not simply 'distill' RL environments, infrastructure to run them at scale, or algorithms"); Z.ai's time-to-release is "days, not months".
