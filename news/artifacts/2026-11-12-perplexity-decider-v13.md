---
company: perplexity
title: "Perplexity Decider v1.3: Training, eval, and use cases"
url: https://www.perplexity.ai/hub/blog/perplexity-decider
date: 2026-11-12
found_via: gap-scrape (Jina worked cleanly this run; backfilled after being missed by prior runs)
---

Perplexity releases Decider v1.3 and Decider Flash v1.3, general-purpose decision models (classification/scoring/ranking/extraction) with a new "locate" span-extraction feature; Decider v1.3 reaches 93.98% judge agreement on real production requests, beating its own v1.2 and the external Jev 1.14 baseline, released on Hugging Face under Apache license.

## card

**Що сталося:** Perplexity випускає Decider v1.3 та дистильовану Decider Flash v1.3 — наступників власних моделей-"класифікаторів рішень" (v1/v1.1/v1.2). Моделі повертають імовірнісні відповіді на множину питань (так/ні, мультивибір, оцінка в балах) за один прохід замість генерації тексту токен-за-токеном; нова функція **locate** витягує текстові фрагменти (NER, PII, екстрактивне QA).

**Контекст:** Побудовані на Qwen3.8-27B (велика) і Qwen3.5-4B (дистильована, Flash); тренування у три етапи — генералістичне fine-tuning, доменно-специфічний LoRA-етап, окремий vision LoRA-етап; використовують двонаправлену увагу з "ізольованими питаннями" замість повної причинної уваги базової моделі.

**Деталі:**
- На внутрішньому тесті 1M продакшн-запитів (2,3M питань) Decider v1.3 досягає 93.98% узгодженості з LLM-суддями проти 93.68% у v1.2 і 93.35% у зовнішнього Jev 1.14.
- Класифікація запитів (63 задачі): 91.6% точності, +6.54 п.п. над продакшн-класифікаторами.
- Reranking (72 задачі): nDCG@10 83.99, краще за Qwen3-Reranker-8B (+1.81) і Jev 1.14 (+2.24).
- Внутрішнє застосування: моніторинг безпекових правил агентів (1 млрд токенів/день, 7000 сесій → 14 виправлень правил, 6 ухвалено за 2 дні, -52% шуму на найгучнішому правилі).
- Доступність: Hugging Face (Apache license), OpenRouter, Perplexity Decisions API.
