---
company: NVIDIA
title: "Scale Agentic Coding Workflows with Meta's Muse Spark Open on NVIDIA GB300 NVL72"
url: https://developer.nvidia.com/blog/scale-agentic-coding-workflows-with-metas-muse-spark-open-on-nvidia-gb300-nvl72/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-10-15
fetched: 2026-10-16
---

NVIDIA publishes a technical blog on running Meta's newly released Muse Spark Open (816B MoE agentic-coding model) on its GB300 NVL72 Blackwell Ultra systems, with NVFP4 checkpoints and deployment options via NIM, SGLang, vLLM, and TensorRT-LLM.

## card

**Що сталося:** Meta випустив Muse Spark Open — модель mixture-of-experts на 816B параметрів, налаштовану для агентного програмування. NVIDIA опублікувала технічний огляд запуску цієї моделі на системах GB300 NVL72 (Blackwell Ultra) з оптимізованими NVFP4-чекпоінтами.

**Контекст:** У статті не вказано, що Muse Spark Open замінює чи продовжує якусь попередню модель.

**Деталі:**
- Архітектура: sparse MoE, 816B параметрів загалом, 42B активних на токен, top-8 routing серед 256 експертів
- Контекст: 1M токенів; обробляє текст, зображення, документи, аудіо й відео через 1.8B perception-енкодер
- Продуктивність (за даними вендора): до 50K токенів/сек на GPU і до 600 токенів/сек на користувача на GB300 NVL72 зі speculative decoding (на 4 Blackwell GPU)
- Квантування: NVFP4-чекпоінти від Meta, оптимізовані під Blackwell Ultra
- Доступність: ваги NVFP4 на Hugging Face, контейнер NVIDIA NIM для production, підтримка inference в SGLang/vLLM/TensorRT-LLM з рецептами NVIDIA Dynamo, post-training через NeMo AutoModel та Megatron Bridge
