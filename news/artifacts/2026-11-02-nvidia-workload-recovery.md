---
company: nvidia
title: "Keep Distributed Training Running with Automated Workload Recovery"
url: https://developer.nvidia.com/blog/keep-distributed-training-running-with-automated-workload-recovery/
date: 2026-11-02
found_via: rss (TIER-1)
---

NVIDIA releases Recovery, an open-source NVIDIA DSX OS service that automatically detects, diagnoses and restarts failed distributed training jobs from their last checkpoint; a production run logged ~8,550 anomaly detections over three months with 69s mean detection latency.

## card

**Що сталося:** NVIDIA випустила Recovery — відкритий сервіс у складі NVIDIA DSX OS для автоматичного відновлення розподілених тренувальних завдань після збоїв без ручного втручання.

**Контекст:** Збої типу NCCL-таймаутів, "зависання" GPU-вузлів чи повільних воркерів витрачають дороговартісний GPU-час; ручне відновлення (аналіз логів, ізоляція причини, рестарт із checkpoint'у) не масштабується зі зростанням кількості й розміру завдань.

**Деталі:**
- Робочий цикл з 4 етапів: виявлення (Detect) → визначення причини (Attribute, опціонально через NVIDIA Attribution) → ізоляція проблемних вузлів (Isolate) → перезапуск або зупинка завдання (Restart/Stop) з останнього checkpoint'у.
- Інтегрується зі Slurm (Helm chart) та Slurm на Kubernetes через slurm-operator; нові деплойменти стартують у режимі monitor (лише рекомендації, без дій).
- У продакшн-прогоні на одному кластері (9 липня — 9 жовтня) сервіс обробляв ~200 завдань на день, зафіксував ~8550 детекцій аномалій; середня латентність виявлення — 69с, дії з відновлення — 94с.
- Відкритий код під Apache 2.0 на GitHub; ранні користувачі — IBM Research та неохмарний провайдер Verda.
