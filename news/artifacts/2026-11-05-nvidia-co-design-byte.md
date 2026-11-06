---
company: nvidia
title: "Five Ways NVIDIA Co-Design Maximizes the Value of Every Byte in the AI Factory"
url: https://developer.nvidia.com/blog/five-ways-nvidia-co-design-maximizes-the-value-of-every-byte-in-the-ai-factory/
date: 2026-11-05
found_via: rss
---

NVIDIA argues AI factories should be measured by useful tokens per byte of memory, describing five co-designed levers (NVFP4 precision, Wide-EP in TensorRT-LLM, Dynamo fleet-wide KV-cache management, the Vera CPU as a warm memory tier, and CMX pod-level flash storage) and claiming Vera Rubin NVL72 delivers up to 30x the throughput per megawatt of GB300 NVL72 on a SemiAnalysis AgentX coding-agent replay, at the same 288GB HBM per GPU.

## card

**Що сталося:** NVIDIA описала п'ять технік спільного дизайну (co-design), що економлять пам'ять AI-фабрик: формат NVFP4, широкий expert-parallelism (Wide-EP) у TensorRT-LLM, NVIDIA Dynamo для керування KV-кешем на рівні флоту, CPU Vera як "тепла" пам'ять, і CMX — пулова flash-пам'ять.

**Контекст:** Теза посту — вимірювати AI-фабрики не обсягом пам'яті, а корисними токенами на байт пам'яті; підсумковий заявлений результат: Vera Rubin NVL72 показує до 30x пропускної здатності на мегават проти GB300 NVL72 на тому самому обсязі HBM (288 ГБ на GPU) у реплеї SemiAnalysis AgentX (сесії coding-агентів).

**Деталі:**
- NVFP4: скорочує вагу модели ~3.5x проти FP16 і 1.8x проти FP8; NVFP4 KV-кеш менший на до 50% проти FP8 (вдвічі більший контекст на пристрої); до 4x пропускної здатності на мегават проти FP8-бейзлайну (DeepSeek R1 на GB300); >99% якості BF16-бейзлайну на 10 бенчмарках DeepSeek-v4-Pro.
- Wide-EP на GB200 NVL72: EP32 дає до 1.8x output tokens/s на GPU проти EP8 при 100 токенів/с на користувача.
- Dynamo: приклади вендорів — VAST до 35 ГБ/с на один H100 через GPUDirect Storage, WEKA — до 270 ГБ/с на вісім H100.
- Vera CPU: 88 ядер Olympus, до 1.5 ТБ LPDDR5X (>5x HBM4 одного Rubin GPU), NVLink-C2C 1.8 ТБ/с (~7x PCIe Gen 6 x16).
- CMX: заявлено до 5x пропускної здатності токенів/с і до 5x енергоефективності проти традиційного сховища для довгоконтекстного інференсу.
- Застереження: цифри — від NVIDIA та вендорів-партнерів на їхніх тестових конфігураціях; власний графік посту (Figure 4) показує дещо нижчі NVFP4 KV-показники на кожному бенчмарку без прямого вимірювання економії пам'яті.
