---
company: huggingface
title: "Ensemble forecasting with IBM Granite time-series models"
url: https://huggingface.co/blog/ibm-research/granite-timeseries-ensemble-r1
date: 2026-10-22
found_via: TIER-1 rss (huggingface.co/blog/feed.xml)
---

IBM Research releases Granite Timeseries Ensemble, combining four pretrained Granite time-series models (PatchTST-FM-r1/r2, FlowState-r1.1, TTM-r3) without retraining via two zero-shot aggregation methods; both ensembles beat all individual members on aggregate MASE on GIFT-Eval (97 configurations).

## card

**Що сталося:** IBM Research випустив Granite Timeseries Ensemble — рецепт прогнозування, що без донавчання об'єднує чотири готові моделі часових рядів Granite (PatchTST-FM-r1, PatchTST-FM-r2, FlowState-r1.1, TTM-r3) у двох варіантах агрегації.

**Контекст:** Два методи агрегації: Probabilistic Ensemble (рівновагове об'єднання квантилів, за замовчуванням) і IQR Ensemble (вага за шириною інтервалу прогнозу, з ізотонічною регресією проти перехресних квантилів).

**Деталі:**
- Бенчмарк GIFT-Eval (97 конфігурацій датасетів, знімок на 20 жовтня 2026, без донавчання): Probabilistic Ensemble — MASE 0.683, IQR Ensemble — MASE 0.684; обидва перевершують усі чотири окремі моделі за сукупним MASE.
- Найкращий CRPS/MWQL серед окремих моделей — у PatchTST-FM-r2 (0.467); серед ансамблів — IQR (0.471, найкращий ранг CRPS).
- Встановлення: `pip install "granite-tsfm>=0.3.11"`, завантаження через `QuantileEnsembleForecaster.from_pretrained(...)`.
- Базовий рецепт і стандартні компоненти Granite — під пермісивною ліцензією; розширені рецепти з іншими чекпоінтами IBM Research можуть мати окремі (включно з некомерційними) обмеження.
- Обмеження: канали прогнозуються незалежно (без міжканальної інформації), запуск чотирьох чекпоінтів збільшує час інференсу й пам'ять.
