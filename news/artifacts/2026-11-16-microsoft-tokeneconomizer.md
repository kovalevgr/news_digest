---
company: microsoft
title: "TokenEconomizer: Learning from Experience to Make AI Coding Agents More Efficient"
url: https://www.microsoft.com/en-us/research/blog/tokeneconomizer-learning-from-experience-to-make-ai-coding-agents-more-efficient/
date: 2026-11-16
found_via: rss (microsoft.com/en-us/research/feed/)
---

Microsoft Research, with UC Berkeley and Microsoft Security, releases TokenEconomizer, an open-source plugin that cuts AI coding-agent token costs 18.4-30.9% on SWE-Bench by learning repository-specific patterns across sessions, without modifying the agent or its model.

## card

**Що сталося:** Microsoft Research разом з UC Berkeley та Microsoft Security випустили TokenEconomizer — опенсорс-плагін, який знижує витрати токенів AI-агентів для кодування, навчаючись на досвіді попередніх сесій у тому ж репозиторії, без змін самого агента чи моделі.

**Контекст:** Підхід базується на профілюванні реальних сесій: виявлено, що 30% викликів інструментів повторювали попередні дії в тому ж репозиторії, 16 з 23 описів інструментів ніколи не використовувались, а невдалі завдання (17%) становили 32% витрат.

**Деталі:**
- Три механізми: мікро-скіли (короткі репозиторій-специфічні нотатки, що додаються в контекст лише після підтвердження паттерну кількома сесіями), обрізання інструментів (видалення незадіяних інструментів, базові завжди лишаються) та втручання в циклах невдач (модель-суддя пропонує інший підхід або сповіщає розробника).
- На 277 задачах SWE-Bench (6 репозиторіїв, 5 комбінацій агент/модель) середня вартість задачі впала на 18,4–30,9%; Pass@1 зросло у 4 з 5 комбінацій.
- На Web-Bench вартість знизилась на 16,0–21,2%; на задачах безпекового аудиту (кожна в новому репозиторії) — на 6,4–19,6%.
- Код відкритий на github.com/microsoft/TokenEconomizer; проєктна сторінка tokeneconomizer.github.io; плагін не потребує власного API-ключа і зберігає вивчене локально на машині розробника.
