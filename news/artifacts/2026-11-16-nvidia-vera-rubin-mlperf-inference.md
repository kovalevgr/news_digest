---
company: nvidia
title: "NVIDIA Vera Rubin NVL72 Leads Agentic Inference Performance on MLPerf Endpoints v1.0"
url: https://developer.nvidia.com/blog/nvidia-vera-rubin-nvl72-leads-agentic-inference-performance-on-mlperf-endpoints-v1-0/
date: 2026-11-16
found_via: rss (developer.nvidia.com/blog/feed)
---

NVIDIA reports provisional MLPerf Endpoints v1.0 results showing its Vera Rubin NVL72 system delivers over 10x the throughput-per-kilowatt of its GB300 NVL72 system at matched interactivity, across Kimi K3, DeepSeek-V4.1-Flash, and Qwen3.6-35B-A3B.

## card

**Що сталося:** NVIDIA опублікувала попередні (ще не верифіковані MLCommons) результати MLPerf Endpoints v1.0: система Vera Rubin NVL72 показує понад 10x пропускну здатність на кіловат порівняно з GB300 NVL72 за однакової мінімальної інтерактивності 50 токенів/с на користувача.

**Контекст:** Порівняння проведено на трьох моделях (Kimi K3, DeepSeek-V4.1-Flash, Qwen3.6-35B-A3B) у стандартизованому дивізіоні категорії Available; результати GB300 верифіковані, результати Vera Rubin очікують верифікації MLCommons.

**Деталі:**
- Пропускна здатність на кВт відносно GB300 NVL72: Kimi K3 ~10x, DeepSeek-V4.1-Flash 9x, Qwen3.6-35B-A3B 5x.
- Інтерактивність (E2E) при однаковому рівні конкурентності відносно GB300 NVL72: Kimi K3 ~3x, DeepSeek-V4.1-Flash 5x, Qwen3.6-35B-A3B 3x.
- Приклад Kimi K3: Vera Rubin — 41 414,2 токенів/с системи, 50,4 токенів/с на користувача, 100,89 кВт (при 1024 запитах); GB300 — 2 210,4 токенів/с, 56,2 токенів/с на користувача, 60 кВт (при 48 запитах).
- Апаратно: прогін Kimi K3 на Vera Rubin використав 32 прискорювачі (GPU Rubin з HBM4, Tensor Cores, NVLink 6-го поколінн); порівняльний прогін GB300 — 48 прискорювачів.
