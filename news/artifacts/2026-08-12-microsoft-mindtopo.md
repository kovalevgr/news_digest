---
company: Microsoft
title: "MindTopo reveals VLMs' spatial reasoning abilities"
url: https://www.microsoft.com/en-us/research/blog/mindtopo-reveals-vlms-spatial-reasoning-abilities/
published: 2026-08-12
source_url: https://www.microsoft.com/en-us/research/feed/
fetched: 2026-08-13
---

Microsoft Research introduces MindTopo, a benchmark testing topological reasoning in vision-language models — path continuity, separation, order, enclosure, and knots — finding models lag well behind humans, especially on interactive planning tasks.

## card

**Що сталося:** Microsoft Research випустила MindTopo — бенчмарк для оцінки топологічного (не евклідового) просторового мислення VLM: чи розуміє модель відношення, які зберігаються при деформації об'єкта (шлях, розділення, порядок, замкненість, вузли).

**Контекст:** Існуючі просторові бенчмарки переважно перевіряють евклідові властивості (відстань, напрямок); MindTopo спирається на класифікацію топологічних здібностей Піаже й закриває цю прогалину. Тести поділені на два рівні: reasoning (аналіз статичної сцени) і planning (послідовні дії в симуляції з контрольованим ground truth).

**Деталі:**
- П'ять топологічних властивостей у тестах: continuity, separation, order, enclosure, knots (справжні вузли проти заплутаного вигляду)
- Моделі стабільно сильніші на статичному reasoning, ніж на інтерактивному plannning, і обидва рівні — далеко позаду людини
- Помилки planning зазвичай виникають ПІСЛЯ розуміння сцени: модель втрачає відношення між об'єктами або пропонує фізично неможливу дію
- Інструменти генерації зображень мало допомагають утримувати топологічну узгодженість між кроками дій
