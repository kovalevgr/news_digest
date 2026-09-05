---
company: Hugging Face
title: "Give Your Coding Agents a Memory You Own"
url: https://huggingface.co/blog/funes
published: 2026-09-03
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-05
---

Hugging Face's David Corvoysier introduces funes, an open-source local-first memory layer for coding agents (Claude Code, Codex, and others) that indexes session traces into searchable datasets, syncable to private HF datasets across machines, with recall measured 4-8x cheaper than a written handoff.

## card

**Що сталося:** Девід Корвуазьє (Hugging Face) представив funes — систему пам'яті для кодинг-агентів (Claude Code, Codex, pi, Hermes), яка індексує сесії в датасети для пошуку і синхронізується через приватні датасети Hugging Face між різними машинами.

**Контекст:** Відповідь на проблему втрати контексту між сесіями агентів при роботі на кількох машинах; побудовано на open-source Lance datasets та інфраструктурі HF для доступу й дистрибуції.

**Деталі:**
- Один бінарник, без залежностей від ML-рантайму; локальний embedding і reranking
- Інструмент `recall` для автономного пошуку агентом і команда `ask` для ручних запитів
- Redaction секретів перед публікацією даних
- На довгих сесіях recall виявився у 8 разів дешевшим за письмовий хендофф в одному завданні і у 4 рази — в іншому, з успішним завершенням там, де компакція іноді провалювалась
