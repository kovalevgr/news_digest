---
company: Cursor
title: "Cloud Agents and Cursor Harness Improvements"
url: https://cursor.com/changelog/08-19-26
published: 2026-08-19
source_url: https://cursor.com/changelog/rss.xml
fetched: 2026-08-20
---

Cursor shipped a set of cloud-agent autonomy features: event-driven subscriptions (PRs, Slack threads, scheduled tasks), pinned custom modes, subagents each running in an isolated cloud VM with clean context, a `/goal` command for long-lived objectives, and non-interrupting steering messages.

## card

**Що сталося:** Cursor випустив пакет покращень для cloud-агентів: підписки на події (PR, Slack-треди, заплановані завдання) автоматично будять агента, custom modes закріплюють навичку в чаті, subagents тепер працюють кожен у власній ізольованій VM з чистим контекстом, команда `/goal` задає довгострокову ціль до повного виконання, а steering дозволяє скеровувати агента повідомленням без переривання поточної дії.

**Контекст:** Розвиток автономності cloud-агентів Cursor після нещодавніх "builds" (пришвидшення старту у 3 рази, 2026-08-13) та Origin Code Hosting (2026-08-17); підписки поки доступні лише для cloud-агентів.

**Деталі:**
- Subscriptions: агент автоматично підписується на створені ним PR і доводить їх до завершення; наразі — тільки cloud agents
- Custom modes: активація командою `/` + ⌥⏎ (Mac) або Alt+Enter (Windows)
- Subagents: ізольована копія проєкту в окремому cloud-середовищі для паралельного тестування/незалежних фіксів
- `/goal`: довгострокова ціль (напр. полагодити нестабільні тести й довести CI до зеленого), можна поєднувати з custom modes або `/loop`
- Steering: повідомлення-уточнення чекають наступного виклику інструменту замість переривання агента
