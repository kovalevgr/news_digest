---
company: Microsoft
title: "Introducing CARE-X: Towards Clinically Useful Radiology VLMs with Auxiliary Supervision, Reward-Aligned Learning, and Tool-Augmented Measurement"
url: https://www.microsoft.com/en-us/research/blog/introducing-care-x-towards-clinically-useful-radiology-vlms-with-auxiliary-supervision-reward-aligned-learning-and-tool-augmented-measurement/
published: 2026-08-11
source_url: https://www.microsoft.com/en-us/research/feed/
fetched: 2026-08-12
note: "TIER-1 rss."
---

Microsoft Research introduces CARE-X, a unified vision-language model for chest X-ray interpretation combining a SigLIP2 vision encoder with Phi-4-mini-instruct, task-specific auxiliary heads, and DAPO reward-aligned RL — reaching first place on the ReXVQA leaderboard (94% accuracy) as a research prototype, not a cleared medical device.

## card

**Що сталося:** Microsoft Research представила CARE-X — уніфіковану vision-language модель для інтерпретації рентгенів грудної клітки, яка в одному forward pass видає і вільнотекстовий звіт, і структуровані діагностичні оцінки з каліброваною впевненістю.

**Контекст:** Дослідницька модель (не медичний пристрій — компанія прямо зазначає відсутність регуляторного схвалення), спрямована закрити розрив між генеративними AI-системами й клінічними потребами радіології.

**Деталі:**
- Архітектура: SigLIP2-so400M vision encoder + Phi-4-mini-instruct (3.8B), задачеспецифічні auxiliary-голови для класифікації й visual grounding
- Тренування: тристадійний supervised fine-tuning + DAPO (reward-aligned RL)
- ReXVQA: 94% точності — 1 місце в лідерборді (станом на серпень 2026), на 6 п.п. вище наступної моделі
- Найвищі CRIMSON-скори з генерації звітів на MIMIC-CXR, IU-Xray, CheXpert-Plus, ReXGradient
- Anatomical grounding: +28.2 п.п. mAP над generative-only baseline
- Tool-augmented вимірювання (пара з Qwen3-VL): +21.4 F1 на кардіомегалії, +60.7–71.4 F1 на розширенні аорти, у середньому +43.6 п.п. на 5 станах
- Валідація на 1047 знеособлених рентгенах з Narayana Health; для CT-підтвердженого розширення recall сягнув 94.26% з tool-augmented інференсом
