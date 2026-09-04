---
company: xAI
title: "Designing Grok Bot for a world of persistent agents"
url: https://x.ai/news/designing-grok-bot
published: 2026-09-03
source_url: https://x.ai/news
fetched: 2026-09-04
---

xAI published a design-philosophy post explaining Grok Bot's interface choices: five core objects (Bots, Chats, Prompts, Tools, Artifacts) replacing the usual chat-session vocabulary, organizing the product around persistent "Bots" rather than disposable chat history.

## card

**Що сталося:** xAI опублікувала пост про дизайн-рішення Grok Bot, пояснюючи, чому інтерфейс побудований навколо персистентних агентів ("Bots"), а не навколо одноразових чат-сесій, як у більшості AI-продуктів.

**Контекст:** Супроводжує запуск Grok Bot for Enterprise того ж дня; пояснює архітектурні рішення, закладені ще при першому запуску Grok Bot 11 серпня 2026.

**Деталі:**
- П'ять базових об'єктів інтерфейсу: Bots (персистентні агенти з власною ідентичністю, пам'яттю, середовищем виконання й інструментами), Chats, Prompts (одноразові, збережені як Skills, або як Routines-тригери), Tools, Artifacts
- Головний об'єкт продукту — не розмова, а Bot: має ім'я, аватар, пам'ятає попередні розмови, має власний "комп'ютер" та інструменти
- Мета — сховати з очей користувача зайву термінологію (сесії, контекстні вікна, конектори тощо), залишивши лише п'ять концептів, необхідних для роботи з агентом
