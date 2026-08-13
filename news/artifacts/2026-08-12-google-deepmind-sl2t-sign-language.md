---
company: Google DeepMind
title: "Putting sign language AI into users' hands"
url: https://deepmind.google/blog/putting-sign-language-ai-into-users-hands/
published: 2026-08-12
source_url: https://deepmind.google/blog/rss.xml
fetched: 2026-08-13
---

Google DeepMind introduces SL2T (sign-language-to-text), a breakthrough on-device translation model now powering sign-to-text dictation in Gboard and Live Transcribe on Pixel 11, trained on 100,000+ hours of data across 50+ sign languages.

## card

**Що сталося:** Google DeepMind випустила SL2T (sign-language-to-text) — модель перекладу жестової мови в текст, яка вже працює на пристрої в Gboard та Live Transcribe на Pixel 11. Модель навчена на понад 100 000 годинах даних із понад 50 жестових мов.

**Контекст:** Розмовні AI-моделі розвивались швидко, а жестові мови залишались недообслугованими — компанія оцінює аудиторію в 70 млн глухих і слабочуючих користувачів у світі; це перший випадок, коли жестова AI масово виходить із дослідницької стадії в споживчий продукт.

**Деталі:**
- Використовує on-device MediaPipe Holistic: відео перетворюється на pose landmarks, сире відео одразу відкидається (приватність)
- Перекладає напряму з послідовностей координат у текст, оминаючи проміжну "gloss"-анотацію
- Zero-shot результат 70 BLEURT на бенчмарку FLEURS-ASL — суттєво вище за будь-який раніше опублікований показник якості перекладу жестової мови
- Розраховано на однорукий жестовий рух, ліворуких користувачів, оптимізацію затримки для стрімінгу
- Доступно зараз на Pixel 11 для American Sign Language → English, безкоштовно; інші пристрої та мови — незабаром
