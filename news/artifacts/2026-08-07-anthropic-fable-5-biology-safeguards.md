---
company: Anthropic
title: "Improving Fable 5's biology safeguards"
url: https://www.anthropic.com/news/improving-fable-5-s-biology-safeguards
published: 2026-08-07
source_url: https://www.anthropic.com/news
fetched: 2026-08-07
note: "Found via gap-scrape WebFetch (no RSS feed exists for Anthropic)."
---

Anthropic refined Claude Fable 5's biology classifiers to substantially reduce false
positives, enabling the model to assist with a broader range of legitimate biology and
healthcare tasks while maintaining safeguards against dual-use misuse.

## card

**Що сталося:** Anthropic оновила біологічні safety-класифікатори Claude Fable 5, скоротивши хибні спрацьовування на біологічних запитах приблизно на 85%. Модель тепер може допомагати з ширшим колом легітимних медичних та освітніх завдань, зберігаючи блокування dual-use запитів.

**Контекст:** Механізм безпеки Fable 5 перенаправляє заблоковані біологічні запити на менш здібну модель Opus 5; за словами компанії, оновлення впроваджувалися протягом останніх кількох тижнів.

**Деталі:**
- Кількість fallback-спрацьовувань на біологічних запитах знижено на ~85% across product surfaces; загальне зниження fallback-ів: 67% на Claude.ai, 55% на Cowork, 17% на Claude Code, 7% на Claude Platform.
- Тепер дозволено: інтерпретація лабораторних результатів, розбір симптомів, вивчення біології в освітньому контексті, підтримка клінічних завдань для медичних працівників.
- Далі блокуються dual-use напрями: вірусологічні й токсикологічні запити, задачі молекулярного дизайну, професійні біологічні дослідження, розробка ліків.
- Процес: переписана «конституція» класифікатора з детальними винятками для benign use; фідбек від внутрішніх і зовнішніх експертів; нові тренувальні дані на основі оновленої конституції; перетренування з верифікацією, що шкідливий контент і далі блокується.
- Anthropic визнає, що хибні спрацьовування частково залишаться: класифікатор і далі блокує деякий дуже низькоризиковий контент «із надлишку обережності».
