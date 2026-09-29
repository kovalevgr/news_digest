---
company: NVIDIA
title: "Add Runtime Controls to AI Agents with NVIDIA OpenShell"
url: https://developer.nvidia.com/blog/add-runtime-controls-to-ai-agents-with-nvidia-openshell/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-09-28
fetched: 2026-09-29
---

NVIDIA details OpenShell 0.1.0, an open-source runtime that enforces security policies around AI agents (filesystem/process controls, credential substitution, formal policy verification) without modifying agent code.

## card

**Що сталося:** NVIDIA випустила OpenShell 0.1.0 — рантайм з відкритим кодом, що дозволяє накладати перевіряємі обмеження на автономних AI-агентів на рівні виконання, без зміни коду самого агента; складається з Gateway (керування пісочницями й політиками), Supervisor (перевірка вихідних запитів проти політик) та Sandbox (контроль на рівні ядра над файловою системою й процесами).

**Контекст:** OpenShell — відкрита складова щойно представленої Open Agent Safety Platform (окремий пост того ж дня), де апаратний рівень примусового виконання забезпечує NVIDIA Sentry на BlueField-4 DPU.

**Деталі:**
- Формальна верифікація політик, підстановка облікових даних поза робочим процесом агента, runtime policy advisors
- Рання інтеграція: Cadence (дизайн чипів), Slack (корпоративна автоматизація), Gecko Robotics (робототехніка)
- Підтримує Codex, Claude Code та інші агентні фреймворки; працює в Docker, Kubernetes та інших середовищах
- Відкритий код, ліцензія Apache 2.0
