---
company: Hugging Face
title: "Deploy local agents everywhere with LFM2.5-2.6B"
url: https://huggingface.co/blog/LiquidAI/lfm2-5-2-6b
published: 2026-08-04
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-05
---

A Hugging Face blog post (LiquidAI) on deploying local agents everywhere using the
LFM2.5-2.6B model.

## card

**Що сталося:** Liquid AI опублікувала в блозі Hugging Face анонс LFM2.5-2.6B — компактної моделі на 2,6 млрд параметрів для запуску локальних агентів на ноутбуках, смартфонах, CPU та GPU. За заявою авторів, модель конкурує з моделями вчетверо більшими у tool use, виконанні інструкцій і багатокрокових агентних задачах.

**Контекст:** Модель побудована на архітектурі LFM2 — продовження лінійки edge-орієнтованих моделей Liquid AI. На Hugging Face викладено дві версії: LFM2.5-2.6B та LFM2.5-2.6B-Base.

**Деталі:**
- 2,6 млрд параметрів; контекст 128K токенів (розширений на етапі mid-training); працює в межах 2,5 ГБ пам'яті
- Pre-training на ~34 трлн токенів; post-training: SFT, teacher specialization, multi-domain on-policy distillation та agentic RL
- Швидкість на CPU: 220 ток/с (Apple M5 Max), 113 ток/с (AMD Ryzen), ~30 ток/с на смартфонах; ~15 000 вихідних ток/с на H100 за високої конкурентності
- Підтримує tool calling, багатокрокові агентні workflow та web search
- Лідирує у протестованих instruction-following бенчмарках; попереду в tool-use задачах (окрім BFCLv4)
- Ліцензія в пості не вказана
