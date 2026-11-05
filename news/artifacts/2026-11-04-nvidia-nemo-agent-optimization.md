---
company: nvidia
title: "Use NVIDIA NeMo to Turn Agent Failures into Tests and Harness Fixes"
url: https://developer.nvidia.com/blog/use-nvidia-nemo-to-turn-agent-failures-into-tests-and-harness-fixes/
date: 2026-11-04
found_via: rss (TIER-1)
---

NVIDIA publishes a tutorial on an agent-optimization loop using NeMo Compass, NeMo Eval Author, and NeMo Relay (via the NemoClaw blueprint) to turn production agent failures into targeted evaluations and harness fixes, with before/after numbers from a workplace-assistant example and a Dassault Systèmes engineering agent.

## card

**Що сталося:** NVIDIA опублікувала тьюторіал з оптимізації AI-агентів: цикл NeMo Compass → NeMo Eval Author → NeMo Relay (через блюпринт NemoClaw), що перетворює реальні провали агента на продакшні у цільові евали й виправлення harness/інструкцій.

**Контекст:** Продовження серії матеріалів NVIDIA про NemoClaw та інструментарій NeMo для агентної оптимізації; приклади взяті з вигаданої компанії-асистента Hermes та реального інженерного агента Dassault Systèmes (проєктування автодверей).

**Деталі:**
- Hermes (workplace assistant): успішні проходження задач розробки зросли з 3/6 до 6/6, кількість викликів інструментів впала з 10 до 6; на відкладеній вибірці — з 4/6 до 6/6 і з 28 до 15 викликів. Фікс — одна зміна в SOUL.md-інструкціях (вимога підтвердження перед надсиланням повідомлень).
- Агент Dassault Systèmes (дизайн автодверей): помилкові (malformed) викликі інструментів впали з 142 до нуля; загальна оцінка покращилась на 28% (відносно), на 35% менше викликів інструментів на сценарій (6 сценаріїв).
- Цикл оптимізації для Dassault тривав приблизно 12 годин (запущений за ніч).
- Вибірки невеликі (6 запусків на набір евалів) — не широкий доказ, радше ілюстрація методу.
