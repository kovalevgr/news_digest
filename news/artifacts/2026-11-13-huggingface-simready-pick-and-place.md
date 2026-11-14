---
company: huggingface
title: "Build a Robot Pick-and-Place Simulation with SimReady Assets"
url: https://huggingface.co/blog/nvidia/simready-assets-robot-pick-and-place
date: 2026-11-13
found_via: rss
---

NVIDIA walks through building a robot pick-and-place simulation in Isaac Sim 6.2 using validated SimReady assets (a UR17G arm, Robotiq 2F-140 gripper, a beverage can) hosted on Hugging Face, driving the task with an AI agent (GPT-6 Sol in the example) using Isaac Sim skills.

## card

**Що сталося:** NVIDIA показав побудову симуляції pick-and-place в Isaac Sim 6.2 на валідованих SimReady-ассетах (рука UR17G, захоплювач Robotiq 2F-140, банка напою), розміщених на Hugging Face, де сценарій (захопити, піднести, перемістити, відпустити) виконує AI-агент (у прикладі — GPT-6 Sol) через навички Isaac Sim.

**Контекст:** Продовження бібліотеки SimReady Central (попередній анонс — запуск бібліотеки); ассети опубліковані в трьох репозиторіях на Hugging Face.

**Деталі:**
- Профілі валідації: Robot-Body 4.0.0 (рука) і Robot-Gripper 3.0.0 (захоплювач) — обидва проходять перевірки PhysX driven-joint.
- Репозиторії ассетів на Hugging Face: Robotiq-Official/simready-assets, TeradyneRobotics/UniversalRobots, nvidia/simready-assets.
- Обмеження: фіксований скриптований сценарій без зору; ліміт крутного моменту захоплення 2 Н·м підібраний емпірично в симуляції; автори прямо зазначають — результати не підтверджують стійкість до інших позицій об'єкта, ваги чи реального апаратного забезпечення.
- Ліцензування/вартість ассетів у статті не вказані.
