---
company: Hugging Face
title: "UIBK-Embedding-v1: A Dense and a Late-Interaction Retriever in One Model, One Index and One Search"
url: https://huggingface.co/blog/abdoelsayed/uibk-embedding-v1
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-12
fetched: 2026-10-13
---

University of Innsbruck's DataScience-UIBK group releases UIBK-Embedding-v1, a 179M-parameter open English retrieval model (Apache 2.0) combining dense and ColBERT-style late-interaction retrieval in one encoder with a single MaxSim search. Found via gap-scrape (WebFetch of huggingface.co/blog — TIER-1 RSS showed zero fresh for HuggingFace).

## card

**Що сталося:** Команда DataScience-UIBK (Інсбрук) випускає UIBK-Embedding-v1 — відкриту (Apache 2.0) англомовну модель пошуку на 179M параметрів, що поєднує dense-ретривер і ColBERT-подібний late-interaction ретривер в одному енкодері з єдиним MaxSim-пошуком, без окремих індексів для кожного типу.

**Контекст:** Модель уникає потреби тримати два окремі індекси (dense + late-interaction) для гібридного пошуку, об'єднуючи обидва підходи в один прохід.

**Деталі:**
- 59.79 nDCG@10 на бенчмарку BEIR
- 70.55 nDCG@10 на NanoBEIR
- Перевершує модель LateOn на всіх 15 датасетах BEIR
- 179M параметрів, ліцензія Apache 2.0
