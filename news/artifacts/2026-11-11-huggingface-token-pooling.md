---
company: huggingface
title: "Token Pooling-Aware Training for Multi-Vector Embedding Models"
url: https://huggingface.co/blog/token-pooling
date: 2026-11-11
found_via: fetch (confirmed via WebFetch on huggingface.co/blog — zero fresh from the rss tier this run)
---

Hugging Face's Tom Aarsen details pooling-aware training for multi-vector retrieval: a compressed-document retrieval objective trains the encoder to preserve useful information after token pooling shrinks the index, retaining 97.8% of unpooled NanoBEIR nDCG@10 at a pool factor of 4 (vs. 94.6% for normal training) while storing ~4x fewer document vectors.

## card

**Що сталося:** Hugging Face (Tom Aarsen) описав pooling-aware training — метод навчання для мультивекторних embedding-моделей, що зберігає якість пошуку навіть після token pooling (об'єднання схожих токен-векторів у документі для зменшення розміру індексу).

**Контекст:** Включає приклад тренування через Sentence Transformers; метод додає до навчання ціль compressed-document retrieval, щоб енкодер навчився зберігати корисну інформацію після об'єднання векторів.

**Деталі:**
- При pool factor 4: модель з pooling-aware training зберігає 97.8% якості пошуку (NanoBEIR nDCG@10) порівняно з непулованою версією.
- Звичайно натренована модель зберігає лише 94.6% за тих же умов.
- Зберігання: приблизно в 4 рази менше векторів документів.
