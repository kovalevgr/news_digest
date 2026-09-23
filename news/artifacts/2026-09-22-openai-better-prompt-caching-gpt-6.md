---
company: OpenAI
title: "Better prompt caching for GPT-6"
url: https://openai.com/index/better-prompt-caching-for-gpt-6
published: 2026-09-22
source_url: https://openai.com/news/rss.xml
fetched: 2026-09-23
---

OpenAI ships an improved prompt-caching system for the GPT-6 family: higher default cache-hit rates, discounts for eligible shared prefixes reused within a 30-minute window, a new Prompt Caching Dashboard, cache-miss diagnostics, explicit cache breakpoints, and the ability to change reasoning effort mid-conversation without breaking the cache.

## card

**Що сталося:** OpenAI випускає покращену систему кешування промптів для моделей GPT-6: вищий стандартний рівень влучень у кеш, знижки за повторне використання спільних префіксів у 30-хвилинному вікні, нову дашборд-панель моніторингу кешу та діагностику причин промахів.

**Контекст:** Розширює можливості кешування, представлені разом із GPT-6, для тривалих агентних застосунків (рефакторинг кодових баз, дослідницькі документи), де запити спираються на спільний контекст із попередніх ходів; кешовані вхідні токени й раніше давали знижку до 90%.

**Деталі:**
- Нова Prompt Caching Dashboard показує частку кешованих запитів і склад вхідних токенів у часі
- Діагностичний інструмент показує причину промаху кешу (наприклад, зміну tools) і кількість зачеплених токенів
- Явні cache breakpoints дозволяють обирати, які префікси промпту кешувати
- На моделях GPT-6 можна змінювати рівень reasoning effort між відповідями, не скидаючи кеш (через `configuration_update`)
