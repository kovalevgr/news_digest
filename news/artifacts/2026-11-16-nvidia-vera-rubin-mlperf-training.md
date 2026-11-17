---
company: nvidia
title: "NVIDIA Vera Rubin NVL72 Achieves up to 2x Blackwell Ultra Performance in MLPerf Training v6.1"
url: https://developer.nvidia.com/blog/nvidia-vera-rubin-nvl72-achieves-up-to-2x-blackwell-ultra-performance-in-mlperf-training-v6-1/
date: 2026-11-16
found_via: rss (developer.nvidia.com/blog/feed)
---

NVIDIA's Vera Rubin NVL72 debuts in MLPerf Training v6.1, posting the fastest time-to-train on six of seven benchmarks and up to 2x per-GPU performance versus an optimized GB300 NVL72 (Blackwell Ultra) baseline, led by a ~2x gain on DeepSeek-V3 671B.

## card

**Що сталося:** NVIDIA Vera Rubin NVL72 дебютувала в MLPerf Training v6.1, показавши найшвидший час тренування на 6 з 7 бенчмарків і вдвічі вищу продуктивність на GPU порівняно з оптимізованим базлайном GB300 NVL72 (Blackwell Ultra).

**Контекст:** Результати отримані від MLCommons 16 листопада 2026; GB300 NVL72 все ж показала найшвидший абсолютний час на DeepSeek-V3 (1,38 хв на 10 240 GPU) цього раунду, тоді як Vera Rubin масштабувалась з 256 до 1024 GPU з ефективністю понад 97%.

**Деталі:**
- DeepSeek-V3 671B (1024 GPU): 4,14 хв проти 8,03 хв у GB300 — приблизно 2x, найбільший виграш раунду.
- Llama 3.1 8B (72 GPU) та gpt-oss 20B (64 GPU): 1,6x; Llama 2 70B LoRA та FLUX.1 (72 GPU кожен): 1,5x.
- Qwen3.5 397B GRPO reinforcement learning (1024 GPU): 10,44 хв проти 13,78 хв — ~1,4x; результат надіслано на обох інференс-бекендах TensorRT-LLM і vLLM.
- Апаратно: стійка Vera Rubin NVL72 — 72 GPU і 36 CPU, з'єднані міддю NVLink 6 (3,6 ТБ/с на GPU); мережа масштабування через ConnectX-9 SuperNIC (Quantum-X800 InfiniBand або Spectrum-X Ethernet); CPU Vera обробляють симуляції RL-середовищ.
