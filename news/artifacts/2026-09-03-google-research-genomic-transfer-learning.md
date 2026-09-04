---
company: Google Research
title: "Transfer learning for genomic prediction in underrepresented populations"
url: https://research.google/blog/transfer-learning-for-genomic-prediction-in-underrepresented-populations/
published: 2026-09-03
source_url: https://research.google/blog/rss/
fetched: 2026-09-04
---

Google Research, with Biobank Japan/RIKEN/University of Tokyo, found that transfer learning from large European genetic datasets helps genomic-risk prediction for underrepresented populations only up to a crossover point (~15-40k target-cohort samples), after which population-specific models win.

## card

**Що сталося:** Google Research спільно з Biobank Japan, RIKEN та Токійським університетом дослідив, чи допомагають великі європейські генетичні датасети покращувати прогнозування генетичних ризиків для недостатньо представлених популяцій — і виявив, що ефект має межу.

**Контекст:** Порівнювались elastic net моделі на європейських GWAS-варіантах, крос-популяційний метааналіз (Європа + Японія) та алгоритм PRS-CSx, що враховує відмінності у зчепленні генів (linkage disequilibrium), на даних UK Biobank (Європа) та Biobank Japan (~200 000 японців), для 8 ознак.

**Деталі:**
- До ~15 000 зразків цільової популяції перенесення з європейських даних покращує точність прогнозів
- Після ~15 000+ зразків моделі, навчені спеціально на цільовій популяції, перевершують перенесені
- Для ознак зі спільною генетичною архітектурою перевага перенесення тримається довше (25–40 тис. зразків), для популяційно-специфічних ознак (напр. ліпіди) — згасає раніше
- Дослідження охопило 8 ознак: ІМТ, систолічний/діастолічний тиск, показники крові, HDL, LDL, глюкоза крові
