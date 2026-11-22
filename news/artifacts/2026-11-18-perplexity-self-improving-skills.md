---
company: perplexity
title: "Self-improving skills"
url: https://www.perplexity.ai/hub/blog/self-improving-skills
date: 2026-11-18
found_via: gap-scrape (Jina worked cleanly this run)
---

Perplexity extends Brain (Computer's memory system) to automatically create and update agent "skills" — reusable task instructions — for individual users, and through a separate human-reviewed pipeline, for all users' built-in skills.

## card

**Що сталося:** Perplexity розширює Brain (систему пам'яті Computer) до автоматичного створення й оновлення agent skills — повторюваних інструкцій для типових задач — як індивідуально для кожного користувача, так і (через окремий пайплайн з людським рев'ю) для вбудованих skills усіх користувачів.

**Контекст:** Brain вже вів структуровану knowledge wiki про користувача; skills — окремий механізм керування поведінкою агента без зміни ваг моделі. Цикл самовдосконалення складається з чотирьох кроків: evidence → reflection → verification → activation.

**Деталі:**
- З 1 серпня по 14 листопада Brain написав 80 000+ персональних skills для 20 000+ користувачів і застосував 100 000+ автооновлень до 30 000+ існуючих skills.
- 8-тижневий A/B-тест: 72.9% користувачів з увімкненим покращенням skills отримали хоча б один новий skill проти 6.5% у контрольній групі; частота збоїв tool call впала на ~11% (≈7% без фонових запусків), незадоволеність користувачів — на 7.6%.
- Ліміт — 10 автоматично створених skills на користувача; щоб додати новий, потрібно прибрати інший.
- Функція доступна всім US Max-підписникам, увімкнена за замовчуванням, можна вимкнути в розділі Plugins.
