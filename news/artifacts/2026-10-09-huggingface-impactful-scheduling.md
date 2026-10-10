---
company: Hugging Face
title: "Impactful scheduling for GPU clusters"
url: https://huggingface.co/blog/allenai/impactful-scheduling
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-09
fetched: 2026-10-10
---

Ai2 (Allen Institute for AI) replaces its priority-based GPU scheduler with a fair-share system — per-team GPU time budgets, hierarchical fair-share with a 7-day lookback, a minimum-runtime "scheduling contract," and time-slicing — across its 88–1024 GPU H100/B200/B300 clusters, cutting debug-job p90 wait from 2h to 30s while holding 98% occupancy.

## card

**Що сталося:** Ai2 замінює свій пріоритетний планувальник GPU-кластерів на систему справедливого розподілу: бюджети GPU-часу для команд/проєктів, ієрархічне fair-share планування з ковзним вікном 7 днів, "контракт" на мінімальний гарантований час виконання (до 8 годин) та time-slicing для м'якого виведення нездорових хостів з черги.

**Контекст:** Пост опубліковано на блозі Hugging Face інфраструктурною командою Ai2; система розвиває ідеї відомих fair-share планувальників (Hadoop Fair Scheduler, SLURM Fair Tree, YARN Fair Scheduler), застосовані до кластерів 88–1024 GPU (H100, B200, B300).

**Деталі:**
- За 30 днів тестування команди отримали 98% належних їм GPU-годин (13 з 15 команд — щонайменше 95%, найгірший випадок — 90%).
- Завантаження кластера залишилось на рівні 98% до і після зміни при попиті у 2–3 рази вищому за ємність; 18% відданого GPU-часу було невиділеним резервом.
- p90 очікування для debug-завдань впало з 2 годин до 30 секунд (симулятор прогнозував 6 год → 5 хв); на найбільшому H100-кластері медіана черги впала з 5 хв до 24 с, p90 — з 2.8 год до 1.8 год.
- Кількість ремонтів, що вимагали ручного втручання, впала на 74%.
- Проблема: інтерактивні сесії страждають від 8-годинного ліміту захисту — команда планує окремий CPU-кластер і відновлювані сесії; також досліджують фрагментацію ємності для дуже великих завдань.
