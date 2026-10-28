---
company: huggingface
title: "Build specialized multimodal models with LFM3"
url: https://huggingface.co/blog/LiquidAI/lfm3
date: 2026-10-27
found_via: rss (TIER-1)
---

Liquid AI releases LFM3, a new ~2B-parameter model family (text, vision, audio, omni, and decision variants) sharing one backbone, with new in-house vision/audio encoders and reported gains over the LFM2.5 generation across WebArena, 62 vision benchmarks, speech quality, and audio-visual video tasks; weights are open on Hugging Face.

## card

**Що сталося:** Liquid AI випускає LFM3 — нове поколінні Liquid Foundation Models (~2B параметрів кожна), що ставить текстову, візуальну, аудіо, omni- та decision-моделі на одну спільну основу (LFM3-1.7B-Base, 24 шари, контекст 256K).

**Контекст:** LFM3-VL-2B — перша vision-модель серії LFM, що приймає відео; LFM3-Omni-2B — перша omni-модель у родині; усі моделі відкриті та доступні на Hugging Face вже зараз, з ноутбуками для донавчання (SFT, DPO, GRPO, CPT) на одній GPU.

**Деталі:**
- LFM3-1.7B перевершує LFM2.5-2.6B із 35% меншою кількістю параметрів; на WebArena-Verified — 38.42 проти 3.02.
- LFM3-VL-2B: середній бал 71.4 на 62 vision-бенчмарках (проти 57.6 у LFM2.5-VL-3B); візуальний енкодер споживає втричі менше обчислень, ніж SigLIP2.
- LFM3-Audio-2B: 3.83 на UTMOSv2 (якість мовлення) проти 3.22 у LFM2.5-Audio-1.5B; новий аудіотокенізатор LiquidCodec підтримує потокове мовлення.
- d1-2B: 75.5 на ImajevBench проти 64.0 у d1-3B.
- LFM3-Omni-2B перевершує Qwen2.5-Omni-7B на кількох аудіо-візуальних відео-бенчмарках; ліцензію сторінка явно не вказує.
