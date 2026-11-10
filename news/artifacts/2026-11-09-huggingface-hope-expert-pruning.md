---
company: huggingface
title: "Your Experts Have Partners. There's HOPE for Keeping Them Together"
url: https://huggingface.co/blog/amazon/higher-order-pruning-experts
date: 2026-11-09
found_via: rss
---

Amazon researchers introduce HOPE (Higher-Order Pruning of Experts), a second-order MoE expert-pruning method (arXiv:2609.18916) that models pairwise expert interactions rather than scoring experts independently; it beats REAP/MAN/EAN/Frequency baselines, with up to +6.1% on agentic coding tasks at 50% pruning on Qwen3.5 and GLM-4.5-Air.

## card

**Що сталося:** Amazon Research представила HOPE — метод прунінгу експертів MoE-моделей другого порядку, що враховує парні взаємодії між експертами (а не оцінює кожного окремо, як попередні методи).

**Контекст:** MoE-моделі тримають усіх експертів у пам'яті під час інференсу, хоча активна лише частина на кожен токен. HOPE будує матрицю парних взаємодій експертів на калібрувальному датасеті й розв'язує квадратичну оптимізацію для вибору, кого видалити; діагональ матриці відтворює ранжування методу REAP (Spearman ρ = 0.988), а виграш пояснюється саме позадіагональними взаємодіями. Протестовано на Qwen3.5-122B/35B та GLM-4.5-Air.

**Деталі:**
- Середній ранг серед 5 методів: 2.07; на рівні прунінгу 50% — 1.58 проти 2.42 у найближчого конкурента (REAP).
- Виграш до +6.1% на агентних coding-задачах над найкращим альтернативним методом.
- Qwen3.5-35B-A3B при 50% прунінгу: SWE-Bench Pro 42.3 (HOPE) проти 41.8 (без прунінгу) і 36.2 (REAP).
- Розв'язання квадратичної оптимізації — ~1–2 с на шар; відкритий код github.com/awslabs/HOPE, вихід — стандартний HF-чекпойнт без змін у vLLM/SGLang.
- Обмеження: перевага зменшується при низьких рівнях прунінгу (10–20%); кожен шар прунується незалежно, крос-шарова версія — попередня.
