---
company: huggingface
title: "Why your fine-tuning job takes longer than the FLOPs say"
url: https://huggingface.co/blog/Dharma-AI/predicting-fine-tuning-time
date: 2026-11-18
found_via: rss (huggingface.co/blog/feed.xml)
---

Dharma-AI shows that FLOP-based estimates of fine-tuning job duration are unreliable (R²=0.31) and that a gradient-boosted model (CatBoost) trained on pre-dispatch job metadata predicts GPU-cluster job time far more accurately (R²=0.98).

## card

**Що сталося:** Dharma-AI опублікувала дослідження про те, чому FLOP-оцінки тривалості fine-tuning задач на спільних GPU-кластерах системно помиляються — ці оцінки ігнорують оверхед (налаштування, періодичні evaluation, збереження чекпоінтів, I/O-конкуренцію), через що GPU простоюють або задачі в черзі затримуються.

**Контекст:** Автори звели задачу до регресії за відомою перед запуском інформацією (гіперпараметри, розмір датасету, ідентифікатор моделі, виділені GPU) плюс ознаками оверхеду (обсяг evaluation, кількість чекпоінтів, обсяг токенів на GPU), натренованої на 272 production SFT-запусках (~7 382 GPU-годин) на NVIDIA H200.

**Деталі:**
- FLOP-базлайн: R²=0.31, MAE=12.41 год при 30% MFU; перебір MFU від 0.25 до 0.65 не усуває розрив.
- Calculon (детальніша аналітична модель): R²=−0.51, MAE=20.36 год, оцінки — медіанно ~11% реального часу.
- Лінійні моделі (Ridge): MAE=7.23 год — зв'язок нелінійний.
- Фінальна модель CatBoost: R²=0.98, MAE=1.71 год, медіанна похибка 0.51 год (5-fold cross-validation); XGBoost — майже так само добре.
- Найважливіша ознака — обсяг evaluation-даних (`num_eval_data`), далі — кількість параметрів, що тренуються, і налаштування eval batch; дані обмежені SFT на одному типі GPU (H200), тож числа не переносяться напряму на інше апаратне забезпечення без перенавчання.
