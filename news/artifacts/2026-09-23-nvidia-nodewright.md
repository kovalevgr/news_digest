---
company: NVIDIA
title: "Manage Kubernetes Node Fleets with NodeWright"
url: https://developer.nvidia.com/blog/manage-kubernetes-node-fleets-with-nodewright
published: 2026-09-23
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-24
---

NVIDIA introduces NodeWright, an open-source, Kubernetes-native declarative package manager for configuring and updating host operating systems across GPU clusters without disrupting active workloads.

## card

**Що сталося:** NVIDIA випускає NodeWright — відкритий, Kubernetes-native декларативний пакетний менеджер для конфігурації та оновлення операційних систем вузлів GPU-кластерів без переривання активних навантажень.

**Контекст:** Керування самими вузлами (kernel-налаштування, системні пакети, storage layout, security agents) традиційно вимагало ручних вікон обслуговування та ad-hoc runbook'ів; NodeWright замінює це декларативним, Kubernetes-orchestrated підходом для флотів із сотень вузлів під продакшн-тренуванням.

**Деталі:**
- Шестиетапна послідовність на кожному вузлі: cordon → wait → drain → apply/configure → interrupt → uncordon
- Поважає Kubernetes-примітиви (PodDisruptionBudgets, workload labels), щоб не переривати роботу
- Прогресивні стратегії розгортання: фіксовані, лінійні, експоненційні розміри пакетів
- Керує kernel tuning, CVE remediation, встановленням security agents, налаштуванням crash dump
- Ліцензія Apache 2.0, відкритий код на GitHub, встановлення через Helm (OCI artifact); частина NVIDIA DSX OS
