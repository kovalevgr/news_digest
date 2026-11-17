---
company: nvidia
title: "Accelerate Molecular Dynamics Simulations with Accurate, Flexible Primitives Using NVIDIA cuPotential"
url: https://developer.nvidia.com/blog/accelerate-molecular-dynamics-simulations-with-accurate-flexible-primitives-using-nvidia-cupotential/
date: 2026-11-16
found_via: rss (developer.nvidia.com/blog/feed)
---

NVIDIA releases cuPotential, an open-source library of modular molecular-dynamics primitives for long-range interactions, delivering roughly 2-3x end-to-end OpenMM speedups across GPUs from T4 to RTX PRO 6000 Blackwell while cutting energy-drift and dispersion-accuracy errors by orders of magnitude.

## card

**Що сталося:** NVIDIA випустила cuPotential — відкриту бібліотеку модульних C API примітивів для молекулярної динаміки, що фокусується на дальніх взаємодіях (електростатика, дисперсія) за періодичних граничних умов, разом з плагіном для OpenMM.

**Контекст:** Нові методи C2-безперервного розщеплення та розмазування розроблені спільно з D. E. Shaw Research та Flatiron Institute; вони досягають потрібної точності при нижчій роздільності гратки та менших відсічках, ніж стандартні методи Ewald та u-series.

**Деталі:**
- Прискорення end-to-end (OpenMM, NPT) ~2–3x+ на GPU від T4 до RTX PRO 6000 Blackwell, на системах 24 000–400 000 атомів; RTX PRO 6000 Blackwell перевищує 3x у окремих тестах.
- Дрейф енергії за 10 нс зменшено у кілька сотень разів порівняно зі стандартними налаштуваннями PME.
- Точність енергії дисперсії покращена у кілька тисяч разів порівняно з традиційними методами при порівнянній похибці сил.
- Код відкритий на GitHub (NVIDIA/cuPotential) з прикладами й бенчмарками; встановлюється як Python wheel, потребує Linux x86-64, сумісний з CUDA 13.1 драйвер, Python 3.12, OpenMM 8.4.0.
