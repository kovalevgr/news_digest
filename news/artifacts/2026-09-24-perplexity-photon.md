---
company: Perplexity
title: "Photon: Building a Retrieval and Ranking Engine From Scratch"
url: https://www.perplexity.ai/hub/blog/photon
source_url: https://www.perplexity.ai/hub/blog
published: 2026-09-24
fetched: 2026-10-10
---

Perplexity replaces its forked open-source retrieval/ranking engine with Photon, an in-house Rust engine now powering its whole search stack and a new "fast" Search API preset; p99 retrieval latency falls from ~800ms to ~65ms, storage per document grows 2.5x on ~20% fewer machines, and the fast preset cuts model+search cost 68% at comparable quality across 6 agentic benchmarks. Backfilled: perplexity.ai is DNS-blocked for WebFetch in this env; confirmed today via Jina.

## card

**Що сталося:** Perplexity замінює форкнутий open-source рушій ретрівалу й ранжування на власний Photon (написаний на Rust), який тепер живить увесь пошуковий стек компанії і новий швидкий (fast) пресет Search API.

**Контекст:** продовження переходу Perplexity на власну пошукову інфраструктуру — після CobbleDB (зберігання) та власного Search API; попередня система впиралась у вартість пам'яті, хвостову латентність і тижневу синхронізацію при відновленні вузлів. Backfilled: perplexity.ai блокується на рівні DNS для WebFetch у цьому середовищі; підтверджено сьогодні через Jina.

**Деталі:**
- p99 латентність ретрівалу впала з ~800мс до ~65мс; зникли піки латентності при перемиканні версій індексу.
- Photon використовує на ~20% менше серверів, зберігаючи при цьому у 2.5 рази більше даних на документ (пінінг того ж обсягу в пам'яті вимагав би у 4.6 рази більше RAM).
- Новий fast-пресет Search API: 160мс (p50) / 230мс (p95) на один пошуковий виклик; на 6 агентних бенчмарках (WideSearch, BrowseComp, DSQA, FRAMES, SEAL-0, SEAL-Hard) коштує на 68% дешевше за дефолтний пресет при порівнянній якості (релевантність нижча на 0.24 п. DCG, доступність відповіді — на ~2.9 в.п.).
- Повний індекс вебу тепер будується за одноцифрову кількість годин (раніше розгортання нового кластера займало понад тиждень).
