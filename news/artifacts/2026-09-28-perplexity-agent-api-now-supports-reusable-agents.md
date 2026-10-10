---
company: Perplexity
title: "Agent API now supports reusable agents"
url: https://www.perplexity.ai/hub/blog/agent-api-now-supports-reusable-agents
source_url: https://www.perplexity.ai/hub/blog
published: 2026-09-28
fetched: 2026-10-10
---

Perplexity's Agent API adds Profiles (versioned agent configs bundling model, instructions, tools, connectors, and run settings under one ID), custom versioned Skills, and managed Connectors (GitHub, Slack, Google Drive, Datadog, Linear, Notion — in preview), so teams configure an agent once and reuse it across applications. Backfilled: perplexity.ai is DNS-blocked for WebFetch in this env; confirmed today via Jina.

## card

**Що сталося:** Perplexity додає до Agent API рівень командних, версіонованих конфігурацій агентів: Profiles (модель + інструкції + інструменти + налаштування під одним версіонованим ID), власні версіоновані Skills та керовані Connectors.

**Контекст:** розвиток Agent API, запущеного в березні 2026 й розширеного минулого місяця до єдиної поверхні для веб-пошуку, виконання коду, MCP і спеціалізованого пошуку. Backfilled: perplexity.ai блокується на рівні DNS для WebFetch у цьому середовищі; підтверджено сьогодні через Jina.

**Деталі:**
- Profiles і власні Skills доступні вже зараз для всіх проєктів Agent API.
- Managed Connectors — у preview: GitHub, Slack, Google Drive, Datadog, Linear, Notion; можна також створювати власні кастомні конектори.
- Адміністратор проєкту налаштовує Profile/Connector один раз в API Console — учасники проєкту використовують це через свій API-ключ без повторної конфігурації в кожному застосунку.
