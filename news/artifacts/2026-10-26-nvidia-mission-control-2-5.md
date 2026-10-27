---
company: nvidia
title: "How NVIDIA Mission Control 2.5 Brings Autonomous Recovery to Kubernetes"
url: https://developer.nvidia.com/blog/how-nvidia-mission-control-2-5-brings-autonomous-recovery-to-kubernetes/
date: 2026-10-26
found_via: rss (TIER-1)
---

NVIDIA extends Mission Control's autonomous recovery engine — previously limited to Slurm-based HPC workloads — to Kubernetes workloads managed by NVIDIA Run:ai, via a three-layer loop combining job placement, job-failure recovery, and hardware-fault isolation/diagnosis.

## card

**Що сталося:** NVIDIA розширює двигун автономного відновлення Mission Control, раніше доступний лише для HPC-навантажень на Slurm, на Kubernetes-навантаження під керуванням NVIDIA Run:ai. Система працює як трирівневий цикл: планувальник Run:ai розміщує задачі, сервіс автономного відновлення задач вирішує, як реагувати на збій з урахуванням контексту задачі, а сервіс автономного відновлення обладнання ізолює та діагностує несправні вузли.

**Контекст:** Продовжує лінійку анонсів NVIDIA про автономне управління AI-фабриками (DSX MaxLPS, OpenShell, Sentry), тепер поширюючи автономне відновлення з HPC/Slurm на Kubernetes/Run:ai.

**Деталі:**
- Апаратний збій → задача перезапускається на здорових вузлах, несправний вузол карантинується.
- Тимчасові програмні помилки → повторна спроба без апаратного втручання.
- Вузли, що деградують, можуть завчасно виводитися з планування.
- Стаття не наводить кількісних показників ефективності чи продуктивності.
