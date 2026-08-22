---
company: NVIDIA
title: "NVIDIA AVO Reaches 100% on ARC-AGI-3, Demonstrating a Frontier-Level General-Purpose Architecture for Long-Horizon Autonomous Agents"
url: https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/
published: 2026-08-21
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-22
---

NVIDIA's AVO (Agentic Variation Operators), a general-purpose autonomous-agent architecture built on Claude Opus 5, achieves a perfect 100.00 RHAE score on the ARC-AGI-3 public set — completing all 183 levels across 25 environments with 12% fewer environment actions than VISTA, up from Claude Opus 5's 30% baseline alone.

## card

**Що сталося:** NVIDIA представила AVO (Agentic Variation Operators) — універсальну архітектуру автономного агента для довготривалих задач, яка досягла ідеального результату 100.00 RHAE на публічному наборі бенчмарку ARC-AGI-3, пройшовши всі 183 рівні у 25 середовищах.

**Контекст:** AVO використовує Claude Opus 5 як базову мовну модель (лише текстовий режим, сітки 64×64 без зображень) у поєднанні з постійною пам'яттю, наглядом та використанням інструментів; демонструє, що саме архітектура агентної системи — а не сама модель — визначає продуктивність на фронтирному рівні. Самостійний Claude Opus 5 без цієї архітектури показував лише 30% на тому ж бенчмарку.

**Деталі:**
- 100.00 RHAE на ARC-AGI-3 public set — усі 183 рівні у 25 середовищах
- 6 624 дії в середовищі проти 7 542 у VISTA (на 12% менше) для тих самих 183 публічних рівнів
- AVO самостійно дослідила понад 500 напрямків оптимізації GPU-ядер, зафіксувавши 40 версій ядер — до 10.5% швидше за FlashAttention-4
- Базова модель: Claude Opus 5 (тільки текст)
