---
company: NVIDIA
title: "Experiment with Qwen3.8-Flash-Next on NVIDIA GB300 NVL72 for Agentic Coding"
url: https://developer.nvidia.com/blog/experiment-with-qwen3-8-flash-next-on-nvidia-gb300-nvl72-for-agentic-coding/
published: 2026-08-26
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-27
---

NVIDIA publishes a guide for running Alibaba's Qwen3.8-Flash-Next (125B-parameter MoE, native 262K context extensible to 1M) on GB300 NVL72, reporting over 16K tokens/s per GPU and 8.6x prefill throughput at 1M-token context versus earlier versions.

## card

**Що сталося:** NVIDIA опублікувала гайд з експериментування з Qwen3.8-Flash-Next (моделлю Alibaba, прев'ю архітектури Qwen4) на платформі GB300 NVL72 для агентного кодингу.

**Контекст:** Qwen3.8-Flash-Next — 125-мільярдна MoE-модель з нативним контекстом 262K токенів (розширюваним до 1M), випущена Alibaba як превью майбутньої архітектури Qwen4; цю ж модель у ці дні відзначили радар (day-0 підтримка SGLang) і Hugging Face trending.

**Деталі:**
- Понад 16 тис. токенів/с на GPU на GB300 NVL72
- 8.6x приріст пропускної здатності prefill при контексті 1M токенів порівняно з попередніми версіями
- Підтримка кількох інференс-рушіїв (SGLang, vLLM) та інструментів NVIDIA для файнтюнінгу
- Дозволяє прототипувати на локальному залізі та масштабувати до продакшену
