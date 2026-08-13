---
company: NVIDIA
title: "Serve Qwen3.8-2.4T-A95B, a 2.4T-Parameter Model, with Configurable Reasoning on NVIDIA GB300 NVL72"
url: https://developer.nvidia.com/blog/serve-qwen3-8-2-4t-a95b-a-2-4t-parameter-model-with-configurable-reasoning-on-nvidia-gb300-nvl72/
published: 2026-08-12
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-13
---

NVIDIA details day-0 serving of Alibaba's Qwen3.8-2.4T-A95B (Qwen3.8-Max) — its largest open-weight model — on GB300 NVL72, reaching 4K+ tok/s per GPU and 350+ tok/s per user in FP8 without extra tuning.

## card

**Що сталося:** NVIDIA опублікувала технічний розбір розгортання Qwen3.8-2.4T-A95B (Qwen3.8-Max) — найбільшої відкритої моделі від Alibaba — на платформі GB300 NVL72, з конфігурованою глибиною reasoning (low/high/xhigh) на рівні запиту.

**Контекст:** Модель поєднує fine-grained MoE-архітектуру з full та linear attention, контекст до 1M токенів і вихід до 128K токенів — це триває тренд day-0 підтримки великих відкритих моделей на NVIDIA-стеку (SGLang, vLLM, NVIDIA Dynamo, NIM, NeMo AutoModel).

**Деталі:**
- 2.4T параметрів усього, 95B активних на токен
- На GB300 NVL72 (72 Blackwell Ultra GPU, 130 TB/s NVLink all-to-all) у FP8: 4000+ токенів/с на GPU і 350+ токенів/с на користувача без додаткового тюнінгу
- Подальший приріст очікується від NVFP4-прецизії
- Ваги доступні на Hugging Face та ModelScope; орієнтована на агентні workload — кодинг, аналіз документів, багатокроковий reasoning
