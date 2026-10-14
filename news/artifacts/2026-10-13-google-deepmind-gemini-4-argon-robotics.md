---
company: Google DeepMind
title: "Gemini 4 Argon for Robotics"
url: https://deepmind.google/blog/gemini-4-argon-for-robotics/
source_url: https://deepmind.google/blog/rss.xml
published: 2026-10-13
fetched: 2026-10-14
---

Google DeepMind shows Gemini 4 Argon as a general-purpose physical-reasoning model for robotics — scoring 87% on the ERQA benchmark and demonstrated across robot control, Real2Sim, physical understanding, and self-improvement workflows, including learning a skill from a single video.

## card

**Що сталося:** Google DeepMind показує застосування Gemini 4 Argon у робототехніці як модель фізичного розуміння загального призначення: контроль роботів, Real2Sim-реконструкція, анотування відео та само-вдосконалення на реальному обладнанні.

**Контекст:** Частина одночасного релізу Gemini 4 Argon (того ж дня); ERQA (Embodied Reasoning QA) — окремий зовнішній бенчмарк просторового/фізичного міркування в 3D-середовищах.

**Деталі:**
- 87% на бенчмарку ERQA (суто reasoning, без донавчання) — найкращий результат серед фронтир-моделей
- Демонстрація "Video-to-Sim-to-Real": Argon подивився відео людини, що грає в корнхол, побудував симуляцію та whole-body рухи, перенесені на гуманоїда Apptronik Apollo — робот влучив 7 підряд кидків у реальному тесті
- Argon керував квадрупедом Boston Dynamics Spot (12-DoF ноги + 6-DoF рука), навчаючись викидати банки у смітник з педаллю, спершу практикуючись у MuJoCo-двійнику
- У тесті "action improvement via simulation": Argon самостійно зібрав 4500+ епізодів симуляції з одного фото столу, підвищивши успішність реального робота з 56% до 75% і скоротивши час виконання з 35с до 24с
- На простому 6-DoF маніпуляторі Argon само-вдосконалювався за 3 ітерації: 58.9с → 22.9с → 17.4с на задачу pick-and-place
- "Video-to-Sim-to-Real" конвеєр стискає тижні ручного моделювання симуляцій до кількох годин
