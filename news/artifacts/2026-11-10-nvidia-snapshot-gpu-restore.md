---
company: nvidia
title: "Start and Restore GPU Workloads in Seconds with NVIDIA Snapshot"
url: https://developer.nvidia.com/blog/start-and-restore-gpu-workloads-in-seconds-with-nvidia-snapshot/
date: 2026-11-10
found_via: rss
---

NVIDIA open-sources Snapshot, a checkpoint/restore system for GPU inference workloads on Kubernetes that restores a fully-initialized vLLM/SGLang/TensorRT-LLM worker (CPU+GPU state) in seconds instead of minutes of cold start, built originally for NVIDIA Dynamo.

## card

**Що сталося:** NVIDIA відкрила Snapshot — систему чекпоінта й відновлення GPU-навантажень на Kubernetes, що зберігає повністю інціалізований inference-воркер (CPU+GPU стан) і відновлює його за секунди замість хвилин холодного старту.

**Контекст:** Компонент платформи NVIDIA DSX AI Factory, створений спершу для воркерів NVIDIA Dynamo; готові приклади для vLLM, SGLang та TensorRT-LLM; код на github.com/ai-dynamo/snapshot.

**Деталі:**
- Відновлення: 3.6–42.7 с — у 8–36 разів швидше за холодний старт (1.5–19 хв) на NVIDIA B200.
- Створення чекпоінта: 15 с – 5.5 хв (одноразова вартість на конфігурацію); чекпоінт+відновлення коротше за один холодний старт у всіх протестованих випадках.
- Для 8-GPU MoE: відновлення GPU-стану 18–29 с, CRIU CPU-відновлення 4.2–10.8 с; мультимульти-GPU чекпоінти до 1 ТБ на 8 GPU.
- Партнери: Crusoe — готовність GLM-5.3 впала з ~8 хв до 31 с на HGX B300; Saturn Cloud — старт vLLM з 2–8.5 хв до 6–34 с на HGX B300.
