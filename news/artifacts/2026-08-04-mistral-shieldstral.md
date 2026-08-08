---
company: Mistral AI
title: "Introducing Shieldstral"
url: https://mistral.ai/news/shieldstral
published: 2026-08-04
source_url: https://mistral.ai/rss.xml
fetched: 2026-08-05
---

Shieldstral is a 3B open-weights multimodal safety classifier from Mistral that outperforms
models up to 7x its size.

## card

**Що сталося:** Mistral випустила Shieldstral — відкритий (open-weights) мультимодальний класифікатор безпеки на 3 млрд параметрів для модерації контенту. Модель приймає політики модерації звичайною мовою прямо під час інференсу без перенавчання і дорівнює або перевершує guard-моделі до 7 разів більші за розміром.

**Контекст:** Реліз 4 серпня 2026 року позиціоновано як внесок Mistral у Open Secure AI Alliance (спільно з NVIDIA) — того ж дня альянс опублікував RFC щодо настанов SAFE із кібербезпеки агентних систем. Модель натреновано на платформі Mistral Forge.

**Деталі:**
- 3B параметрів; ваги відкриті під ліцензією Apache 2.0, доступні на Hugging Face
- Працює на одному GPU NVIDIA з 16 ГБ пам'яті
- Policy-adaptive: приймає plain-language політики на інференсі, без донавчання
- Модальності: текст (промпти, відповіді, пари промпт-відповідь), зображення з опційним текстом, комбінований контент
- Повертає калібровані ймовірнісні оцінки за один forward pass
- Сильні результати у text safety, refusal detection, адаптивності до політик і мультимодальній безпеці; усі тестові вибірки виключені з тренувальних даних
- Мультимовне покриття заявлене як напрям подальшої роботи; API-ціни не оголошені
