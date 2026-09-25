---
company: Hugging Face
title: "Accelerating vision-language models with LFM2.5-VL-DSpark"
url: https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark
source_url: https://huggingface.co/blog/feed.xml
published: 2026-09-24
fetched: 2026-09-25
---

Liquid AI releases LFM2.5-VL-DSpark, an experimental speculative-decoding draft model for its LFM2.5-VL-3B vision-language model, delivering up to 3.13x faster on-device decoding at just 8.9% parameter overhead.

## card

**Що сталося:** Liquid AI випустив LFM2.5-VL-DSpark — експериментальну draft-модель для спекулятивного декодування поряд з базовою vision-language моделлю LFM2.5-VL-3B, що прискорює inference без втрати якості.

**Контекст:** Драфтер додає лише 280M параметрів (8.9% оверхеду до 3B базової моделі) і використовує 4-шаровий attention-only дизайн з блоком розміру 8-9; побудований за рецептом DSpark на даних vision-language supervised fine-tuning.

**Деталі:**
- Прискорення декодування: до 3.13x на пристрої (MLX, Apple Silicon) і до 2.66x на H100
- Наскрізне прискорення: до 2.62x (Apple Silicon) і 2.27x (H100)
- Виміряно на шести vision-задачах: VQA, image captioning, багатоходові діалоги
- Відкриті ваги без обмежень на розгортання, формати Safetensors і GGUF на Hugging Face
- День-один підтримка в llama.cpp, MLX-VLM, SGLang
