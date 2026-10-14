---
company: NVIDIA
title: "NVIDIA Run:ai Is Now Open Source as Part of NVIDIA DSX AI Factory Platform"
url: https://developer.nvidia.com/blog/nvidia-runai-is-now-open-source-as-part-of-nvidia-dsx-ai-factory-platform/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-10-13
fetched: 2026-10-14
---

NVIDIA open-sources the full Run:ai Kubernetes AI-workload platform under the DSX AI Factory org, with its KAI Scheduler contributed to CNCF as a Sandbox project and eight ecosystem partners integrating it.

## card

**Що сталося:** NVIDIA відкриває повну платформу Run:ai (керування GPU-навантаженнями на Kubernetes) як відкритий код в організації NVIDIA DSX AI Factory на GitHub (github.com/dsx-ai-factory/run-ai), також доступна на NGC як Community Product із Helm chart.

**Контекст:** Run:ai раніше була комерційною платформою NVIDIA для планування GPU-навантажень; тепер її ядро стає відкритим фундаментом DSX AI Factory Platform, а комерційні пропозиції (стандалон Run:ai, Mission Control, AI Enterprise) лишаються окремо.

**Деталі:**
- 4 модульні компоненти, які можна використовувати незалежно: KAI Scheduler (Kubernetes-GPU-планувальник: gang scheduling, fair-share/квоти, топологія, GPU sharing, DRA), GPU Fractioning Operator (CUDA 13.4-нативний поділ GPU на частки), KAI Resource Management (проєкти/департаменти/квоти/node pools), Workload Map (Go-бібліотека опису типів навантажень Kubernetes без хардкоду CRD)
- KAI Scheduler — під ліцензією Apache 2.0, переданий у CNCF як Sandbox-проєкт; ліцензія решти платформи залежить від застосовних open source ліцензій (єдина ліцензія для всієї платформи не названа)
- 8 партнерів DSX інтегрують платформу: Crusoe, Mirantis, Nebius, OpenNebula Systems, Rafay, Saturn Cloud, Spectro Cloud, vCluster
- Супутні відкриті проєкти: Model Streamer (швидше завантаження ваг моделей) і Grove (оркестрація мультикомпонентних inference-навантажень)
- Завантаження NGC Community Product вимагає прийняття NVIDIA Software License Agreement, без потреби платної підписки; підтримка NVIDIA enterprise не включена
