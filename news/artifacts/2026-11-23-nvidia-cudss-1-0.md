---
company: nvidia
title: "Accelerating Direct Sparse Solvers for Computational Engineering with NVIDIA cuDSS 1.0"
url: https://developer.nvidia.com/blog/accelerating-direct-sparse-solvers-for-computational-engineering-with-nvidia-cudss-1-0/
date: 2026-11-23
found_via: TIER-1 rss
---

NVIDIA releases cuDSS 1.0, a GPU-accelerated direct solver for large sparse linear systems used in engineering/scientific simulation, reporting large speedups over Intel MKL plus improved accuracy and a hybrid memory mode that fits bigger problems on a single GPU.

## card

**Що сталося:** NVIDIA випускає cuDSS 1.0 — прямий розв'язувач великих розріджених лінійних систем на GPU для інженерних і наукових симуляцій, що звітує про суттєві прискорення порівняно з Intel MKL, покращену точність на симетричних невизначених системах та гібридний режим пам'яті, який дозволяє запускати більші задачі на одному GPU.

**Контекст:** cuDSS 1.0 — це загальна доступність (general availability), яку NVIDIA позиціонує як production-ready бібліотеку для комерційних застосунків; оновлення з попередніх версій дає прискорення без змін коду застосунків.

**Деталі:**
- Прискорення проти Intel MKL 2026.1.0 (geomean, NVIDIA B200 vs Intel Xeon Platinum 8570): аналіз — 2.5×, числова факторизація — 5.9×, пряме/зворотне розв'язання — приблизно 151×.
- Точність: symmetry-preserving matching (HSL MC64) та Bunch-Kaufman pivoting увімкнені за замовчуванням для симетричних систем; на тестових матрицях SuiteSparse зворотна похибка покращилась до ~10 порядків.
- Гібридний режим пам'яті використовує CPU DRAM разом з GPU-пам'яттю: знизив мінімальну потрібну пам'ять GPU на ~30% на великих VLSI-кейсах порівняно з версією 0.7.1, дозволяючи розв'язки на одному GPU (H100/B200/Vera Rubin), які раніше вимагали кількох GPU.
- Символьна факторизація на GPU — у 2.21× швидша, ніж у cuDSS 0.8.0; оцінені наскрізні прискорення — ~1.18× на B200 та ~1.14× на H100.
- Доступно для завантаження зі сторінки cuDSS на сайті NVIDIA; ціна не вказана.
