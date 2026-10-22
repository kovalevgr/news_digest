---
company: huggingface
title: "How Specializing the Vocabulary of SLMs Can Cut Inference Cost by 77% in Real Applications"
url: https://huggingface.co/blog/Dharma-AI/vocabx-vocabulary-specialization
date: 2026-10-21
found_via: TIER-1 rss (huggingface.co/blog/feed.xml)
---

Dharma AI previews VocabX, a method that specializes a small language model's tokenizer vocabulary by per-token cost rather than frequency, without changing the base model; on a Qwen3-4B Portuguese essay grader, inference cost fell 77% while the bench score rose from 0.703 to 0.810 (paper under review).

## card

**Що сталося:** Dharma AI публікує препринт VocabX — метод спеціалізації словника токенізатора малої мовної моделі за вартістю кожного токена (а не за частотою), без зміни базової моделі.

**Контекст:** Стаття ще перебуває на рецензії. Перевірено на класифікаторі есе португальською мовою на базі Qwen3-4B, а також на п'яти доменах і трьох сімействах моделей проти трьох референсних методів адаптації словника.

**Деталі:**
- На бенчмарку з есе португальською: вартість інференсу впала на 77,0%, середня довжина відповіді — з 350 до 101 токена.
- Оцінка бенчмарку зросла з 0,703 до 0,810; розмір вихідного шару зменшився приблизно з 152 000 до 65 000 рядків.
- У 15 комбінаціях (5 доменів × 3 сімейства моделей) VocabX перевершив три референсні методи стиснення на 1,2–9,3 бала.
