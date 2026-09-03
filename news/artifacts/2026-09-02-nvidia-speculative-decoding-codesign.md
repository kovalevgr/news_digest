---
company: NVIDIA
title: "Co-Designing AI Models Using Speculative Decoding for Faster LLM Inference"
url: https://developer.nvidia.com/blog/co-designing-ai-models-using-speculative-decoding-for-faster-llm-inference/
published: 2026-09-02
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-03
---

NVIDIA published the third post in its AI model co-design series, giving concrete guidelines for tuning speculative-decoding draft length across hardware/workload profiles, with SPEED-Bench numbers showing 5-6 token acceptance lengths at draft length 9-11.

## card

**Що сталося:** NVIDIA опублікував третю статтю серії про спільне проєктування (co-design) моделі та апаратного забезпечення, цього разу фокусуючись на прискоренні інференсу LLM через спекулятивне декодування.

**Контекст:** Продовження попередніх двох статей серії про co-design AI-моделей; малий "draft"-модель пропонує кілька наступних токенів, які велика "target"-модель верифікує паралельно.

**Деталі:**
- П'ять конкретних рекомендацій для підбору довжини драфта (D) залежно від профілю навантаження, зокрема формула D = 128/G − 1 для attention-обмежених навантажень
- На SPEED-Bench довжина прийнятих токенів становить 5–6 при D=9–11
- Надано готові приклади тренування на базі NVIDIA/Model-Optimizer
- Включає апаратно-специфічні оптимізації та криві продуктивності
