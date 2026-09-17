---
company: NVIDIA
title: "Translating CUDA Tile Operations from Python to Rust Using Agentic AI"
url: https://developer.nvidia.com/blog/translating-cuda-tile-operations-from-python-to-rust-using-agentic-ai/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-09-16
fetched: 2026-09-17
---

NVIDIA describes using a multi-agent workflow (separate subagents for analysis, kernel writing, host/FFI code, and benchmarking, with machine-checkable verdicts at each stage) to port all 24 public TileGym operators (~40 GPU kernels) from cuTile Python to the new cuTile Rust front end, reaching 99.5% of the Python version's performance on NVIDIA DGX B200.

## card

**Що сталося:** NVIDIA описує, як мультиагентний AI-workflow переніс усі 24 публічні оператори TileGym (~40 GPU-ядер) з cuTile Python на новий фронтенд cuTile Rust — систему для написання безпечних, ідіоматичних GPU-ядер на Rust, що розширює модель володіння Rust на GPU-ядра.

**Контекст:** cuTile Python, Triton-TileIR і cuTile Rust — три фронтенди на спільному фундаменті CUDA Tile IR; workflow використовує спеціалізовані субагенти (аналіз, написання ядра, host/FFI-код, бенчмаркінг) з перевірюваними на кожному етапі вердиктами та IR-діффінгом проти референсної реалізації замість перевірки на основі тексту.

**Деталі:**
- Перенесено всі 24 публічні оператори TileGym (~40 GPU-ядер)
- Продуктивність: у середньому 99.5% від швидкості cuTile Python; усі 24 оператори перевищили поріг 0.95 geomean-прискорення відносно Python-базлайну
- Бенчмарк: NVIDIA DGX B200, 347 парних конфігурацій
- Обмежені ліміти повторних спроб запобігають нескінченним циклам; збій маршрутизується конкретному відповідальному
- Доступно в репозиторії TileGym на GitHub: agent skill, 49 правил кодування, довідкові документи, скрипти-валідатори, приклади; вимоги — CUDA 13.1+, GPU Blackwell, Rust 1.89+, компілятор tileiras
