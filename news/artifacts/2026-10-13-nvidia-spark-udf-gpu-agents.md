---
company: NVIDIA
title: "How to Rewrite Apache Spark UDFs for GPU Acceleration with AI Agents"
url: https://developer.nvidia.com/blog/rewrite-apache-spark-udfs-gpu-acceleration-ai-agents/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-10-13
fetched: 2026-10-14
---

NVIDIA releases "cuDF skills for Apache Spark," an agent skill pack that rewrites CPU-bound Spark UDFs into GPU-accelerated SQL/cuDF/CUDA implementations, reporting 20x+ speedups and one production rewrite cutting 274.55 hours to 12.78 hours on a 600-billion-row job.

## card

**Що сталося:** NVIDIA випускає cuDF skills for Apache Spark — пакет навичок для AI-агентів, що переписують CPU-прив'язані Spark UDF у GPU-прискорені реалізації (SQL / cuDF Java API / CUDA через JNI), щоб їх міг виконувати cuDF plugin for Spark замість падіння в CPU-режим.

**Контекст:** CPU-прив'язані UDF у Spark змушують cuDF plugin відкочуватися на CPU з додатковими конвертаціями даних рядок↔колонка — саме ці конверсії й CPU-виконання є вузьким місцем, який skills усувають.

**Деталі:**
- 4 стадії роботи агента: генерація тестів (gen-test), конвертація (convert-to-{sql|cudf|cuda}), бенчмаркінг, оптимізація — з циклами верифікації на кожному кроці
- Заявлені прискорення: понад 20x (у прикладах статті — 22x+ у Spark-джобах)
- Велика техкомпанія-споживач конвертувала 30+ продакшн UDF цим методом
- Один UDF, що впливав на 3000+ джобів, скоротив час оператора з 274.55 до 12.78 годин на завданні з 600 млрд рядків (16 ТБ вхід, 17.4 ТБ вихід)
- Доступно на GitHub: NVIDIA/cudf-spark; встановлення через `npx skills add NVIDIA/cudf-spark --skill '*'`
- За словами NVIDIA, переписування за допомогою агентів займає години замість днів/тижнів (конкретних доларових цифр економії стаття не наводить)
