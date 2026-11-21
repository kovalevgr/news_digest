---
company: perplexity
title: "Escaping SPACE: Part II"
url: https://www.perplexity.ai/hub/blog/escaping-space-part-ii
date: 2026-11-11
found_via: gap-scrape (Jina worked cleanly this run; backfilled after being missed by prior runs)
---

Perplexity's follow-up red-team study of SPACE (the sandbox behind Computer) finds that general-purpose frontier models (GPT-6 Astra, Claude Opus 5.5) outperformed specialized cybersecurity models (GPT-5.6 Cyber) at VM-to-host network-policy bypass, and that explicit attack hints raised success rates sharply (7 of 12 models succeeding at least once).

## card

**Що сталося:** Perplexity публікує другу частину red-team дослідження SPACE (sandbox-платформа Computer, вперше описана у вересневій Part I). Дослідження показує, що спеціалізовані моделі з кібербезпеки іноді поступаються моделям загального призначення у реалістичних задачах обходу мережевих політик VM-to-host.

**Контекст:** У налаштуванні з доступом до коду GPT-5.6 Sol успішно обходив мережеву ізоляцію через DNS-спуфінг у всіх трьох прогонах (середньо 20.8 хв), тоді як спеціалізований GPT-5.6 Cyber провалив усі три спроби (витративши в середньому 51.6 хв) — Cyber не шукав ключову змінну `vpeer_ip`, бо підходив до коду як до вразливого, а не як до топології мережі.

**Деталі:**
- У налаштуванні з джерельним кодом та частковим доступом до мережі 5 моделей (Opus 5.0, Opus 5.5, Mythos 5.1, GPT-5.6 Sol, GPT-6 Astra) успішно обходили ізоляцію в усіх трьох прогонах; Kimi K3 — у двох з трьох; 6 інших моделей — у нулі.
- GPT-6 Astra досягав успіху в середньому за 4.8 хв проти 36.6 хв у Claude Mythos 5.1 і 21.6 хв у Opus 5.5; Mythos передчасно відкинув робочу гіпотезу DNS-спуфінгу, вважаючи її нездійсненною.
- Без доступу до джерельного коду: Sol — 2/3 успіхи, Cyber — 1/3; решта моделей (включно з найновішими) — 0 успіхів, частково через те, що вважали обхід через релеї "поза межами дозволеного".
- Надання явної підказки про атаку підняло успішність різко: 7 з 12 моделей досягли успіху хоча б раз (напр. GPT-6 Astra — з 0/3 до 2/3 за менш ніж 12 хв).
