---
company: Hugging Face
title: "Training and Finetuning Multi-Vector Embedding Models with Sentence Transformers"
url: https://huggingface.co/blog/train-multi-vector-encoder
published: 2026-08-26
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-28
---

Hugging Face publishes a guide (Tom Aarsen, Sentence Transformers v6.0) to training multi-vector (ColBERT-style) embedding models, demonstrating a medical-retrieval model that beats 50+ general-purpose models after 14.5 hours of finetuning on a single RTX 3090.

## card

**Що сталося:** Hugging Face опублікувала гайд з тренування мультивекторних (ColBERT-style) embedding-моделей через Sentence Transformers v6.0, з прикладом медичної retrieval-моделі mLateOn-medical.

**Контекст:** Мультивекторні моделі зберігають по одному невеликому вектору на токен замість стиснення тексту в один вектор, що вирішує проблему обрізання довгих документів (більшість моделей обмежені 180–512 токенами).

**Деталі:**
- mLateOn-medical досягла 0.9139 NDCG@10, обійшовши 50+ моделей загального призначення
- Тренування: лише 14.5 години на одній GPU RTX 3090, 1 млн пар медичних питання-уривок
- Непідконтрольований (unsupervised) старт значно кращий за supervised у доменній адаптації
- Обрізання документів саме по собі коштувало до 0.24 NDCG@10 (медичні уривки в оцінці — в середньому 941 токен)
- Автор: Tom Aarsen, за участі 55+ контриб'юторів спільноти
