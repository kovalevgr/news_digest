---
company: OpenAI
title: "Rapidly scaling online storage to serve over 1 billion ChatGPT users"
url: https://openai.com/index/scaling-storage-one-billion-users-part-one
published: 2026-09-11
source_url: https://openai.com/news/rss.xml
fetched: 2026-09-12
---

OpenAI details Habitat, the online storage platform behind ChatGPT/Codex/GPTs: now handling 70M+ requests/second for 1B+ weekly users across ~40 regions and 500+ PB of data, evolved from a small Python client library (DevDay 2023) into a distributed service layered over Azure Cosmos DB. Part one of a two-part series (the second covers multi-tenancy reliability, read-performance layering, and scaling the Cosmos DB partnership).

## card

**Що сталося:** OpenAI публікує перший з двох постів про Habitat — власну платформу онлайн-сховища даних, що обслуговує ChatGPT, Codex і GPTs. Habitat обробляє понад 70 мільйонів запитів на секунду для понад 1 мільярда користувачів щотижня.

**Контекст:** Habitat почав як проста Python-бібліотека для GPTs на DevDay 2023, підключена до єдиної бази даних; відтоді OpenAI зростала понад 10x рік до року три роки поспіль, що змусило перетворити бібліотеку на розподілений сервісний шар. Другий пост серії (ще не опублікований) розкриє деталі мультитенантної надійності та масштабування партнерства з Azure Cosmos DB.

**Деталі:**
- 70+ млн запитів на секунду
- 1+ млрд користувачів щотижня, майже 40 географічних регіонів
- 500+ петабайт даних
- Побудовано поверх Azure Cosmos DB; сервіс написаний на Python — нетиповій мові для serving-стеку такого масштабу
