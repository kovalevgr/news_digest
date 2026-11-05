---
company: nvidia
title: "NVIDIA CUDA 13.5 Brings NVIDIA Vera Rubin GA Support"
url: https://developer.nvidia.com/blog/nvidia-cuda-13-5-brings-nvidia-vera-rubin-ga-support/
date: 2026-11-04
found_via: rss (TIER-1)
---

NVIDIA ships CUDA 13.5, moving Vera Rubin GPU support from early developer access to general availability, extends Windows-on-Arm support to DGX Station for Windows, and adds multi-GPU communication inside CUDA Tile kernels plus a Tile-to-SIMT interop preview.

## card

**Що сталося:** NVIDIA випустила CUDA 13.5: підтримка Vera Rubin переходить з раннього доступу розробникам у повну доступність (GA) для production; Windows on Arm, що став GA в CUDA 13.4, тепер поширюється на NVIDIA DGX Station for Windows.

**Контекст:** Релізу передувала серія CUDA-оновлень 2026 року (13.1–13.4), що поступово готували стек до архітектур Rubin/Vera; CUDA Tile й CCCL отримують паралельні вдосконалення в цьому ж релізі.

**Деталі:**
- cuBLAS/кернел-тюнінг прискорюють NVFP4- та MXFP8-матмули на Rubin "з коробки" (без наведених цифр); для Rubin і новіших GPU на Windows підтримуються WDDM/MCDM, TCC — ні.
- CUDA Tile: мультимейл/мультикаст-комунікація через NVLink/NVSwitch SHARP між GPU всередині Tile-кернелів; публічний preview інтеропу Tile-до-SIMT (виклик library device-функцій NVSHMEM/CCCL Coop/Warp/MathDx).
- cuSPARSE: FP32/FP64 CSR SpMM (ALG3) швидше у 1.65–2.27x; нова SpSV ALG2 швидша за ALG1 у 2.7x (геометричне середнє); аналіз SpSV — 2.79x.
- cuBLAS: native FP64 SYR2K/HER2K/SYRKX/HERKX до 1.5x швидше на B200; nvJPEG GPU Hybrid decode — на 10–600% швидше залежно від розміру зображення.
- MPS v3 додає weighted timeslicing, запозичення/передачу SM-партицій, cgroup-based маршрутизацію по namespace.
