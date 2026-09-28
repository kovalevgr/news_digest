---
company: NVIDIA
title: "How NVIDIA DSX MaxLPS Maximizes AI Factory Throughput and Efficiency"
url: https://developer.nvidia.com/blog/how-nvidia-dsx-maxlps-maximizes-ai-factory-throughput-and-efficiency/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-09-28
fetched: 2026-09-28
---

NVIDIA details DSX MaxLPS, a software framework for policy-governed dynamic power sharing across GPU infrastructure, letting operators reclaim stranded power capacity to fit more GPUs into an existing power budget.

## card

**Що сталося:** NVIDIA представила DSX MaxLPS — програмний фреймворк динамічного розподілу живлення між GPU в AI-дата-центрах за політиками оператора, що дозволяє розгортати більше GPU в межах наявного бюджету живлення без збільшення потужності об'єкта.

**Контекст:** AI-фабрики зазвичай резервують живлення на випадок одночасного пікового споживання всіх GPU, що створює невикористаний запас, оскільки реальні навантаження (навчання, inference) циклічно чергують фази обчислень і простою. DSX MaxLPS повторно використовує цей "застряглий" резерв; описана в парній статті "Maximizing AI Factory Performance per Watt with NVIDIA DSX MaxLPS" і документації NVIDIA Dynamic Power Software (v0.8). Майбутні системи Vera Rubin NVL72 поєднають MaxLPS із додатковими оптимізаціями продуктивності на ват.

**Деталі:**
- Спільна оцінка NVIDIA-Nscale: inference Kimi K2.5 на GB300 NVL72 (кампус Nscale Verne в Ісландії), фіксований бюджет живлення 264.4 kW
- Кількість GPU: 140 → 192 (+37.1%)
- Сукупна пропускна здатність: 1.085M → 1.618M токенів/с (+49.2%)
- Ефективність: 4.10 → 6.12 токенів/с на ват потужності (+49.2%)
- Пропускна здатність на інстанс не змінилась; медіанна/P75 затримка — в межах 5% від базової лінії; P99 затримка зросла на 17% (компроміс, що потребує моніторингу)
- Даних про ціну чи загальну доступність немає
