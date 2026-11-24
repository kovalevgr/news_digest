---
company: huggingface
title: "RoboTrack: Point tracking for real-world robotic manipulation"
url: https://huggingface.co/blog/allenai/robotrack
date: 2026-11-23
found_via: TIER-1 rss
note: "Same story also covered in news/radar/research-institutes.md (2026-11-23, allenai.org/blog/robotrack URL) — different URL/host, kept in both per workflow (company topics vs radar are separate systems)."
---

Allen Institute for AI (Ai2) introduces RoboTrack: a benchmark + synthetic training-data suite for point tracking in robotic manipulation, plus two new trackers (RoboTracker, RoboTracker-Warp), finding leading trackers perform notably worse on real manipulation video than on existing robotics benchmarks.

## card

**Що сталося:** Ai2 представляє RoboTrack — бенчмарк і набір синтетичних тренувальних даних для point tracking (трекінгу точок) у задачах роботизованого маніпулювання, а також два нові трекери, RoboTracker і RoboTracker-Warp. Дослідження показує, що провідні трекери працюють помітно гірше на реальному відео маніпуляцій, ніж на існуючих бенчмарках з робототехніки.

**Контекст:** Point tracking стежить за позицією точки через кадри відео, включно з моментами оклюзії та повторної появи; робототехнічні системи часто використовують готові (off-the-shelf) трекери, тож автори перевірили, чи тримаються вони на різних сценах, ракурсах і взаємодіях з об'єктами. Тренування на синтетичних даних з Ai2's MolmoSpaces частково закриває цей розрив.

**Деталі:**
- RoboTrack-Bench: 307 відео з людською анотацією (DROID, Ego-Exo4D, MolmoAct 2, EgoVerse), 2522 перевірені точкові треки, 33 синхронізовані двокамерні пари.
- Чотири провідні трекери (CoTracker3, BootsTAPNext, AllTracker, CoWTracker) показали AJ на 3.0–6.6 нижче на RoboTrack-Bench, ніж на RoboTAP (CoWTracker: 70.5 → 63.9).
- RoboTrack-15M: синтетичний датасет із 3000 відео з 300 симульованих будинків, 5000 треків на відео — 15 млн треків загалом, побудований на MolmoSpaces.
- RoboTracker (дотренований з AllTracker, ~17M параметрів): AJ на RoboTrack-Bench зріс з 62.6 до 63.4. RoboTracker-Warp (дотренований з CoWTracker, ~1B параметрів): AJ зріс з 63.9 до 66.0, найкращий результат на 4 з 5 бенчмарків.
- Демо на роботі (пайпетування у вологій лабораторії): point tracking завершив перенесення у 17 з 20 спроб проти 8 для масок об'єктів (SAM3) і 5 для оптичного потоку (RAFT); з частковою оклюзією — 7 з 10 проти 1 для масок.
- Доступність: моделі, дані, код, сторінка проєкту й технічний звіт опубліковані на Hugging Face, GitHub і сайті проєкту. Ваги RoboTracker-Warp — лише для некомерційного використання.
