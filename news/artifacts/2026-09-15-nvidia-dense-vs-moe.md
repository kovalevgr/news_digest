---
company: NVIDIA
title: "Dense vs. MoE Models: Active Parameters, Throughput, and When to Choose Each"
url: https://developer.nvidia.com/blog/dense-vs-moe-models-active-parameters-throughput-and-when-to-choose-each/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-09-15
fetched: 2026-09-16
---

NVIDIA publishes a comparison of dense vs. Mixture-of-Experts (MoE) model architectures, covering memory/compute tradeoffs and deployment guidance. Nemotron 3.5 Lightning (30B total, 3B active) reaches 235.7-494.2 tok/s at $0.22/M output, four to five times the throughput of dense Gemma 4 31B (36.9-222.4 tok/s, $0.40/M) at lower cost; Mistral Small 4 (119B total, 6-8B active) reaches 147.3 tok/s at $0.60/M.

## card

**Що сталося:** NVIDIA публікує порівняльний гайд dense vs. MoE (Mixture-of-Experts) архітектур із конкретними числами пропускної здатності й вартості для вибору відповідного типу моделі.

**Контекст:** MoE відв'язує вартість пам'яті від вартості обчислень — усі експерти мають бути завантажені у VRAM, але на кожен токен активується лише частина з них. Гайд дає рекомендації: MoE — коли пріоритет пропускна здатність і вартість на масштабі; dense — коли потрібне просте fine-tuning, передбачувана затримка або пріоритет reasoning.

**Деталі:**
- Nemotron 3.5 Lightning (30B всього, 3B активних): 235.7–494.2 ток/с за $0.22/M вихідних токенів
- Gemma 4 31B (dense): 36.9–222.4 ток/с за $0.40/M
- Mistral Small 4 (119B всього, 6-8B активних): 147.3 ток/с за $0.60/M
- Nemotron демонструє у 4-5 разів вищу пропускну здатність за нижчої вартості порівняно з подібною dense-моделлю
