---
company: Google DeepMind
title: "WeatherNext: AI model achieves breakthrough in forecasting cyclones"
url: https://deepmind.google/blog/weathernext-ai-model-achieves-breakthrough-in-forecasting-cyclones
published: 2026-08-06
source_url: https://deepmind.google/blog/rss.xml
fetched: 2026-08-07
---

Google DeepMind's WeatherNext AI model achieves a breakthrough in forecasting cyclones,
improving on prior weather-prediction approaches.

## card

**Що сталося:** Google DeepMind представила модель WeatherNext Cyclones, яка суттєво покращує прогнозування тропічних циклонів: триденні прогнози тепер такі ж точні, як раніше дводенні — фактично додатковий день передбачуваності. Код і ваги моделей відкриті, результати опубліковані в Nature.

**Контекст:** За постом, моделі WeatherNext вже використовувалися Національним ураганним центром США (NHC) під час сезону ураганів 2025 року — зокрема модель передбачила швидку інтенсифікацію урагану Melissa та його вихід на сушу на Ямайці.

**Деталі:**
- Для 3-денних прогнозів: похибка позиції ~100 км, похибка інтенсивності ~11 вузлів; перевага понад 24 години для треку, інтенсивності та структури вітру. DeepMind оцінює це як еквівалент приблизно десятиліття метеорологічного прогресу.
- Єдина AI-модель прогнозує одночасно трек, інтенсивність і структуру вітру; 15-денний прогноз генерується менш ніж за хвилину на TPU.
- Роздільна здатність 28×28 км (у ~100 разів грубша за традиційні моделі); ансамбль із 1000 членів (проти 50 торік); компактна WeatherNext 2-mini працює на одному TPU і доступна через публічний Colab.
- Код і ваги WeatherNext Cyclones та WeatherNext 2 відкриті на GitHub; прогнози доступні через платформу Weather Lab.
- Партнери: National Hurricane Center (NOAA/NWS/NCEP), CIRA, UK Met Office; публікація в Nature — 6 серпня 2026.
