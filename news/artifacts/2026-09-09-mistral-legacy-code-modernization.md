---
company: Mistral AI
title: "Modernizing complex legacy code with AI agents."
url: https://mistral.ai/news/legacy-code-modernization/
published: 2026-09-09
source_url: https://mistral.ai/rss.xml
fetched: 2026-09-10
---

Mistral shares a case study on using AI agents to migrate 40,000 lines of Fortran 77 to C++ for a European energy operator, with a "parity harness" for numerical verification and a planner/coder/tester/reviewer agent workflow gated by human review.

## card

**Що сталося:** Mistral описує проєкт для європейського енергетичного оператора: міграцію 40 000 рядків коду Fortran 77 у C++ за допомогою AI-агентів, з наголосом на збереження числової еквівалентності старого й нового коду.

**Контекст:** Продовжує серію практичних кейсів Mistral про застосування агентів у реальних enterprise-задачах (після Agentic Search і Shieldstral); фокус тут — на legacy-коді без документації й авторів, які вже пішли з проєкту.

**Деталі:**
- Обсяг: 40 000 рядків наукового коду Fortran 77 → C++
- Побудовано "parity harness" — систему числової перевірки відповідності до початку міграції
- Агенти спершу документували кодову базу через аналіз дерева викликів (caller-callee), перш ніж почати зміни
- Робочий процес: агенти в ролях planner/coder/tester/reviewer над окремими модулями, з людськими контрольними точками замість повної автономності
- Результат: перехід від процедурного коду з глобальним станом до об'єктно-орієнтованого дизайну зі збереженням числової еквівалентності
