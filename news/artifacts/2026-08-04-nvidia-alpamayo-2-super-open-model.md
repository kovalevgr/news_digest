---
company: NVIDIA
title: "NVIDIA Alpamayo 2 Super, the Frontier Open Model for Robotaxis and Autonomous Vehicles, Now Available for Commercial Use"
url: https://blogs.nvidia.com/blog/alpamayo-2-super-open-model-now-available
published: 2026-08-04
source_url: https://blogs.nvidia.com/feed/
fetched: 2026-08-05
---

NVIDIA makes Alpamayo 2 Super, its frontier open model for robotaxis and autonomous
vehicles, available for commercial use, aimed at handling rare, complex long-tail driving
scenarios.

## card

**Що сталося:** NVIDIA відкрила Alpamayo 2 Super — відкриту reasoning-модель для роботаксі й автономних авто — для комерційного використання. Модель доступна на Hugging Face під пермісивною ліцензією OpenMDW-1.1 від Linux Foundation, що дозволяє fine-tuning, похідні моделі й комерційне поширення.

**Контекст:** Alpamayo 2 Super замінює Alpamayo 1 та 1.5 як флагман родини Alpamayo — за NVIDIA, найпоширенішої родини відкритих reasoning-моделей для автономного водіння на Hugging Face (понад 500 тис. завантажень). Побудована на NVIDIA Cosmos 3 Super Reasoner із RL-пост-тренуванням.

**Деталі:**
- Масштаб: 3x відносно попередніх 10-мільярдних моделей (Alpamayo 1/1.5).
- П'ять інтегрованих виходів для кожної дорожньої ситуації: траєкторія, chain-of-causation пояснення рішень, мета-дії (поступитися, змінити смугу, зупинитися), автолейбли для розмітки даних, VQA з 2D-прив'язкою до зображень.
- Обробляє 360°-покриття камер (фронт, боки, тил).
- Бенчмарк LingoQA: 1-ше місце серед ~40 моделей; відрив від Qwen2.5-VL 72B — 17.0 бала, Gemini 2.5 Pro — 15.1, GPT-4o — 23.2.
- Екосистема: AlpaSim, AlpaGym, датасети Physical AI, safety-валідація NVIDIA Halos у руслі ISO/PAS 8800.
