---
company: Google Research
title: "TimesFM-3: A zero-shot foundation model for multivariate forecasting"
url: https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/
published: 2026-08-31
source_url: https://research.google/blog/rss/
fetched: 2026-09-01
---

Google Research released TimesFM-3, a 330M-parameter time series foundation model trained on 1T+ time points — the first in the TimesFM family to natively support multivariate forecasting. It tops the Gift-Eval, FEV-Bench, and Time benchmarks against Chronos-2 and TimesFM-2.5.

## card

**Що сталося:** Google Research випустила TimesFM-3 — модель-фундамент для прогнозування часових рядів на 330М параметрів, навчену на понад 1 трильйоні точок даних. Це перша версія в лінійці TimesFM з нативною підтримкою мультиваріативного прогнозування.

**Контекст:** Модель замінює TimesFM-2.5 (вересень 2025), додаючи підтримку кількох цільових рядів одночасно, історичних коваріат і майбутніх відомих подій (акції, прогноз погоди). Порівнюється з Chronos-2 та власною попередньою версією.

**Деталі:**
- Найкращий результат на трьох ключових бенчмарках: Gift-Eval, FEV-Bench, Time (точкове і ймовірнісне прогнозування)
- Доступна одразу через GitHub і Hugging Face
- Інтеграція з BigQuery — найближчими тижнями
- Підтримує мультиваріативні сценарії: кілька цільових рядів, історичні коваріати, майбутні відомі події
