---
company: nvidia
title: "How to Optimize NVFP4 Attention on NVIDIA RTX Blackwell Through Register Recycling"
url: https://developer.nvidia.com/blog/how-to-optimize-nvfp4-attention-on-nvidia-rtx-blackwell-through-register-recycling/
date: 2026-11-25
found_via: TIER-1 rss
---

NVIDIA introduces "register recycling," a kernel-scheduling technique for NVFP4 attention on RTX Blackwell (SM120) GPUs that splits each 128-wide score tile into two 64-wide halves and reuses registers after softmax quantization, overlapping Tensor Core work with remaining softmax work.

## card

**Що сталося:** NVIDIA представляє "register recycling" — техніку планування обчислень для NVFP4 attention на GPU RTX Blackwell (SM120). Кернел розбиває кожен 128-широкий tile оцінок на дві 64-широкі половини і повторно використовує регістри кожної половини після квантування softmax для обчислення QK-добутку наступного tile, що накладає роботу Tensor Core на роботу softmax, що залишилась, без другого повного буфера оцінок.

**Контекст:** Техніка цілить саме споживчу архітектуру RTX Blackwell (SM120), яка відрізняється від дата-центрової Blackwell/Hopper, на яку орієнтовані FlashAttention3/4; пост опубліковано 25 листопада 2026 автором Atharva Joshi.

**Деталі:**
- Прискорення кернела: до 1.64× на синтетичному causal-бенчмарку з 8192 токенами на RTX PRO 6000 Blackwell Server Edition (з 0.76466 мс до 0.46659 мс).
- Наскрізний ефект: Reactor зафіксував зниження латентності до 15.34% на world-model навантаженнях (LongLive, Helios, OmniDreams, Cosmos 3 Nano).
- Апаратна ціль: GPU NVIDIA RTX Blackwell (SM120).
- Доступність: оптимізація влита в основну гілку FlashInfer; API для SM120 NVFP4 attention документовано в FlashInfer.
