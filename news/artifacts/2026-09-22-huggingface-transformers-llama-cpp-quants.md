---
company: Hugging Face
title: "Transformers now runs llama.cpp quants"
url: https://huggingface.co/blog/transformers-llama-cpp-quants
published: 2026-09-22
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-23
---

Hugging Face adds GGUF quantized-model support directly in the Transformers library via `from_pretrained(..., gguf_file=...)`, reusing ggml's Metal kernels through the `kernels` library to reach near-llama.cpp performance on Apple Silicon, initially for Qwen3.5-architecture models.

## card

**Що сталося:** Hugging Face додає підтримку GGUF-квантованих моделей прямо в бібліотеці Transformers через параметр `gguf_file` у `from_pretrained()`, з початковою підтримкою архітектури Qwen3.5 на Apple Silicon.

**Контекст:** Реалізація перевикористовує Metal-ядра ggml через бібліотеку `kernels`, наближаючись до продуктивності llama.cpp; llama.cpp залишається рекомендованим рушієм для чистого локального inference, а нова інтеграція дозволяє експериментувати з квантованими моделями у звичному PyTorch-воркфлоу (оцінювання, донавчання, кастомні шари).

**Деталі:**
- Завантаження через стандартний API `from_pretrained()` з параметром `gguf_file`
- Підтримувані рівні квантування: Q4_K_M, Q5_K_M, Q6_K — компроміс памʼяті й точності
- Бенчмарки показують продуктивність, близьку до llama.cpp, на різних розмірах моделей на M2 Max
- Початковий фокус — Apple Silicon; можливість стала доступною після приєднання GGML і llama.cpp до Hugging Face
