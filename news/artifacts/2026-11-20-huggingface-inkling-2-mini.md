---
company: huggingface
title: "Welcome Inkling 2 Mini, Cutting-edge Performance for your Local Setup"
url: https://huggingface.co/blog/inkling2mini
date: 2026-11-20
found_via: gap-scrape (WebFetch — huggingface.co/blog/feed.xml returned zero fresh in-window entries this run)
---

Hugging Face and Thinking Machines Lab release Inkling 2 Mini, an open-weight ~26B-total/3B-active MoE "looped transformer" (24 physical layers run with middle-layer looping for 48 logical layers), 1M-token multimodal context, with day-zero Transformers/llama.cpp/MLX/SGLang support.

## card

**Що сталося:** Hugging Face у партнерстві з Thinking Machines Lab представляє Inkling 2 Mini — відкриту мультимодальну MoE-модель "looped transformer" для локальних установок (~26 млрд параметрів всього, 3 млрд активних на токен). 12 із 24 фізичних шарів виконуються тричі, що дає 48 логічних шарів при зберіганні лише 24 фізичних.

**Контекст:** Модель заявлена як топова у своєму класі за Artificial Analysis Intelligence Index v5, лідирує у 32 з 48 бенчмарків проти Gemma 4 31B, Muse Glimmer, Qwen3.8-27B і Nemotron 3.5 Super VL (нарівні з Qwen3.8-27B на Terminal-Bench 4.0, позаду на AutomationBench-AA v1.0.6).

**Деталі:**
- Прихований розмір 2304, 8 з 128 експертів обираються на кожному проході шару; контекст 1M токенів, текст + зображення.
- Змішана точність NVFP4/MXFP8 для ваг експертів; DSpark-драфтер для спекулятивного декодування.
- Дослідницький чекпоінт TML-d24-varloop-research дозволяє 1-3 проходи циклу (менше проходів = швидше, можливо гірша якість).
- Доступність: `thinkingmachines/Inkling-2-Mini` на Hugging Face; підтримка день-у-день у Transformers (`AutoModelForMultimodalLM`), llama.cpp/Llama App (GGUF IQ4_NL/Q8_0), MLX (через mlx-lm/mlx-community), SGLang (потребує SM103).
