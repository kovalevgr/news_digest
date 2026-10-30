---
company: huggingface
title: "Granite Switch 4.1.1 — Update models like you update software"
url: https://huggingface.co/blog/ibm-granite/granite-switch-4-1-1
date: 2026-10-29
found_via: rss (TIER-1)
---

IBM ships Granite Switch 4.1.1, a backwards-compatible patch release retraining only the ASR speech model and the Decision adapter on top of the unchanged Granite Switch base model.

## card

**Що сталося:** IBM випускає Granite Switch 4.1.1 — патч-реліз модульної системи кеш-ефективних адаптерів поверх однієї базової моделі; перенавчені лише мовленнєвий (ASR) компонент і Decision-адаптер, базова модель не змінена.

**Контекст:** Granite Switch — підхід IBM до конфігурування LLM через спеціалізовані адаптери на одному ендпойнті; 4.1.1 повністю сумісний з 4.1 — існуючі налаштування не потребують змін.

**Деталі:**
- Мовлення (ASR): оновлена модель Granite Speech розпізнає 10 мов і додає пунктуацію/капіталізацію нативно.
- Decision-адаптер: оновлений адаптер у granitelib-core показує кращий результат на тестовому наборі Jev Decision Index (конкретні цифри не наведені).
- Ефективність: перенавчені лише два компоненти, решта не перераховувалась — достатньо скомпонувати нові адаптери й розгорнути.
- Доступність: granite-switch-4.1-30b (30B), granite-speech-5.0-470m-turboctc (0.5B), granitelib-core-r1.0 — усі на Hugging Face; є колекція моделей і демо-простір "Speech to Decisions".
- Плани: IBM обіцяє туторіали та Adapter SDK для сторонніх розробників адаптерів.
