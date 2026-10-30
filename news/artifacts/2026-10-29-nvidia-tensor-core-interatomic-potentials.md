---
company: nvidia
title: "Unlocking Tensor Core Performance for Machine Learning Interatomic Potentials"
url: https://developer.nvidia.com/blog/unlocking-tensor-core-performance-for-machine-learning-interatomic-potentials/
date: 2026-10-29
found_via: rss (TIER-1)
---

NVIDIA describes two Tensor Core methods (BF16x9 on Blackwell, TF32x3 on Ampere) that speed up FP32 matrix multiplications for machine learning interatomic potentials without retraining, tested on the Point Edge Transformer (PET) model.

## card

**Що сталося:** NVIDIA публікує два методи прискорення FP32-обчислень на Tensor Core (BF16x9 для Blackwell, TF32x3 для Ampere) для моделей міжатомних потенціалів машинного навчання — без перенавчання моделі, перевірені на Point Edge Transformer (PET).

**Контекст:** Атомістичні симуляції (хімічні реакції, фазові переходи, механічні руйнування) традиційно обмежені пропускною здатністю FP32-обчислень; NVIDIA пропонує апаратне прискорення через Tensor Core замість зміни архітектури моделі.

**Деталі:**
- BF16x9 (Blackwell, B300): прискорення великих GEMM у 2.2–2.5x на системі з 17 280 атомами, до 1.7x для повного кроку молекулярної динаміки; похибка нижче рівня власної недетермінованості моделі.
- TF32x3 (Ampere, A100): прискорення ключових GEMM у 1.7–1.9x, повний крок MD — до 1.5x, похибка сили близька до базового рівня FP32.
- Фізична коректність: TF32x3 зберігає закон збереження енергії в NVE-симуляціях і сходиться за 218–222 кроки на 539-атомній структурі (FP32 — 218 кроків); одно-прохідний TF32 "пливе" за енергією і не сходиться.
- Доступність: BF16x9 — через налаштування cuBLAS, TF32x3 — реалізація через CUTLASS; чекпойнти PET у репозиторії UPET.
- Застереження: приріст залежить від розміру системи та частки часу в GEMM-операціях; TF32x3 варто перевіряти під вимоги точності конкретної моделі.
