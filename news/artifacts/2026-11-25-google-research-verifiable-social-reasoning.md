---
company: google-research
title: "Verifiable Social Reasoning for LLM Assistants"
url: https://research.google/blog/verifiable-social-reasoning-for-llm-assistants/
date: 2026-11-25
found_via: TIER-1 rss
---

Google Research introduces an evaluation framework (extending the Concordia library) and 20,000+-example open dataset testing whether LLM assistants can infer a hidden motive from a user's one-sided account of a social situation; across 12 evaluated models, accuracy drops when events are filtered through the user's perspective.

## card

**Що сталося:** Google Research представляє фреймворк для оцінки того, чи здатні LLM-асистенти визначити скритий мотив людини на основі односторонньої, суб'єктивної розповіді користувача про соціальну ситуацію. Кожному агенту в симуляції призначається скритий мотив, що дає перевірну ("verifiable") еталонну відповідь для, за своєю природою, суб'єктивних питань повсякденної соціальної взаємодії. Застосувавши фреймворк до 12 LLM, команда виявила, що точність падає, коли асистент чує про події лише через призму сприйняття користувача, а не напряму.

**Контекст:** Симуляції розширюють відкриту бібліотеку Concordia від Google; статтю опубліковано 25 листопада 2026 авторами Zorik Gekhman та Amir Taubenfeld (Google Research).

**Деталі:**
- Відкритий датасет містить понад 20 000 згенерованих прикладів.
- Оцінено 12 LLM на здатності визначати скритий мотив.
- Правильність перевіряє LLM-суддя, який звіряє, чи асистент визначив скритий мотив цілі.
- Фреймворк і датасет опубліковані на GitHub, стаття — на arXiv (2609.17496).
