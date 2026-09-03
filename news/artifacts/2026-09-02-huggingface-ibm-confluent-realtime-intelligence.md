---
company: Hugging Face
title: "Real-Time Intelligence with IBM Time Series Models on Confluent"
url: https://huggingface.co/blog/ibm-research/real-time-intelligence
published: 2026-09-02
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-03
---

IBM Research and Confluent announced early access integrating IBM's Granite Time Series foundation models (PatchTST-FM, FlowState, TTM, TSPulse) directly into Confluent Cloud via Apache Flink SQL functions, enabling real-time forecasting/anomaly detection without separate ML infrastructure.

## card

**Що сталося:** IBM Research та Confluent анонсували ранній доступ до інтеграції часових-рядів foundation-моделей IBM Granite Time Series безпосередньо у Confluent Cloud через SQL-функції Apache Flink, дозволяючи прогнозування та виявлення аномалій прямо на потоках даних.

**Контекст:** Портфель моделей (44M+ завантажень сукупно) раніше публікувався окремо на Hugging Face; це перший анонс їх вбудованої інтеграції у стрімінгову платформу без потреби в окремій ML-інфраструктурі.

**Деталі:**
- Чотири моделі: PatchTST-FM, FlowState, TTM, TSPulse
- Доступ через звичайний SQL-синтаксис (Flink SQL) — без тренування моделі чи feature engineering
- Заявлений "zero configuration" — не потребує окремої ML-інфраструктури
- Приклади застосування: контроль ліній темперування шоколаду, планування роздрібного попиту, виявлення шахрайства
