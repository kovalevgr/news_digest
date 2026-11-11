---
company: google-deepmind
title: "Introducing AlphaProof Code: a breakthrough in verifying complex software at depth"
url: https://deepmind.google/blog/introducing-alphaproof-code/
date: 2026-11-10
found_via: rss
---

Google DeepMind introduces AlphaProof Code, an agentic formal-verification framework; Gemini Carbon-powered agents wrote over six million lines of Lean proofs to verify the actual compiled code of Signal's cryptographic protocol, a first for AI verifying a widely deployed protocol at this depth.

## card

**Що сталося:** Google DeepMind представила AlphaProof Code — агентний фреймворк формальної верифікації ПЗ, де люди визначають, що треба довести, а група AI-агентів виконує доведення. Систему застосували для формальної верифікації реального скомпільованого коду криптографічного протоколу Signal.

**Контекст:** Це вперше AI використали для формальної верифікації широко розгорнутого криптографічного протоколу на такому рівні глибини — раніше подібна верифікація зупинялась на рівні дизайну протоколу, а не скомпільованого коду. Агенти працюють на базі Gemini 4 Carbon (анонсований того ж дня) і доповнюють CodeMender — агента безпеки коду від DeepMind (жовтень 2025).

**Деталі:**
- Агенти згенерували понад 6 млн рядків доведень на Lean; ~1% кодової бази позначено для ручної перевірки людьми, решту автоматично перевіряє Lean.
- Весь процес зайняв ~4 тижні проти років, які зазвичай потрібні командам експертів.
- Для перевірки системи у ізольовану копію коду Signal повернули два раніше виправлені баги — в обох випадках AlphaProof Code згенерувала машинно-перевірені доведення небезпечності цих версій.
- Артефакти верифікації відкриті на google-deepmind.github.io/code-verification; CTO Signal Ehren Kret назвав це важливим проривом для гарантій приватності компанії.
