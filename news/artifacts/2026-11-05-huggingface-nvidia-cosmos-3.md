---
company: huggingface
title: "New NVIDIA Cosmos 3 Open Models for Interactive World Simulation"
url: https://huggingface.co/blog/nvidia/cosmos-interactive-world-simulation
date: 2026-11-05
found_via: rss
---

NVIDIA releases four open-weight (16B-parameter) Cosmos 3 Nano post-trained checkpoints on Hugging Face — Transfer-Auto (offline multi-view driving data), Sim-Auto (streaming distilled version), Sim-Transfer (simulator-control-to-photorealistic video), and Sim-Bimanual (two-arm robot video prediction) — under the OpenMDW1.1 license, with post-training recipes for adapting to new sensors/embodiments.

## card

**Що сталося:** NVIDIA випустила на Hugging Face чотири нові відкриті (16B параметрів) чекпоінти Cosmos 3 Nano для інтерактивної симуляції світу: Transfer-Auto (офлайн мультивʼю дані для автономного водіння), Sim-Auto (стрімінгова дистильована версія), Sim-Transfer (перетворення керування симулятором на фотореалістичне відео), Sim-Bimanual (передбачення відео для двоrукої робото-симуляції).

**Контекст:** Усі чотири моделі — post-trained варіанти Cosmos 3 Nano; надаються рецепти для подальшого донавчання під нові сенсорні установки, середовища чи "тіла" роботів.

**Деталі:**
- 16B параметрів кожна (на картках HF вказано 15B); кожен латентний крок відповідає 4 RGB-кадрам.
- Transfer-Auto генерує до 11 синхронізованих ракурсів камер (включно з fisheye) + спільні RGB-LiDAR дані.
- Sim-Bimanual використовує 59 значень керування (доповнено до 64 під час тренування) для embodiment YAM та AgiBot.
- Ліцензія — OpenMDW1.1 (дозволяє комерційне й некомерційне використання); інференс потребує Linux, NVIDIA GPU, Docker; тестова конфігурація vLLM-Omni — одна GB200 (не мінімальна вимога).
