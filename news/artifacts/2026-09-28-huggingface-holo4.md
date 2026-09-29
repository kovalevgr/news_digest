---
company: Hugging Face
title: "Holo4: powering generalist computer-use agents"
url: https://huggingface.co/blog/Hcompany/holo4
source_url: https://huggingface.co/blog/feed.xml
published: 2026-09-28
fetched: 2026-09-29
---

H Company releases Holo4, a family of open-weight agentic models for computer-use tasks (GUI, code, MCP, APIs), trained via supervised+RL on ~10,000 tasks from an internal Agentic Task Factory.

## card

**Що сталося:** H Company випустила Holo4 — серію відкритих агентних моделей для роботи з комп'ютером через будь-який доступний інтерфейс (GUI, код, MCP, API), навчених за допомогою supervised + reinforcement learning на ~10 000 задачах з власної Agentic Task Factory, з переробленим виконавчим харнесом.

**Контекст:** Моделі опубліковані у партнерстві з Hugging Face; порівнюються з Claude Opus 5.5 на бенчмарку OSWorld 2.0 як орієнтиром для computer-use агентів.

**Деталі:**
- Розміри моделей: Holo4-27B (dense), Holo4-35B-A3B (MoE), Holotron4 Nano (30B-A3B)
- OSWorld 2.0: Holo4-27B — 61.7% проти 81.8% у Claude Opus 5.5, але за суттєво нижчої обчислювальної вартості на задачу
- Доступність: H Models API та Hugging Face у форматах BF16, FP8, NVFP4, 4-bit GGUF
- Відкриті ваги; усі траєкторії бенчмарків публічно доступні для перевірки
