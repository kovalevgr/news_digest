---
company: Google Research
title: "Automating coherent long-form video generation"
url: https://research.google/blog/coherent-long-form-video-generation/
source_url: https://research.google/blog/rss/
published: 2026-09-24
fetched: 2026-09-25
---

Google Research introduces a unified multi-agent framework (AI Video Co-Director, CANVAS, A²RD, VQQA) that orchestrates existing Gemini/Veo foundation models to autonomously generate minutes-long, visually coherent video, addressing semantic drift and cascading failures that plague longer generations.

## card

**Що сталося:** Google Research представив уніфікований мультиагентний фреймворк для автономної генерації довгого відео: AI Video Co-Director оркеструє творчі рішення (наратив, структура, візуальна естетика) через multi-armed bandit оптимізацію, CANVAS підтримує візуальну узгодженість персонажів/локацій через персистентну пам'ять, A²RD генерує відео по сегментах з адаптивним перемиканням екстраполяції/інтерполяції, а VQQA замикає цикл через visual question-answering та ітеративну оптимізацію промптів.

**Контекст:** Фреймворк працює як шар оркестрації над існуючими фундаційними моделями (Gemini, Veo), успадковуючи їхні механізми безпеки, включно з водяним знаком SynthID. Це рух від лінійних цепочок модулів (де помилки накопичуються і потрібне ручне втручання) до замкненого автономного контуру.

**Деталі:**
- Успішно згенеровано відео тривалістю кілька хвилин, включно з 10-хвилинною демонстрацією
- AI Video Co-Director досягає оцінки якості 81.4 на GenAD-Bench
- Створено три спеціалізовані бенчмарки: GenAD-Bench (400 сценаріїв), HardContinuityBench, LVBench-C (120 сценаріїв)
- Вирішує проблеми "семантичного дрейфу" (зміна персонажів/декорацій), каскадних збоїв і "дрейфу ознак"
