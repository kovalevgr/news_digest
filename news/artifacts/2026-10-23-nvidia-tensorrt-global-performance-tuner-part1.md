---
company: nvidia
title: "Scaling NVIDIA TensorRT Performance Optimization Beyond a Single Build Route with the Global Performance Tuner, Part 1"
url: https://developer.nvidia.com/blog/scaling-nvidia-tensorrt-performance-optimization-beyond-a-single-build-route-with-the-global-performance-tuner-part-1/
date: 2026-10-23
found_via: rss (TIER-1)
---

NVIDIA introduces the Global Performance Tuner, a new TensorRT 11.1 feature that builds a set of candidate engines from customizable "build routes," checks each candidate's accuracy and performance, and picks the fastest one meeting an accuracy tolerance. Part 1 frames engine building as a scheduling problem (chef analogy, mathematical model of builder/search algorithms) explaining why no single fixed build strategy suits every model; no benchmark numbers in this part (those are in Part 2).

## card

**Що сталося:** NVIDIA представила Global Performance Tuner — нову функцію TensorRT 11.1, яка будує набір кандидатних "build routes", перевіряє точність і швидкість кожного та вибирає найшвидший варіант у межах допустимої похибки точності.

**Контекст:** Частина 1 пояснює концептуальну проблему: чому жодна фіксована стратегія компіляції не підходить для всіх моделей — через аналогію з шеф-кухарем і математичну модель алгоритмів побудови/пошуку. Числові результати описані в частині 2.

**Деталі:**
- Фіча випущена в TensorRT 11.1.
- Підхід будує кілька кандидатних engine-конфігурацій ("build routes") і вибирає найшвидшу за умови точності.
- Ця частина — концептуальна, без бенчмарків (вони в Part 2).
