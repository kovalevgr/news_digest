---
company: nvidia
title: "Validating GPU Platforms with Runtime AI Inventory via the NVIDIA DSX AI Factory"
url: https://developer.nvidia.com/blog/validating-gpu-platforms-with-runtime-ai-inventory-via-the-nvidia-dsx-ai-factory/
date: 2026-11-11
found_via: rss
---

NVIDIA's AI Cluster Runtime (AICR) adds an AI bill-of-materials component built on Google's open-source k8s-aibom project, inventorying supported AI workloads on Kubernetes and emitting CycloneDX 1.6 records with per-attribute confidence tiers and evidence; two H100 GKE inference recipes enable it by default, with low measured runtime overhead (~2.2 millicores CPU, 28-34 MiB memory).

## card

**Що сталося:** NVIDIA додала до AI Cluster Runtime (AICR) компонент AI bill-of-materials (AI BOM), побудований на базі відкритого проєкту Google k8s-aibom — він інвентаризує AI-навантаження, що підтримуються на Kubernetes, і видає записи у форматі CycloneDX 1.6 з рівнем довіри та доказами для кожного атрибута.

**Контекст:** Частина платформи NVIDIA DSX AI Factory. Два inference-рецепти для H100 на GKE увімкнюють цю функцію за замовчуванням; інші namespace повинні підключати її вручну (opt-in).

**Деталі:**
- Версія для валідації: AICR v1.2.0, яка фіксує k8s-aibom 1.6.2.
- Виміряне навантаження контролера: середнє 2.2 мілікора CPU, 28-34 МіБ пам'яті, ~4 запити до API-сервера на хвилину в стабільному режимі.
- Формат виводу: CycloneDX 1.6.
- AICR і k8s-aibom — обидва проєкти з відкритим кодом, доступні на GitHub.
