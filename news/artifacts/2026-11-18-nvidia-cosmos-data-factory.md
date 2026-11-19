---
company: nvidia
title: "Build Training-Ready Physical AI Datasets with Two Prompts in NVIDIA Cosmos"
url: https://developer.nvidia.com/blog/build-training-ready-physical-ai-datasets-with-two-prompts-in-nvidia-cosmos/
date: 2026-11-18
found_via: rss (developer.nvidia.com/blog/feed)
---

NVIDIA introduces Cosmos Data Factory, five cloud-native blueprints and six composable skills that a coding agent can orchestrate to turn a prompt into a training-ready physical-AI dataset, plus open-sourcing Cosmos Dataset Search under Apache 2.0.

## card

**Що сталося:** NVIDIA представила Cosmos Data Factory (CDF) — п'ять готових cloud-native blueprint'ів і шість композованих "skills" для курації, обробки та синтетичної генерації даних для physical AI, якими керує coding-агент: один промпт налаштовує середовище, другий — запускає blueprint для конкретного кейсу.

**Контекст:** Проблема, яку вирішують: зйомка рідкісних дефектів, нічних інцидентів та інших складних сценаріїв — дорога й повільна, а перетворення сирих даних у тренувальний датасет зазвичай вимагає зшивання окремих інструментів для курації, розмітки, генерації та оцінки.

**Деталі:**
- П'ять кейсів: сценарії для тренування автономних авто, варіація одягу/атрибутів людей для re-identification, аугментація відео по погоді/освітленню, генерація відео рідкісних подій (пожежі, падіння), генерація зображень дефектів для візуальної інспекції.
- Вимірювання NVIDIA на 8×GPU RTX PRO 6000 Blackwell (~$40/год): AV-сценарії — ~130 клипів/день по $2.66 (у ~45x дешевше за $125 на зібраний вручну сценарій); аугментація зображень — ~42 649 пар/день по $0.023 (у ~10x дешевше); аугментація відео — ~305 клипів/день по $3.15 (у ~7x дешевше); збірка датасету дефектів скоротилась з двох місяців до одного дня (60x).
- Заявлені результати клієнтів: до 24% кращий recall на реальних аномаліях (Encord, ANYbotics), до 85% менше ручної інженерної роботи в оптичній інспекції (Siemens), очікувані 90% зменшення фізичних тест-драйвів (Volkswagen).
- Cosmos Dataset Search відкрито під Apache 2.0; Cosmos Curator тепер підтримує мультикамерне відео, IMU, GPS і початкову підтримку lidar.
