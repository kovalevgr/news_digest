---
company: NVIDIA
title: "Validate GPU Cluster Readiness Before AI Workloads Land"
url: https://developer.nvidia.com/blog/validate-gpu-cluster-readiness-before-ai-workloads-land
published: 2026-09-23
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-24
---

NVIDIA introduces the Cluster Readiness Engine (NVCRE), an open-source Kubernetes controller that validates GPU cluster readiness by running real distributed workloads across topology-aware node groups and isolating faulty nodes.

## card

**Що сталося:** NVIDIA випускає NVIDIA Cluster Readiness Engine (NVCRE) — відкритий Kubernetes-контролер, що перевіряє готовність GPU-кластера, запускаючи реальні розподілені навантаження на topology-aware групах вузлів замість перевірок "за замовчуванням".

**Контекст:** Кластер може пройти всі окремі health-check'и (кожен GPU, мережевий лінк, под — "здорові"), але все одно не впоратися з реальним тренувальним навантаженням на 512 GPU; NVCRE усуває саме цей розрив між перевіркою окремих компонентів і реальною готовністю системи.

**Деталі:**
- Автоматично ділить групи, що провалили тест, і перезапускає тести, доки не локалізує невеликий набір підозрілих вузлів — замість звинувачення всієї групи
- Трирівнева ієрархія API: Certification → Workflow → Job, що прив'язує збої до конкретних вузлів і категорій
- Покриття тестів: 5 варіантів NCCL-комунікації, DCGM level-4 diagnostics, NeMo pretraining на Nemotron 5 (8B та 56B)
- Вимоги: Kubernetes 1.29+, NVIDIA GPU Operator; ліцензія Apache 2.0, доступний на GitHub
- Частина екосистеми NVIDIA DSX OS, працює разом з AI Cluster Runtime та NVSentinel
