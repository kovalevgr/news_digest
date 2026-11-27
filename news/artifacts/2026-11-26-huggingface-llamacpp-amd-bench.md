---
company: huggingface
title: "Introducing the llama.cpp benchmark dashboard for AMD Ryzen and Radeon"
url: https://huggingface.co/blog/ggml-org/llamacpp-amd-bench
date: 2026-11-26
found_via: TIER-1 rss
---

The ggml-org team publishes a public Hugging Face-hosted dashboard tracking llama.cpp prompt-processing and text-generation throughput across builds, models, and quantizations on AMD hardware.

## card

**Що сталося:** Команда ggml-org (автори llama.cpp) публікує на блозі Hugging Face панель моніторингу продуктивності llama.cpp на AMD-обладнанні — Radeon 8060S (gfx1151) та Radeon AI Pro R9700S (gfx1201). Панель відстежує два показники у токенах/с: PP512 (обробка 512 вхідних токенів) та TG128 (генерація 128 токенів), а також окрему вкладку масштабування за розміром контексту.

**Контекст:** Бенчмарки запускаються щотижня через автоматизовані workflow на базі `llama-bench` (Flash Attention увімкнено/вимкнено, 10 повторів на конфігурацію), використовуючи попередньо зібрані бінарники з `llama-install.sh`. Проєкт продовжує серію Hugging Face-постів з інфраструктурними інструментами спільноти llama.cpp.

**Деталі:**
- Моделі в бенчмарку: Inkling 2 Mini, Qwen, Gemma, gpt-oss, LFM — покриває як dense, так і MoE-архітектури.
- Квантизації: Q4_K_M, Q8_0, BF16, F16 та інші.
- Дані відкриті публічно в Hugging Face Storage Bucket (`ggml-org/install.sh-benches-data`), організовані як JSONL-файли за build/hardware/model/quantization.
- Тестову інфраструктуру надала AMD; команда запрошує пропозиції щодо нових моделей і навантажень.
