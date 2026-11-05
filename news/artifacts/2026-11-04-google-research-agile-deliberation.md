---
company: google-research
title: "Agile Deliberation: How AI helps humans define the gray areas"
url: https://research.google/blog/agile-deliberation-how-ai-helps-humans-define-the-gray-areas/
date: 2026-11-04
found_via: rss (TIER-1)
---

Google Research introduces Agile Deliberation, a framework turning the building of image classifiers for subjective categories (e.g. "healthy food") into an iterative conversation: a VLM surfaces borderline images that challenge the user's current definition, and feedback drives automatic prompt refinement.

## card

**Що сталося:** Google Research представили Agile Deliberation — метод побудови класифікаторів зображень для суб'єктивних категорій (напр. "здорова їжа") як ітеративного діалогу: спершу користувач ділить широке поняття на підкатегорії-включення і явні винятки, потім vision-language модель показує межові приклади, що випробовують поточне визначення, і правки користувача автоматично уточнюють промпт.

**Контекст:** Підхід розвиває ідею active learning, але вибирає приклади для розкриття неоднозначності визначення, а не для зниження невизначеності моделі — відповідь на проблему стандартних пайплайнів розмітки, які вимагають жорстких міток до того, як саме визначення користувача ще сформувалося.

**Деталі:**
- Перевірено у 18 живих сесіях (~1.5 години кожна) на двох доменах: "Healthy Food" і "Pay-to-Play" (клікбейтні обіцянки нагород в іграх/розвагах).
- Порівняння з трьома базовими підходами: zero-shot класифікатор, автоматичний "modeling collaborator" без участі користувача, і ручна депутація (таблиці, промпти вручну).
- Класифікатори учасників з Agile Deliberation перевершили всі базові підходи, з найбільшим відривом на найскладніших суб'єктивних прикладах; ручна депутація часто не покращувала zero-shot точність або навіть погіршувала її.
- Учасники повідомили значно менше зусиль, стресу й фрустрації порівняно з ручним промпт-інженірингом; кожен учасник надав перевагу Agile Deliberation над ручними методами.
