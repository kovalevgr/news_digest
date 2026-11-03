---
company: nvidia
title: "Diagnose Distributed AI Workload Failures with NVIDIA Attribution"
url: https://developer.nvidia.com/blog/diagnose-distributed-ai-workload-failures-with-nvidia-attribution/
date: 2026-11-02
found_via: rss (TIER-1)
---

NVIDIA releases Attribution, an open-source, deterministic-rules root-cause diagnosis system for distributed AI workload failures, already analyzing millions of workloads weekly across hundreds of thousands of production GPUs.

## card

**Що сталося:** NVIDIA випустила Attribution — відкритий сервіс для діагностики збоїв розподілених AI-навантажень, який визначає першопричину збою, а не лише місце, де робота зупинилась.

**Контекст:** В розподілених тренуваннях одна апаратна чи мережева проблема може викликати каскад симптомів (NCCL-помилки на інших рангах, зміни стану scheduler'а, шквал логів); Attribution доповнює системи моніторингу й відновлення, пояснюючи причину, а не усуваючи її.

**Деталі:**
- 4 етапи роботи: визначення межі навантаження → збір спостережень (логи/метрики/телеметрія/стан scheduler'а) → кореляція подій → структурований діагноз (причина, уражені вузли, симптоми, доказовий ланцюжок).
- Детерміновані правила — результати відтворювані й налаштовувані.
- У продакшені NVIDIA аналізує мільйони навантажень щотижня на сотнях тисяч GPU; наведений приклад — виявлення проблеми цілісності сигналу NVLink (XID 149) в одному RDMA-кластері.
- Складається з Attribution Service (self-hosted REST API) та Attribution Blueprint (Python-оркестратор з коннекторами до Slurm, Kueue, Loki, Kubernetes pod logs, PromQL); код і приклади — репозиторій dsx-ai-factory/attribution на GitHub.
