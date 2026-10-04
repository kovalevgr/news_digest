---
company: Hugging Face
title: "The Agent Said It Was Done. The Database Disagreed."
url: https://huggingface.co/blog/microsoft/thinkingbox
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-03
fetched: 2026-10-04
---

Microsoft and Hugging Face introduce ThinkingBox, an agent-evaluation benchmark that judges AI agents by the actual backend database state left after a task rather than just the agent's final response or tool calls; each task runs 20 times against isolated databases to measure both one-shot success (pass@1) and consistency (pass@20). Evaluates 18 models (9 proprietary, 9 open-weight) across 507 stateful business workflows in 5 domains (retail, insurance, travel, banking, consulting); code MIT-licensed, data CDLA-Permissive-2.0, both on Hugging Face.

## card

**Що сталося:** Microsoft і Hugging Face представили ThinkingBox — бенчмарк, що оцінює AI-агентів за фактичним станом бекенд-бази даних після виконання задачі, а не лише за відповіддю агента чи викликами інструментів. Кожна задача прогоняється 20 разів на ізольованих базах даних, щоб вимірювати і одноразовий успіх (pass@1), і стабільність результату (pass@20).

**Контекст:** Охоплює 507 стейтфул бізнес-воркфлоу у 5 доменах (ритейл, страхування, подорожі, банкінг, консалтинг); протестовано 18 моделей (9 проприєтарних, 9 відкритих вагою). Код відкритий під MIT, дані — під CDLA-Permissive-2.0, обидва на Hugging Face.

**Деталі:**
- 67% провалених прогонів завершувалися "чисто" — з валідними викликами інструментів і без помилок — тобто агент сам вважав задачу виконаною, хоча база даних свідчила про інше
- Лідер за pass@1: Claude Opus 5.5 — 67.16% загальної точності
- Лише 3 з 18 моделей зберегли понад 70% точності одноразового запуску при 20 повторах; у більшості показник падав приблизно до 8%
- 79.9% провалів пов'язані з обробкою інструментів, а не з помилками міркування
- GPT-5.4 — найнижча вартість за надійно виконану (а не просто одноразово успішну) задачу: $6.80
