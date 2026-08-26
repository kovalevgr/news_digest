---
company: Hugging Face
title: "Quantization-Aware Healing: a compressed, 4-bit model that outperforms its full-precision original"
url: https://huggingface.co/blog/MultiverseComputingCAI/quantization-aware-healing
published: 2026-08-25
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-26
---

Multiverse Computing introduces Quantization-Aware Healing (QAH), a recovery technique that distills a compressed, quantized student directly from the original full-precision teacher, compressing GPT-OSS 120B to a 60B 4-bit (MXFP4) model that beats its own 16-bit original on 7 of 9 benchmarks.

## card

**Що сталося:** Multiverse Computing опублікувала техніку Quantization-Aware Healing (QAH) — спосіб "лікувати" точність моделі після стиснення, дистилюючи стиснутого студента напряму з оригінального повнорозмірного вчителя, а не з проміжного деградованого чекпоінта.

**Контекст:** Стандартний пайплайн стиснення (структурне стиснення → квантизація → healing) страждає від того, що існуючі методи healing (QAT, QAD) або дорогі й нестабільні, або "прив'язані до деградованої цілі", коли вчитель сам є стисненою апроксимацією.

**Деталі:**
- Застосовано до GPT-OSS 120B → стиснуто до 60B параметрів у форматі MXFP4 (4-біт)
- Стиснена 4-бітна модель перевершує свій оригінал на 16-біт (bfloat16) на 7 з 9 бенчмарків
- Long-context reasoning: +7.4 пункти (42.7 проти 35.3); математика: +5.6 пункти (76.3 проти 70.7); код: +1.0–2.7 пункти
- ~4x менше пам'яті для ваг порівняно з bfloat16
- QAH досягає пікової продуктивності за ~100 кроків тренування проти ~700 кроків у QAT
