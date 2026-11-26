---
company: huggingface
title: "Building on Nemotron 3.5 Parse: Open Data, Fine-Tuning, and Faster Inference"
url: https://huggingface.co/blog/nvidia/building-on-nemotron-35-parse-open-data-fine-tunin
date: 2026-11-26
found_via: TIER-1 rss
---

NVIDIA releases follow-up resources for its 0.6B Nemotron 3.5 Parse document-to-structured-data model: three open training datasets, a GRPO-based fine-tuning recipe, and a DFlash2 speculator for faster inference.

## card

**Що сталося:** NVIDIA публікує доповнення до Nemotron 3.5 Parse — компактної моделі (0.6B параметрів, доступна на Hugging Face як `nvidia/Nemotron-3.5-Parse`), що перетворює зображення сторінок документів у структуровані дані для RAG та агентів. Випуск включає три відкриті тренувальні датасети, рецепт файнтюнінгу (спершу supervised fine-tuning, потім RL/GRPO) та спекулятор DFlash2 для швидшого інференсу.

**Контекст:** Пост опубліковано 26 листопада 2026 на блозі Hugging Face від імені NVIDIA, як продовження лінійки моделей Nemotron Parse.

**Деталі:**
- Відкриті датасети: Synthetic Charts V1 (9.98M прикладів), Synthetic Tables V1 (1M), OCR Synthetic Multilingual v2 (7.9M).
- Швидкість інференсу: на concurrency 512, одна H200, BF16 — DFlash2 досягає 20.44 сторінки/с проти 2.98 у Parse 2.0.
- Ефект тренування: GRPO знизив кількість позначених циклічними помилками сторінок з 126 до 29 і підняв загальний скор з 66.24 до 71.38 (у порівнянні на етапі розробки).
