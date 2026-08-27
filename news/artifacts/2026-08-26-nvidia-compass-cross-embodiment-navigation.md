---
company: NVIDIA
title: "How to Train a Cross-Embodiment Robot Navigation Policy with AI Agents"
url: https://developer.nvidia.com/blog/how-to-train-a-cross-embodiment-robot-navigation-policy-with-ai-agents/
published: 2026-08-26
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-27
---

NVIDIA introduces COMPASS, a framework that adapts a pretrained X-Mobility navigation policy to new robots/environments via residual reinforcement learning instead of training from scratch, using an agent-driven workflow with human approval gates across built-in, generated, and reconstructed scenes.

## card

**Що сталося:** NVIDIA представила COMPASS — фреймворк, що адаптує попередньо натреновану навігаційну політику X-Mobility під нові роботи й середовища через residual reinforcement learning замість тренування з нуля.

**Контекст:** Розвиток напрямку крос-платформної (cross-embodiment) мобільності роботів; демонструється на прикладі кастомізації під Boston Dynamics Spot.

**Деталі:**
- Агентний воркфлоу з точками схвалення людиною автоматизує валідацію середовища, підготовку сцен, smoke-тестування, тренування й оцінку чекпоінтів
- Три джерела сцен: вбудовані склади, згенеровані сцени SAGE-10K, реконструйовані середовища через Omniverse NuRec
- Дозволяє повторно використовувати навігаційну експертизу з однієї платформи (embodiment) для кастомізації під конкретних роботів
