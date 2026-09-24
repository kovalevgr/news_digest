---
company: NVIDIA
title: "How SWE-Serve Exposes the Gap Between Local Tests and Live Serving"
url: https://developer.nvidia.com/blog/how-swe-serve-exposes-the-gap-between-local-tests-and-live-serving
published: 2026-09-23
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-24
---

NVIDIA and the SGLang team introduce SWE-Serve, a benchmark of 53 inference-engineering tasks from 83 merged SGLang PRs, showing AI coding-agent patches that pass local tests often fail once deployed through live serving infrastructure.

## card

**Що сталося:** NVIDIA спільно з командою SGLang випускає SWE-Serve — бенчмарк із 53 задач з інженерії інференсу, побудований на 83 злитих pull request'ах SGLang, що показує: патчі AI coding-агентів, які проходять локальні тести, часто провалюються при реальному розгортанні на сервінгу.

**Контекст:** Задачі охоплюють шість доменів: спекулятивне/просунуте декодування, enablement моделей, kernels/квантизація, serving API, кешування та розподілене виконання.

**Деталі:**
- Ті самі патчі проходять у 45.9% випадків при повній верифікації, але у 69.4% — якщо виключити live-serving перевірки (близько третини локально-валідних патчів провалюють продакшн-сервінг)
- Мультидоменні задачі показують на 21.3 в.п. нижчий рівень проходження, ніж однодоменні, у всіх протестованих моделей
- Продуктивність моделей: від 34.6% до 75.5% pass@1; лідери — Claude Opus 5 та GPT-5.6 Sol (~75%)
- Різниця у вартості до 7.5x та у часі виконання до 4x при однаковому результаті
- Лідерборд: research.nvidia.com/benchmarks/swe-serve; відкритий репозиторій та методологія (стаття) доступні
