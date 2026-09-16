---
company: Hugging Face
title: "Your Agent Aced the Task. Will It Do It Again?"
url: https://huggingface.co/blog/ibm-research/altk-evolve-consistency
source_url: https://huggingface.co/blog/feed.xml
published: 2026-09-15
fetched: 2026-09-16
---

IBM Research introduces a consistency metric for LLM agents alongside accuracy: a Consistency Analyzer resamples each step of a recorded trajectory (k=5) to find unstable decision points, then auto-generates reusable Consistency Guidelines injected back into the agent's context. A ReAct agent on GPT-4.1 succeeded on 77.4% of runs (Mean@5) but all 5 runs on only 53.0% of tasks (Pass^5); guidelines closed the gap from 24.4pp to 12.0pp, lifting Pass^5 to 69.0% and Mean@5 to 81.0%, with +13.0pp generalization to related tasks.

## card

**Що сталося:** IBM Research пропонує метрику консистентності для AI-агентів на додачу до точності: задачі, що проходять у тестуванні, можуть провалюватися при повторному однаковому запиті.

**Контекст:** Consistency Analyzer перевибирає (resampling, k=5) кожен крок записаної траєкторії, щоб знайти нестабільні точки рішень без повторного запуску всієї задачі; знайдені проблемні кроки автоматично перетворюються на Consistency Guidelines, які вбудовуються назад у контекст агента. Ключова відмінність: Mean@k (середній відсоток успіху) проти Pass^k (успіх у всіх k прогонах).

**Деталі:**
- ReAct-агент на GPT-4.1: 77.4% успіху за Mean@5, але лише 53.0% задач пройшли всі 5 прогонів (Pass^5)
- З guidelines розрив Mean@5 vs Pass^5 звузився з 24.4 до 12.0 п.п.
- Pass^5 зросло з 53.0% до 69.0%, Mean@5 — з 77.4% до 81.0%
- Guidelines узагальнюються на суміжні задачі: +13.0 п.п. приросту
