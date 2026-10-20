---
company: openai
title: "Advancing coding in low-resource programming languages"
url: https://openai.com/index/low-resource-programming-languages
date: 2026-10-19
found_via: TIER-1 rss (openai.com/news/rss.xml)
---

OpenAI is improving its models' coding ability in "low-resource" programming languages (COBOL, Fortran, Visual Basic, OCaml and similar) that have little training data compared to Python/JavaScript but still run critical infrastructure, and introduces two new evals — MultiLangBench (build a SQLite-compatible database engine from scratch across 20 languages) and a COBOL-migration eval (port COBOL to C++/Java/Kotlin/Python/Rust with byte-for-byte output parity) — to measure and drive that progress.

## card

**Що сталося:** OpenAI публікує роботу з покращення здатності своїх моделей писати код мовами з малим обсягом тренувальних даних (COBOL, Fortran, Visual Basic, OCaml тощо), які попри це лежать в основі критичної інфраструктури. Компанія представляє два нові бенчмарки: MultiLangBench (побудова SQL-сумісного з SQLite движка бази даних "з нуля" на 20 мовах, звірка з еталонним виводом SQLite) та окремий eval на міграцію COBOL-коду (переклад у C++/Java/Kotlin/Python/Rust з точним байт-у-байт збігом виводу на прихованих тестах).

**Контекст:** COBOL і Fortran — мови, на яких написана значна частина банківської, платіжної та наукової/інженерної інфраструктури; за словами OpenAI, COBOL підтримує понад 40% систем онлайн-банкінгу, близько 80% офлайн-транзакцій по картах і близько 95% транзакцій через банкомати, а Fortran і далі використовується в прогнозуванні погоди та аналізі безпеки атомних реакторів. Код і результати evals опубліковані на GitHub.

**Деталі:**
- MultiLangBench (максимальний рівень reasoning): GPT-6 Astra — середній pass rate 87.4% (проти 26.8% у GPT-5.6 Sol), вище 83% у 19 з 20 мов; найслабший результат — COBOL, 72.1% (було 10.9% у попередньої моделі).
- Приклади приросту по мовах для GPT-6 Astra: OCaml 25.6%→85.8%, Fortran 21.4%→83.5%, Visual Basic 27.5%→89.4%.
- Дешевша модель GPT-6 Luna показує середній pass rate 40.3% за приблизно $0.77/приклад — проти $3.48/приклад у GPT-5.6 Sol (дешевше на ~78%).
- На eval з міграції COBOL: GPT-6.1 Sol на низькому рівні reasoning дає 86.6% точності (проти 5.4% у GPT-5.6 Sol) за ~39% нижчої вартості API; на вищому рівні reasoning — 97.9% точності.
- OpenAI наголошує, що мігрований код усе ще потребує перевірки експертами, а не прямого деплою без ревʼю.
