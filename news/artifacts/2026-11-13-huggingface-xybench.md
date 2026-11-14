---
company: huggingface
title: "XYBench: Helping with the problem behind the question"
url: https://huggingface.co/blog/allenai/xybench
date: 2026-11-13
found_via: rss
---

Ai2 publishes XYBench, an 8,115-question benchmark (built from Stack Overflow, Stack Exchange, and WikiHow) testing whether LLMs recognize when a user's stated request (Y) rests on a misconception about their real underlying goal (X) — models mention Y-solutions far more than X-solutions and steer users away from the mistaken approach less often than human reference answers. Won Best Resource Paper at EMNLP 2026.

## card

**Що сталося:** Ai2 опублікував XYBench — бенчмарк із 8 115 питань (Stack Overflow, Stack Exchange, WikiHow), що перевіряє, чи розпізнає модель ситуацію, коли заявлений запит користувача (Y) насправді базується на хибному уявленні про справжню мету (X), і чи пропонує відповідь, орієнтовану на X. Claude Sonnet 4.5 генерує WikiHow-похідні питання і слугує автоматичним суддею (валідованим людьми).

**Контекст:** Нагорода Best Resource Paper на EMNLP 2026; пряме продовження теми "evals у реальному використанні" агентів/моделей.

**Деталі:**
- Моделі згадують рішення для Y значно частіше, ніж для X (75-86% проти 59-71% на Stack Overflow).
- Лише 35-41% відповідей фокусуються переважно на X.
- Моделі відводять користувача від хибного підходу рідше, ніж людські референсні відповіді (47-60% проти 79%).
- При виборі між двома готовими відповідями модель обирає орієнтовану на мету (X) у 71-84% випадків — але сама пише таку відповідь значно рідше (розрив "розпізнавання проти генерації").
