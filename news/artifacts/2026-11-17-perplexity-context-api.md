---
company: perplexity
title: "Context API extracts full context from any web page"
url: https://www.perplexity.ai/hub/blog/context-api-extracts-full-context-from-any-web-page
date: 2026-11-17
found_via: gap-scrape (Jina worked cleanly this run)
---

Perplexity launches the Context API, which reads up to 10 URLs and returns clean Markdown, HTML, links, and query-based snippets for each page, sourced from Perplexity's web index or a live fetch.

## card

**Що сталося:** Perplexity запускає Context API — ендпоінт, що читає до 10 URL і повертає чистий markdown, HTML, список лінків та релевантні до запиту фрагменти для кожної сторінки, з індексу Perplexity або через живий fetch.

**Контекст:** Вирішує проблему «сирого» HTML і урізаних пошукових сніпетів для агентів, яким потрібен повний контекст сторінки для складних задач — інтеграцій API, порівняння цін, питань політики, досліджень.

**Деталі:**
- У тесті на 715 сайтах проти Firecrawl/Exa/Parallel/Keenable/Context.dev: 92.3% «usable»-відповідей, 87.9% повнота фактів (fact recall), 80.3% точність контенту.
- Ціна: $1 за 1000 fetched URL; оплата лише за успішні (ok) результати.
- Контроль свіжості через `max_age_seconds` (0 = завжди live) та `cache_only`.
- URL обробляються паралельно, кожен зі своїм таймаутом і статусом — одна повільна сторінка не блокує решту.
