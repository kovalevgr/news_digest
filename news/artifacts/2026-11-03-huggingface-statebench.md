---
company: huggingface
title: "StateBench: Testing how language models track state changes over long documents"
url: https://huggingface.co/blog/allenai/statebench
date: 2026-11-03
found_via: rss
---

Ai2 publishes StateBench, a benchmark with four difficulty levels (grounded in Krohn-Rhodes algebraic theory) testing whether language models and architectures (transformer, Gated DeltaNet, hybrid) can track entity-state changes across long inputs; frontier models drop to ≤13% accuracy on the hardest, longest tasks.

## card

**Що сталося:** Ai2 випустили StateBench — бенчмарк для перевірки того, наскільки добре мовні моделі відстежують зміни стану сутностей у довгих вхідних даних. Чотири рівні складності (immutable assignment → reassignment → self-referential updates → assignment by reference) побудовані на алгебраїчній теорії Крона-Роудса. На найскладнішому рівні провідні моделі (Gemini 3.8 Flash, Claude Opus 5.5, GPT‑6 Sol/Luna) падають до ≤13% точності на найдовших входах.

**Контекст:** Робота спирається на теоретичні межі трансформерів щодо state tracking (arXiv 2404.08819) та на рекурентні/гібридні архітектури типу Gated DeltaNet, які переносять пам'ять між кроками. Випущено tech report, датасет на Hugging Face та код на GitHub.

**Деталі:**
- Моделі, навчені з нуля (275M-параметрів: transformer, hybrid, Gated DeltaNet) тренувались на послідовностях до 256 присвоєнь, тестувались до 64 000 (у 250 разів довше).
- Gated DeltaNet та hybrid-варіанти узагальнювались майже ідеально на перших трьох рівнях; трансформери деградували на довгих послідовностях і взагалі не навчились найскладнішого рівня.
- Варіант Gated DeltaNet з гнучкішим оновленням пам'яті лишався майже ідеальним на найскладнішому рівні аж до ~10x довжини тренування.
- Нова теорема показує, що Gated DeltaNet з невід'ємними власними значеннями розв'язує всі aperiodic-задачі та частину periodic (напр. parity) за фіксованою точністю; повне місце в ієрархії (включно з soluble-рівнем) лишається невідомим.
