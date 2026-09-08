---
company: Perplexity
title: "Fast Embeddings on GPUs"
url: https://www.perplexity.ai/hub/blog/fast-embeddings-on-gpus
published: 2026-09-04
source_url: https://www.perplexity.ai/hub/blog
fetched: 2026-09-08
---

Perplexity details the GPU serving stack (Ivy, Tulip, ROSE) behind its pplx-embed and ranking models, covering CUDA-graph management, an async result-tracking abstraction, and a Rust request path. Written as a backfill: the primary source has been blocked by a Cloudflare JS challenge on every transport attempted (WebFetch, curl, Jina reader) across two consecutive runs (2026-09-07, 2026-09-08); this write-up rests on the canonical URL plus content confirmed via WebSearch synthesis of the actual article text, not on a direct read of the page.

## card

**Що сталося:** Perplexity описала внутрішню архітектуру обслуговування (serving) моделей ембеддингів на GPU — стек з трьох компонентів (Ivy, Tulip, ROSE), який обслуговує їхню модель pplx-embed і ранжувальні моделі для Perplexity Search, Computer та API Platform.

**Контекст:** Пост розділяє навантаження ембеддингів на два типи: пакетне (batch) — при побудові чи переіндексації векторної бази, де головне — пропускна здатність і вартість; та онлайнове (online) — на момент запиту, де короткий запит потрібно обробити швидко.

**Деталі:**
- Стек складається з трьох компонентів: Ivy, Tulip, ROSE
- Ключові техніки: керування CUDA graphs, асинхронна абстракція відстеження результатів, шлях обробки запитів на Rust
- Мета архітектури: швидко обробляти малі запити на ембеддинги, водночас підвищуючи утилізацію GPU за рахунок спільного обслуговування batch- та online-навантажень
- Обслуговує модель pplx-embed та супутні ранжувальні моделі для трьох продуктів: Search, Computer, API Platform
