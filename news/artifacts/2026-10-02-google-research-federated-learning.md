---
company: Google Research
title: "Toward provably private learning from federated data"
url: https://research.google/blog/toward-provably-private-learning-from-federated-data/
source_url: https://research.google/blog/rss/
published: 2026-10-02
fetched: 2026-10-03
---

Google Research details a next-generation Federated Learning system using Trusted Execution Environments (TEEs) and public transparency logs to give externally-verifiable privacy guarantees while moving compute from client devices to servers; deployed in Gboard for English/Japanese next-word prediction with reduced noise multipliers and training time cut from 1-2 months per model.

## card

**Що сталося:** Google Research представив нове поколінні системи федеративного навчання (FL), яке дає зовнішньо-перевірювані гарантії приватності за допомогою довірених середовищ виконання (TEE) та публічних журналів прозорості, одночасно перенісши обчислювальне навантаження з клієнтських пристроїв на сервери.

**Контекст:** Розвиток попередніх систем федеративного навчання Google, які не могли довести зовнішнім аудиторам, що сирі дані ніколи не логувались чи переглядались; систему вже розгорнуто в Gboard.

**Деталі:**
- Архітектура: клієнтське шифрування + публічні журнали прозорості для політик доступу; Key Management System на RAFT-консенсусі перевіряє відповідність навантажень авторизованим обчисленням; виконання відбувається в серверних TEE
- Розгорнуто в Gboard для моделей передбачення наступного слова англійською та японською мовами
- Прискорення тренування — перенесення вузьких місць з пристроїв на сервери (раніше 1-2 місяці на модель)
- Сильніші гарантії приватності при менших множниках шуму порівняно з попередніми FL-системами
- Зовнішні аудитори можуть перевіряти гарантії приватності через відтворювані збірки й опубліковані політики доступу
