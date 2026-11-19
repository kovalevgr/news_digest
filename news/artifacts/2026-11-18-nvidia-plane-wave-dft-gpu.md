---
company: nvidia
title: "Tackling GPU Bottlenecks in Plane-Wave DFT with K-Point Batching and Mixed Precision"
url: https://developer.nvidia.com/blog/tackling-gpu-bottlenecks-in-plane-wave-dft-with-k-point-batching-and-mixed-precision/
date: 2026-11-18
found_via: rss (developer.nvidia.com/blog/feed)
---

NVIDIA introduces Daviator, a k-point-batching library plus a mixed-precision layer for the plane-wave DFT code VASP, cutting GPU underutilization and FP64 bottlenecks for generating ML interatomic-potential training data.

## card

**Що сталося:** NVIDIA представила Daviator — бібліотеку батчингу k-point'ів разом з шаром змішаної точності для VASP (plane-wave DFT код, що широко використовується для генерації тренувальних даних machine learning interatomic potentials).

**Контекст:** Проблема: для малих елементарних ячейок з щільними k-point гратками GPU-порт VASP обробляє k-points послідовно — через багато маленьких запусків GPU недовантажений (приклад: система з одним атомом заліза і 752 k-points виконувалась у 8x повільніше на дорожчому GPU, ніж на CPU); окремо, FP64-пропускна здатність на датацентрових GPU залишається майже незмінною, тоді як FP32 росте (на RTX PRO 6000 співвідношення FP32:FP64 = 64:1), тож FP64-тільки код не використовує пікову пропускну здатність апаратного забезпечення.

**Деталі:**
- K-point batching (Daviator): батчовані GPU-ядра (включно з батчованим Davidson eigensolver'ом) обробляють k-points і спіни разом, зменшуючи кількість запусків ядер; увімкнення через `LDAVIATOR = True`, наразі підтримує лише однонодові запуски.
- Mixed precision: FFT, застосування Hamiltonian та оновлення орбіталей — у FP32; підпросторова eigenproblem та перевірки збіжності/енергії — у FP64; увімкнення через `LDAVIATOR_MIXED_PRECISION = 1`.
- Час до результату: до 22x швидше за CPU для проєктованого навантаження датасету OMat24, і до 7x швидше за OpenACC GPU-версію VASP; вартість — до 75% нижче за CPU (економія оцінена як $5-6M для датасету розміру OMat24).
- Приклади: одноатомне залізо — >2x прискорення проти CPU; 64-атомний Bi-допований GaAs — скорочення часу виконання на >85%; mixed precision дає ~2x прискорення на RTX PRO 6000 (FP32 Davidson solver у 3-7x швидше), тоді як на H100/H200/B200 виграш лише маргінальний.
