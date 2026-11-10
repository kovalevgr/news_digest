---
company: huggingface
title: "Nemotron-Personas-Finance-Japan: A Synthetic Dataset Capturing Japan's Demographics and Financial Context"
url: https://huggingface.co/blog/nvidia/nemotron-personas-finance-japan
date: 2026-11-09
found_via: rss
---

NVIDIA and Elith release Nemotron-Personas-Finance-Japan, a CC BY 4.0 synthetic dataset of 9M personas (1M records × 9 personas, ~1.5B tokens) extending Nemotron-Personas-Japan with household-finance and financial-literacy fields, built on Japan's official statistics with input from Sompo Japan, Tokio Marine, Bank of Fukuoka, Mizuho, Meiji Yasuda, and the FDUA.

## card

**Що сталося:** NVIDIA та Elith випустили Nemotron-Personas-Finance-Japan — синтетичний датасет на 9M персон (1M записів по 9 персон кожен, ~1.5 млрд токенів), побудований на офіційній японській статистиці, з полями про домашні фінанси та фінансову грамотність.

**Контекст:** Розширює попередній Nemotron-Personas-Japan (у 1.5x більше персон, 50 полів замість 22). Згенерований через NeMo SDG-PGMs та NeMo Data Designer, японський текст — через gemma-4-31B-it. Зворотний зв'язок надали Sompo Japan, Tokio Marine, Bank of Fukuoka, Mizuho Financial Group, Meiji Yasuda Life Insurance та FDUA. Того ж дня вийшов супутній Nemotron-PII-Japan (100K синтетичних бізнес-документів з розміченими персональними даними).

**Деталі:**
- Розмір: 9M персон (1M записів × 9 персон), ~1.5 млрд токенів (~750M токенів власне персон).
- Структура: 50 полів на запис (9 персональних, 11 атрибутів, 30 контекстних); ~950k унікальних імен, 1600+ категорій професій.
- Ліцензія: CC BY 4.0 (дозволено комерційне використання); завантаження через `load_dataset("nvidia/Nemotron-Personas-Finance-Japan")`.
- Усі персони повністю синтетичні — реальних людей не представлено.
