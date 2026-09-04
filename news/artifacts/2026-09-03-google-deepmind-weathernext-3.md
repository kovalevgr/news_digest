---
company: Google DeepMind
title: "Introducing WeatherNext 3, our most advanced and accurate global weather AI model"
url: https://deepmind.google/blog/introducing-weathernext-3-our-most-advanced-and-accurate-global-weather-ai-model/
published: 2026-09-03
source_url: https://deepmind.google/blog/rss.xml
fetched: 2026-09-04
---

Google DeepMind and Google Research introduced WeatherNext 3, ingesting real-time satellite data hourly to produce forecasts roughly five times sharper than WeatherNext 2, now integrated across Search, Gemini, Maps, Google Maps Platform, and Cloud.

## card

**Що сталося:** Google DeepMind і Google Research представили WeatherNext 3 — найточнішу на сьогодні глобальну модель прогнозування погоди, за незалежними оцінками Brightband. Модель навчається безпосередньо на супутникових спостереженнях у реальному часі й генерує погодинні прогнози високої роздільної здатності.

**Контекст:** Продовжує лінійку WeatherNext (WeatherNext 2 — попередня версія на сітці 25 км з кроком 6 годин). WeatherNext 3 вже інтегровано в Search, Gemini, Maps, Google Maps Platform і Cloud.

**Деталі:**
- Погодинні прогнози на кількох просторових роздільностях: приземні змінні (температура, вологість) — 5 км, інші приземні змінні — 10 км, атмосферні (вітер) — 25 км
- Приблизно у 5 разів точніша за WeatherNext 2 (сітка 25 км, крок 6 год)
- Архітектура — єдина Functional Generative Network (FGN) mesh-transformer, що обробляє живі 1-годинні геостаціонарні супутникові мозаїки разом з історичними даними
- Видає щільні сітчасті поля, дискретні треки циклонів і прогнози для окремих метеостанцій нативно
