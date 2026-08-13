---
company: Google Research
title: "Empty shelves or lost keys? Recall is the bottleneck for parametric factuality"
url: https://research.google/blog/empty-shelves-or-lost-keys-recall-is-the-bottleneck-for-parametric-factuality/
published: 2026-08-12
source_url: https://research.google/blog/rss/
fetched: 2026-08-13
---

Google Research introduces "knowledge profiling," a framework separating encoding from recall in LLMs, finding frontier models like Gemini-3-Pro and GPT-5 encode 95-98% of facts but directly recall only 66-74% of them.

## card

**Що сталося:** Google Research представила framework "knowledge profiling", який розділяє encoding (чи факт взагалі закодований у вагах моделі) та recall (чи модель може його дістати без підказок). Флагманські моделі — Gemini-3-Pro, GPT-5 — кодують 95–98% фактів, але напряму пригадують лише 66–74% із них: знання є, але недоступне.

**Контекст:** Дослідження зсуває фокус зі "scaling дає більше знань" на "utilization — головна проблема": навіть при увімкненому reasoning ("thinking") моделі не дають відповіді на 11–12% фактів; для рідкісних фактів розрив у recall значно ширший, ніж розрив в encoding, що переосмислює класичну "long-tail problem".

**Деталі:**
- Бенчмарк WikiProfile: 2150 фактів з Wikipedia, кожен — 10 завдань (2 на encoding, 4 на knowledge, 4 multiple-choice), прямі й зворотні формулювання питань
- П'ять профілів факту: encoding failure, recall failure, direct recall, recall with thinking, inference without encoding
- Reasoning ("thinking") відновлює 40–65% фактів, які закодовані, але не пригадуються напряму, у thinking-оптимізованих моделях
- Висновок: подальші покращення факт-точності потребують кращих механізмів retrieval, а не лише більших моделей
