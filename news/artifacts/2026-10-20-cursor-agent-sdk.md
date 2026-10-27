---
company: cursor
title: "Agent SDK"
url: https://cursor.com/changelog/agent-sdk
date: 2026-10-20
found_via: gap-scrape (WebFetch of cursor.com/changelog — missed by TIER-1 RSS and prior runs' gap-scrapes)
---

Cursor ships the Agent SDK as generally available, letting developers define an agent as a code project (an `instructions.md` prompt plus folders for tools, skills, MCP connections, and channels), test it with evals, and deploy it to Cursor's infrastructure or their own; agents can be triggered via GitHub, GitLab, Bitbucket, Slack, webhooks, or cron.

## card

**Що сталося:** Cursor випускає Agent SDK у загальному доступі (GA) — набір інструментів, що дозволяє визначати агента як код-проєкт (файл `instructions.md` плюс папки для інструментів, навичок, MCP-з'єднань і каналів), тестувати його evals-ами та розгортати на інфраструктурі Cursor або власній.

**Контекст:** Продовжує лінійку Cursor з розширення можливостей агентів поза редактором (Projects, Remote Control, Origin App Marketplace) до повноцінного SDK для побудови власних агентів-ботів.

**Деталі:**
- Агенти стартують із шаблонів, наприклад "security reviewer" чи "PR autofixer".
- Тригери запуску: GitHub, GitLab, Bitbucket, Slack, webhooks, cron.
- Команда `agent-sdk github replay` дозволяє відтворювати реальні pull request'и для тестування GitHub-ботів.
- Стаття не наводить цін чи показників використання.
