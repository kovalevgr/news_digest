---
company: nvidia
title: "Reducing Rollout Bottlenecks in Reinforcement Learning with NVIDIA Dynamo"
url: https://developer.nvidia.com/blog/reducing-rollout-bottlenecks-in-reinforcement-learning-with-nvidia-dynamo/
date: 2026-11-19
found_via: rss (developer.nvidia.com/blog/feed)
---

NVIDIA details how Dynamo's KV-aware routing, ModelExpress weight distribution, and automatic worker recovery address rollout-generation bottlenecks (idle workers, redundant prefix processing, slow weight updates) in RL training, citing customer-reported speedups.

## card

**Що сталося:** NVIDIA показала, як Dynamo усуває вузькі місця генерації rollout'ів у reinforcement learning: нерівномірний час завершення rollout'ів (швидкі воркери простоюють), повторна обробка спільних префіксів промптів і повільне розповсюдження нових ваг моделі між воркерами.

**Контекст:** Це продовження серії технічних постів NVIDIA про Dynamo як інфраструктуру для inference та — тепер — для RL-тренування; Dynamo вже інтегрована з verl, NeMo RL, Slime та prime-rl.

**Деталі:**
- KV-aware routing балансує повторне використання KV-кешу з навантаженням воркерів, щоб запити зі спільним префіксом потрапляли туди, де кеш уже є.
- ModelExpress дозволяє воркерам копіювати ваги напряму з інших GPU через NIXL замість завантаження зі сховища; дельта-передача надсилає лише стиснені зміни між версіями.
- Recovery виявляє відмови воркерів, перенаправляє запити на здорові воркери та додає заміни в маршрутизацію після готовності (з можливістю мігрувати запити "на льоту").
- CoreWeave: оновлення ваг моделі до 15x швидше з Dynamo + ModelExpress. H Company: середній час кроку тренування знижено до 20%, GPU-годин — до 5%.
