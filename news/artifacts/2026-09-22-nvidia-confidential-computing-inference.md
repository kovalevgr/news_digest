---
company: NVIDIA
title: "Enabling Private High-Performance Production AI Inference with NVIDIA Confidential Computing"
url: https://developer.nvidia.com/blog/enabling-private-high-performance-production-ai-inference-with-nvidia-confidential-computing/
published: 2026-09-22
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-23
---

NVIDIA details framework-level optimizations (in TensorRT-LLM) that let confidential-computing-protected LLM inference on Blackwell GPUs retain 96.1-98.2% of standard throughput with only 1.2-4.3% added per-token latency, tested with DeepSeek-R1 on 8x B200.

## card

**Що сталося:** NVIDIA публікує оптимізації на рівні фреймворку в TensorRT-LLM, які дозволяють запускати LLM-inference під захистом confidential computing на GPU Blackwell зі збереженням 96.1-98.2% пропускної здатності звичайного режиму.

**Контекст:** Обробка чутливих даних і власного контексту моделей у продакшн-inference дедалі частіше вимагає конфіденційних обчислень; стаття показує, що для збереження продуктивності фреймворк inference і середовище confidential computing треба оптимізувати спільно, а не окремо.

**Деталі:**
- Тестування: DeepSeek-R1, вхід 32K / вихід 1K токенів, 8x NVIDIA B200
- Пропускна здатність: 96.1-98.2% від базового рівня на конкурентності 1-16
- Оверхед латентності на токен: 1.2-4.3% понад базовий рівень
- Три оптимізації в TensorRT-LLM: CC-aware вибір памʼяті для передачі даних, автотюнінг ядер на основі GPU-таймера, вибір алгоритмів з урахуванням недоступності NVLS multicast
- Доступно в TensorRT-LLM 1.3.0rc22 і новіших версіях
