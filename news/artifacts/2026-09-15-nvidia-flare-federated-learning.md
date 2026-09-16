---
company: NVIDIA
title: "Scaling Federated Learning Across Docker, Kubernetes, and Slurm with NVIDIA FLARE"
url: https://developer.nvidia.com/blog/scaling-federated-learning-across-docker-kubernetes-and-slurm-with-nvidia-flare/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-09-15
fetched: 2026-09-16
---

NVIDIA details FLARE's two-layer architecture (persistent federation/coordination services + dynamic job workers) and its expansion across execution environments: FLARE 2.8 added Docker/Kubernetes deployment, FLARE 2.9 added Slurm support, letting one federated-learning deployment span single-host, cloud/cluster, and HPC/shared-GPU environments with portable per-site resource specs and multi-tenant "Studies" boundaries.

## card

**Що сталося:** NVIDIA розповідає, як FLARE (платформа федеративного навчання) розширила підтримку середовищ виконання: 2.8 додав Docker/Kubernetes, 2.9 — Slurm, тож один деплой охоплює одиночний хост, хмару/кластер і HPC/спільні GPU-кластери.

**Контекст:** Дворівнева архітектура розділяє постійні сервіси федерації/координації від динамічних job-воркерів, що виконують тренування і звільняють ресурси після завершення. Функція "Studies" дає логічні межі мультитенантності всередині одного деплою, прив'язуючи кожне дослідження до локальних даних, секретів, дозволених образів і політик планування конкретної сторони.

**Деталі:**
- Підтримувані середовища: Docker (одиночний хост), Kubernetes (хмара/кластер), Slurm (HPC/спільні GPU-кластери)
- Портовані специфікації ресурсів (GPU, CPU, пам'ять), незалежні від конкретної платформи — кожен лаунчер сайту транслює їх у нативні налаштування
- Studies дають мультитенантні межі: локальні дані, секрети, дозволені образи, політики планування на кожній стороні
