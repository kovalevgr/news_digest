---
company: nvidia
title: "When One GPU Isn't Enough: Serving GLM-5.3 Across Two NVIDIA DGX Stations with vLLM"
url: https://developer.nvidia.com/blog/when-one-gpu-isnt-enough-serving-glm-5-3-across-two-nvidia-dgx-stations-with-vllm/
date: 2026-11-13
found_via: rss
---

NVIDIA details deploying GLM-5.3 NVFP4 (753B total / 40B active parameters, ~464GB of weights) across two ConnectX-8-linked DGX Stations using vLLM 0.30.0 with tensor parallelism, multi-token prediction, FP8 KV cache, and prefix caching — benchmarked with AIPerf's SPEED-Bench Coding, peaking at 607.8 tok/s overall throughput at concurrency 16 before latency rises sharply at 32.

## card

**Що сталося:** NVIDIA показав, як розгорнути GLM-5.3 NVFP4 (753B параметрів загалом, 40B активних) на двох DGX Station, з'єднаних через ConnectX-8 RDMA, використовуючи vLLM 0.30.0 з tensor parallelism (TP=2) — модель вагою ~464 ГБ не вміщується в 252 ГБ HBM3e однієї GPU GB300.

**Контекст:** Частина серії технічних матеріалів NVIDIA про розгортання великих MoE-моделей на DSX-інфраструктурі; використані оптимізації — multi-token prediction (4 draft-токени), FP8 KV cache, prefix caching, контекст до 98 304 токенів.

**Деталі:**
- Пам'ять: ~218 ГіБ ваг на GPU, ~231 ГіБ використаної пам'яті після завантаження.
- Бенчмарк SPEED-Bench Coding (prefix caching увімкнено): при concurrency=16 — 607.8 ток/с сумарно (42.4 ток/с на користувача, середня латентність 136.46 с); при concurrency=32 пропускна здатність падає до 385.0 ток/с, а латентність різко зростає до 453.54 с.
- Передумови: гейтований датасет на Hugging Face, NVIDIA Open Model Agreement, щонайменше 464 ГБ вільного диска на кожній Station.
