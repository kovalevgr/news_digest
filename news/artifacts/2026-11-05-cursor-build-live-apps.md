---
company: cursor
title: "Build Live Apps in Cursor"
url: https://cursor.com/changelog/build-live-apps
date: 2026-11-05
found_via: fetch (backfill — missed by prior gap-scrapes; zero fresh from the rss tier this run, confirmed via WebFetch of cursor.com/changelog)
---

Cursor lets users build and publish web apps directly in the editor: a cloud agent scaffolds the app, provisions Postgres and hosting as needed, and sets up authentication behind Cursor SSO; Cursor runs security checks before a user explicitly publishes the app to a domain of their choice.

## card

**Що сталося:** Cursor додав можливість створювати повноцінні веб-застосунки прямо в редакторі та публікувати їх за посиланням — cloud-агент самостійно розгортає застосунок, за потреби підключає Postgres і хостинг, та налаштовує автентифікацію через Cursor SSO.

**Контекст:** Перед публікацією Cursor проводить перевірки безпеки; користувач має явно натиснути "опублікувати" та обрати домен — нічого не йде в публічний доступ автоматично.

**Деталі:**
- Автоматичне розгортання: cloud-агент сам scaffold'ить застосунок.
- База даних і хостинг: провіднюються за потреби (Postgres).
- Автентифікація: через Cursor SSO.
- Безпека: перевірки безпеки перед публікацією; публікація — явна дія користувача, домен обирає сам користувач.
