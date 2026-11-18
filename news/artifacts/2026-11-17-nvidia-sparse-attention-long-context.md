---
company: nvidia
title: "Co-Designing Sparse Attention for Efficient Long-Context Inference"
url: https://developer.nvidia.com/blog/co-designing-sparse-attention-for-efficient-long-context-inference/
date: 2026-11-17
found_via: rss (developer.nvidia.com/blog/feed)
---

NVIDIA publishes a practical guide to co-designing trained-in sparse attention for long-context inference, using a production FP8 kernel to sweep indexer design choices and distill eight concrete design guidelines for efficient NVIDIA-GPU deployment.

## card

**Що сталося:** NVIDIA опублікувала технічний гайд із ко-дизайну "sparse attention" (розрідженої уваги), вбудованої в модель під час тренування, для ефективного інференсу на довгому контексті. На продакшн FP8-ядрі протестували різні варіанти дизайну indexer'а (компонента, що відбирає ключі) і звели результати у вісім конкретних рекомендацій.

**Контекст:** Проблема: вартість dense attention росте з довжиною контексту (на 128K токенів вона домінує у prefill), а sparse attention зменшує вартість core attention, але сам indexer все ще оцінює кожен ключ — у DeepSeek V3.2 indexer + Top-k займають 47% часу prefill-шару, тобто вартість лише переміщується, а не зникає.

**Деталі:**
- Розмір групи decode: при зростанні group size у 16 разів час decode змінився лише на ~2% (пам'ять домінує); правило — тримати G×(D+1) в межах одного Tensor Core tile (~200 рядків).
- Кількість key heads: при зростанні з 1 до 8 key heads час decode зріс у 7.6x, а prefill — лише у 1.3-1.6x; рекомендація — один key head з cross-head reduction.
- FP16-епілог дав прискорення decode у 1.31x, а FP16-акумуляція — до 1.45x в одній конфігурації.
- "Guess-verify-refine" метод повторного використання вибірки з попереднього decode-кроку був у 2.1-2.4x швидшим за стандартний radix select на DeepSeek V3.2 та V4.
- Посилання на готові реалізації: fused Top-k у TensorRT-LLM та open-source selective Top-k у FlashInfer.
