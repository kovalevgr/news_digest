---
company: perplexity
title: "Freeze the web with Perplexity Time Machine"
url: https://www.perplexity.ai/hub/blog/freeze-the-web-with-perplexity-time-machine
date: 2026-11-25
found_via: gap-scrape (Jina — anonymous Jina worked cleanly this run)
---

Perplexity launches Time Machine for the Search API and Context API: a `snapshot_as_of` parameter that limits retrieval to stored page copies at or before a chosen date, up to 365 days back.

## card

**Що сталося:** Perplexity запускає Time Machine для Search API та Context API — параметр `snapshot_as_of`, що обмежує пошук і читання сторінок збереженими копіями станом на обрану дату (до 365 днів назад). Це дозволяє агентам та бенчмаркам працювати з "вебом як він був" без витоку майбутньої інформації (результатів виборів, звітів про прибутки тощо) у відповідь.

**Контекст:** Кожна сторінка, яку сканує Perplexity, зберігається з позначкою часу, формуючи історію версій для кожної URL. Функція продовжує лінійку розвитку Search API та Context API (анонсованого 17 листопада).

**Деталі:**
- Приклад застосування: RL-тренування GLM-5.3 Flash на прогнозування подій з Polymarket — без Time Machine модель просто "підглядає" відповідь (90% груп тренування дають нульовий градієнт); з Time Machine обмеження активне лише у ~25% груп, а reward на hold-out зростає з 0.77 до 0.80 (вище за ринкову оцінку 0.79).
- Порівняння з Exa Snapshot на 3 наборах по 1000 запитів: Time Machine повертає дату публікації у 98.8–99.5% сторінок (Exa: 66.1–77.7%); частка сторінок із витоком інформації "з майбутнього" — 0.25–0.5% у Time Machine проти 1.10% у Exa на випадковій вибірці.
- Ціна без надбавки за історичні запити: Search API — $5/1000 запитів, Context API — $1/1000 URL; працює з існуючим API-ключем.
