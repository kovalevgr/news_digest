---
company: NVIDIA
title: "Simplifying Model Serving Across Multiple GPUs with NVIDIA TensorRT Multi-Device Integration in NVIDIA Dynamo-Triton"
url: https://developer.nvidia.com/blog/simplifying-model-serving-across-multiple-gpus-with-nvidia-tensorrt-multi-device-integration-in-nvidia-dynamo-triton/
published: 2026-09-21
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-22
---

NVIDIA details TensorRT multi-device inference (TensorRT 11.0), now integrated into Dynamo-Triton 26.07, letting a single TensorRT network run distributed across multiple GPUs via NCCL while keeping a conventional single-endpoint serving interface; on a Cosmos 3 Nano video-generation workload with Ulysses context parallelism, 8 GPUs cut end-to-end latency from 156.6s to 34.2s (4.58x speedup, 78.17% latency reduction).

## card

**Що сталося:** NVIDIA представляє TensorRT multi-device inference (TensorRT 11.0), інтегрований у Dynamo-Triton (реліз 26.07) — можливість виконувати одну TensorRT-мережу розподілено на кількох GPU через NCCL-колективи, зберігаючи для клієнтів звичний єдиний інтерфейс обслуговування моделі.

**Контекст:** Рішення вирішує проблему зростання обчислювальних і пам'яттєвих вимог генеративного ШІ, що дедалі частіше перевищують можливості однієї GPU; один інстанс Triton `KIND_MODEL` тепер може володіти кількома GPU і створювати per-rank контексти виконання TensorRT, CUDA-потоки та NCCL-комунікатори без потреби клієнтам самим координувати ранги GPU.

**Деталі:**
- Тест на генерації відео Cosmos 3 Nano з Ulysses context parallelism (44 160 відео-токенів)
- 1 GPU: 156.6 с наскрізної затримки; 8 GPU: 34.2 с — прискорення 4.58x
- Прискорення трансформерного RPC — 6.09x, зниження затримки — 78.17% на 8 GPU
- Доступно для завантаження через NVIDIA NGC (Dynamo-Triton 26.07)
