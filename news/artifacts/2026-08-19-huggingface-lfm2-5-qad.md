---
company: Hugging Face
title: "LFM2.5 Q4_0 Checkpoints from Quantization-Aware Distillation"
url: https://huggingface.co/blog/LiquidAI/qad
published: 2026-08-19
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-20
---

Liquid AI released Quantization-Aware Distillation (QAD) Q4_0 checkpoints for four LFM2.5 models (230M, 350M, 1.2B-Instruct, 2.6B), recovering ~96.5–97.4% of BF16 baseline accuracy while running 3–33% faster than higher-precision alternatives on MacBook Pro, NucBox EVO-X2, Samsung Galaxy S26 Ultra, and Raspberry Pi 5.

## card

**Що сталося:** Liquid AI випустила Q4_0-чекпоінти для чотирьох моделей LFM2.5 (230M, 350M, 1.2B-Instruct, 2.6B), отримані через Quantization-Aware Distillation (QAD) — дистиляцію з високоточного вчителя одразу в квантизованого учня, на відміну від пост-тренувальної квантизації (PTQ).

**Контекст:** Продовження серії LFM2.5 для edge-пристроїв (Liquid AI раніше публікували LFM2.5-VL-3B та LFM2.5-2.6B на Hugging Face); QAD спрямований на компенсацію втрати якості при квантизації.

**Деталі:**
- Відновлення точності відносно BF16: 230M — 97.1%, 350M — 96.5%, 1.2B — 97.4%, 2.6B — 96.6%
- Тестовано на MacBook Pro, NucBox EVO-X2 (GPU), Samsung Galaxy S26 Ultra та Raspberry Pi 5 (ARM CPU)
- Пропускна здатність декодування на 3–33% вища за старші-точні аналоги при порівнянній якості
- Бенчмарки: GPQA Diamond, MMLU-Pro, IFEval; моделі доступні на Hugging Face (LiquidAI)
