---
company: Hugging Face
title: "Sparseup-fr: A French replication of Linkup's sparse embedding model"
url: https://huggingface.co/blog/alphaedge-ai/french-sparseup
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-12
fetched: 2026-10-13
---

AlphaEdge AI releases Sparseup-fr, a French replication of Linkup's ~150M-parameter sparse embedding model, trained ~55 hours on one RTX 6000 Pro, outperforming other open French sparse models on a cleaned NanoBEIR-fr benchmark. Found via gap-scrape (WebFetch of huggingface.co/blog — TIER-1 RSS showed zero fresh for HuggingFace).

## card

**Що сталося:** AlphaEdge AI випускає Sparseup-fr — французьку репліку sparse embedding-моделі Linkup (~150M параметрів) з мультимовним backbone mLateOn-unsupervised і словником, урізаним до 50 240 токенів; тренування зайняло ~55 годин на одній RTX 6000 Pro.

**Контекст:** Автори порівнюють модель з іншими відкритими sparse-моделями французькою на очищеному бенчмарку NanoBEIR-fr; заявляють нову SOTA серед відкритих sparse-моделей французькою.

**Деталі:**
- 56.37 nDCG@10 на NanoBEIR-fr (очищений) — проти opensearch (53.94) і splade-camembert-base-v2 (53.15)
- Все ще помітно позаду late-interaction моделі mLateOn (66.13)
- ~55 годин тренування на одній RTX 6000 Pro
