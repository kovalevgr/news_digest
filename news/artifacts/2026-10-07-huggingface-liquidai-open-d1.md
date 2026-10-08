---
company: Hugging Face
title: "Multimodal open d1 decision models for the edge"
url: https://huggingface.co/blog/LiquidAI/open-d1
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-07
fetched: 2026-10-08
---

Liquid AI open-sources two decision models on Hugging Face — d1-3B (text+image) and an experimental d1-omni-600M (text+image/audio) — with d1-3B topping the sub-10B Decision Index.

## card

**Що сталося:** Liquid AI випустив у відкритий доступ на Hugging Face дві decision-моделі: d1-3B (текст + зображення) та експериментальну d1-omni-600M (текст + зображення або аудіо). d1-3B набирає 48.57 на Decision Index 0.2.1 — найкращий результат серед моделей до 10B, випереджаючи Decider 35B-A3B (47.11); відповідь — за 16 мс на Jetson AGX Thor.

**Контекст:** Релізи того ж дня про цю саму модель висвітлені і в радарі (`radar/community.md`, community-гілка) — окремий pipeline зі своїм фокусом; тут мова про саму офіційну публікацію на HF.

**Деталі:**
- d1-3B: Decision Index 0.2.1 = 48.57, найвище серед моделей <10B; Decider 35B-A3B = 47.11
- d1-3B: inference 16 мс на Jetson AGX Thor
- d1-omni-600M: експериментальна, мультимодальність текст+зображення або текст+аудіо
- Ваги завантажувані з Hugging Face; демо — у System One Arcade Space
