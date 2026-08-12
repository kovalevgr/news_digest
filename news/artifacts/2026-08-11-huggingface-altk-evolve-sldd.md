---
company: Hugging Face
title: "Thinking of ACE? We Can Do It with Fewer Tokens"
url: https://huggingface.co/blog/ibm-research/altk-evolve-sldd
published: 2026-08-11
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-12
note: "TIER-1 rss; guest post by IBM Research on the HF blog."
---

IBM Research publishes a comparison of its ALTK-Evolve agentic-memory framework against the ACE (Agentic Context Engineering) approach: both let agents learn from task history without weight updates, but ALTK-Evolve's configurable memory retrieval reaches comparable-or-better AppWorld accuracy at roughly 15-40% of ACE's inference token cost.

## card

**Що сталося:** IBM Research (гостьовий пост на блозі Hugging Face) опублікувала порівняння свого фреймворку агентної памʼяті ALTK-Evolve з підходом ACE (Agentic Context Engineering) — обидва дозволяють агентам вчитися на власній історії задач без оновлення ваг моделі.

**Контекст:** Обидві системи відмовляються від стиснення накопичених уроків у загальні summary, зберігаючи детальні, поелементні репозиторії з лічильниками частоти — це запобігає "brevity bias" і "context collapse" (терміни ACE). Розходяться в стратегії: ACE вставляє повний playbook на кожному кроці інференсу, ALTK-Evolve робить інʼєкцію памʼяті налаштовуваною (мінімальний набір або задаче-специфічна вибірка).

**Деталі:**
- Бенчмарк AppWorld, 168 задач
- DeepSeek-V3.2: ACE — 80.4/73.2 (TGC/SGC) за 634K токенів; ALTK-Evolve — 89.3/80.4 за 263K токенів
- gpt-oss-120b: ACE — 54.8/35.7 за 777K токенів; ALTK-Evolve — 56.0/37.5 за 116K токенів
- На сильнішій моделі ALTK-Evolve досягає порівнянної/вищої точності приблизно за 40% вартості інференсу ACE; на слабшій — приблизно за 15%
