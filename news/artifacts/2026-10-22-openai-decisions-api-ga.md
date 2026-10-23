---
company: openai
title: "Build more responsive apps with the Decisions API"
url: https://openai.com/index/decisions-api
date: 2026-10-22
found_via: TIER-1 rss (openai.com/news/rss.xml)
---

OpenAI makes the Decisions API generally available: built on GPT-6 Luna, it answers bounded questions (predicate/choice/score) from text, images, or structured input up to 10x faster than the Responses API, now with GPT-Live integration, prompt caching, EU/US inference residency, and up to 400 questions per request.

## card

**Що сталося:** OpenAI переводить Decisions API у статус загальної доступності (GA). API на базі GPT-6 Luna дає швидкі відповіді на обмежені за форматом запитання (ймовірність, вибір варіанту, оцінка) з тексту, зображень або структурованих даних — до 10 разів швидше, ніж звичайний виклик GPT-6 Luna через Responses API.

**Контекст:** Продовжує публічну бету Decisions API, яку OpenAI відкрила раніше (представлена на DevDay у вересні). З моменту бети додано нативну інтеграцію з GPT-Live, кешування промптів для повторного контексту та резидентність інференсу в США і ЄС.

**Деталі:**
- Три типи відповіді: predicate (ймовірність від 0 до 1), choice (вибір з заданих варіантів з рівнем довіри), score (оцінка за шкалою рівнів).
- До 400 запитань на один запит — удвічі більше за попередній лімід.
- Підтримка нативного JSON та зображень у складі інструкцій до запитання.
- Ціна (за зовнішніми джерелами): $0.10 за мільйон вхідних токенів, вихідні токени та кеш не тарифікуються.
- Внутрішнє використання в OpenAI: команди Dots (швидкість відповідей), Personal Finance (категоризація транзакцій), Communications (класифікація згадок у ЗМІ).
