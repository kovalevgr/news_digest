---
company: nvidia
title: "3 Ways to Boost MoE Inference on NVIDIA DGX Spark"
url: https://developer.nvidia.com/blog/3-ways-to-boost-moe-inference-on-nvidia-dgx-spark/
date: 2026-10-27
found_via: rss (TIER-1)
---

NVIDIA combines three inference optimizations — Humming MXFP4 MoE kernels, online FP8 LM-head quantization, and NEXTN multi-token-prediction speculative decoding — for Ling-3.0-flash (124B MoE, 5.1B active) on DGX Spark, reporting a 42.5% decode throughput gain and 24.5% lower latency on GSM8K with no measurable accuracy loss.

## card

**Що сталося:** NVIDIA показує три техніки прискорення inference для MoE-моделі Ling-3.0-flash (Inclusion AI, 124B параметрів, 5.1B активних) на DGX Spark при batch size 1: заміну MXFP4 MoE-ядер на бібліотеку Humming, онлайн-квантування LM head з BF16 у FP8, і спекулятивне декодування через вбудований шар NEXTN (multi-token prediction).

**Контекст:** Частина серії технічних публікацій NVIDIA про оптимізацію inference на DGX Spark; автори окремо зазначають, що комбінація FP8 LM-head і MTP потребує спільного LM-head модуля між моделлю й драфт-моделлю — інакше конфігурація непомітно сповільнюється нижче базового рівня.

**Деталі:**
- Лише Humming (синтетичне навантаження 32K/2K): час на токен впав з 27.71 до 25.35 мс (+9.3% throughput).
- + FP8 LM head: 22.76 мс/токен, 43.94 tok/s (+21.7% проти базового рівня).
- + MTP (NEXTN): 9.72 мс/токен, 102.88 tok/s (+185.1% на синтетичному навантаженні, 3.90 прийнятих токенів за раунд).
- Повний набір GSM8K (1319 задач, усі три оптимізації разом): throughput +42.5% (37.81→53.89 tok/s), латентність -24.5% (15.21с→11.49с), точність 96.89%→96.82% (статистично невідчутна зміна).
- Автори попереджають: показник +185.1% — із синтетичного навантаження з жадібним декодуванням, не гарантує такого ж приросту на інших задачах.
