---
company: NVIDIA
title: "From Wafer-Out to First Token: Codifying Supply Chain Expertise with Nemotron and Palantir Foundry"
url: https://developer.nvidia.com/blog/from-wafer-out-to-first-token-codifying-supply-chain-expertise-with-nemotron-and-palantir-foundry/
published: 2026-09-10
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-11
---

NVIDIA describes a supply-chain material-allocation system built on Palantir Foundry's Ontology and a post-trained 30B-parameter Nemotron 3.5 Lightning model, reaching 86.7% allocation-decision accuracy — 31.2 points above a larger Nemotron 3 Ultra model — by learning from historical planner decisions and operational context.

## card

**Що сталося:** NVIDIA описує систему автоматизації рішень з розподілу матеріалів у власному ланцюгу постачання, побудовану на платформі Palantir Foundry та дотюненій моделі Nemotron 3.5 Lightning (30B параметрів).

**Контекст:** NVIDIA продовжує серію матеріалів про застосування власних моделей Nemotron до внутрішніх операційних задач; описує, як експертиза людей-планувальників (які традиційно перевершували кількісні солвери за рахунок якісних сигналів — листів, прогнозів погоди, геополітики) кодифікується через контрольований feedback loop.

**Деталі:**
- Точність рішень з розподілу — 86.7%, на 31.2 в.п. вище за більшу модель Nemotron 3 Ultra без спеціального дотюнингу
- Модель — Nemotron 3.5 Lightning, 30 млрд параметрів, дотюнена на історичних рішеннях планувальників
- Дані про операційний контекст і результати зберігаються у фреймворку Ontology (Palantir Foundry)
- Рішення планувальників постійно стають новими навчальними даними для покращення моделі
