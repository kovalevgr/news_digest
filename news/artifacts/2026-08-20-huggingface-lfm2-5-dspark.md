---
company: Hugging Face
title: "Up to 3.2x Faster Inference with LFM2.5-DSpark"
url: https://huggingface.co/blog/LiquidAI/lfm25-dspark
published: 2026-08-20
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-21
---

Liquid AI releases LFM2.5-DSpark draft-model checkpoints (~300M params each) for three LFM2.5 models, using speculative decoding to speed up decoding up to 2.87x on H100 and 2.54x on MacBook M4 Max with identical output quality.

## card

**Що сталося:** Liquid AI випустив LFM2.5-DSpark — чекпоінти чорнових (draft) моделей для трьох моделей родини LFM2.5, що використовують speculative decoding: легка draft-модель пропонує токени, а цільова модель перевіряє їх за один прохід, отримуючи суттєве пришвидшення декодування ціною невеликого приросту пам'яті.

**Контекст:** Продовження серії релізів LFM2.5 від Liquid AI (LFM2.5-VL-3B, LFM2.5 Q4_0 QAD-чекпоінти — обидва вже покриті раніше в серпні); якість виводу залишається ідентичною завдяки greedy-decoding верифікації.

**Деталі:**
- LFM2.5-2.6B: прискорення до 2.87× на H100, 2.27× на MacBook M4 Max; латентність function-calling нижча на 57%
- LFM2.5-1.2B-Instruct: 2.10× на H100, 2.54× на M4 Max
- LFM2.5-8B-A1B: 2.54× на H100, 1.18× на M4 Max
- Тестування на п'яти бенчмарках: MATH500, HumanEval, MBPP, GSM8K, MT-Bench (block size 9, batch size 1)
- Доступні у форматах Safetensors і GGUF на Hugging Face з підтримкою llama.cpp та SGLang з першого дня; draft-моделі містять ~300M параметрів кожна
- Код інтеграції відкритий у upstream-репозиторіях
