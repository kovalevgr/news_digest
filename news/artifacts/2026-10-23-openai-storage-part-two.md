---
company: openai
title: "Rapidly scaling online storage to serve over 1 billion ChatGPT users (Part II)"
url: https://openai.com/index/scaling-storage-one-billion-users-part-two
date: 2026-10-23
found_via: rss (TIER-1)
---

OpenAI publishes Part II of its Habitat storage engineering writeup, covering how it added reliable multi-tenancy, global caching, and migration to Azure Cosmos DB to deliver 12x faster reads for ChatGPT's storage layer. Continues Part I (2026-09-11, already on file), which introduced Habitat itself (70M+ requests/second, 1B+ weekly users, ~40 regions, 500+ PB of data).

## card

**Що сталося:** OpenAI опублікувала другу частину технічного розбору Habitat — внутрішньої платформи онлайн-зберігання, що обслуговує ChatGPT. Стаття описує, як команда додала надійну мультитенантність, глобальне кешування та перехід на Azure Cosmos DB.

**Контекст:** Продовжує частину I (2026-09-11), де описано сам Habitat — 70+ млн запитів/с для понад 1 млрд тижневих користувачів у ~40 регіонах і понад 500 ПБ даних, що виросла з невеликої Python-бібліотеки (DevDay 2023) у розподілений сервіс.

**Деталі:**
- Головний результат частини II — 12-кратне прискорення читань завдяки новій архітектурі кешування.
- Ключові техніки: мультитенантність, глобальне кешування, міграція на Azure Cosmos DB.
- Стаття — суто інженерний розбір інфраструктури, без анонсу нового продукту.
