---
company: NVIDIA
title: "Deploy an Open Model from Checkpoint to Inference in Two Commands with NVIDIA TensorRT Model Connect"
url: https://developer.nvidia.com/blog/deploy-an-open-model-from-checkpoint-to-inference-in-two-commands-with-nvidia-tensorrt-model-connect/
published: 2026-08-28
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-29
---

NVIDIA releases TensorRT Model Connect, an open-source collection of reference implementations that deploys open Hugging Face models straight into native C++ applications via a two-command build/run workflow, without PyTorch or a Python interpreter at runtime.

## card

**Що сталося:** NVIDIA випустила TensorRT Model Connect — набір відкритих референсних реалізацій для розгортання відкритих моделей з Hugging Face у нативні C++-застосунки всього за дві команди: збірка (`trtmc build`) і виконання без PyTorch чи Python-інтерпретатора під час інференсу.

**Контекст:** Інструмент вирішує проблему фрагментованого, специфічного для кожної моделі коду конвертації/препроцесингу/рантайму, слугуючи мостом між наскрізним досвідом інференсу відкритих моделей і GPU-прискоренням TensorRT.

**Деталі:**
- Build-фаза (Python CLI): `trtmc build Qwen/Qwen3-0.6B -o qwen3-0.6B.bundle`; runtime-фаза — C++, без PyTorch/Python
- Два рівні API: семантичний (задачі на рівні вхід/вихід) і модульний (прямий контроль тензорів)
- Підтримка 80+ родин моделей; кастомні kernels підключаються через TVM FFI
- Цільові платформи: x86, ARM, DRIVE AGX, Jetson AGX
- Нічні релізи; продуктивність на валідованих навантаженнях перевищує torch.compile
- Код відкритий: репозиторій NVIDIA/TensorRT-Model-Connect на GitHub
