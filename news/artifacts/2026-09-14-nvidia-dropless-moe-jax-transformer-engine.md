---
company: NVIDIA
title: "Accelerating Dropless MoE Training in JAX with NVIDIA Transformer Engine"
url: https://developer.nvidia.com/blog/accelerating-dropless-moe-training-in-jax-with-nvidia-transformer-engine/
published: 2026-09-14
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-15
---

NVIDIA details dropless MoE training optimizations for JAX built on Transformer Engine: grouped GEMM kernels handle ragged per-expert token counts without padding or host transfers, NCCL-based expert parallelism fuses dispatch/combine while deduplicating cross-network tokens, and JAX host offloading plus MXFP8 quantization round out the stack. Reports a 10.4x TFLOPS/GPU improvement for DeepSeek-V3 671B (103→1,068 TFLOPS/GPU on GB200) and 97% scaling efficiency sustained to 1,024 GPUs on GB300 NVL72. Ships in the NVIDIA NGC MaxText container (ghcr.io/nvidia/jax:maxtext-2026-09-09 or newer).

## card

**Що сталося:** NVIDIA публікує оптимізації для dropless-тренування MoE-моделей у JAX на базі Transformer Engine — без відкидання чи паддінгу токенів між експертами.

**Контекст:** Розв'язує стандартну проблему MoE-тренування: нерівномірний розподіл токенів між експертами створює "рвані" тензори, а комунікація між GPU домінує над корисним обчисленням. Рішення поєднує grouped GEMM-кернели, NCCL-based expert parallelism (об'єднані dispatch/combine з дедуплікацією токенів) та MXFP8-квантизацію.

**Деталі:**
- 10.4x приріст TFLOPS/GPU на DeepSeek-V3 671B: 103 → 1,068 TFLOPS/GPU на NVIDIA GB200
- 97% ефективності масштабування утримується аж до 1,024 GPU на GB300 NVL72
- Доступно в контейнері NVIDIA NGC MaxText (ghcr.io/nvidia/jax:maxtext-2026-09-09 і новіші)
- Документація конфігурації — в MoE-гайдах репозиторію MaxText на GitHub
