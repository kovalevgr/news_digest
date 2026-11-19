---
company: huggingface
title: "Time-Series Models in the Streamhouse: A New Frontier and Use Cases"
url: https://huggingface.co/blog/ibm-research/time-series-powered-streamhouse
date: 2026-11-18
found_via: rss (huggingface.co/blog/feed.xml)
---

IBM Research and Confluent build IBM's Granite time-series foundation models (TTM, PatchTST-FM, TSPulse) into Confluent's Streamhouse, letting Flink SQL run forecasting, anomaly detection, and similarity search on live streaming data via CPU-only models.

## card

**Що сталося:** IBM Research і Confluent вбудували time-series foundation-моделі сімейства IBM Granite (TTM, PatchTST-FM, TSPulse) у Streamhouse — стрімінгову архітектуру Confluent — щоб прогнозування, детекція аномалій і similarity search працювали на живих даних через Apache Flink SQL (у Confluent Cloud або на власній інфраструктурі).

**Контекст:** Моделі працюють на CPU (без потреби в GPU-інфраструктурі); сімейство моделей має понад 50 мільйонів завантажень. Flink готує стрімінгові дані, викликає моделі й повертає результати разом з подіями, що їх породили; Lightning Tables дають низьколатентний доступ до поточного стану.

**Деталі:**
- SQL-функції AI_FORECAST та AI_DETECT_ANOMALIES; моделі можна донавчати або комбінувати з іншими даними й бізнес-логікою.
- Кейси: оптимізація виробництва (прогноз частки продукції в межах специфікації на 4 години вперед), детекція аномалій за власною історією кожного ряду замість фіксованих порогів, 28-денний прогноз попиту з P10-P90 діапазоном для supply chain, виявлення фрод-транзакцій за відхиленням від очікуваного діапазону конкретної картки, прогноз обсягу торгів на 30 хвилин вперед (PatchTST-FM) для трейдингу, семантичний пошук за схожістю сенсорних паттернів (TSPulse) — звужує розслідування, але не визначає причину.
- Один претренований модель обслуговує багато часових рядів без окремої моделі для кожного; прогнози оновлюються при надходженні нових даних.
