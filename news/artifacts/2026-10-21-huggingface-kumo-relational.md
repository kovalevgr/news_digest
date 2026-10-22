---
company: huggingface
title: "NVIDIA Kumo Relational Outperforms Supervised Machine Learning on Relational Data, No Training Required"
url: https://huggingface.co/blog/nvidia/kumo-relational
date: 2026-10-21
found_via: TIER-1 rss (huggingface.co/blog/feed.xml)
---

NVIDIA introduces Kumo Relational, a pre-trained relational foundation model that predicts directly on enterprise databases in a single forward pass via in-context learning (up to 10,000 historical examples), outperforming supervised relational deep learning and AutoGluon ensembles (+8% mean reciprocal rank on SAP SALT) across 41 tasks on 15 databases.

## card

**Що сталося:** NVIDIA представляє Kumo Relational — попередньо треновану реляційну фундаментну модель, що робить прогнози безпосередньо на корпоративних базах даних за один прямий прохід, без завдання-специфічного тренування чи інженерії ознак.

**Контекст:** Модель попередньо тренована на синтетичних реляційних даних і використовує навчання в контексті (in-context learning) з до 10 000 історичних прикладів; доступна через відкриту бібліотеку NVIDIA для структурованих даних або як NVIDIA NIM.

**Деталі:**
- На 41 задачі з 15 баз даних перевершує supervised relational deep learning та експертно сконструйовані gradient-boosted tree пайплайни.
- Перевершує ансамблі AutoGluon на 8% за mean reciprocal rank на бенчмарку SAP SALT.
- Не вимагає тренування під конкретну задачу чи ручної інженерії ознак.
