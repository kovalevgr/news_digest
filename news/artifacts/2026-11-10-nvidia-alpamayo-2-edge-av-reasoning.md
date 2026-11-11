---
company: nvidia
title: "Running AV Reasoning Models Within Onboard Compute and Latency Limits"
url: https://developer.nvidia.com/blog/running-av-reasoning-models-within-onboard-compute-and-latency-limits/
date: 2026-11-10
found_via: rss
---

NVIDIA introduces Alpamayo 2 Edge, a 2B-parameter vision-language-action reasoning model for autonomous vehicles built on Cosmos 3 Edge, plus AlpaJudge, its evaluation/reward model, with deployment guidance for NVIDIA DRIVE AGX Thor.

## card

**Що сталося:** NVIDIA представила Alpamayo 2 Edge — компактну 2B-параметричну VLA reasoning-модель для автономних авто на базі Cosmos 3 Edge — та AlpaJudge, інструмент для оцінки якості її reasoning, разом з гайдом розгортання на NVIDIA DRIVE AGX Thor.

**Контекст:** Частина відкритої платформи NVIDIA Alpamayo для reasoning-based автономного водіння; модель і чекпоінти AlpaJudge опубліковані на Hugging Face, код і рецепти — на GitHub (NVlabs).

**Деталі:**
- Closed-loop RL (AlpaGym) покращив керування на 48.9% проти найкращого чекпоінта без closed-loop RL.
- Проти Qwen-Drive-1.0 (4B): 15.15 проти 0.25 км між інцидентами з вини моделі в AlpaSim (~60x); open-loop minADE 0.53м проти 1.68м.
- Latency "pixel-to-trajectory" на DRIVE AGX Thor-X: 160–190 мс залежно від обсягу reasoning; потрібні FP8-калібрування, ONNX-експорт, TensorRT та DFlash2 speculative decoding.
- Партнери: PORT (вдвічі швидше планування за Alpamayo 1.5), Niulinx (−13.6% minADE після fine-tuning −44.2%), Embedl (10 Гц реального часу на AGX Thor за 48 годин).
