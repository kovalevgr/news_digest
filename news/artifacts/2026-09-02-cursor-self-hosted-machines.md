---
company: Cursor
title: "Self-hosted machines"
url: https://cursor.com/changelog/self-hosted-machines
published: 2026-09-02
source_url: https://cursor.com/changelog/rss.xml
fetched: 2026-09-03
---

Cursor added self-hosted machines for Cloud Agents, letting teams keep codebases/secrets on their own infrastructure (My Machines for individuals, Team Pools with dynamic scaling/hibernation for teams), with integrations for AWS Lambda, Coder, Cloudflare, Vercel, and E2B, plus Linux/Mac computer-use support.

## card

**Що сталося:** Cursor додав self-hosted machines для Cloud Agents — можливість виконувати tool-виклики агентів повністю у власній інфраструктурі користувача, залишаючи кодову базу, білд-артефакти та секрети на внутрішніх машинах.

**Контекст:** Гап-скрейп зловив цей пункт лише сьогодні (RSS-фід не показав його як "fresh" учора попри позначку публікації 2026-09-02 00:00 UTC) — записано заднім числом, дублікатів у topics немає.

**Деталі:**
- "My Machines" — підключення одного ноутбука/VM до акаунту для персональних воркфлоу
- "Team Pools" — іменовані черги воркерів з динамічним масштабуванням і гібернацією простою
- Пули не прив'язані до одного репозиторію — будь-який доступний воркер може взяти запит
- Інтеграції: AWS Lambda, Coder, Cloudflare, Vercel, E2B; self-hosted воркери тепер підтримують computer use на Linux і Mac
