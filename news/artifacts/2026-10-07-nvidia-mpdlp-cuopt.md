---
company: NVIDIA
title: "Scaling Decision Optimization to 100 Million Variables and Beyond with mPDLP in NVIDIA cuOpt"
url: https://developer.nvidia.com/blog/scaling-decision-optimization-to-100-million-variables-and-beyond-with-mpdlp-in-nvidia-cuopt/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-10-07
fetched: 2026-10-08
---

NVIDIA introduces mPDLP, a multi-GPU Primal-Dual Hybrid Gradient method in cuOpt, reaching up to 11.4x speedup on solver steps and cutting per-GPU memory use up to 6x on large linear programs.

## card

**Що сталося:** NVIDIA представляє mPDLP — мульти-GPU версію методу Primal-Dual Hybrid Gradient у розв'язувачі cuOpt, що розділяє великі задачі лінійного програмування між GPU, з'єднаними через NVLink, використовуючи min-cut-партиціонування для зменшення міжGPU-комунікації.

**Контекст:** Порівнюється з попереднім підходом D-PDLP; тестовано на понад 100 задачах LP на DGX B200, а також у партнерів Kinaxis і PSR.

**Деталі:**
- До 11.4x прискорення на кроках PDLP (4.2x end-to-end) для найбільшої задачі
- Типово 1.2–2.5x швидше за D-PDLP на великих задачах; повільніше на 3 надвеликих бенчмарках
- Пікова пам'ять на GPU знижена до 6x
- Kinaxis: 3.3x на моделі з 135M змінних (8×H100); PSR: понад 5x на моделі з 185M змінних (8×B200)
