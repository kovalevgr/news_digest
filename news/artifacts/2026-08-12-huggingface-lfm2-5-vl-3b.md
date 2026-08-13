---
company: Hugging Face
title: "LFM2.5-VL-3B for Better and Faster Vision Capabilities for the Edge"
url: https://huggingface.co/blog/LiquidAI/lfm2-5-vl-3b
published: 2026-08-12
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-13
---

Liquid AI releases LFM2.5-VL-3B, a 3.1B-parameter vision-language model (SigLIP2 400M NaFlex encoder + LFM2.5-2.6B text backbone) for edge deployment, with strong screen/UI understanding and 228 tok/s on M5 Max.

## card

**Що сталося:** Liquid AI випустила LFM2.5-VL-3B — vision-language модель на 3.1 млрд параметрів (енкодер SigLIP2 400M NaFlex + текстовий бекбон LFM2.5-2.6B) для роботи на edge-пристроях.

**Контекст:** Продовжує лінійку LFM2.5, доповнюючи вже опубліковану на Hugging Face LFM2.5-2.6B (текстова модель, 4 серпня) мультимодальною версією; претрейн — близько 34 трлн токенів із вчетверо збільшеним обсягом visual-даних.

**Деталі:**
- Чотири напрями покращень: розуміння екранів/UI на різних пристроях, grounding та object detection за природномовними запитами, multi-image reasoning, покращений function calling у тексті й мультимодалі
- 40+ бенчмарків: 78–82% на ScreenSpot-v2 (розуміння екрана), 91.1% на DocVQA, 87.9% на RefCOCO (grounding), середній показник 69.4% по vision+language задачах
- Інференс: 228 ток/с на M5 Max, 20 ток/с на мобільному пристрої (~3GB пам'яті), до 11K ток/с на GPU при масштабуванні
- Доступна вже сьогодні на Hugging Face; підтримка llama.cpp, MLX, vLLM, SGLang, ONNX; є WebGPU-демо в браузері без встановлення
