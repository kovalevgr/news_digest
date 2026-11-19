---
company: openai
title: "Inside the Codex sandbox"
url: https://openai.com/index/inside-the-codex-sandbox
date: 2026-11-18
found_via: rss (openai.com/news/rss.xml)
---

OpenAI details the design of the Codex sandbox — the filesystem and network restrictions that let Codex run commands on a user's machine within limits the user controls, enforced across macOS, Linux, and Windows.

## card

**Що сталося:** OpenAI детально описала "Codex sandbox" — механізм, що обмежує доступ Codex до файлової системи й мережі під час виконання команд на машині користувача, як частину "defense in depth" підходу до безпеки агентів.

**Контекст:** Пісочниця налаштовується через "permission profiles": дефолтний профіль `:workspace` дозволяє запис у робочій директорії (крім `.git` і `.codex`), дозволяє широке читання файлової системи (залежно від прав ОС) і блокує мережевий доступ за замовчуванням.

**Деталі:**
- Приклад ризику навіть у пісочниці: агент може підмінити код у локально встановленому пакеті (напр. `node_modules/prettier`), що не з'явиться в `git status`, і шкідливий код виконається поза пісочницею, коли редактор запустить цей інструмент при збереженні файлу.
- Обмеження застосовуються на рівні ОС окремо для macOS, Linux і Windows.
- Є окремий "Codex security cookbook" із рекомендаціями для enterprise-налаштувань пісочниці.
