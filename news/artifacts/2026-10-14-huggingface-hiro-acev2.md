---
company: Hugging Face
title: "HiRO-ACEv2: Simulating extreme weather at 3 km resolution for a fraction of the cost"
url: https://huggingface.co/blog/allenai/hiro-acev2
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-14
fetched: 2026-10-15
---

Ai2 releases HiRO-ACEv2, an updated downscaling model that turns its coarse 100km ACE climate emulator output into 3km-resolution extreme-weather simulations at roughly 1/300th the cost of the reference high-resolution model X-SHiELD.

## card

**Що сталося:** Ai2 (Allen Institute for AI) випустив HiRO-ACEv2 — оновлену версію свого кліматичного емулятора HiRO-ACE, який апскейлить грубий (100 км) вихід моделі ACE до роздільної здатності 3 км і відтворює рідкісні екстремальні погодні явища (дощ, вітер, тиск) з високою точністю.

**Контекст:** HiRO-ACE складається з двох частин — ACE (AI-модель на 100 км) та HiRO (модель даунскейлінгу до 3 км); у v2 головна зміна — нова модель даунскейлінгу HiROv2, яка одразу прогнозує кілька полів високої роздільної здатності замість лише дощу.

**Деталі:**
- HiROv2 відтворює статистику екстремальних подій (включно з подіями ~1 на мільйон точок даних) з похибкою до 3% порівняно з цільовою симуляцією X-SHiELD
- Оцінка енергії тропічних циклонів точна навіть для штормів, відсутніх у тренувальних даних
- Генерація глобальних даних 3 км коштує приблизно у 300 разів дешевше за запуск X-SHiELD; для окремого регіону економія може перевищувати 100x
- Спрощена HiROv2 у розробці може бути у понад 10 разів швидшою
- Обмеження: модель прив'язана до версії ACE, узгодженої з X-SHiELD, і ще не працює з іншими кліматичними сценаріями (напр., потеплілий світ чи ERA5)
- Доступно на Hugging Face (allenai/HiRO-ACEv2), веб-демо на ace.allen.ai, стаття arXiv:2610.17693
