---
company: Microsoft
title: "Broadening access to Skala creates a faster path to predictive DFT"
url: https://www.microsoft.com/en-us/research/blog/broadening-access-to-skala-creates-a-faster-path-to-predictive-dft/
published: 2026-08-20
source_url: https://www.microsoft.com/en-us/research/feed/
fetched: 2026-08-21
---

Microsoft Research releases Skala 1.1, an updated deep-learning exchange-correlation functional for density functional theory (DFT), trained on 2.5x more data and now integrated into CP2K with more packages in progress.

## card

**Що сталося:** Microsoft Research випустив Skala 1.1 — оновлену версію свого DFT-функціонала на основі глибокого навчання для обчислювальної хімії, натреновану на вдвічі більшому обсязі даних, ніж попередня версія, з розширеною доступністю для екосистеми та новим живим бенчмарк-звітом продуктивності.

**Контекст:** Розвиток проєкту Skala — функціонала обмінно-кореляційної енергії для DFT, який Microsoft Research розробляє як альтернативу традиційним гібридним функціоналам; співпраця включає партнерство з Center for Advanced Systems Understanding (CASUS) для інтеграції в CP2K.

**Деталі:**
- Натренований на 2.5× більшій кількості даних порівняно з попередньою версією
- Зважена середня похибка 2.8 ккал/моль на бенчмарку GMTKN55, перевершує провідні гібридні функціонали
- Перше місце у 32 з 55 категорій GMTKN55
- Обчислювальна ефективність зіставна з напівлокальними meta-GGA функціоналами
- Вже інтегрований у CP2K (open-source), інтеграція триває для Psi4, FHI-aims, ORCA та VASP
- Доступний через open-source реліз на базі PySCF; новий живий звіт продуктивності відстежує ефективність на різних апаратних платформах
