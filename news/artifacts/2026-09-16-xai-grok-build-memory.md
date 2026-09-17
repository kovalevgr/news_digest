---
company: xAI
title: "Memory in Grok Build"
url: https://x.ai/news/grok-build-memory
source_url: https://x.ai/news
published: 2026-09-16
fetched: 2026-09-17
---

xAI adds persistent memory to Grok Build (its coding agent): after each completed turn, Grok records conventions, decisions, and durable project facts as markdown notes (per-project plus a global preferences set), organized over time by a new `/dream` command into topic files; a new `/memory` command gives a read-only browser of memory files. Available now for new sessions.

## card

**Що сталося:** xAI додає постійну пам'ять до Grok Build (свого coding-агента): після кожного завершеного ходу Grok фіксує домовленості, рішення та факти про проєкт у вигляді нотаток, які читає в наступних сесіях.

**Контекст:** Захоплення відбувається у фоновому режимі й не блокує сесію; команда `/dream` періодично організовує нотатки в тематичні файли (наприклад, `topics/testing.md`), а нова команда `/memory` дає доступ до перегляду цих файлів.

**Деталі:**
- Пам'ять зберігає: конвенції написання й рев'ю коду, рішення та їх обґрунтування, стійкі факти про проєкт (де живе підсистема, яка команда запускає тести)
- НЕ зберігає: стан задачі, попередні висновки, секрети, і все, що вже покрито в репозиторії чи документації
- Нотатки ведуться окремо по проєкту плюс один глобальний набір для налаштувань, що застосовуються всюди
- Інструкції в поточній розмові мають пріоритет над будь-якою нотаткою
- Нові команди: `/memory` (перегляд), `/dream` (організація нотаток у тематичні файли, також запускається періодично сам)
- Доступно вже зараз у Grok Build; застосовується до нових сесій (`/new` або новий запуск `grok`)
