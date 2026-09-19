---
company: NVIDIA
title: "Benchmarking LLM Inference at Scale with AIPerf"
url: https://developer.nvidia.com/blog/benchmarking-llm-inference-at-scale-with-aiperf/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-09-18
fetched: 2026-09-19
---

NVIDIA introduces AIPerf, an open-source, multiprocess redesign of GenAI-Perf for benchmarking LLM inference at scale, removing client-side bottlenecks (single-process limits, Python's GIL) so throughput/latency measurements reflect server performance rather than the benchmarking client.

## card

**Що сталося:** NVIDIA представила AIPerf — повністю перероблений інструмент для бенчмаркінгу LLM inference, наступник GenAI-Perf, побудований на мультипроцесній архітектурі, щоб клієнт бенчмарку сам не ставав вузьким місцем вимірювань.

**Контекст:** Традиційні підходи до бенчмаркінгу обмежені продуктивністю одного процесу та Python GIL, що обмежує паралелізм і спотворює вимірювання; AIPerf розділяє генерацію навантаження та обробку результатів на окремі процеси, координовані через ZMQ.

**Деталі:**
- Архітектура: worker-процеси генерують навантаження, окремі record-processor сервіси обробляють результати, координація через ZMQ
- Підтримує 15+ типів endpoint'ів (chat, responses, генерація зображень, rankings) та публічні датасети (ShareGPT, формати trace replay)
- Патерни навантаження: constant, Poisson, gamma-розподіли з керованою "burstiness", ramping для тестування конкурентності
- Метрики: TTFT, ITL, latency запиту, output token throughput з перцентилями та інтеграцією GPU-телеметрії (DCGM/pynvml)
- Відкритий код: github.com/ai-dynamo/aiperf; приклад у walkthrough — Qwen3-0.6B на vLLM, інструмент апаратно-агностичний
