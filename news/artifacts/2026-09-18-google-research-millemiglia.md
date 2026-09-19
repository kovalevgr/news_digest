---
company: Google Research
title: "MilleMiglia: A realistic instance generator for middle-mile logistics"
url: https://research.google/blog/millemiglia-a-realistic-instance-generator-for-middle-mile-logistics/
source_url: https://research.google/blog/rss/
published: 2026-09-18
fetched: 2026-09-19
---

Google Research open-sources MilleMiglia, a C++ instance generator producing realistic, privacy-preserving synthetic benchmarks for middle-mile logistics (continental-scale movement of goods between distribution centers), a domain starved of public datasets because real network topologies and demand data are proprietary.

## card

**Що сталося:** Google Research випустила у відкритий доступ MilleMiglia — генератор синтетичних тестових наборів на C++ для задач middle-mile логістики (переміщення товарів між розподільчими центрами в масштабі континенту).

**Контекст:** Дослідження middle-mile логістики стримувалося браком публічних датасетів, оскільки компанії вважають топології своїх мереж і обсяги попиту комерційною таємницею; MilleMiglia генерує приватні за задумом синтетичні дані на основі публічної та розкритої індустріальної статистики, щоб зняти цей бар'єр.

**Деталі:**
- Модель задачі: граф "простір-час" із багатопродуктовим потоком, фіксованими розкладами транспорту, обмеженнями пропускної здатності розподільчих центрів і синхронізацією
- Масштабованість: від невеликих академічних прикладів до великих індустріальних сценаріїв у масштабі континенту
- Серіалізація через Protocol Buffers для сумісності між мовами програмування
- Код і документація: github.com/or-tools/millemiglia, включно із прикладами наборів даних
- Партнери: дослідники Google (Aymane Lotfi, Thibaut Cuvelier) разом з UniBrescia та ENPC Paris, робота триває у напрямку спеціалізованого solver'а для middle-mile
