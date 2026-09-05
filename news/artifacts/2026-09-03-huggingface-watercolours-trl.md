---
company: Hugging Face
title: "Training a coding model to paint watercolours with TRL and OpenEnv"
url: https://huggingface.co/blog/train-to-paint-with-code
published: 2026-09-03
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-05
---

Hugging Face's Sergio Paniego reproduces and open-sources an RL pipeline training a 35B Qwen coding model to write JavaScript that paints watercolours via p5.brush, using TRL's GRPO trainer with a multi-component reward (gate, length, pairwise judge, HPSv3 preference model) against 178 curated reference paintings.

## card

**Що сталося:** Серхіо Паньєго (Hugging Face) відтворив і опублікував пайплайн, який через RL (GRPO у TRL) навчає 35B-модель Qwen писати JavaScript-код, що малює акварелі бібліотекою p5.brush.

**Контекст:** Інженерне відтворення вірусного проєкту Сур'ї Нарредді (23 серпня) з повністю опублікованими артефактами й деталями нагородної функції.

**Деталі:**
- LoRA-тюнінг (`all-linear` модулі) для MoE-архітектури Qwen 35B
- Нагорода: gate (0.05) + довжина (0.05) + парний суддя (0.60) + модель переваг HPSv3 (0.30), проти 178 еталонних акварелей
- Три тренувальні прогони: hps-only (60 кроків), judge-led (110), hps-led (110); ~15-18 хв на крок (70-80% часу — рендеринг)
- 1×H200 GPU, ~34 години на 110-кроковий прогін; приріст середньої нагороди: +0.13 / +0.27 / +0.24 відповідно
