---
company: NVIDIA
title: "AICR v1.0: Open, stable, and verifiable GPU cluster configuration"
url: https://developer.nvidia.com/blog/aicr-v1-0-open-stable-and-verifiable-gpu-cluster-configuration/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-10-06
fetched: 2026-10-07
---

NVIDIA ships AICR (AI Cluster Runtime) v1.0, a stable compatibility contract for GPU-accelerated Kubernetes clusters with version-locked, validated recipes across CLI, REST API, and Go SDK.

## card

**Що сталося:** NVIDIA випускає AICR v1.0 — стабільний контракт сумісності для GPU-прискорених Kubernetes-кластерів із версіоно-закріпленими, валідованими рецептами для CLI, REST API та Go SDK.

**Контекст:** Вирішує проблему складності конфігурації — закріплює сумісні версії компонентів серед десятків залежностей (host kernels, GPU-драйвери тощо) і надає підписані доказові дані валідації.

**Деталі:**
- 100+ контриб'юторів проєкту
- Рецепти охоплюють 11 Kubernetes-сервісів, 10 GPU-акселераторів і кілька інструментів деплою
- Публічні інтерфейси (CLI/REST/Go SDK) тепер стабільні — можна будувати на них з довірою
- Dashboard валідації допомагає командам знаходити потрібні рецепти
