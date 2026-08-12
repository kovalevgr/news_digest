---
company: NVIDIA
title: "NVIDIA Nemotron 3.5 Lightning Delivers Fast, Accurate Specialized Task Execution for Long-Running Agents"
url: https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/
published: 2026-08-11
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-12
note: "TIER-1 rss."
---

NVIDIA releases Nemotron 3.5 Lightning, an open-weight 30B (3B-active) MoE model (OpenMDW-1.1 license) purpose-built for the fast "execution layer" of long-running agents, claiming up to 4x output speed of similarly-sized models and 86% accuracy on PinchBench (10,000 tasks), 30% faster than Qwen3.6 35B.

## card

**Що сталося:** NVIDIA випустила Nemotron 3.5 Lightning — відкриту (ліцензія OpenMDW-1.1) MoE-модель 30B (3B активних параметрів), заточену під "execution layer" довготривалих AI-агентів: швидке й точне виконання вузьких спеціалізованих задач, а не загальне міркування.

**Контекст:** Разом з моделлю NVIDIA випустила NeMo Switchyard — бібліотеку маршрутизації задач між моделями (окремий артефакт), у зв'язці з якою Lightning позиціонується як "дешевий і швидкий" виконавець у мультимодельних агентних пайплайнах.

**Деталі:**
- Архітектура: MoE 30B параметрів, 3B активних; квантизації NVFP4 та BF16
- Розгортання: NVIDIA DGX Spark, Jetson, GeForce RTX 5090, дата-центри; сумісність з vLLM, SGLang, TensorRT-LLM, LM Studio, llama.cpp, Ollama
- Швидкість: до 4x вихідної швидкості моделей подібного розміру
- PinchBench: 86% точності на 10 000 задач, на 30% швидше за Qwen3.6 35B
- Спекулятивне декодування з multi-token prediction (draft-моделі DSpark, DFlash)
- Тюнінг через LoRA, SFT, RL-інструменти; екосистема 40+ партнерів
