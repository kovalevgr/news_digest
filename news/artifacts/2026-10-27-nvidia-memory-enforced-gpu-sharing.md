---
company: nvidia
title: "Memory-Enforced GPU Sharing in Kubernetes with NVIDIA CUDA 13.4"
url: https://developer.nvidia.com/blog/memory-enforced-gpu-sharing-in-kubernetes-with-nvidia-cuda-13-4/
date: 2026-10-27
found_via: rss (TIER-1)
---

NVIDIA's CUDA 13.4 adds enforced per-workload memory limits for GPU sharing in Kubernetes, paired with the open-source GPU Fractioning Operator and KAI Scheduler v0.18.0's new NvFractions mode, letting several workloads share one GPU under hard or burstable memory caps.

## card

**Що сталося:** NVIDIA додає в CUDA 13.4 примусові ліміти памʼяті для спільного використання GPU в Kubernetes: кожне навантаження отримує фіксований або гарантований мінімум/максимум обсягу памʼяті, без потреби модифікувати застосунки.

**Контекст:** Можливість працює поряд з існуючим режимом компʼютингу sm-sharing у Multi-Process Service (MPS); для оркестрації на рівні Kubernetes NVIDIA пропонує відкритий GPU Fractioning Operator, а KAI Scheduler v0.18.0 став першим планувальником з інтеграцією через новий режим NvFractions.

**Деталі:**
- Режими компʼютингу: sm-sharing (паралельно) або типовий time-slicing (по черзі); на один GPU — лише один режим одночасно.
- Ліміт памʼяті опційний: якщо не вказано, рівний запиту; для часткових запитів ліміт має бути більшим за частку і меншим за 1.
- Запит може охоплювати кілька GPU одразу з однаковим обсягом на кожен.
- GPU Fractioning Operator — відкритий код (організація KAI Scheduler на GitHub); увімкнення NvFractions — через Helm-флаг `global.nvFractions.set=true`.
- CUDA 13.4 доступна на сторінці завантажень NVIDIA; деталей щодо апаратних вимог чи підтримки хмарних провайдерів не наведено.
