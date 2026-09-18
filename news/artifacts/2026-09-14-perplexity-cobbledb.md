---
company: Perplexity
title: "CobbleDB: Lower-Latency, Lower-Cost AI Search Storage"
url: https://www.perplexity.ai/hub/blog/cobbledb
source_url: https://www.perplexity.ai/hub/blog
published: 2026-09-14
fetched: 2026-09-18
---

Perplexity built CobbleDB, a ~40,000-line Rust key-value hot store, to replace DynamoDB reads in its search-serving stack, cutting batch-read latency ~82% and a claimed $100M/year cost saving; plans to open-source it after further production validation. Backfilled: primary source blocked on every transport tried today (WebFetch/curl-jina: EGRESS_BLOCKED / Cloudflare challenge on perplexity.ai, consistent with prior runs); written on canonical-URL + content confirmation via WebSearch (corroborated by NVIDIA/Perplexity's own X post and independent coverage).

## card

**Що сталося:** Perplexity побудувала CobbleDB — власне key-value сховище на Rust (~40 000 рядків коду), що замінило читання з DynamoDB у критичному пошуковому ворклоді, скоротивши затримку пакетного читання приблизно на 82%.

**Контекст:** CobbleDB — це hot-store шар у новій розв'язаній архітектурі Perplexity (Pillar — durable-state, Lorry — batch-update, CobbleDB — query-time retrieval), розробленій двома інженерами за два місяці за участі сотень постійно працюючих AI-агентів.

**Деталі:**
- Медіанна затримка пакетного читання: 31,4 мс → 5,6 мс (~82% покращення)
- p99 затримка: 123 мс → 24,2 мс
- Заявлена економія: до $100 млн на рік
- CobbleDB зберігає ключі — хешовані URL сторінок, значення — попередньо розбиті на фрагменти пасажі з векторними ембеддингами
- Perplexity планує відкрити код CobbleDB після підтвердження продуктивності на масштабі сотень тисяч запитів на секунду в проді
