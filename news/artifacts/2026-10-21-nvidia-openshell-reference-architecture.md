---
company: nvidia
title: "How NVIDIA OpenShell Reference Architecture Secures and Governs AI Agent Workloads at Scale"
url: https://developer.nvidia.com/blog/how-nvidia-openshell-reference-architecture-secures-and-governs-ai-agent-workloads-at-scale/
date: 2026-10-21
found_via: TIER-1 rss (developer.nvidia.com/blog/feed)
---

NVIDIA releases OpenShell, an open-source reference architecture (Gateway, Supervisor, Sandbox, Policy Prover) that treats AI agents as untrusted and grants access only when needed; on NVIDIA Vera CPUs, CoreWeave reported 3x faster sandbox startup and 1.8x faster agentic-loop completion vs. a leading x86 CPU. Available on GitHub.

## card

**Що сталося:** NVIDIA випускає OpenShell Reference Architecture — відкриту еталонну архітектуру для безпеки й управління AI-агентами у великому масштабі, яка розглядає агентів як недовірені сутності та надає доступ лише за потреби.

**Контекст:** Архітектура складається з чотирьох компонентів: Gateway (контрольна площина), Supervisor (перевірка політик і опосередкування облікових даних), Sandbox (ізоляція навантаження) і Policy Prover (формальна верифікація прав доступу). Працює на процесорах NVIDIA Vera; код доступний на GitHub (NVIDIA/OpenShell), документація — у Secure Agent Workspace Reference Design.

**Деталі:**
- CoreWeave на NVIDIA Vera CPU зафіксував запуск sandbox у 3 рази швидше та завершення агентного циклу в 1,8 раза швидше, ніж на провідному x86-процесорі.
- Архітектура — частина довідкової системи NVIDIA Sentry/OpenShell для безпеки агентів на рівні інфраструктури.
- Доступна як відкритий код на GitHub.
