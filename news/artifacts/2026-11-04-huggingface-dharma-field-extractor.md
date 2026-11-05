---
company: huggingface
title: "Dharma Field Extractor: Any Document In, Structured Fields in JSON Out"
url: https://huggingface.co/blog/Dharma-AI/dharma-field-extractor
date: 2026-11-04
found_via: rss (TIER-1)
---

Dharma-AI releases Dharma Field Extractor, a 2B-parameter model (LoRA on DharmaOCR-LITE v1.1) that converts a document image to structured JSON — either schema-free or against a user-defined schema — positioned to replace general-purpose LLMs for field extraction at a fraction of the cost.

## card

**Що сталося:** Dharma-AI випустила Dharma Field Extractor — 2-мільярдну модель (LoRA-адаптер на DharmaOCR-LITE v1.1), що перетворює зображення документа у структурований JSON: у режимі без схеми сама знаходить пари "ключ-значення"/таблиці, у режимі зі схемою повертає задані поля (відсутні поля — `null`, без вигадування значень).

**Контекст:** Позиціонується як заміна для великих LLM (Claude Opus 5, GPT‑5.6 Luna) саме на задачі екстракції полів із документів — вузькоспеціалізована модель замість універсальної.

**Деталі:**
- Навчання: LoRA на 43 384 прикладах; дані — англомовні веб-документи, внутрішні бразильсько-португальські документи, менший мультимовний набір.
- Власний бенчмарк (546 документів, 1638 тест-кейсів): Field Extractor — 0.834 (field-level F1 × схожість значень × частка валідного JSON); Claude Opus 5 — 0.816; GPT‑5.6 Luna — 0.741.
- Вартість: фронтир-моделі обходяться в 6–147x дорожче за екстракцію; оцінка Field Extractor — self-hosted GPU-час на одній L40S за $2.24/год (не прайс-лист).
- Узагальнення на відкладених наборах: всі 18 полів правильні на SROIE-рахунках; стани чекбоксів і рукописний ID співпали на формі FUNSD.
- Бенчмарк і порівняння вартості — від самих авторів, потребують незалежної перевірки.
