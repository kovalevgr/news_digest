---
company: Google Research
title: "How Diffusion Controller unifies and simplifies AI image generation"
url: https://research.google/blog/how-diffusion-controller-unifies-and-simplifies-ai-image-generation/
source_url: https://research.google/blog/rss/
published: 2026-09-29
fetched: 2026-09-30
---

Google Research introduces Diffusion Controller, a lightweight add-on network that steers image generation toward better prompt alignment without modifying the base model, treating generation as a continuous control problem.

## card

**Що сталося:** Google Research представила Diffusion Controller — легку додаткову мережу, яка "керує" процесом генерації зображень для кращої відповідності промпту, не змінюючи базову модель; підходить як "демпфер керування", що можна приєднати навіть до closed-source моделей.

**Контекст:** Позиціонується як альтернатива LoRA — поточному галузевому стандарту для адаптації дифузійних моделей.

**Деталі:**
- Тестування на Stable Diffusion v1.4: 90% winrate проти базової моделі
- Перевершує LoRA на бенчмарку Human Preference Score v2
- Кращі результати відповідності промпту за оцінками людей
