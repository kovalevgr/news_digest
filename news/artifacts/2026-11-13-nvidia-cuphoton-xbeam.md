---
company: nvidia
title: "Run GPU-Powered Black Hole Interferometry with NVIDIA cuPhoton"
url: https://developer.nvidia.com/blog/run-gpu-powered-black-hole-interferometry-with-nvidia-cuphoton/
date: 2026-11-13
found_via: rss
---

NVIDIA walks through xBeam, the FX correlator in its open-source cuPhoton v0.1.3 toolkit, built with the Harvard-Smithsonian Center for Astrophysics and MIT Haystack Observatory — on a 64-GPU Vera Rubin NVL72 system it correlates a 10 TB radio-interferometry dataset in 70 seconds versus ~8.9 hours on an x86 CPU baseline.

## card

**Що сталося:** NVIDIA показав xBeam — FX-кореляційний модуль у відкритому пакеті cuPhoton v0.1.3 (створений разом із Гарвард-Смітсонівським центром астрофізики та MIT Haystack Observatory) — для кореляції даних радіоінтерферометрії (наприклад, для зображень чорних дір), запущений на системі NVIDIA Vera Rubin NVL72 (64 GPU).

**Контекст:** Продовження серії публікацій про cuPhoton (попередній матеріал — про побудову зображень); xBeam виконує лише побудову видимостей (visibilities), калібрування та реконструкцію зображення — завдання наступних інструментів.

**Деталі:**
- Кореляція 10 ТБ даних за 70 секунд на 64 GPU (Vera Rubin NVL72, GPUDirect Storage) проти ~31 992 секунд (~8.89 год) на CPU x86 — приблизно 460x.
- Пропускна здатність читання: ~20 ГБ/с на 4 GPU → ~170 ГБ/с на 64 GPU.
- Масштабування: `--devices` (кілька GPU на вузлі), `--shard-count`/`--shard-index` (кілька вузлів) + `merge-shards`.
- Вихідні формати: DiFX SWIN або власний xbeam-v1.
- Код, модулі побудови зображень і приклади — у репозиторії NVIDIA/cuPhoton на GitHub.
