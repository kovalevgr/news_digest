---
company: google-research
title: "Supercharging transformer residual connections"
url: https://research.google/blog/supercharging-transformer-residual-connections/
date: 2026-11-23
found_via: TIER-1 rss
---

Google Research introduces DeepCrossAttention (DCA), which replaces standard transformer residual connections with learnable, depth-wise cross-attention that dynamically combines outputs from earlier layers, reaching the same quality in up to 5x fewer training steps.

## card

**Що сталося:** Google Research представляє DeepCrossAttention (DCA) — заміну стандартних residual-з'єднань трансформера на навчальне, depth-wise cross-attention, яке динамічно комбінує виходи попередніх шарів замість простого додавання їх з рівною вагою.

**Контекст:** DCA розвиває ідею стандартних residual-з'єднань, які зважують усі попередні виходи шарів однаково і можуть деградувати інформацію у глибоких мережах; це частина ширшого тренду динамічної residual-маршрутизації поряд з attention residuals, hyper-connections та manifold-constrained hyper-connections. Метод представлено у статті ICML 2025, опублікований сьогодні, 23 листопада, авторами Kyriakos Axiotis та Thomas Fu.

**Деталі:**
- Та ж якість, що в стандартного трансформера, за до 5× менше кроків тренування на бенчмарках C4 та LM1B.
- На LM1B: стандартний трансформер потребує 42 шари для перплексії нижче 14, DCA досягає цього з 30 шарами (−29% глибини й параметрів).
- Додає менш ніж 0.2% до загального розміру моделі.
- Може бути ініціалізований як звичайна residual-мережа, тож підходить для "дотренування" вже навчених трансформерів: у тесті це знизило перплексію LM1B на 0.19 проти 0.02 при продовженні звичайного тренування.
- Стаття доступна на arXiv (2502.06785); анонс не згадує ціни чи випуск продукту.
