---
company: Hugging Face
title: "How Much Memory Does Your Agent Actually Need?"
url: https://huggingface.co/blog/ibm-research/altk-evolve-hmm
published: 2026-08-18
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-19
---

IBM Research uses its ALTK-Evolve framework to test how much self-distilled behavioral guidance an agent needs, finding the optimal memory strategy depends on model strength: weak models benefit most from curated retrieval, strong models from full guideline injection, and saturated models see no gain either way.

## card

**Що сталося:** IBM Research дослідив на фреймворку ALTK-Evolve (вилучення поведінкових гайдлайнів з траєкторій агента), скільки "пам'яті" реально потрібно AI-агенту, протестувавши 8 моделей (30B–745B параметрів) на бенчмарку AppWorld (585 багатокрокових завдань).

**Контекст:** ALTK-Evolve — фреймворк IBM Research для агентної пам'яті; порівнюється з попереднім підходом ACE (менша токен-вартість при порівнянній чи кращій точності), продовження серії досліджень про agentic memory.

**Деталі:**
- Слабкі моделі (gpt-oss-120b): куровану вибірку (curated retrieval) дає приріст 16.1пп при збільшенні токенів лише на 5% — краще за повне впорскування гайдлайнів
- Сильні моделі (DeepSeek-V3.2, Claude): повні гайдлайни дають оптимальний результат — приріст TGC 9.5пп і 4.1пп відповідно
- "Насичені" моделі (GLM-5): вимірного приросту немає за жодної стратегії пам'яті
- Висновок авторів: agentic memory — це не фіча "увімкнув і забув", а дозування, яке треба калібрувати під конкретну модель
