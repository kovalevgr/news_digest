---
company: NVIDIA
title: "How DOCA GPUNetIO Unifies GPU-Initiated Networking Across the NVIDIA Software Stack"
url: https://developer.nvidia.com/blog/doca-gpunetio-gda-ki-unified-gpu-networking/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-10-06
fetched: 2026-10-07
---

NVIDIA unifies GPU-initiated networking across its software stack with DOCA GPUNetIO, an open-source foundation letting CUDA kernels directly control Ethernet, RDMA, and DMA operations without CPU intervention.

## card

**Що сталося:** NVIDIA представляє DOCA GPUNetIO як єдину відкриту основу для GPU-initiated networking — CUDA-ядра безпосередньо керують Ethernet, RDMA та DMA операціями без участі CPU.

**Контекст:** Фреймворк стає спільним GDA-KI (GPUDirect Async Kernel-Initiated) бекендом для кількох комунікаційних бібліотек NVIDIA одразу, усуваючи дублювання реалізацій по стеку.

**Деталі:**
- Спільний бекенд для NCCL, NVSHMEM та NVQLink
- ~2.6 мікросекунди латентності для quantum-classical воркфлоу
- Покращене масштабування пропускної здатності для малих повідомлень у розподілених GPU-застосунках
