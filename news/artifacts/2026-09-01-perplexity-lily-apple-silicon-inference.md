---
company: Perplexity
title: "Optimizing On-Device Inference for Apple Silicon"
url: https://www.perplexity.ai/hub/blog/optimizing-on-device-inference-for-apple-silicon
published: 2026-09-01
source_url: https://www.perplexity.ai/hub/blog
fetched: 2026-09-02
---

Perplexity detailed Lily, a custom Rust/Metal inference engine for running Qwen3.6-35B-A3B on Apple silicon, reaching 1.23x MLX-LM's prefill throughput and 1.35x decode throughput on an M5 Max; to be open-sourced.

## card

**Що сталося:** Perplexity описала Lily — власний інференс-двигун на Rust з кастомними Metal-ядрами для запуску Qwen3.6-35B-A3B на Apple silicon, замість використання універсальних фреймворків.

**Контекст:** Оптимізації охоплюють фазу prefill (розкладка sparse MoE-маршрутизації на GPU, дековантизація 4-біт ваг під час матричного множення, чанкінг довгих промптів) та фазу decode (мінімізація переміщення даних на токен, злиття операцій); двигун планують відкрити.

**Деталі:**
- На MacBook Pro M5 Max (40-ядерний GPU, 128GB памʼяті): prefill 4156 tok/s проти 3388 у MLX-LM (у 1.23 рази швидше)
- Decode: 170.0 tok/s проти 126.4 у MLX-LM (у 1.35 рази швидше)
- При 4K токенах: 5749.9 tok/s prefill, 186.6 tok/s decode
- Числова узгодженість — розбіжність перплексії в межах 0.04%
- Двигун "буде відкритий незабаром", дата не вказана
