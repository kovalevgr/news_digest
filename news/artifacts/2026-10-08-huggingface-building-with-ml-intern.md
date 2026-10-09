---
company: Hugging Face
title: "The model that didn't exist, so you made it yourself"
url: https://huggingface.co/blog/building-with-ml-intern
source_url: https://huggingface.co/blog
published: 2026-10-08
fetched: 2026-10-09
---

A Hugging Face blog post walks through building six custom models with the ML Intern agent in HuggingChat, including a 0.8B prompt rewriter distilled from a 9B teacher and a citrus-disease vision model raising test accuracy from 14.9% to 52.8%, for roughly $103 total compute spend.

## card

**Що сталося:** Hugging Face опублікував кейс-стаді про використання власного агента ML Intern (у HuggingChat) для створення шести кастомних моделей — включно з 0.8B-моделлю переписування промптів, дистильованою з 9B-вчителя, та моделлю розпізнавання хвороб цитрусових, що підняла точність тесту з 14.9% до 52.8%. Загальна вартість обчислень — приблизно $103.

**Контекст:** Промо-дописи Hugging Face про власні інструменти (агенти, Spaces) регулярно з'являються поряд з технічними релізами на цьому блозі; цей пост водночас технічний (конкретні методи, бейзлайни, held-out тести) і промоційний щодо власного продукту.

**Деталі:**
- Загальна вартість 6 проєктів: ~$103; вартість на проєкт: від ~$1.90 до ~$37
- Prompt-rewriter: 0.8B, дистильований з 9B-вчителя, 8,797 розмічених вчителем запитів
- Vision-модель хвороб цитрусових: точність тесту зросла з 14.9% до 52.8%
- 1,030 відсканованих об'єктів відрендерено у 24,722 зображення
- 67.5% правильного розміщення об'єктів на 160 тестових парах doodle-edit
- GenEval: 0.509 → 0.536 для 4-крокової студентської моделі Agate проти 0.563 у 50-крокового вчителя
