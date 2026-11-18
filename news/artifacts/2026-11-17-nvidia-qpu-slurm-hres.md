---
company: nvidia
title: "Integrating QPUs into Supercomputing Centers Using Slurm HRES Plugins"
url: https://developer.nvidia.com/blog/integrating-qpus-into-supercomputing-centers-using-slurm-hres-plugins/
date: 2026-11-17
found_via: rss (developer.nvidia.com/blog/feed)
---

NVIDIA's developer blog covers Slurm 26.11's new Hierarchical Resources (HRES) plugins, which let supercomputing centers schedule quantum processing units (QPUs) as native, cluster-level resources instead of per-site custom code; several quantum vendors (IBM, IQM, Pasqal, Quantinuum) have announced HRES integrations.

## card

**Що сталося:** Slurm 26.11 додав плагіни Hierarchical Resources (HRES), що дозволяють планувати квантові процесори (QPU) як рідний, кластерного рівня ресурс замість кастомного коду під кожен сайт/пристрій. Перша реалізація — `hres/lua`, що запускає короткий Lua-скрипт.

**Контекст:** HRES виріс із механізму licenses у Slurm (бета з версії 25.05). Попередні підходи — generic resources (GRES, прив'язка пристрою до одного вузла) та licenses+SPANK — мали проблеми: вузол стає недосяжним при падінні ноди, вузли простоюють в очікуванні QPU, конфлікти при кількох QPU на кластері, та відсутність у Slurm обізнаності про стан пристрою (запускає завдання навіть під час калібрування QPU).

**Деталі:**
- Налаштування QPU — у `resources.yaml` (mode, плагін-блок, `maintenance_cycle`, наприклад 30 сек між health-check, та layers з вузлами); завдання запитують пристрій через `--resources=qpu:1`.
- Логіка пристрою — у портативному плагіні, не лінкується з libslurm, тож не вимагає перезбірки під кожен реліз Slurm.
- 12 callback-ів виконуються по черзі на slurmctld/slurmstepd/compute nodes (health-check, допуск завдання, резервування, setup/cleanup тощо); код `ESLURM_HRES_REMOTE_FAIL` позначає сервіс недоступним (завдання чекає, а не "drains" ноду).
- Slurm і плагін ніколи не звертаються до QPU напряму — між ними стороннє access middleware (приклади: QRMI — бронює доступ під завдання; QDMI — допускає завдання лише коли пристрій вільний).
- Інтеграції з HRES анонсували IBM, IQM, Pasqal, Quantinuum.
