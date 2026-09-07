---
company: Hugging Face
title: "Introducing @huggingface/kernels: 200+ WebGPU Kernels for Local AI"
url: https://huggingface.co/blog/webgpu-kernels
published: 2026-09-01
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-07
---

Hugging Face releases @huggingface/kernels, a JavaScript library with 207 optimized WebGPU kernels published on the Hub as versioned packages (shaders, correctness tests, benchmarks), plus Fleet, a browser-based crowdsourced benchmarking tool. Backfilled: missed by TIER-1 (blog listing outpaced the RSS feed); confirmed today via WebFetch.

## card

**Що сталося:** Hugging Face випускає `@huggingface/kernels` — бібліотеку на JavaScript із понад 200 оптимізованих WebGPU-ядер для локального інференсу в браузері; кожне ядро публікується на Hub як версійований пакет із реалізацією шейдера, тестами коректності та бенчмарками.

**Контекст:** Частина ширшого руху HF у бік локального/браузерного AI (WebGPU, on-device inference); доповнює попередні релізи на кшталт локальних/edge-моделей від Liquid AI та інших партнерів Hub.

**Деталі:**
- 207 WebGPU-ядер опубліковано в організації webgpu-kernels на Hub
- У середньому геометричному — у 2.57 раза швидше за ORT WebGPU на 809 тестових кейсах
- Медіанне прискорення — у 1.90 раза
- Разом із бібліотекою запущено Fleet — інструмент для краудсорсингового бенчмаркінгу продуктивності й коректності на різному апаратному забезпеченні
