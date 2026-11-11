---
company: nvidia
title: "Agent Substrate: Advancing Kubernetes for Agents at Scale"
url: https://developer.nvidia.com/blog/agent-substrate-advancing-kubernetes-for-agents-at-scale/
date: 2026-11-10
found_via: rss
---

NVIDIA open-sources Agent Substrate, now a CNCF Sandbox project — a runtime that maps many sandboxed AI-agent sessions onto a small pool of warm Kubernetes worker Pods, checkpointing idle sessions instead of keeping a Pod per agent or paying cold starts.

## card

**Що сталося:** NVIDIA відкрила вихідний код Agent Substrate (тепер проєкт CNCF Sandbox) — runtime, що розміщує багато сесій ізольованих AI-агентів на невеликому пулі "теплих" Kubernetes Pod-воркерів, чекпоінтячи неактивні сесії замість утримання Pod на кожного агента.

**Контекст:** Входить до платформи NVIDIA DSX AI Factory й інтегрується з NVIDIA Dynamo (маршрутизація за ідентичністю сесії й KV-кешем) та KAI Scheduler; подано як противагу власницьким agent-runtime, що оминають Kubernetes.

**Деталі:**
- Заявлена "10x вища щільність, ніж у стандартних контейнерах" і підтримка "мільйонів агентів" — без наведеної методології чи вимірювань.
- Request parking у роутері ставить запити в черу, коли всі воркери зайняті, замість відмови (PR #221, #1229); ізоляція CPU/памʼяті на контейнер для microVM-сенбоксів (PR #859).
- Запланована підтримка GPU через Kubernetes DRA (спершу NVIDIA GPU).
- Проєкт ще змінюється: API нестабільні, підтримка GPU перебудовується, частина інтеграції з Dynamo експериментальна. Джерело на GitHub: `agent-substrate/substrate`.
