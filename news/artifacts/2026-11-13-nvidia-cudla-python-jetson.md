---
company: nvidia
title: "Run Native DLA Inference in Python on NVIDIA Jetson AGX Orin Using cuDLA"
url: https://developer.nvidia.com/blog/run-native-dla-inference-in-python-on-nvidia-jetson-agx-orin-using-cudla/
date: 2026-11-13
found_via: rss
---

NVIDIA ships `cuda.bindings.cudla`, a new Python wrapper for the cuDLA C++ API (13 functions, 9 data types, 8 enums) as part of cuda-bindings 13.3.0, letting Jetson AGX Orin — and for the first time RTX Spark on Windows — run Deep Learning Accelerator inference directly from Python without a separate cuDLA SDK.

## card

**Що сталося:** NVIDIA випустив `cuda.bindings.cudla` — новий Python-модуль (у складі cuda-bindings 13.3.0), що обгортає C++ API cuDLA, і вперше дозволяє запускати інференс на NVIDIA DLA (Deep Learning Accelerator) просто з Python — на Jetson AGX Orin і, вперше, на RTX Spark під Windows.

**Контекст:** Раніше робота з cuDLA вимагала C++; новий Python API знижує порог входу, зберігаючи ту саму логіку (лише hybrid-режим на базі CUDA stream підтримується в цьому релізі).

**Деталі:**
- Встановлення: `pip install "cuda-bindings>=13.3.0"`, потрібен Python 3.10+.
- `libcudla.so` вже входить у JetPack — окремий SDK cuDLA не потрібен для запуску інференсу.
- TensorRT потрібен лише для компіляції DLA loadable через `trtexec` (приклад перевірено на TensorRT 11.4.1, CUDA 13.4 Update 1, JetPack 7.2.2+).
- Standalone-режим у цьому релізі не підтримується — лише hybrid.
- Приклади — у репозиторії NVIDIA Deep Learning Accelerator samples; юніт-тести працюють без апаратного DLA.
