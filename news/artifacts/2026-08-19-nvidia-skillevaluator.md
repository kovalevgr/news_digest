---
company: NVIDIA
title: "Evaluating AI Agent Skill Performance with NVIDIA SkillEvaluator"
url: https://developer.nvidia.com/blog/evaluating-ai-agent-skill-performance-with-nvidia-skillevaluator/
published: 2026-08-19
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-20
---

NVIDIA released SkillEvaluator, an open-source three-tier framework (static safety/structure checks, embedding-based distinctiveness analysis, live agent evaluation via the Harbor sandbox) for measuring how AI agent skills affect performance, benchmarked across 300+ verified skills spanning 30+ NVIDIA products.

## card

**Що сталося:** NVIDIA випустила SkillEvaluator — open-source фреймворк з трирівневою оцінкою навичок AI-агентів: статичні перевірки безпеки/структури, аналіз відмінності на ембеддингах, і живе виконання завдань у пісочниці Harbor (з навичкою та без неї).

**Контекст:** Оцінка проведена на 300+ верифікованих навичках у 30+ продуктах NVIDIA; інтегровано з ClawHub (OpenClaw), Hermes Agent від Nous Research (сканування SkillSpector), а також плагінами для Claude, Codex і Cursor.

**Деталі:**
- Загальний приріст (Skill Lift): +31 бал у середньому (+39 без урахування безпеки)
- Correctness: 46→87 (+41); Discoverability: 42→82 (+40); Effectiveness: 39→78 (+39); Efficiency: 43→78 (+35)
- Протестовано два harness: Claude Code (+34 в середньому) і OpenAI Codex (+29)
- Код відкритий на GitHub (nvidia/skillevaluator), документація на порталі NVIDIA
