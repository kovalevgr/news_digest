---
company: NVIDIA
title: "How Generative Recommenders Are Redefining RecSys at Scale"
url: https://developer.nvidia.com/blog/how-generative-recommenders-are-redefining-recsys-at-scale/
published: 2026-08-20
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-21
---

NVIDIA details generative recommenders (GRs) that reframe recommendation as sequence prediction like LLMs, covering HSTU and Semantic ID approaches with production-scale training/inference numbers on H100 and open-source repos.

## card

**Що сталося:** NVIDIA опублікував технічний огляд генеративних рекомендаційних систем (GR) — підходу, що моделює рекомендації як задачу передбачення наступного токена (подібно до LLM) замість геометричного пошуку схожості ембеддингів; розглянуто два підходи — HSTU (Hierarchical Sequential Transduction Units) та Semantic IDs.

**Контекст:** Продовження серії технічних матеріалів NVIDIA про масштабування рекомендаційних систем (RecSys) на GPU-інфраструктурі; матеріал доповнює існуючі бібліотеки TorchRec, Megatron-Core та PyTorch AOTInductor конкретними продакшн-орієнтованими реалізаціями.

**Деталі:**
- Тренування HSTU на двох вузлах DGX H100: Model FLOP Utilization зросла з 7.65% до 31.40%
- Inference на Triton: PyTorch AOTI без кешу — прискорення 1.14–1.28×; з кешем (all-GPU cache-hit) — 2.20–2.38×
- Semantic ID-GR serving (Qwen3-1.7B на H100): офлайн-латентність швидша у 2.14–2.27× за SGLang baseline; онлайн-пропускна здатність вища у ~1.85× (~19.7 проти ~10.7 req/s); медіанна латентність нижча на ~46% (~198 проти ~370 мс)
- MLPerf DLRM v3 inference: 99 997 запитів/секунду
- Відкрито два репозиторії: `recsys-examples` та `nv-embedding-cache`
- DynamicEmb керує ембеддингами між GPU HBM та host memory через scored hash tables
