---
company: Hugging Face
title: "IBM releases SOTA Granite Time Series PatchTST-FM-r2 model with commercial-friendly license"
url: https://huggingface.co/blog/ibm-research/ibm-releases-sota-granite-time-series
published: 2026-09-09
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-10
---

IBM Research releases Granite Time Series PatchTST-FM-r2, a ~385M-parameter zero-shot forecasting foundation model with an updated conformer-block architecture, ranking second overall and first among permissively-licensed models on GIFT-Eval.

## card

**Що сталося:** IBM Research випустила Granite Time Series PatchTST-FM-r2 — foundation-модель для zero-shot прогнозування часових рядів (попит, енергоспоживання, трафік), з відкритими вагами, архітектурою та кодом інференсу на Hugging Face Hub.

**Контекст:** Оновлена версія попередньої PatchTST-FM з переробленою архітектурою (conformer-блоки замість попередньої) та розширеним масштабом; сумісна з інтеграцією IBM у Confluent Cloud (Apache Flink) для real-time прогнозування.

**Деталі:**
- ~385M параметрів, контекст до 8192 кроків, ймовірнісні прогнози на 99 квантилях
- На GIFT-Eval (станом на 2026-09-08): друге місце серед відтворюваних zero-shot конкурентів за CRPS і MASE, перше — серед моделей з permissive-ліцензією
- Архітектура: conformer-блоки (self-attention + temporal convolution), патчі з 50% перекриттям і Hamming-вікном, 30 блоків замість 20 у попередній версії
- Ліцензія: подвійна Apache 2.0 / OpenMDW 1.0
- Ранній доступ до розгортання через Apache Flink на Confluent Cloud для streaming-застосунків
