---
company: huggingface
title: "NVIDIA Cosmos3-H-Dreams: Bringing Clinical Surgery to Life Through Generative Simulation"
url: https://huggingface.co/blog/nvidia/cosmos3-h-dreams
date: 2026-10-20
found_via: TIER-1 rss (huggingface.co/blog/feed.xml)
---

NVIDIA introduces Cosmos3-H-Dreams, a real-time generative video simulator for clinical cholecystectomy (gallbladder removal) surgery, trained on real surgical video and robot kinematics and runnable interactively on a single RTX PRO 6000 GPU; explicitly framed as a research tool, not a validated clinical system.

## card

**Що сталося:** NVIDIA публікує Cosmos3-H-Dreams — генеративний відео-симулятор хірургічної операції (холецистектомія, видалення жовчного міхура) в реальному часі, навчений на реальному відео операцій та кінематиці хірургічного робота CMR Surgical Versius.

**Контекст:** Це наступник попередньої Cosmos-H-Dreams, яка симулювала накладання швів на настільному тренажері dVRK. Автори прямо зазначають: "дослідницький симулятор, не перевірена система для догляду за пацієнтами".

**Деталі:**
- База: Cosmos3-H-Embodied-Nano (16B параметрів), попередньо натренована на наборі Open-H-Embodiment; двонапрямковий teacher-модель спеціалізовано на кураторському відео й кінематиці холецистектомії.
- 28 вимірів керування (поза та захват для обох рук, енергетичні контролі, осі джойстика), відео 832×480, дії синхронізовані на 10 Гц.
- Фокус на двох інструментах: лівий грасп Cadiere та правий монополярний гачок.
- Teacher дотренований на послідовностях 24 та 72 кадри (2.4с і 7.2с); дистиляція через causal teacher forcing і Self-Forcing дає causal student-модель, що генерує відео короткими блоками.
- Перший реліз — 4-кроковий чекпойнт; окремо натренований 2-кроковий чекпойнт жертвує якістю зображення заради швидкості.
- Інференс прискорює бібліотека FlashDreams (NVIDIA), з адаптованим модулем FadeMem для консолідації KV-кешу під час довгих rollout; працює інтерактивно на одному GPU RTX PRO 6000.
- Код, чекпойнти, Cosmos3-H-Embodied-Nano, Open-H-Embodiment і FlashDreams відкриті (GitHub / Hugging Face).
- Заявлені наступні кроки: моделювання повної процедури, поєднання генеративної та числової симуляції, оцінка хірургами, підтримка більшої кількості інструментів, автономні хірургічні політики в замкнутому циклі.
