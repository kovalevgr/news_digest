---
company: google-deepmind
title: "Finding faster quantum algorithms with agents and formal verification"
url: https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/
date: 2026-11-23
found_via: TIER-1 rss
---

Google DeepMind and Google Quantum AI used teams of Gemini 4 agents to find more efficient quantum circuits for known algorithms, verifying each result with the Lean theorem prover since the circuits are too large to test classically or on today's small quantum processors.

## card

**Що сталося:** Google DeepMind і Google Quantum AI використали команди агентів на базі Gemini 4 для пошуку ефективніших квантових схем для відомих алгоритмів; кожен результат верифікується за допомогою theorem prover Lean, бо самі схеми надто великі для класичної перевірки або прогону на сьогоднішніх малих квантових процесорах.

**Контекст:** Робота спирається на препринт arXiv 2611.09822 і продовжує попередні напрацювання команди — AlphaEvolve (агент на базі Gemini для пошуку алгоритмів) та AlphaQubit (корекція квантових помилок). Незалежні команди агентів працювали над кожною задачею паралельно, обмінюючись верифікованими ідеями через спільний журнал і "зустрічаючись" кожні 4 години.

**Деталі:**
- Термоядерний синтез (inertial confinement): вартість обчислень впала у 11.8×, кількість потрібних кубітів з корекцією помилок — з 5650 до 4338.
- Молекулярна симуляція: типова світлочутлива молекула стала у 8× дешевшою для симуляції; для цитохрому P450 (фермент метаболізму ліків) — покращення у 2.5×, кубіти з 481 до 333.
- Прискорення алгоритмів: конкретна реалізація пошуку Гровера — у 2.57×, рутина arcsin для завантаження чисел у квантові стани — у 290×.
- Бібліотека Lean, специфікації задач і верифіковані рішення опубліковані у відкритому доступі на GitHub.
- Обмеження: оптимізовані алгоритми все ще потребують більше ресурсів, ніж імовірно матимуть перші квантові комп'ютери з корекцією помилок.
