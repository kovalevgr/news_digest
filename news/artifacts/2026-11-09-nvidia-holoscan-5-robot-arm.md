---
company: nvidia
title: "Make a Robot Arm Feel Weightless with NVIDIA Holoscan 5"
url: https://developer.nvidia.com/blog/make-a-robot-arm-feel-weightless-with-nvidia-holoscan-5/
date: 2026-11-09
found_via: rss
---

NVIDIA's Technical Blog publishes a tutorial building a gravity-compensation control loop for a robot arm on Holoscan 5 (launched Oct 20, 2026), using three custom operators (joint-state read, Pinocchio-based gravity-torque solve, motor-command send); CPU-core pinning cuts p99.99 latency up to roughly 9.6x for the Python implementation and 5x for C++.

## card

**Що сталося:** NVIDIA опублікувала технічний тьюторіал із побудови контуру гравітаційної компенсації для роботизованої руки на базі Holoscan 5 — трьох кастомних операторів Holoscan (читання стану суглобів, розрахунок гравітаційних моментів через Pinocchio, передача команд моторам).

**Контекст:** Продовжує лінійку Holoscan 5 (запущений 20 жовтня 2026), який додав керування роботами поряд з обробкою сенсорних даних. Протестовано на Jetson Orin Nano, Jetson Thor та x86 Ubuntu 24.04, на роборуці Seeed Studio reBot Arm B601-DM.

**Деталі:**
- Прив'язка control-партиції до CPU-ядра + cgroup-ізоляція знизили p99.99-латентність приблизно у 5x (C++) і 9.6x (Python) без перезавантаження ядра.
- Латентність (Nsight Systems, 1M циклів): C++ pinned p50 7.1 мкс / p99.99 17.2 мкс; Python pinned p50 93.0 мкс / p99.99 142.6 мкс.
- Watchdog вимикає мотори, якщо команда не надійшла за 100 мс (дефолтний таймаут).
- Репозиторій тьюторіалу включає реалізації на Python і C++, плюс приклад з кінематикою та impedance control.
