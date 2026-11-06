---
company: nvidia
title: "Configure, Certify, and Operate Kubernetes GPU Clusters with NVIDIA DSX OS"
url: https://developer.nvidia.com/blog/configure-certify-and-operate-kubernetes-gpu-clusters-with-nvidia-dsx-os/
date: 2026-11-05
found_via: rss
---

NVIDIA open-sources DSX OS (Apache 2.0), a layer of the DSX AI Factory Platform with three tools — AI Cluster Runtime (version-locked config recipes), Cluster Readiness Engine (NCCL/training-based node certification that bisects failing node groups), and NVSentinel (health monitoring that can cordon/drain/remediate nodes) — aimed at goodput, not just utilization, on accelerated Kubernetes clusters.

## card

**Що сталося:** NVIDIA відкрила вихідний код DSX OS (Apache 2.0) — три інструменти для налаштування, сертифікації та підтримки здоров'я Kubernetes GPU-кластерів: AI Cluster Runtime (конфігурація), Cluster Readiness Engine (сертифікація через NCCL-тести й тренувальні навантаження), NVSentinel (моніторинг і автоматичне виведення несправних вузлів).

**Контекст:** Мета — goodput (корисна пропускна здатність), а не просто утилізація: один недопрацьований GPU може сповільнити весь розподілений тренувальний прогін, навіть пройшовши базові health-check'и.

**Деталі:**
- Cluster Readiness Engine при провалі тесту ділить групу вузлів навпіл і повторює тести, щоб звузити коло підозрюваних вузлів до мінімального розміру групи.
- NVSentinel за замовчуванням встановлюється в режимі моніторингу; подальші дії (cordon/drain/remediate) — опціональні.
- Приклад порогу: `busBandwidthGBps: "value >= 300"` — порогів за замовчуванням немає.
- Валідовано на претренуванні з NVIDIA NeMo Framework (моделі 8B і 56B параметрів).
- Усі три проєкти — Apache 2.0, доступні на GitHub з інструкціями встановлення; NVIDIA також проводить окремий воркшоп на KubeCon + CloudNativeCon North America.
