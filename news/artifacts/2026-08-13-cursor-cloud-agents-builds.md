---
company: Cursor
title: "Cloud Agents Start 3x Faster with Builds"
url: https://cursor.com/changelog/08-13-26
published: 2026-08-13
source_url: https://cursor.com/changelog/rss.xml
fetched: 2026-08-14
---

Cursor introduces "builds" — pre-configured development environments that cloud agents boot into with repositories already cloned, dependencies installed, and setup scripts run — cutting agent startup time 3x, with automatic fallback to the last successful build if recent commits break the environment.

## card

**Що сталося:** Cursor запустив "builds" — заздалегідь підготовлені середовища розробки, в які хмарні агенти завантажуються одразу з клонованим репозиторієм, встановленими залежностями й виконаними setup-скриптами.

**Контекст:** Функція входить у продукт Cloud Agents і додається без додаткової оплати; логічне продовження оптимізації швидкості старту агентів після недавнього запуску Cursor Router (маршрутизація моделей).

**Деталі:**
- Приріст швидкості: 3× швидше до першого токена; 10× швидше завантаження середовища всередині
- Вартість: входить у Cloud Agents безкоштовно
- Доступність: автоматично для нових середовищ; для існуючих — вмикається у вкладці "Builds" в дашборді Cloud Agents
- Стійкість: якщо свіжі коміти ламають середовище, агент продовжує використовувати останній вдалий build
- Дебаг: нова вкладка "Builds" показує статус, логи, commit SHA і який build використав кожен запуск агента
