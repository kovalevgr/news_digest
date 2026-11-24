---
company: nvidia
title: "Get Started with GPU-Accelerated DuckDB Analytics Using the Sirius Core Extension"
url: https://developer.nvidia.com/blog/get-started-with-gpu-accelerated-duckdb-analytics-using-the-sirius-core-extension/
date: 2026-11-23
found_via: TIER-1 rss
---

NVIDIA and DuckLabs release Sirius, a GPU-native SQL engine shipped as a DuckDB core extension, letting users run supported analytical queries on NVIDIA GPUs with no SQL/schema changes (two-command install, automatic CPU fallback for unsupported features).

## card

**Що сталося:** NVIDIA та DuckLabs випускають Sirius — GPU-native SQL-движок у вигляді core-розширення DuckDB, що дозволяє виконувати підтримувані аналітичні запити на GPU NVIDIA без переписування SQL чи зміни схем (встановлення двома командами: `INSTALL sirius;` та `LOAD sirius;`); DuckDB продовжує парсити й оптимізувати кожен запит, а непідтримані запити автоматично падають назад на CPU-движок DuckDB.

**Контекст:** Sirius розроблено у співпраці University of Wisconsin–Madison та NVIDIA, проєкт з відкритим кодом; пост опубліковано 23 листопада 2026.

**Деталі:**
- Вимоги: DuckDB 2.0 та GPU NVIDIA зі сумісним драйвером; розмір розширення — близько 700 МБ.
- Бенчмарки: холодні запуски TPC-H-подібних запитів від SF100 (100 ГБ) до SF10K (10 ТБ), дані в Amazon S3.
- Прискорення: налаштовані конфігурації з двома GPU дали 3.25×–5.50× проти найкращих CPU-конфігурацій DuckDB.
- SF1K: загальний час впав з 347.3 до 63.2 секунди; SF3K: з 752.4 до 160.6 секунди (4.69×, −71% обчислювальної вартості запиту); SF10K: 729.9 с проти 2369.4 с на CPU (3.25×, −79% вартості); дефолтна конфігурація з двома GPU на SF10K не завершила тест.
- Застереження: тести використовували закріплені dev-білди, час не враховує вибірку/експорт результатів; вартість обчислень не включає запуск, сховище, S3 чи час очікування — автори зазначають, що результати залежатимуть від структури запиту, розміру даних, апаратного забезпечення та кешування.
