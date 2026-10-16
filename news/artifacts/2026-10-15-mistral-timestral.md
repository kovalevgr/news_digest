---
company: Mistral AI
title: "Introducing Timestral"
url: https://mistral.ai/news/timestral/
source_url: https://mistral.ai/rss.xml
published: 2026-10-15
fetched: 2026-10-16
---

Mistral releases Timestral, its first family of time-series foundation models (5M–209M params), forecasting probabilistic multivariate time series; the 209M model claims first place on GIFT-Eval, TIME, and fev-bench leaderboards.

## card

**Що сталося:** Mistral випустив Timestral — свою першу родину foundation-моделей для часових рядів, які прогнозують ймовірнісні мультиваріантні часові ряди з підтримкою минулих і майбутніх ковариат. За даними Mistral, найбільша модель посідає 1-е місце в лідербордах GIFT-Eval, TIME і fev-bench.

**Контекст:** Це перша модель Mistral у цій категорії (нічого не замінює); позиціонується проти класичних методів (ARIMA), deep learning моделей (PatchTST) та інших foundation-моделей для часових рядів (Chronos-2, TimesFM-3, Falcon-2.0).

**Деталі:**
- Розміри: 5M, 28M, 123M, 209M параметрів — одна архітектура й рецепт тренування
- 209M-модель перевершує попередній SOTA приблизно двома третинами його параметрів
- Швидкість на 8-потоковому серверному CPU: прогноз на день вперед (з 3 тижнів історії по 15 хв) — 10 мс (5M) і 140 мс (209M); 28M-модель приблизно в 5 разів швидша за 209M
- Контекст: до 32,768 часових кроків; вивід — ймовірнісні прогнози по 21 квантилю
- Доступність: відкрито на GitHub і Hugging Face, документація на docs.mistral.ai; fine-tuning через Mistral Forge; варіанти розгортання — on-prem, VPC, air-gapped
- Ліцензія: Modified MIT
