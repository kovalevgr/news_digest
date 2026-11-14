---
company: nvidia
title: "Faster Scientific Simulations with New FP64 Algorithms in NVIDIA cuBLAS"
url: https://developer.nvidia.com/blog/faster-scientific-simulations-with-new-fp64-algorithms-in-nvidia-cublas/
date: 2026-11-13
found_via: rss
---

NVIDIA ships new Ozaki-II and 2M floating-point-emulation algorithms in cuBLAS (CUDA Toolkit 13.4.2) that speed up FP64 and complex (ZGEMM) matrix multiplication with no code changes required — cuBLAS auto-selects the algorithm and falls back to native FP64 to preserve accuracy, with Rubin GPUs getting a new TI16 format for further acceleration.

## card

**Що сталося:** NVIDIA додав у cuBLAS (CUDA Toolkit 13.4.2) нові алгоритми емуляції чисел із рухомою комою — Ozaki-II (на основі китайської теореми про залишки, вдвічі менше цілочисельних GEMM за Ozaki-I при тій самій точності) та 2M (комплексне множення матриць за 2 реальні GEMM замість 4). Зміни коду не потрібні — cuBLAS сам вибирає алгоритм і повертається до нативного FP64, якщо точність під загрозою.

**Контекст:** Продовження роботи над Ozaki-I (емуляція FP64); нова ревізія Rubin GPU (compute capability 10.7) отримує окремий формат TI16 для прискорення Ozaki-I/II.

**Деталі:**
- DGEMM проти нативного FP64: 5.5x (Vera Rubin NVL72), 3.9x (GB200), до 23x (RTX PRO 6000 Blackwell Server Edition).
- DGEMM проти Ozaki-I: 2x швидше на GB200.
- ZGEMM (2M) проти нативного комплексного FP64: 5x на GB200.
- Квантова хімія (CCSD): 2x/1.4x end-to-end у повному FP64 (VR NVL72/GB200), 5x/3.5x у змішаній точності.
- Матеріалознавство (BerkeleyGW): 6.6x/3.9x проти нативного ZGEMM (VR NVL72/GB200).
- Доступно в документації cuBLAS (секція floating-point emulation, `cublasSetEmulationStrategy`) і прикладах на GitHub.
