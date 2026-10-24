---
company: nvidia
title: "Scaling NVIDIA TensorRT Performance Optimization Beyond a Single Build Route with the Global Performance Tuner, Part 2"
url: https://developer.nvidia.com/blog/scaling-nvidia-tensorrt-performance-optimization-beyond-a-single-build-route-with-the-global-performance-tuner-part-2/
date: 2026-10-23
found_via: rss (TIER-1)
---

Part 2 of NVIDIA's Global Performance Tuner (TensorRT 11.1) writeup covers the algorithm and architecture: C++ APIs for applying/inspecting build routes, the `trtexec` tuning loop, and best practices (previewing routes via dry runs, resumable tuning, re-tuning on model/hardware change). Across ten evaluated workloads, tuning improved end-to-end performance 1.14x-1.63x over the default build route.

## card

**Що сталося:** Частина 2 розбору Global Performance Tuner (TensorRT 11.1) описує алгоритм і архітектуру фічі: C++ API для застосування/перевірки build routes, цикл тюнінгу `trtexec` та практичні рекомендації.

**Контекст:** Продовжує частину 1 (концептуальне пояснення без чисел) — тут наведено фактичні вимірювання продуктивності на реальних навантаженнях.

**Деталі:**
- На 10 тестових навантаженнях тюнінг покращив продуктивність у 1.14–1.63 рази порівняно зі стандартним build route.
- Практики: попередній перегляд routes через dry run, можливість призупинити/відновити тюнінг, повторний тюнінг при зміні моделі чи апаратного забезпечення.
