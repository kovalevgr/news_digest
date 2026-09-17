---
company: NVIDIA
title: "TensorRT Edge-LLM Completes the MLPerf Edge Agentic Benchmark 6.4x Faster on Jetson AGX Thor"
url: https://developer.nvidia.com/blog/tensorrt-edge-llm-completes-the-mlperf-edge-agentic-benchmark-6-4x-faster-on-jetson-agx-thor/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-09-16
fetched: 2026-09-17
---

NVIDIA's TensorRT Edge-LLM sets a record on the MLPerf Inference v6.1 Edge Agentic benchmark on a single Jetson AGX Thor Developer Kit, reaching 52.33 tokens/sec (6.4x faster than the llama.cpp reference) via NVFP4 quantization, FP8 KV cache, tree-based multi-token prediction, and KV-cache reuse across agent turns.

## card

**Що сталося:** NVIDIA TensorRT Edge-LLM встановлює рекорд на бенчмарку MLPerf Inference v6.1 Edge Agentic на одному пристрої Jetson AGX Thor Developer Kit — 52.33 токени/сек, у 6.4 рази швидше за референсну реалізацію llama.cpp.

**Контекст:** Бенчмарк моделює агентне навантаження на edge-пристрої (робота через кілька ходів розмови, виклики функцій) на відміну від одноразової відповіді чат-бота — саме тут дають ефект оптимізації на рівні кешу й квантизації.

**Деталі:**
- Час проходження бенчмарку: 24 хв 36 с проти 2 год 37 хв у референсній реалізації
- Медіанний час до першого токена: 247.12 мс; точність 87.94% на Berkeley Function Calling Leaderboard v4
- Навантаження: 1007 ходів у 20 розмовах, контекст сягає ~23.5K токенів; ~96% токенів промпту обслуговується з гарячого кешу
- Оптимізації: NVFP4-квантизація ваг і активацій, FP8 KV-кеш, дерево multi-token prediction (8 кроків, top-2, 16 вузлів верифікації), перевикористання KV-кешу між ходами агента
- Залізо: NVIDIA Jetson AGX Thor Developer Kit (одна одиниця), 128GB уніфікованої пам'яті, архітектура Blackwell
- Код доступний у гілці release/0.9.1-mlpinf репозиторію TensorRT Edge-LLM; калібрований чекпоінт Qwen3.6-27B NVFP4 — на Hugging Face
