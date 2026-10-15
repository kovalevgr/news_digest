---
company: Google Research
title: "Analyzing technical documents with Deep Review"
url: https://research.google/blog/analyzing-technical-documents-with-deep-review/
source_url: https://research.google/blog/rss/
published: 2026-10-14
fetched: 2026-10-15
---

Google Research publicly launches Deep Review, an agentic document-verification system that grew out of its conference-paper review pilot (Paper Assistant Tool) to also cover legal and financial documents.

## card

**Що сталося:** Google Research відкрив публічний доступ до Deep Review — агентної системи перевірки складних документів на логічну послідовність і фактичну обґрунтованість. Система виросла з пілоту Paper Assistant Tool для наукових статей і тепер охоплює юридичні та фінансові документи.

**Контекст:** Пілотними партнерами були STOC 2026, ICML 2026, NeurIPS 2026 та ICLR 2027; супровідна стаття — arXiv:2606.28277 ("Towards Automating Scientific Review with Google's Paper Assistant Tool").

**Деталі:**
- Пілот охопив понад 16,000 рукописів авторів, які самі погодилися на приватний попередній відгук
- Кількість поданих робіт на ICLR/NeurIPS/ICML цьогоріч перевищила 74,000 (проти ~45,000 у 2025 та ~32,000 у 2024)
- Безкоштовно — 2 перевірки документів на тиждень; вищі ліміти та Deep Review API за власним Gemini-ключем
- Чотириетапний конвеєр: сегментація документа → адаптивний розподіл обчислень → паралельна верифікація сегментів → синтез і зовнішня перевірка фактів
- Завантажені документи не використовуються для тренування моделей; зберігаються рік лише для показу користувачу
- Формати на старті — PDF і plain text; підтримка кількох файлів одночасно "скоро"
- Додано підтримку Gemini 4 Argon
