---
company: Microsoft
title: "Offloaded inference for real-world physical AI robotics"
url: https://www.microsoft.com/en-us/research/blog/offloaded-inference-for-real-world-physical-ai-robotics
published: 2026-09-23
source_url: https://www.microsoft.com/en-us/research/feed/
fetched: 2026-09-24
---

Microsoft Research shows that moving AI inference off small/lightweight onboard robot GPUs to remote edge/cloud GPUs improves task success, obstacle detection, and battery life versus running inference fully onboard.

## card

**Що сталося:** Microsoft Research показує, що перенесення обчислень AI-інференсу з бортових GPU роботів на віддалені edge/cloud GPU ("offloaded inference") покращує успішність виконання завдань, ефективність та підтримує складніші фізичні AI-навантаження порівняно з повністю бортовим інференсом.

**Контекст:** Слабші бортові GPU (Jetson Nano, Raspberry Pi-5) обмежують точність VLA-моделей та швидкість реакції роботів; потужніші бортові GPU (Jetson Thor) різко скорочують час автономної роботи від батареї. Дослідження протестоване на роботах Stretch-3, Mobile Aloha, SO-101, UR10e з offload на Jetson Thor/A100.

**Деталі:**
- На слабших бортових GPU швидкість mapping/planning падає до 383% відносно A100; своєчасне виявлення перешкод — на 30% гірше
- Точність VLA-моделей на слабших бортових GPU падає на 50%
- Потужні бортові GPU (Jetson Thor) скорочують час роботи батареї робота до 160% за кілька годин; offloading покращує ресурс батареї Stretch-3 більш ніж на 100%
- Випущено Kubernetes-based Physical AI Toolchain для автоматичної контейнеризації та розподіленого розгортання інференсу
