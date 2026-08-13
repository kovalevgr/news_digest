---
company: Hugging Face
title: "Introducing OlmoEarth embeddings: Custom embedding exports from OlmoEarth Studio for downstream analysis"
url: https://huggingface.co/blog/allenai/olmoearth-embeddings
published: 2026-08-12
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-13
---

Allen AI adds custom embedding exports to OlmoEarth Studio — three encoder sizes (Nano/Tiny/Base) over Sentinel-1/2 satellite imagery, exported as int8 Cloud-Optimized GeoTIFFs for downstream geospatial analysis.

## card

**Що сталося:** Allen Institute for AI додав до OlmoEarth Studio експорт кастомних ембедингів — векторних представлень супутникових даних Землі — для подальшого аналізу поза платформою.

**Контекст:** Будується на фундаментальних моделях OlmoEarth для remote sensing з відкритими вагами й опублікованою статтею; доповнює наявні продуктові можливості студії новим downstream-сценарієм використання.

**Деталі:**
- Три розміри енкодера: Nano (128-вимірний, 1.4M параметрів), Tiny (192-вимірний, 6.2M), Base (768-вимірний, 89M)
- Налаштовувані просторова роздільність (10–80 м/піксель), часовий діапазон (1–12 місячних періодів), джерела знімків (Sentinel-2 L2A, Sentinel-1 RTC або обидва)
- Ембединги експортуються як Cloud-Optimized GeoTIFF у форматі int8 (-127…+127)
- Приклад few-shot сегментації (60 розмічених пікселів) дав F1 0.84 для класифікації мангрових заростей у В'єтнамі; кластеризація тестувалась на 1.1M pretraining-семплах з різних континентів
- Кастомні ембединги наразі доступні користувачам OlmoEarth Studio за запитом; публічні моделі та код — на Hugging Face й GitHub
