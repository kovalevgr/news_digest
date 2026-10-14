---
company: Hugging Face
title: "Run fast, private agents on-device with LFM2.5-24B-A2B"
url: https://huggingface.co/blog/LiquidAI/lfm25-24b-a2b
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-13
fetched: 2026-10-14
---

Liquid AI releases LFM2.5-24B-A2B, a 24B-parameter (2B-active) reasoning MoE built for on-device agents, leading or matching the larger Qwen3.6-35B-A3B on 5 of 8 tool-use/agentic benchmarks and all 3 instruction-following benchmarks.

## card

**Що сталося:** Liquid AI випускає LFM2.5-24B-A2B — MoE-модель на 24B параметрів (2B активних), призначену для швидких приватних агентів на локальних пристроях; модель тільки-reasoning (явний ланцюжок міркувань перед відповіддю, на відміну від попередника LFM2-24B-A2B).

**Контекст:** Продовжує лінійку LFM2.5 (включно з LFM2.5-VL, LFM2.5-DSpark); як орієнтир близького класу порівнюється з Qwen3.6-35B-A3B.

**Деталі:**
- Архітектура: 40 шарів, 64 експерти на MoE-блок, top-4 routing, gated short convolutions + GQA; контекст зріс з 32K до 131K токенів, словник — з 65K до 128K
- Попереднє навчання масштабовано з ~17T до ~33T токенів; постнавчання включає SFT, дистиляцію та agentic RL у харнесах OpenClaw, Hermes Agent, Pi, OpenCode
- Проти Qwen3.6-35B-A3B: лідирує/на рівні на 5 з 8 tool-use/agentic бенчмарків (LiveClaw 48.09 vs 38.19; AutomationBench 27.69 vs 8.72; ToolSandbox 80.71 vs 75.02; BFCLv4 65.01 vs 65.00) і на всіх 3 instruction-following (IFEval 96.75 vs 93.06; IFBench 74.69 vs 64.21); відстає на знаннях і коді (GPQA Diamond 74.42 vs 83.69; SWE-Bench Verified 51.00 vs 66.20; PinchBench 83.18 vs 89.93)
- Швидкість: ~184 ток/с на Apple M5 Max, ~114 ток/с на Ryzen AI Max+ 395, 21K+ вихідних ток/с при високій конкурентності на одному NVIDIA B300
- Відкриті ваги на Hugging Face (LFM2.5-24B-A2B, LFM2.5-24B-A2B-Base), day-one підтримка llama.cpp/MLX/vLLM/SGLang/ONNX, сумісність з transformers>=5.0.0; конкретну ліцензію сторінка релізу не називає (деталі на картці моделі)
