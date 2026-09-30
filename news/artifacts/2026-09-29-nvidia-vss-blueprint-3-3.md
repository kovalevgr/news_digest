---
company: NVIDIA
title: "Lower the Cost of Building and Running Visual AI Agents with NVIDIA VSS Blueprint 3.3"
url: https://developer.nvidia.com/blog/lower-the-cost-of-building-and-running-visual-ai-agents-with-nvidia-vss-blueprint-3-3/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-09-29
fetched: 2026-09-30
---

NVIDIA releases VSS Blueprint 3.3, adding a "Build Vision Agent" natural-language skill and Adaptive Efficient Video Sampling that prunes unchanged visual patches to cut VLM token processing costs for visual AI agents.

## card

**Що сталося:** NVIDIA випустила VSS Blueprint 3.3 з двома функціями зниження вартості: навичкою "Build Vision Agent" для складання мультиворкфлоу візуальних AI-застосунків із текстового промпту менш ніж за 30 хвилин, та Adaptive Efficient Video Sampling — динамічним відсіюванням незмінних візуальних патчів для VLM.

**Контекст:** Наступна ітерація VSS Blueprint для відео-аналітики на базі VLM; код доступний одразу на GitHub.

**Деталі:**
- Adaptive EVS: затримка алертів 1021мс→844мс (-17%), паралельні VLM-потоки 13→19 (+46%), на 80% менше вхідних токенів VLM для 60-хвилинного відеосумаризування
- Тестовано на RTX PRO 6000 Blackwell з Cosmos 3 Super FP8
- Наживо-сесія 2026-10-01 09:00 PT на YouTube
