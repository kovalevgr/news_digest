---
company: NVIDIA
title: "How NVIDIA Groq 3 LPX Deterministic Execution Drives Power-Efficient High-Interactivity Inference on NVIDIA Vera Rubin"
url: https://developer.nvidia.com/blog/how-nvidia-groq-3-lpx-deterministic-execution-drives-power-efficient-high-interactivity-inference-on-nvidia-vera-rubin/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-09-15
fetched: 2026-09-16
---

NVIDIA details how Groq 3 LPX's deterministic execution (a compiler-generated cycle-exact schedule across 256 LPU chips) enables two power-optimization techniques — Preemptive Power (pre-adjusts voltage before demand spikes) and Clock Period Synthesis (smooths current increases) — cutting voltage droop over 60% and enabling up to 35x higher throughput per megawatt vs. GB200 NVL72 for 2T+ parameter models at long context. Groq 3 LPX ships on Vera Rubin in H2 2026.

## card

**Що сталося:** NVIDIA пояснює, як детермінований виконавчий рух Groq 3 LPX на платформі Vera Rubin забезпечує енергоефективний inference з високою інтерактивністю для моделей 2T+ параметрів.

**Контекст:** Компілятор будує точний за тактами розклад попиту для всіх 256 LPU-чипів наперед, що вмикає дві доповнюючі технології: Preemptive Power (заздалегідь підлаштовує напругу перед сплеском попиту) та Clock Period Synthesis (згладжує найгостріші стрибки струму). Разом вони знижують просідання напруги понад 60% і дозволяють зменшити напругу з мінімальним запасом.

**Деталі:**
- До 35x вищої пропускної здатності на мегават проти GB200 NVL72 для моделей 2T+ параметрів при довгому контексті й високій інтерактивності
- 40% більше GPU в тому ж енергетичному бюджеті завдяки DSX MaxLPS
- 35% вищої пропускної здатності токенів завдяки керуванню живленням на рівні фабрики
- Зниження напруги на 5-10% дає ~8-19% економії споживання
- Groq 3 LPX виходить на Vera Rubin у другій половині 2026 року
