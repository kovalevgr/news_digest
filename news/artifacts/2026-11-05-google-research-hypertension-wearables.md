---
company: google-research
title: "Detecting signs of hypertension using wearable sensors"
url: https://research.google/blog/detecting-signs-of-hypertension-using-wearable-sensors/
date: 2026-11-05
found_via: rss
---

Google Research publishes AI-PPG-ACC-HTN, a multimodal AI system using consumer smartwatch PPG and accelerometry to passively screen for hypertension without cuff calibration, published in Nature and validated in a 196-participant, 5-site study against 24-hour ambulatory blood pressure monitoring; findings inform a new blood-pressure-trends feature in the Google Health app.

## card

**Що сталося:** Google Research опублікувала в Nature AI-PPG-ACC-HTN — систему, що за допомогою фотоплетизмографії (PPG) та акселерометрії (балістокардіограма) на звичайному смарт-годиннику пасивно виявляє ознаки гіпертонії без калібрування манжетою.

**Контекст:** Систему валідовано у проспективному дослідженні на 196 учасниках без відомих серцево-судинних захворювань у 5 центрах США проти золотого стандарту — 24-годинного амбулаторного моніторингу тиску (ABPM). Результати лягли в основу нової функції трендів артеріального тиску в застосунку Google Health.

**Деталі:**
- Початковий скринінг: чутливість 65.8%, специфічність 90.0%, PPV 80.6% (для порівняння — офісний замір: чутливість 55.3%, PPV 77.8%).
- Підтверджувальне тестування (n=48 з підвищеним офісним тиском): чутливість 78.4%, специфічність 90.9%, PPV 96.7%; багатоденний домашній моніторинг — чутливість 89.2%, специфічність 81.8%, PPV 94.3%.
- Модель навчена у два етапи: self-supervised contrastive pretraining на 492,347 годинах даних 2,109 учасників, потім логістична регресія на усереднених ембеддингах + зріст.
- Автори наголошують: це раннє дослідження можливості, не заміна манжети і не комерційний продукт — призначення — опортуністичний скринінг, що спонукає звернутися до лікаря.
