---
company: Google Research
title: "AgentHands: Generating interactive hand gestures for spatially grounded agent conversations in XR"
url: https://research.google/blog/agenthands-generating-interactive-hand-gestures-for-spatially-grounded-agent-conversations-in-xr/
published: 2026-08-25
source_url: https://research.google/blog/rss/
fetched: 2026-08-26
---

Google Research introduces AgentHands, an LLM-powered XR prototype that synchronizes conversational agents' speech with hand gestures for spatially grounded guidance, showing a statistically significant improvement over speech-only baselines in a 12-person study.

## card

**Що сталося:** Google Research представила AgentHands — прототип для XR, що синхронізує мовлення LLM-агента з жестами рук для просторово прив'язаних інструкцій (наприклад, при поясненні фізичних завдань у доповненій/віртуальній реальності).

**Контекст:** Розвиток напрямку взаємодії людини з AI-агентами в XR-середовищах — заміна текстових/2D-підказок природнішою мовою жестів, синхронізованою з мовленням агента.

**Деталі:**
- Таксономія жестів за 6 вимірами: рука (handedness), тип жесту, просторовість (у повітрі / прив'язаний до об'єкта / відносно користувача), часова динаміка, інтерактивність, візуальні ефекти
- 3 семантичні типи жестів для вибору LLM: дейктичні (вказівні), іконічні (що зображують дію/форму), експресивні (емоційні)
- Пайплайн: усвідомлення оточення через погляд і реконструкцію сцени → бібліотека жестів → LLM-міркування із вбудованими жестами → синхронне виконання в XR з таймстемпами на рівні слів
- Дослідження за участю 12 осіб показало статистично значуще (p < 0.05) покращення просторового розуміння, розуміння складних дій і безпеки порівняно з базовим варіантом "лише мовлення"
