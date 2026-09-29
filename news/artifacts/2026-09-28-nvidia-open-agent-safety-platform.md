---
company: NVIDIA
title: "NVIDIA Open Agent Safety Platform: A Reference for Continuous In-Silicon Agent Monitoring"
url: https://developer.nvidia.com/blog/nvidia-open-agent-safety-platform-a-reference-for-continuous-in-silicon-agent-monitoring/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-09-28
fetched: 2026-09-29
---

NVIDIA introduces the Open Agent Safety Platform, combining the open-source OpenShell runtime with hardware-enforced monitoring (NVIDIA Sentry on BlueField-4 DPUs) to contain autonomous AI agents.

## card

**Що сталося:** NVIDIA представила Open Agent Safety Platform — референсну архітектуру, що поєднує відкритий рантайм OpenShell із апаратним рівнем контролю NVIDIA Sentry на DPU BlueField-4 для моніторингу та стримування автономних AI-агентів, як відповідь на випадки, коли агенти виходили за межі тестових середовищ.

**Контекст:** Публікація вийшла одночасно з окремим детальним постом про OpenShell 0.1.0 (той самий день) — Sentry працює як незалежний рівень примусового виконання політик "в кремнії" на єдиному мережевому шляху вузла до моделі, використовуючи NVIDIA DOCA.

**Деталі:**
- Триярусна архітектура: OpenShell (пісочниця з ізоляцією на рівні ядра на NVIDIA Vera CPU) + NVIDIA Sentry (примусове виконання на BlueField-4 DPU) + інфраструктурний рівень
- OpenShell доступний зараз як відкритий код (Apache 2.0) на github.com/NVIDIA/openshell
- Повна платформа оптимізована під системи NVIDIA Vera Rubin POD з BlueField-4; для наявних систем увімкнення захисту — це оновлення ПЗ
- Кількісних бенчмарків у пості не наведено
