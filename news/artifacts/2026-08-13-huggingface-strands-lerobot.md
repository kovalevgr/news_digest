---
company: Hugging Face
title: "Record, train, and deploy from one place with Strands Agents, LeRobot, and Hugging Face Storage Buckets"
url: https://huggingface.co/blog/amazon/strands-lerobot-streaming-data-loop
published: 2026-08-13
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-14
---

AWS's open-source Strands Robots SDK now closes the full robot-learning data loop with Hugging Face: record demonstrations into Storage Buckets, stream-train policies directly from the Hub, and deploy back to hardware — all in LeRobot format throughout.

## card

**Що сталося:** AWS Strands Robots (open-source SDK) отримав повний цикл роботи з даними разом із Hugging Face: запис демонстрацій у Storage Buckets, тренування політик потоковим читанням прямо з Hub, і деплой натренованих моделей назад на роботів — усе у форматі LeRobot.

**Контекст:** Це розширення екосистеми LeRobot/Hugging Face Storage Buckets на робототехніку конкретно через партнерство з AWS; використовує Xet-дедуплікацію та інтеграцію з політиками NVIDIA (GR00T, Cosmos 3) й іншими провайдерами.

**Деталі:**
- Xet-дедуплікація на рівні байтів знижує повторні завантаження приблизно на 75% при наступних синхронізаціях
- Стрімінгове тренування через `StreamingLeRobotDataset` — без повного локального завантаження, відео декодується "на льоту"
- Підтримувані роботи: SO-100/SO-101 (демо), плюс десятки інших через фабрику `Robot()`
- Провайдери політик: ACT, GR00T (NVIDIA), Cosmos 3 (NVIDIA), MolmoAct2 — через уніфіковані `TrainSpec`/`Trainer` API
- Бенчмарк: 500 кроків оптимізатора ACT на NVIDIA L4 — 133 секунди; читання з теплого CDN — ~1086 МБ/с
- Приклад-ноутбук працює в симуляції на ноутбуці без GPU; для заліза потрібне каліброване обладнання
