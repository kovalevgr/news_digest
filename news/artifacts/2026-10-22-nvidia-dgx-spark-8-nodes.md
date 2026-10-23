---
company: nvidia
title: "Running Frontier-Class AI Models Across 8 NVIDIA DGX Spark Nodes"
url: https://developer.nvidia.com/blog/running-frontier-class-ai-models-across-8-nvidia-dgx-spark-nodes/
date: 2026-10-22
found_via: TIER-1 rss (developer.nvidia.com/blog/feed)
---

NVIDIA announces official 8-node DGX Spark cluster support (1TB unified memory) at GTC Berlin, running the full 753B-parameter GLM 5.3 model locally via a new RoCEnante collective backend and NeMo Switchyard router, with near-linear scaling shown on a 896.5M-parameter nanochat pretraining run (7.79x speedup, 97.4% efficiency at 8 nodes).

## card

**Що сталося:** NVIDIA анонсувала офіційну підтримку 8-вузлових кластерів DGX Spark (до 1 ТБ об'єднаної пам'яті, 128 ГБ на вузол) на GTC Berlin, що дозволяє локально запускати повну модель GLM 5.3 (753 млрд параметрів, NVFP4-чекпоінт ~470 ГБ).

**Контекст:** Представлено новий бекенд колективних операцій RoCEnante (оптимізований для Spark-кластерів зі свічами, з fallback на NCCL) та маршрутизатор NeMo Switchyard для розподілу запитів між пулами моделей на спільному кластері.

**Деталі:**
- GLM 5.3 Flash: ~80 токенів/с на генерацію на 8 вузлах.
- Повна GLM 5.3 (753B, NVFP4): 1600 токенів/с prefill загалом; decode 31 ток/с на користувача при concurrency 1, падає до 18 ток/с (67 ток/с загалом) при concurrency 8.
- Qwen3.8-27B decode: прискорення 4.43x на 8 вузлах зі свічем і RoCEnante (проти 3.05x без нього).
- Nanochat (~896,5 млн параметрів): 8741 ток/с на 1 вузлі → 68 079 ток/с на 8 вузлах (прискорення 7.79x, ефективність масштабування 97.4%).
- Підтримка 8 вузлів у NVIDIA Sync (Cluster Assistant) — "до кінця року", ще не доступна; код і гайди — на GitHub і build.nvidia.com. Усі цифри — власні вимірювання NVIDIA на конкретних конфігураціях.
