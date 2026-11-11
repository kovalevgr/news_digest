---
company: nvidia
title: "Manage Kubernetes Clusters for GPU Infrastructure with NVIDIA Kubernetes Engine"
url: https://developer.nvidia.com/blog/manage-kubernetes-clusters-for-gpu-infrastructure-with-nvidia-kubernetes-engine/
date: 2026-11-10
found_via: rss
---

NVIDIA releases two Apache-2.0 public-preview open-source projects — NVIDIA Kubernetes Engine (NVKE), a managed-Kubernetes-service software stack with a REST API, and NVIDIA Kubernetes Recipes (NVKR), which builds the node/container images and Helm charts clusters need — as part of the DSX AI Factory Platform.

## card

**Що сталося:** NVIDIA випустила у публічному preview (Apache 2.0) два відкриті проєкти: NVIDIA Kubernetes Engine (NVKE) — ПЗ для керованого Kubernetes-сервісу з REST API, та NVIDIA Kubernetes Recipes (NVKR) — збірку образів нод/контейнерів і Helm-чартів для таких кластерів; вони не залежать одне від одного і можуть використовуватись окремо.

**Контекст:** Частина платформи NVIDIA DSX AI Factory; хмарні партнери Firmus і SK Telecom вже інтегрують ці проєкти, а Mirantis, Rafay, Spectro Cloud, OpenNebula Systems, vCluster та Netris вбудовують компоненти у власні продукти.

**Деталі:**
- NVKE пройшла conformance-тест на Kubernetes 1.36 і сертифікована як Certified Kubernetes AI Platform та Certified Kubernetes Installer.
- Приклад розгортання: 3 control-plane ноди, 3 ноди для workload control plane, пул з 4 GPU-воркерів.
- Обидва проєкти — публічний preview; API можуть змінюватись, для продакшн не рекомендовано; бенчмарків продуктивності немає.
- Код відкритий на GitHub під організацією DSX AI Factory, документація — docs.nvidia.com/nvke.
