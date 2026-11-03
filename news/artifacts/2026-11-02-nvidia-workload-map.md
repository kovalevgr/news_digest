---
company: nvidia
title: "Support New AI Frameworks Faster Using NVIDIA Workload Map"
url: https://developer.nvidia.com/blog/support-new-ai-frameworks-faster-using-nvidia-workload-map/
date: 2026-11-02
found_via: rss (TIER-1)
---

NVIDIA open-sources Workload Map, a Kubernetes CRD + Go library (formerly "Karta") describing distributed AI workload structure in a common format so schedulers/platforms need no per-framework adapter; already used in production inside NVIDIA Run:ai.

## card

**Що сталося:** NVIDIA випустила Workload Map — відкритий Kubernetes-компонент (CRD + Go-бібліотека), що описує структуру розподілених AI-навантажень у єдиному форматі, зрозумілому для будь-якого scheduler'а чи платформи без написання окремого адаптера під кожен фреймворк.

**Контекст:** Раніше кожен AI-фреймворк (JobSet, PyTorchJob, RayCluster тощо) кодував структуру завдання по-своєму, тому інструментам доводилося писати окремий адаптер під кожен custom resource — це затримувало підтримку нових фреймворків.

**Деталі:**
- Готовий каталог визначень для JobSet, PyTorchJob, RayCluster, RayJob, KServe, MPIJob, NVIDIA NIM, LeaderWorkerSet, NVIDIA Dynamo; нові типи додаються написанням YAML-визначення.
- Використовується в продакшені всередині NVIDIA Run:ai; KAI Scheduler застосовує його як fallback для типів навантажень без власного плагіна gang scheduling.
- Elotl Nova використовує Workload Map для рішень з мультикластерного планування.
- Ліцензія Apache 2.0, доступно через GitHub-організацію NVIDIA DSX AI Factory.
