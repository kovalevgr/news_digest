---
company: Perplexity
title: "Multimodal embeddings beyond a single vector"
url: https://www.perplexity.ai/hub/blog/multimodal-embeddings-beyond-a-single-vector
source_url: https://www.perplexity.ai/hub/blog
published: 2026-10-07
fetched: 2026-10-10
---

Perplexity ships pplx-embed-v2-late, a family of ColBERT-style multi-vector embedding models (0.6B/9B, shared embedding space) handling both text-to-text and text-to-image retrieval (searching rendered PDF pages directly, no OCR); state-of-the-art on ViDoRe(V3) for their size class and 92.4% accuracy on the agentic MADQA benchmark. Both sizes open on Hugging Face.

## card

**Що сталося:** Perplexity випускає pplx-embed-v2-late — сімейство мультивекторних embedding-моделей (0.6B і 9B) у стилі ColBERT зі спільним простором ембедингів, що шукають і текст-текст, і текст-зображення напряму по відсканованих PDF-сторінках, без OCR.

**Контекст:** третя модель лінійки embedding після pplx-embed-v1 (лютий) та контекстної pplx-embed-v2-context (минулого тижня); адресує обмеження одновекторних embedding-ів — інформаційне "вузьке горло" при стисканні цілого документа в один вектор, особливо гостре для мультимодальних даних.

**Деталі:**
- На ViDoRe(V3) (візуальний пошук документів) 0.6B-модель — 62.3%, наздоганяючи моделі у 5 разів більші за розміром; 9B-модель — 65.2%.
- На Q2D-Web (комбіновані судження релевантності) обидві моделі перевершують усіх конкурентів: 74.8% (9B) і 73.6% (0.6B) проти попереднього найкращого результату 69.3%.
- На агентному MADQA (800 PDF, 18,000+ сторінок, у парі з Gemini 3.5 Flash) 9B-модель — нова SOTA серед ретріверів, 92.4% точності (на 3.5 в.п. краще за ретрівер Mixedbread).
- Обидва розміри поділяють простір ембедингів — можна індексувати 9B-моделлю, а запити кодувати дешевою 0.6B для швидкого пошуку.
- Обидві моделі відкриті на Hugging Face, сумісні з sentence-transformers≥6.0.0 / transformers≥5.4.0.
