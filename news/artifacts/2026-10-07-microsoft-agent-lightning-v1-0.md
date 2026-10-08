---
company: Microsoft
title: "Agent Lightning v1.0: A 3,500-Line Lightweight Agentic RL Framework for Training Agents with Real Harnesses"
url: https://www.microsoft.com/en-us/research/blog/agent-lightning-v1-0-a-3500-line-lightweight-agentic-rl-framework-for-training-agents-with-real-harnesses/
source_url: https://www.microsoft.com/en-us/research/feed/
published: 2026-10-07
fetched: 2026-10-08
---

Microsoft Research Asia open-sources Agent Lightning v1.0, a ~3,500-line reinforcement-learning framework that trains AI agents on their actual deployment harnesses, reporting a 2x RL speedup and a 14.6-point SWE-bench Verified gain.

## card

**Що сталося:** Microsoft Research Asia випустив Agent Lightning v1.0 — відкритий фреймворк агентного RL на ~3,500 рядків коду, що тренує агентів прямо на тих самих harness'ах, у яких вони працюють у продакшені (без переписування агента під окремий тренувальний контур). Ключова фіча — Collocated Async RL, що дає приблизно 2x прискорення end-to-end порівняно з синхронним RL, плюс нативна підтримка Kubernetes для rollout'ів агентів.

**Контекст:** Відповідає на поширену проблему агентного RL — тренувальні та продакшн-harness'и агентів зазвичай різні, що ускладнює перенесення навченої поведінки назад у реальну систему.

**Деталі:**
- Collocated Async RL: ~2x прискорення end-to-end проти синхронного RL
- Coding-агент на Qwen3.5-9B: SWE-bench Verified Pass@1 зросло з 41.8% до 56.4%
- Експеримент використав ~6,000 тренувальних прикладів
- Нативна підтримка Kubernetes для запуску rollout'ів агентів; код на GitHub (ліцензія не вказана в статті)
