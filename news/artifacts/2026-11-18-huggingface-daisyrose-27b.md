---
company: huggingface
title: "DaisyRose-27B: Pushing the Frontier of Post-Training Efficiency"
url: https://huggingface.co/blog/RadixArk/daisyrose-27b-pushing-the-frontier-of-post-trainin
date: 2026-11-18
found_via: rss (huggingface.co/blog/feed.xml)
---

RadixArk releases DaisyRose-27B, an RL post-trained Qwen3.8-27B fine-tune for long-horizon agent tasks (sessions up to 1M tokens), trained with its open-source asynchronous Miles framework, released under Apache 2.0.

## card

**Що сталося:** RadixArk (новий автор на Hugging Face) випустила DaisyRose-27B — свою першу модель, побудовану на базі Qwen3.8-27B і донавчену для довгих агентних задач (сесії до 1M токенів), зі збереженою архітектурою, токенайзером, розумінням зображень і контекстом 256K токенів базової моделі.

**Контекст:** Пост-тренування виконане через reinforcement learning у власному відкритому асинхронному фреймворку Miles (агент продовжує працювати, поки модель тренується), на наборі ~1 200 курованих задач, побудованих навколо помилок базової моделі; "harness summarization" згортає дуже довгі сесії в кілька траєкторій. Тренування зайняло 18 днів на 144 GPU H200.

**Деталі:**
- Terminal Bench 4.1: 5.6 → 12.0 (найбільший прирост).
- Terminal Bench 2.1: 73.0 → 75.5; DeepSWE v1.1: 42.2 → 46.2; SWE Bench Pro v2: 91.3 → 94.7.
- HLE (text-only): 33.9 → 34.3; IFBench: 79.5 → 82.4; GPQA Diamond: 89.2 → 90.7.
- Чекпоінти (BF16, FP8, NVFP4) випущені під ліцензією Apache 2.0.
