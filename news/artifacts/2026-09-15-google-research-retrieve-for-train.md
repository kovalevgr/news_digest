---
company: Google Research
title: "Bypassing inference bottlenecks: Accelerating complex AI search with Retrieve-for-Train"
url: https://research.google/blog/bypassing-inference-bottlenecks-accelerating-complex-ai-search-with-retrieve-for-train/
source_url: https://research.google/blog/rss/
published: 2026-09-15
fetched: 2026-09-16
---

Google Research introduces Retrieve-for-Train, a framework that trains a compact 53.9M-parameter diffusion model offline (via an RL-trained fan-out model generating labeled data) to map queries directly to complete search-result sets in one non-autoregressive pass, replacing expensive inference-time reasoning. Reports 12-20x speedup over autoregressive fan-out approaches (sub-second vs. up to 50s at large batch sizes) while beating zero-shot and Best-of-N baselines on two retrieval tasks.

## card

**Що сталося:** Google Research представляє Retrieve-for-Train — фреймворк офлайн-RL-тренування компактної дифузійної моделі (53.9M параметрів), яка за один непослідовний прохід генерує повний набір результатів пошуку замість дорогого inference-time міркування.

**Контекст:** Вирішує дві проблеми складного AI-пошуку: паразитне дублювання підзапитів (paraphrastic collapse) та затримку авторегресивних підходів, які заважають повертати узгоджені набори результатів у продакшн-масштабі. RL-тренована fan-out модель генерує підзапити з композитною винагородою (обґрунтованість, різноманітність за Vendi Score, семантична відповідність запиту) і офлайн синтезує дані для тренування дифузійної моделі.

**Деталі:**
- 12-20x пришвидшення проти авторегресивного fan-out
- Авторегресивний підхід — до ~50 секунд затримки при великих батчах; Retrieve-for-Train — від часток секунди до кількох секунд
- Перевершує zero-shot та Best-of-N бейзлайни на двох задачах пошуку
- Прибирає потребу в довгих chain-of-thought токенах
