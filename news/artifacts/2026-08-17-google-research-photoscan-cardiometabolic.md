---
company: Google Research
title: "Seeing beyond BMI: Estimating cardiometabolic risk with smartphone imagery"
url: https://research.google/blog/seeing-beyond-bmi-estimating-cardiometabolic-risk-with-smartphone-imagery/
published: 2026-08-17
source_url: https://research.google/blog/rss/
fetched: 2026-08-18
---

Google Research introduces PhotoScan, a deep-learning framework that estimates body composition from standard smartphone photos to predict insulin resistance, reaching near-DXA-scan accuracy without radiation exposure or specialized equipment.

## card

**Що сталося:** Google Research представив PhotoScan — фреймворк на основі глибокого навчання, що оцінює склад тіла зі звичайних смартфонних фото для прогнозування інсулінорезистентності, з точністю, близькою до клінічного DXA-сканування.

**Контекст:** Традиційне вимірювання складу тіла покладається на дороге DXA-сканування (з опроміненням) або обмежений біоелектричний імпеданс (BIA) смарт-годинників; PhotoScan пропонується як масштабована неінвазивна альтернатива.

**Деталі:**
- Дані: попереднє навчання на 35 323 записах UK Biobank (МРТ + DXA), donavчання на когорті PhotoBIA (677 дорослих, фото з Pixel + дані смарт-годинника), валідація на незалежній когорті MetabolicMosaic (132 особи, 30-тижневе дослідження)
- Точність відсотка жиру в тілі: MAE 2.13 проти 2.91 у BIA
- Класифікація інсулінорезистентності: AUROC 0.760 з ознаками PhotoScan проти 0.692 базових демографічних даних (і 0.773 з DXA)
- Net Reclassification Index: покращення на 0.593 порівняно з базовою моделлю
- Статус: дослідницький прототип, широкого доступу поки немає
