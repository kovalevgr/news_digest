---
company: Perplexity
title: "Building shared workspaces for people and agents"
url: https://www.perplexity.ai/hub/blog/building-shared-workspaces-for-people-and-agents
source_url: https://www.perplexity.ai/hub/blog
published: 2026-10-12
fetched: 2026-10-13
---

Perplexity details the architecture behind Projects in Perplexity Computer: a cloud-hosted Git forge (purpose-built for human-agent and agent-agent collaboration, without review screens or branch management) giving each project a persistent, concurrent, traceable shared filesystem. Found via gap-scrape (anonymous Jina worked today; perplexity.ai is DNS-blocked for direct WebFetch in this environment).

## card

**Що сталося:** Perplexity описує архітектуру Projects у Perplexity Computer — хмарний Git forge, спроєктований спеціально для співпраці людина-агент та агент-агент, що дає кожному проєкту стійку, конкурентну та прослідковувану спільну файлову систему.

**Контекст:** Projects раніше були Spaces; нова архітектура вирішує три вимоги багатогравцевої співпраці, що триває місяцями — persistence (робота переживає окрему сесію агента), concurrency (кілька агентів редагують паралельно без перезапису) та traceability (видно, хто що змінив, і можна відкотити зміни) — запозичуючи модель Git, але без частин, призначених для людей (review-екрани, керування гілками, нотифікації).

**Деталі:**
- Архітектура працює повністю в хмарі й підтримує будь-яку інтелектуальну роботу, не лише кодування
- Кожен проєкт Computer підтримується Git-репозиторієм із 5 компонентів: CLI, control plane, Git-сервіс, зберігання на AWS S3, downstream-обробка документів
- Кожен агент має власний ізольований чекаут; конфлікти вирішуються повторним застосуванням змін програвшого запису на новій версії
