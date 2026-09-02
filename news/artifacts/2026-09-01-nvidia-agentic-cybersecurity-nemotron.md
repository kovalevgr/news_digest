---
company: NVIDIA
title: "Building an Adaptive Agentic Cybersecurity System with NVIDIA Nemotron"
url: https://developer.nvidia.com/blog/building-an-adaptive-agentic-cybersecurity-system-with-nvidia-nemotron/
published: 2026-09-01
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-02
---

NVIDIA and CrowdStrike built a closed-loop red/blue-agent cybersecurity system on Nemotron models, lifting backtested detection rates from 16.5% to 41.9% and generalizing to 45% of unseen attacks versus 29% for a frontier system.

## card

**Що сталося:** NVIDIA та CrowdStrike побудували замкнену систему кібербезпеки на базі моделей Nemotron, де "червоні" агенти виконують атаки, а "сині" — генерують детекції, з постійною ітерацією для покращення захисту.

**Контекст:** Використано Nemotron 3 Ultra для оркестрації захисту та кастомізований Nemotron 3 Super для генерації детекцій, навчений на 9349 прикладах 59 типів помилок; інфраструктура навчання — NVIDIA NeMo Gym і NeMo RL.

**Деталі:**
- Рівень детекції при бектестуванні зріс з 16.5% до 41.9% (у 2.5 рази)
- 45% детекцій відкритої моделі узагальнилися на нові атаки проти 29% у передової системи
- 3 детекції отримали "золотий стандарт" без хибних спрацювань, покрили всі 8 невідомих тестових атак
- Шестикомпонентний harness: база схем, прив'язка до телеметрії, спеціалізоване авторство, лінтинг артефактів, replay детекцій, незалежний огляд
