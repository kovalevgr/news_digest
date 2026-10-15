---
company: NVIDIA
title: "Optimizing Agent Reliability and Tool Calling Efficiency for Chip Design Using NVIDIA NeMo Gym"
url: https://developer.nvidia.com/blog/optimizing-agent-reliability-and-tool-calling-efficiency-for-chip-design-using-nvidia-nemo-gym/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-10-14
fetched: 2026-10-15
---

NVIDIA and Siemens EDA use NVIDIA NeMo Gym to make the Siemens Fuse EDA AI Agent more reliable at standard-cell characterization, cutting agent turns and output tokens roughly two-thirds while nearly doubling a composite benchmark score.

## card

**Що сталося:** NVIDIA та Siemens EDA описали, як за допомогою відкритої бібліотеки NVIDIA NeMo Gym підвищили надійність AI-агента Siemens Fuse (оркеструє інструменти Solido Characterization Suite через MCP-сервери) для характеризації стандартних елементів мікросхем — задачі, яку доводиться повторювати щоразу, коли фабрика випускає новий PDK.

**Контекст:** Головна теза публікації — агентів для багатоетапної інженерної роботи варто оцінювати за фінальним артефактом (файли Liberty), а не за окремими кроками, бо ранні помилки інакше непомітно поширюються далі.

**Деталі:**
- Композитний бенчмарк-скор зріс з ~55% до ~95%
- Кількість кроків агента впала з 155 до 53 (≈66%), середній обсяг вихідних токенів — з ~81K до ~29K (≈64%)
- Тестовий набір: відкритий PDK GF180MCU, 229 стандартних елементів × 36 PVT-умов; SPICE-симуляція через Solido AFS
- Модель і харнес зафіксовані для всіх прогонів: Claude Opus 4.8 у Claude Code
- Верифікатор дає нагороду 0, якщо не пройдено будь-який з 5 ґейтів (повнота, валідність, відносна валідація, точність, цілісність результату)
- Агент сумісний з Claude Code, Codex та Cursor
