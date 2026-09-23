---
company: NVIDIA
title: "Topology-Aware Workload Scheduling with NVIDIA Topograph"
url: https://developer.nvidia.com/blog/topology-aware-workload-scheduling-with-nvidia-topograph/
published: 2026-09-22
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-23
---

NVIDIA open-sources Topograph, a toolkit that auto-discovers cluster network topology across cloud providers and on-prem fabrics and feeds it to schedulers (Kubernetes, Slurm, KAI Scheduler) for topology-aware GPU workload placement.

## card

**Що сталося:** NVIDIA відкриває код Topograph — інструменту, що автоматично виявляє топологію мережі кластера й нормалізує її для розумного розміщення GPU-навантажень в AI-фабриках.

**Контекст:** Погане розміщення GPU-навантажень фрагментує мережеві домени та змушує трафік йти через спільні канали, знижуючи пропускну здатність і підвищуючи витрати; Topograph вирішує це, даючи планувальникам реальну видимість звʼязків GPU і мережевої фабрики в реальному часі.

**Деталі:**
- Нормалізує дані топології від Google Cloud, Lambda, Nebius, Nscale, OCI та on-premises фабрик в єдину модель
- Автоматично перебудовує карту топології при зміні кластера — без ручної підтримки
- Формати виводу: мітки вузлів Kubernetes, конфігурації Slurm, Slinky ConfigMaps
- Інтегрується з KAI Scheduler для topology-aware gang scheduling; є утиліти симуляції без реального обладнання
- Доступний зараз у репозиторії `dsx-ai-factory/topograph` (Helm для Kubernetes, Debian/RPM-пакети для Slurm)
