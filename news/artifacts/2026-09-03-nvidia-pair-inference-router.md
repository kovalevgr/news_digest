---
company: NVIDIA
title: "NVIDIA PAIR Virtual Inference Router Expands Available Compute on Your Local Network"
url: https://developer.nvidia.com/blog/nvidia-pair-virtual-inference-router-expands-available-compute-on-your-local-network/
published: 2026-09-03
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-04
---

NVIDIA released PAIR (Personal AI Router) in open-source beta — a virtual inference router that distributes independent inference requests across Ollama/LM Studio nodes on a local network without code changes, cutting a 5-subagent test from 18 min to 8m48s on a 3-device cluster.

## card

**Що сталося:** NVIDIA випустив у відкритій бета-версії PAIR (Personal AI Router) — віртуальний маршрутизатор інференсу, що розподіляє незалежні запити інференсу між доступними пристроями в локальній мережі, усуваючи вузькі місця в багатоагентних сценаріях без змін коду агентів.

**Контекст:** Працює як проксі до наявних рушіїв інференсу (Ollama, LM Studio), не об'єднує GPU і не розбиває окремі запити між машинами — кожен інференс виконується повністю на одному вузлі.

**Деталі:**
- У тесті з 5 підагентами (Hermes Desktop + Ollama, модель Qwen): одна RTX Spark — 18 хв, кластер із 3 пристроїв PAIR — 8 хв 48 с
- Підтримувані пристрої: NVIDIA GeForce RTX 20-ї серії і новіші, RTX PRO workstation GPU, DGX Spark, Apple Silicon M4+
- Виявлення пристроїв через mDNS, взаємне TLS-шифрування, безпечне спарювання
- Бета доступна для Windows, macOS, Linux (GUI та термінал); проєкт відкритий на GitHub
