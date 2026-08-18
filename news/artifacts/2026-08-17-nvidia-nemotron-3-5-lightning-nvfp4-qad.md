---
company: NVIDIA
title: "Developing Nemotron 3.5 Lightning NVFP4 with QAD Using NVIDIA Model Optimizer"
url: https://developer.nvidia.com/blog/developing-nemotron-3-5-lightning-nvfp4-with-qad-using-nvidia-model-optimizer/
published: 2026-08-17
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-18
---

NVIDIA details how it built the Nemotron 3.5 Lightning NVFP4 checkpoint using Quantization-Aware Distillation (QAD) with NVIDIA Model Optimizer, compressing the model from 66GB to 22GB while recovering up to 99.7% of baseline accuracy.

## card

**Що сталося:** NVIDIA опублікував технічний розбір того, як побудований NVFP4-чекпоінт моделі Nemotron 3.5 Lightning за допомогою Quantization-Aware Distillation (QAD) в NVIDIA Model Optimizer — двоетапного пайплайну квантизації, що зберігає точність при агресивному стисненні.

**Контекст:** Розвиток відкритої родини моделей Nemotron і формату низької точності NVFP4; порівнюється з попередньою технікою post-training quantization (PTQ) як baseline.

**Деталі:**
- Стиснення: з 66 ГБ (BF16) до 22 ГБ (NVFP4), формат W4A16
- Пропускна здатність: до 4× вища
- Відновлення точності (проміжний чекпоінт A): PTQ — 96.33% медіанного відновлення, QAD — 99.72%; QAD покращив 10 з 11 бенчмарків; AIME 2025 відновлено на 3.13 пункти
- Фінальний чекпоінт: PTQ — 99.24% медіанного відновлення скору, QAD — 98.97%; Terminal-Bench v2.1 покращено на 3.79 пункти завдяки QAD
- Тренування: довжина послідовності 522K для фінального прогону, learning rate 5e-6 (constant), 400–6400 ітерацій в різних конфігураціях, калібрування на 1000 семплах на одному DGX B300
- Доступність: фінальний NVFP4-чекпоінт опубліковано на Hugging Face; рецепт QAD доступний у GitHub-репозиторії NVIDIA Model Optimizer
