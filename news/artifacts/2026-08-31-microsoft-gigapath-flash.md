---
company: Microsoft
title: "GigaPath-Flash and GigaTIME-Flash: Toward population-scale discovery with efficient pathology foundation models"
url: https://www.microsoft.com/en-us/research/blog/gigapath-flash-and-gigatime-flash-toward-population-scale-discovery-with-efficient-pathology-foundation-models/
published: 2026-08-31
source_url: https://www.microsoft.com/en-us/research/feed/
fetched: 2026-09-01
---

Microsoft Research released GigaPath-Flash and GigaTIME-Flash, two efficient pathology foundation models built to cut the compute cost of population-scale cancer research while keeping most of the predictive accuracy of their larger predecessors. Both ship open-weight (Apache 2.0) on Hugging Face.

## card

**Що сталося:** Microsoft Research випустила GigaPath-Flash і GigaTIME-Flash — компактні версії своїх фундаментальних моделей для патології, розраховані на масштабні дослідження раку з набагато меншими обчислювальними витратами.

**Контекст:** Обидві моделі будуються на попередніх GigaPath і GigaTIME, зберігаючи точність оригіналів при значно нижчих вимогах до ресурсів — це дозволяє дослідникам аналізувати значно більші когорти пацієнтів дешевше.

**Деталі:**
- GigaPath-Flash: 22М-параметровий тайл-енкодер + 21М-параметровий слайд-енкодер, ~97% продуктивності GigaPath при ~50x менших обчисленнях
- GigaTIME-Flash (передбачає просторові карти білків з H&E-зображень): ~6x швидше, ~8x менше памʼяті, точність на рівні або вища за оригінал на кількох типах раку
- Обидві моделі — відкриті ваги під ліцензією Apache 2.0 на Hugging Face
