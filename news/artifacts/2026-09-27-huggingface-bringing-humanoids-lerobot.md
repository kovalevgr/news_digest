---
company: Hugging Face
title: "Bringing Humanoids to LeRobot"
url: https://huggingface.co/blog/nepyope/bringing-humanoids-to-lerobot
source_url: https://huggingface.co/blog
published: 2026-09-25
fetched: 2026-09-27
note: "Backfilled — huggingface.co/blog/feed.xml reported 304-not-modified at this run's cursor (and at the 2026-09-26 run's), so TIER-1 never surfaced it; found via gap-scrape WebFetch of the blog listing page (post showed as '1 day ago') and confirmed via primary-source fetch."
---

Hugging Face's LeRobot team adds humanoid-robot support centered on the Unitree G1: a vision-language policy predicts compact motion tokens that a fast controller decodes into whole-body movement, demonstrated on a pick-and-place task.

## card

**Що сталося:** Команда LeRobot (Hugging Face) додала підтримку гуманоїдних роботів на базі Unitree G1: архітектура керування, де vision-language policy передбачає компактні "motion tokens", які швидкий контролер декодує у рухи всього тіла. Продемонстровано на задачі pick-and-place.

**Контекст:** Демо натреновано на політиці π0.5 з енкодером руху SONIC, файнтюн — 12 000 кроків на 4×H100, з використанням ~100 епізодів телеоперації (~71 хвилина запису).

**Деталі:**
- Відкрите апаратне забезпечення: модифікації "заліза" плюс телеоперативний екзоскелет Homunculus
- Доступ до датасетів гуманоїдів, включно з HIW-500 (500+ годин, 23 тис. епізодів)
- Базова модель: π0.5 policy + SONIC motion encoder
- Файнтюн: 12 000 кроків на 4×H100 GPU
