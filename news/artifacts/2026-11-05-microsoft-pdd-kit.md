---
company: microsoft
title: "Formally verifying agent-written full-stack web apps with PDD Kit"
url: https://www.microsoft.com/en-us/research/blog/formally-verifying-agent-written-full-stack-web-apps-with-pdd-kit/
date: 2026-11-05
found_via: rss
---

Microsoft Research introduces PDD Kit, a Proof-Driven Development toolkit (running in GitHub Next's Chopin environment) that turns developer intent into Verus formal specifications, has coding agents write code and matching proofs, mutation-tests the specs for gaps, and gates CI on the proof — demonstrated on a ~5,000-line Rust storefront's login logic.

## card

**Що сталося:** Microsoft Research представила PDD Kit — набір інструментів для Proof-Driven Development: намір розробника перетворюється на формальні специфікації Verus, агенти пишуть код і докази одночасно, а CI блокує збірку, якщо доказ не проходить.

**Контекст:** Інструмент працює в середовищі планування GitHub Next Chopin і поки верифікує лише Rust через мову доведень Verus (з SMT-розв'язувачем Z3). Автори називають це дослідницьким прототипом без публічного релізу чи цінової моделі.

**Деталі:**
- Кейс: логіка логіну в Pet Store (~5000 рядків Rust, Axum + SQLite + Leptos/WASM) — двосторінковий запит розробника дав 8 клаузул `ensures`.
- Розробник прийняв 6 "довірених" частин (напр. запити до БД, `check_password`), що перевіряються тестами, а не доказами — і не читав згенерований код рядок за рядком.
- Verus-перевірка "виявила наявні баги" в коді логіну.
- Перевірка доказів займає секунди для малих модулів, до кількох хвилин — для більших кодових баз.
- Обмеження: лише Rust сьогодні; доказ підтверджує відповідність коду специфікації, а не те, що сама специфікація відповідає намірам.
