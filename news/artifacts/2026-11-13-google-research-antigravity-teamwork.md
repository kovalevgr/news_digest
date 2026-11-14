---
company: google-research
title: "Advancing science & engineering with Antigravity's /teamwork"
url: https://research.google/blog/advancing-science-engineering-with-antigravitys-teamwork-feature/
date: 2026-11-13
found_via: rss
---

Google Research details /teamwork, a multi-agent workflow pattern in its Antigravity platform that runs parallel explorations paired with automated "falsifiers" (proof checkers, test suites, simulators) to verify candidate solutions on open problems across math, chemistry, systems software, and ML engineering. Highlights include a full Lean-4 formalization of the Courtade–Kumar conjecture, a 20-30% faster Rust rewrite of libgav1, and production gains at Google (24% less TPU preemption).

## card

**Що сталося:** Google Research описав /teamwork — шаблон мультиагентної роботи в Antigravity, що запускає паралельні спроби розв'язання і перевіряє кандидатів автоматичними "фальсифікаторами" (Lean 4, тестові набори, симулятори) замість довіри до одної спроби. Координатори передають роботу свіжим агентам, а критики перевіряють результат без контексту автора.

**Контекст:** Частина сімейства шаблонів Antigravity поряд із Deep Review (перевірка документів) і /boost (ітеративний код); Gemini 4 з /teamwork, /boost і Deep Review вже доступні зовнішнім користувачам.

**Деталі:**
- Повне формальне доведення гіпотези Courtade–Kumar (2013) в Lean 4 (~50 млн рядків).
- Формалізація гіпотез Вейля (~1.8 млн рядків Lean, фреймворк LEAP).
- У хімії: 30 агентів + спектральний симулятор — 95% top-1 і 100% top-3 на визначенні структури за ЯМР (майже вдвічі краще за одного агента).
- Rust-переписування libgav1 (~170 тис. рядків) — на 20-30% швидше за оригінальний C++/асемблер, побітова відповідність.
- DuoDiscover: прискорення у 4.09x (JAX) і 2.99x (vLLM TPU kernels), геометричне середнє.
- Виробниче впровадження в Google: -24% простою TPU через витіснення завдань (Borg).
- Deep Review використали автори 578 заявок STOC 2027; 90% з 70 опитаних оцінили фідбек переважно фактологічно точним.
- Доступність: Gemini 4 з /teamwork зовнішнім користувачам вже зараз; 10 000 дослідників отримають 6 місяців безкоштовного доступу найвищого рівня за заявкою.
