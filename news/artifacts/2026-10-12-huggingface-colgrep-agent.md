---
company: Hugging Face
title: "ColGrep-Agent: Cutting Frontier Coding Agents' Tokens by a Third"
url: https://huggingface.co/blog/lightonai/colgrep-agent
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-12
fetched: 2026-10-13
---

LightOn AI releases ColGrep-Agent-2B, a 2B-parameter local open model for repository code search; delegating search to it instead of grep cut Claude Code's API tokens 34% in tests across 13 unseen repositories. Found via gap-scrape (WebFetch of huggingface.co/blog — TIER-1 RSS showed zero fresh for HuggingFace).

## card

**Що сталося:** LightOn AI випускає ColGrep-Agent-2B — локальну відкриту модель на 2 млрд параметрів для пошуку коду в репозиторії, призначену для використання coding-агентами замість grep.

**Контекст:** Тестування проводилося з Claude Code на 52 запитаннях з пошуку коду в 13 репозиторіях, не бачених моделлю під час тренування.

**Деталі:**
- Скорочення API-токенів на 34% проти grep, скорочення cache-aware вартості на 40%
- Точність статистично не змінилася (80.8% проти 83.3% для grep)
- Кожен запит займав довше: 21.6с проти 13.0с для grep
