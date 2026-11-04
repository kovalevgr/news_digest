---
company: huggingface
title: "Palette: teaching a small model to build decks in your design language"
url: https://huggingface.co/blog/ibm-research/palette-deck-building
date: 2026-11-03
found_via: rss
---

IBM Research releases Palette, a fine-tuned open-weight 20B LoRA model that builds slide decks in IBM's design language via a designer/coder two-role pipeline with a check-and-repair harness, reaching near-frontier quality (2nd of 3 models on the PresentBench three-domain mean) while staying on local infrastructure.

## card

**Що сталося:** IBM Research випустили Palette — донавчену open-weight 20B-модель (LoRA-адаптер), яка генерує слайд-деки у фірмовому дизайн-мові IBM. Архітектура з двох ролей: "дизайнер" пише JSON-бриф (палітра, типографіка, макет кожного слайду), "кодер" паралельно пише pptxgenjs-код для кожного слайду (прискорення ~6-7x), а harness перевірки й виправлення автоматично усуває помилки верстки (накладання, обрізання, переповнення).

**Контекст:** Побудовано на бенчмарку PresentBench (5 критеріїв якості) та LoRA fine-tuning; тренувальні дані — ~1000 синтетичних дек (~10 000 слайдів), згенерованих великою "вчительською" моделлю, з контрфактуальними поясненнями чому альтернативи відхилено.

**Деталі:**
- На PresentBench (3 домени): 1-е місце в Economics та Education, 3-є в Talk; середнє по трьох доменах — 59.7 проти 60.8 у NotebookLM (2-е місце).
- Check-and-repair harness додає в середньому +3.5 бала на 131 деці PresentBench.
- Користувачі керують генерацією короткими директивами `[[ ]]` (напр. `[[make this a timeline]]`) — тренування покриває 12 категорій директив.
- Напрямки розвитку: RL (GRPO) на сигналах перевірки, витяг графіків із документів через Docling, "перескін" існуючих .pptx-шаблонів без перенавчання.
