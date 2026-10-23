---
company: microsoft
title: "Flint-interactive: A language for creating interactive data visualizations"
url: https://www.microsoft.com/en-us/research/blog/flint-interactive-a-language-for-creating-interactive-data-visualizations/
date: 2026-10-22
found_via: TIER-1 rss (microsoft.com/en-us/research/feed/)
---

Microsoft Research introduces Flint-interactive, a language letting AI agents build interactive charts (click, filter, zoom, highlight, link) via high-level semantic events and update operators instead of low-level visualization code, usable through MCP, an app canvas, or a programming API.

## card

**Що сталося:** Microsoft Research представив Flint-interactive — мову для створення інтерактивних візуалізацій даних, яка дозволяє AI-агентам будувати графіки, що користувач може досліджувати кліками, фільтрами, масштабуванням і виділенням, замість низькорівневого коду візуалізації.

**Контекст:** Розробка на основі існуючого Flint (генерація статичних графіків агентами); вирішує дві проблеми — високу вартість генерації (повторні цикли міркування/кодування/дебагу) і ненадійність (поламані layout чи взаємодії).

**Деталі:**
- Flint Canvas — машина станів, що відстежує взаємодії користувача та керує рендерингом; компілятор Flint перетворює кліки/драги/натискання клавіш на семантичні події.
- Три способи використання: у чаті через Flint-MCP та MCP Apps, у застосунках через Flint Interactive Canvas, або через програмний API для власних взаємодій.
- Приклади: лінковані scatterplots Gapminder (1952 і 2007), таблиця синхронізована з графіком, сезонна кліматична візуалізація DimpVis для п'яти міст США.
- Документація та приклади — на microsoft.github.io/flint-chart; кількісних результатів (бенчмарків) пост не наводить.
