---
company: Hugging Face
title: "Scaling Indic Pretraining: 2.8 Trillion Tokens and an Open Data Generation Pipeline"
url: https://huggingface.co/blog/nvidia/scaling-indic-pretraining
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-16
fetched: 2026-10-16
---

NVIDIA, IIT Madras and AI4Bharat announce Nemotron-pretraining-Indic-v1, a ~2.8T-token corpus across 22 Indian languages (releasing soon) plus its open data-generation pipeline; a 12-language subset already boosted Nemotron 3.5 Super VL's continued pretraining.

## card

**Що сталося:** NVIDIA разом із IIT Madras та лабораторією AI4Bharat анонсували Nemotron-pretraining-Indic-v1 — корпус приблизно на 2.8 трильйони токенів для 22 індійських мов, який "скоро буде випущено" разом із відкритим GPU-прискореним пайплайном генерації даних. Підмножина з 12 мов цього корпусу вже використана для continued pretraining моделі Nemotron 3.5 Super VL.

**Контекст:** Розширює попередній відкритий індійський корпус AI4Bharat — Sangraha — за рахунок масштабних синтетичних даних, згенерованих перекладом англомовних джерел із 15 підмножин Nemotron-CC-v2 через NeMo Data Designer.

**Деталі:**
- Обсяг: 2,601.0B токенів у рідних скриптах + 224.6B романізованих токенів (підрахунок токенізатором Gemma-4)
- Покриття: 22 мови в рідному скрипті та 12 романізованих — 34 мовно-скриптових конфігурації
- Порог якості: не менше 75/100 за MQM-подібною рубрикою; виправлення відновили 438.4B токенів
- Моделі перекладу: Gemma-4-31B-it (12 мов), Indic Translate від Bodhan AI (інші 10)
- Результати continued pretraining: прирости на 4.98–9.82 відсоткових пункти на 5 індійських бенчмарках
- Доступність: датасет ще не випущено; пайплайн генерації — відкритий код на GitHub
