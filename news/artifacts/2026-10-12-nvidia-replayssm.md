---
company: NVIDIA
title: "ReplaySSM: Rethinking State Storage for Faster Hybrid-Model Decoding"
url: https://developer.nvidia.com/blog/replayssm-rethinking-state-storage-for-faster-hybrid-model-decoding/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-10-12
fetched: 2026-10-13
---

NVIDIA and the Dao AI Lab (Princeton) introduce ReplaySSM, a state-storage technique for hybrid SSM/attention models that stores a checkpoint plus a buffer of recent inputs instead of rewriting full state every decode step, integrated into TensorRT-LLM, vLLM, and FlashInfer.

## card

**Що сталося:** NVIDIA та Dao AI Lab (Прінстон) представляють ReplaySSM — техніку зберігання стану для декодування гібридних моделей (SSM-шари + кілька attention-шарів), яка замість повного перезапису стану на кожному кроці зберігає чекпоінт плюс буфер останніх входів; інтегровано в TensorRT-LLM, vLLM та FlashInfer.

**Контекст:** На серверних batch size SSM-шари стають вузьким місцем через трафік пам'яті на запис/читання повного стану, дорогий rollback при спекулятивному декодуванні та накопичення похибки квантування в рекурентному стані; ReplaySSM вирішує всі три проблеми одним механізмом checkpoint+buffer (L=16 кроків у роботі).

**Деталі:**
- Швидкість ядер на B300 (batch 256): прискорення кернелів 1.46–1.80x, end-to-end декодування 1.20–1.47x на чотирьох моделях (без прискорення при batch 1)
- Спекулятивне декодування (T=4, batch 512, дві моделі класу 120B): пропускна здатність 1.85x і 2.10x проти vLLM при однаковій довжині прийняття
- Верифікація: при T=8 vLLM витрачає майже 5x часу звичайного кроку декодування, тоді як ReplaySSM верифікує 8 токенів приблизно за час одного кроку
- NVFP4-читання на Mamba-2: у 3.8x швидше за FP32; на Qwen3.5-4B (128K контексту) NVFP4-читання з FP32-рекурсією знизило KL-розбіжність з 0.136 до 0.0038 проти FP32-декодування
- Точність на GPQA-Diamond: спільний NVFP4-чекпоінт втрачає 3.2–31.3 пункту; NVFP4-читання з FP16+SR рекурсією тримає три з чотирьох моделей у межах ~2 пунктів від FP32 (виняток — Nemotron-3-Nano-4B, −6.7)
