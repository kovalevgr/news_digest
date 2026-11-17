---
company: nvidia
title: "Post-Training NVIDIA Nemotron to Increase Accuracy in Your Scientific Domain"
url: https://developer.nvidia.com/blog/post-training-nvidia-nemotron-to-increase-accuracy-in-your-scientific-domain/
date: 2026-11-16
found_via: rss (developer.nvidia.com/blog/feed)
---

NVIDIA publishes a post-training recipe for Nemotron 3.5 Super VL on scientific tasks (drug-metabolism prediction as the worked example), combining RLVR with GRPO/LoRA via NeMo Gym and NeMo RL, reporting +12% accuracy from SFT and a further +17% from RL.

## card

**Що сталося:** NVIDIA опублікувала рецепт пост-тренування моделі Nemotron 3.5 Super VL для наукових задач, на прикладі передбачення метаболізму ліків: експериментальні CSV-дані перетворюються на пари промпт-відповідь, а верифікатор оцінює відповідь моделі (RLVR — reinforcement learning with verifiable rewards, без потреби в людських перевагах).

**Контекст:** Тренування використовує GRPO з LoRA через інфраструктуру NeMo Gym (середовище) та NeMo RL (фреймворк пост-тренування); винагорода — подібність Моргана-відбитків за Таніото (радіус 2, 2048 біт), яку можна замінити іншою метрикою оцінки.

**Деталі:**
- При бюджеті виводу 16 384 токени SFT підвищив точність на 12%, подальше RL додало ще 17%.
- Дані — з MetxBioDB (база експериментально підтверджених реакцій біотрансформації); згадано також датасет Nemotron RL Litmus-Bench V2.0 для молекулярних властивостей.
- Опційна дистиляція: сильніша вчителька-модель (Claude Sonnet 5.5) згенерувала ланцюжки міркувань; з 1934 тренувальних промптів залишено 1123 траси за порогом Таніото ≥0,7 для розігріву студента перед RL.
- Налаштування: RL-прогін на 16 GPU (4 вузли×4) за 100 кроків, learning rate 1e-6; SFT — 55 кроків, learning rate 1e-5. Nemotron 3.5 Super VL лідирує на 7 з 11 наукових бенчмарків (75,9 на ChemBench, 39 на ether0).
