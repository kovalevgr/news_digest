---
company: NVIDIA
title: "CUDA Toolkit 13.4 Adds Windows on Arm Support and Greater Control over Shared GPUs"
url: https://developer.nvidia.com/blog/cuda-toolkit-13-4-adds-windows-on-arm-support-and-greater-control-over-shared-gpus/
published: 2026-09-09
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-10
---

NVIDIA ships CUDA Toolkit 13.4: Windows on Arm support, an early preview of the Rubin architecture, a modernized Multi-Process Service (V3), CUDA Python updates, and CCCL 3.4 performance work on Blackwell.

## card

**Що сталося:** NVIDIA випустила CUDA Toolkit 13.4 з підтримкою Windows on Arm (раніше лише Linux), попереднім доступом до архітектури Rubin (compute capability 107) та оновленим Multi-Process Service V3 для точнішого розподілу GPU-пам'яті в контейнерах.

**Контекст:** Черговий квартальний реліз CUDA Toolkit; продовжує лінію інструментів для розробників (Nsight, CCCL) і розширює платформну підтримку напередодні виходу архітектури Rubin.

**Деталі:**
- Windows on Arm: CUDA-застосунки тепер працюють на цій платформі
- MPS V3: скриптовий CLI, іменовані серверні інстанси, TOML-конфігурація, cgroup-інтегровані ліміти пам'яті GPU
- cuda.core 1.1.0: робота з текстурами/поверхнями, NUMA-aware managed memory, типові stub-файли; cuda.compute 1.1: ahead-of-time компіляція під кілька архітектур GPU без наявного заліза
- CCCL 3.4: до 92% використання пропускної здатності пам'яті для device-wide scan на Blackwell, єдині виклики API для алгоритмів
- Інструменти розробника: Nsight Python 1.0 (автоматичне профілювання ядер), Nsight Compute з підтримкою Tile IR, Nsight Systems 2026.5.1
