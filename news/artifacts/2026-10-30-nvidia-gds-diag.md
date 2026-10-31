---
company: nvidia
title: "How to Check and Configure NVIDIA GPUDirect Storage for Your Platform"
url: https://developer.nvidia.com/blog/how-to-check-and-configure-nvidia-gpudirect-storage-for-your-platform/
date: 2026-10-30
found_via: rss (TIER-1)
---

NVIDIA's GPUDirect Storage team releases gds-diag, an open-source command-line utility that assesses GPUDirect Storage deployments, flags problems (FAIL/WARN/INFO/PASS), and suggests fixes, with an optional coding-assistant skill for Claude/Codex.

## card

**Що сталося:** Команда NVIDIA GPUDirect Storage випускає `gds-diag` — відкритий CLI-інструмент, що перевіряє середовище розгортання GDS, знаходить проблеми та пропонує виправлення; код не змінює систему самостійно.

**Контекст:** GDS забезпечує прямий шлях даних між сховищем і GPU для вищої пропускної здатності й нижчої затримки/навантаження на CPU; `gds-diag` — доповнення до існуючого стеку GDS, а не новий продукт у самому GDS.

**Деталі:**
- Підкоманди у чотирьох групах: наскрізні перевірки (`all`), перед встановленням (`support-matrix`, `pre-install`), валідація встановлення (`post-install`, `config-audit`), глибока діагностика контейнерів/точок монтування (`container-check`, `mount-check`).
- Рівні знахідок: FAIL (блокер), WARN (потенційний блокер), INFO, PASS (лише з `--verbose`); кожна знахідка має пояснення та план усунення.
- Вимоги: Linux + Python 3.8+; сам GDS потребує датацентрового GPU NVIDIA та CUDA Toolkit 12.2+, але `gds-diag` цих залежностей не вимагає.
- Опційний agent skill для Claude/Codex — маршрутизує запити до підкоманд, інтерпретує результати, може пропонувати/виконувати виправлення (з підтвердженням).
- Доступність: репозиторій NVIDIA Magnum IO на GitHub, код під Apache 2.0, agent skill — під CC BY 4.0.
