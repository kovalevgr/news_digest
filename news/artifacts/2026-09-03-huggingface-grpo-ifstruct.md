---
company: Hugging Face
title: "Fine-tuning a 350M Model for Better Structured Outputs in 100 GRPO Steps"
url: https://huggingface.co/blog/grpo-with-trl-ifstruct
published: 2026-09-03
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-05
---

Hugging Face (with Liquid AI contributors) shows lightweight GRPO fine-tuning of LFM2.5-350M lifting IFStruct structured-output accuracy from 22.6% to 29.7% in just 100 training steps on ~500 samples via TRL, using a LoRA adapter of ~1.66% of model size.

## card

**Що сталося:** Hugging Face опублікували практичний приклад тонкого налаштування маленької моделі LFM2.5-350M за допомогою GRPO (100 кроків, ~500 прикладів) через бібліотеку TRL — точність на бенчмарку структурованих виводів IFStruct зросла з 22.6% до 29.7%.

**Контекст:** Продовження серії практичних постів HF про RL-тюнінг малих моделей через TRL; співавтори з Liquid AI (розробники LFM2.5).

**Деталі:**
- Модель: LFM2.5-350M (350М параметрів)
- LoRA-адаптер: ~6М тренованих параметрів (1.66% моделі)
- IFStruct benchmark: 22.6% → 29.7%; коректність JSON-формату: 18.0% → 31.9%
- Три reward-функції: валідність JSON, точність кількості полів, відповідність схемі
- Використано аугментацію даних для усунення розбіжності між тренувальним і оцінювальним розподілами
