---
company: nvidia
title: "Adapt Human Motion for Robots with NVIDIA SOMA Retargeter"
url: https://developer.nvidia.com/blog/adapt-human-motion-for-robots-with-nvidia-soma-retargeter/
date: 2026-11-13
found_via: rss
---

NVIDIA releases v0.2 of the open-source SOMA Retargeter, which adapts human motion-capture data to a target humanoid robot's proportions and joint structure via inverse kinematics (Newton/NVIDIA Warp) plus foot-plant correction, outputting per-frame joint CSVs for downstream policy training (SONIC, ProtoMotions). Reference configurations ship for Unitree G1/H2, Booster T1, and AgiBot X2 Ultra/A3T3.

## card

**Що сталося:** NVIDIA випустив версію 0.2 відкритого інструменту SOMA Retargeter — переносить дані захоплення руху людини (BVH на скелеті SOMA) на конкретного гуманоїдного робота через зворотну кінематику (Newton на базі NVIDIA Warp) з постобробкою (корекція постановки стопи), результат — CSV з позами/кутами суглобів для подальшого тренування політик.

**Контекст:** Вихідні дані руху можуть надходити з motion-capture (BONES-SEED), реконструкції з відео (GEM-X) або генеративних моделей (Kimodo, ARDY); вихід сумісний із тренувальними фреймворками SONIC та ProtoMotions.

**Деталі:**
- Готові референсні конфігурації й результати (v0.2): Unitree G1, Unitree H2, Booster T1, AgiBot X2 Ultra, AgiBot A3T3.
- Додаткові інструменти: Robot Configurator (додавання/уточнення конфігурацій роботів), експериментальний оптимізатор ваг IK, пакетний retargeting без GUI.
- Також описано експеримент з роботом MicroDuck.
- Відкритий код: репозиторій NVIDIA/soma-retargeter на GitHub (ліцензія в описі не вказана — дивитись у репозиторії).
