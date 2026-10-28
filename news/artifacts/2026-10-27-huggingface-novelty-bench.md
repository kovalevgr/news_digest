---
company: huggingface
title: "Can we trust LLMs to judge whether a research idea is novel?"
url: https://huggingface.co/blog/allenai/novelty-bench
date: 2026-10-27
found_via: rss (TIER-1)
---

Ai2 publishes "Old Ideas, Novel Problems," a benchmark of ICLR 2026 peer-review novelty judgments testing six LLM judges (GPT-5.1–5.4, Claude Sonnet/Opus 4.5/4.6), finding verdicts are highly unstable to prompt wording and that purpose-built novelty evaluators underperform a simple Claude Opus 4.6 baseline at a fraction of the cost.

## card

**Що сталося:** Ai2 публікує дослідження "Old Ideas, Novel Problems" — бенчмарк на основі рецензій ICLR 2026, що перевіряє, чи можуть LLM-судді надійно оцінювати новизну дослідницької ідеї. Протестовано шість суддів (GPT-5.1, 5.2, 5.4, Claude Sonnet 4.5, Claude Opus 4.5, Claude Opus 4.6); висновок — переважно ні, вердикти нестабільні.

**Контекст:** Новизна оцінюється за явними коментарями рецензентів про оригінальність (154 ідеї високої новизни, 145 — нижчої), а не за рішенням про прийняття; окремий сетап порівнює людські ідеї з 154 ідеями від простого LLM-генератора як слабшими еталонами.

**Деталі:**
- Формулювання підказки критично впливає: для GPT-5.4 на парах людина-проти-AI точність впала з 93.5% до 40.9% при спрощеній підказці; для Claude Opus 4.6 зсув — 21 пункт.
- Немає універсально найкращої підказки — те, що допомагає одній моделі, може шкодити іншій.
- Більше обчислень не допомогло: агентний суддя GPT-5.6 Sol з пошуком по arXiv набрав 0.78 macro-F1 проти 0.89 у Claude Opus 4.6 із простою підказкою, коштуючи приблизно в 10 разів більше.
- Спеціалізовані оцінювачі показали гірші результати: базовий Opus 4.6 — 0.854 macro-F1 за $2.59; Idea Novelty Checker — 0.642 за $30.66; оцінювач Sakana AI Scientist — 0.772 за $82.05.
- Дані: Hugging Face dataset `allenai/novelty-judge-bench`; код: GitHub `allenai/novelty-eval`; препринт: arXiv 2610.02022.
