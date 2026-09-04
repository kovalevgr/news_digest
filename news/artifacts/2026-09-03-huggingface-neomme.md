---
company: Hugging Face
title: "NeoMME: an efficient Multimodal-native and Multilingual Encoder"
url: https://huggingface.co/blog/Hcompany/neomme
published: 2026-09-03
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-04
---

H Company released NeoMME, a family of unified encoder models (260M/800M) processing image patches and text tokens in one bidirectional transformer; the retrieval variant sets a new state of the art among sub-800M models on ViDoRe v3 with a 255x smaller late-interaction index.

## card

**Що сталося:** H Company випустила NeoMME — родину ефективних мультимодальних енкодерів (260M і 800M параметрів), що обробляють патчі зображень і текстові токени в єдиному двонапрямленому трансформері замість окремих vision-башти й мовної моделі.

**Контекст:** Випущено під ліцензією Apache 2.0 з інтеграцією в Hugging Face Transformers. Варіант NeoMME-Retriever донавчений для пошуку у візуальних документах (visual document retrieval).

**Деталі:**
- Тренування з нуля на 524 млрд токенів через masked discrete-diffusion pretraining; контекст 16 384 токени, багатомовний BPE-словник 131k токенів
- NeoMME-Retriever: 0.523 nDCG@10 (260M) і 0.556 nDCG@10 (800M) на ViDoRe v3 — найкращий результат серед моделей до 800M параметрів
- Швидкість кодування ~51 сторінки/с при роздільності 2048×2048 — вдвічі швидше за ColModernVBERT
- Стиснення індексу пізньої взаємодії з ~1.5 МБ до 6 КБ на сторінку (у 255 разів) через ієрархічний token pooling та асиметричну квантизацію, зі збереженням 95%+ якості пошуку
