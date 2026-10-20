---
company: nvidia
title: "Accelerating Mamba-2 with High-Performance Forward Pass Kernels in NVIDIA CUDA Tile"
url: https://developer.nvidia.com/blog/accelerating-mamba-2-with-high-performance-forward-pass-kernels-in-nvidia-cuda-tile/
date: 2026-10-19
found_via: TIER-1 rss (developer.nvidia.com/blog/feed)
---

Engineers from Jane Street, working with NVIDIA, implemented the Mamba-2 state-space model's forward pass as three custom kernels in NVIDIA's cuTile Python DSL, exploiting the fact that Mamba-2's recurrence can be computed in chunks via matmuls usable on Tensor Cores — reporting 1.14x–1.82x speedups over a Triton-based baseline on a Blackwell Ultra B300 GPU; the backward pass is left for a future post.

## card

**Що сталося:** Інженери Jane Street у співпраці з NVIDIA реалізували forward pass моделі стейт-спейс архітектури Mamba-2 як три кастомні кернели на Python-DSL NVIDIA CUDA Tile (cuTile), скориставшись тим, що рекурентність Mamba-2 можна рахувати по чанках через матричні множення, придатні для Tensor Cores (на відміну від звичайних RNN).

**Контекст:** Три кернели — `chunk_cumsum`, `fwd_pass_state` та `compute_out` (останній обʼєднує carried-state, decayed causal-masked взаємодію та skip-connection доданки, тримаючи матрицю взаємодії в регістрах). Backward pass автори залишають для майбутнього посту; код доступний у репозиторії TileGym (`tilegym.ops.mamba2_chunk_forward`).

**Деталі:**
- Тестова конфігурація: batch 4, 16 384 токени, 8 голів, розмір стейту 128, розмір голови 64, chunk size 128, bf16-входи/fp32-стейт, одна GPU NVIDIA B300 SXM6 (Blackwell Ultra, 1920 MHz, 1100 W).
- Софт: PyTorch 2.13.0, CUDA 13.3, Triton 3.7.1, cuda-tile 1.5.0.
- Результат: кернели на cuTile швидші на 1.14x–1.82x за Triton-базлайн `mamba_ssm` 2.3.2.post1; прискорення зростає з довжиною послідовності та розміром стейту.
- Автори уточнюють: наведені цифри — приріст лише на рівні кернелів, не end-to-end вимірювання.
