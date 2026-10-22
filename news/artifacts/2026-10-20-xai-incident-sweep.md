---
company: xai
title: "Using Grok Bot to detect and respond to incidents"
url: https://x.ai/news/incident-sweep
date: 2026-10-20
found_via: gap-scrape (curl r.jina.ai, anonymous — TIER-1 skipped, x.ai is jina-only kind)
---

xAI describes two new Grok Bot "AI teammates" used internally by SpaceXSI customer support: IncidentWatch detects ticket spikes signaling a possible incident, and IncidentSweep clears the resulting backlog in reviewed, approved batches — in one case closing 204 tickets in about 10 minutes.

## card

**Що сталося:** xAI розповідає про два нові "AI-товариші" Grok Bot, які служба підтримки SpaceXSI використовує для роботи з інцидентами: IncidentWatch виявляє сплески однотипних звернень, що можуть свідчити про інцидент, а IncidentSweep масово опрацьовує й закриває відповідні тікети після затвердження інженером.

**Контекст:** Це продовження попереднього анонсу Support Bot для клієнтської підтримки SpaceXSI. IncidentWatch кожні 5 хвилин переглядає тікети за останні 15 хвилин у пошуку сплесків однакової проблеми й сповіщає дежурного інженера. IncidentSweep підбирає тікети за критеріями, показує інженеру пропонований пакет і точний текст відповіді перед відправкою, і ніколи не додає тікети в пакет після затвердження.

**Деталі:**
- 18 вересня IncidentSweep закрив 204 тікети за приблизно 10 хвилин із перевіркою й затвердженням інженера підтримки.
- Раніше довелося б відповідати на кожен тікет окремо (години роботи) або використовувати масову макро-дію з меншим контролем над тим, хто отримає повідомлення.
- IncidentWatch сповіщає про ймовірний інцидент, кількість відповідних тікетів і приклади для розслідування; якщо інцидент підтверджено, інформація публікується на статус-сторінці.
