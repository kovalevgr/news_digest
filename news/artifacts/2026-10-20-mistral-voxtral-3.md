---
company: mistral
title: "Voxtral 3"
url: https://mistral.ai/news/voxtral-3/
date: 2026-10-20
found_via: TIER-1 rss (mistral.ai/rss.xml)
---

Mistral launches Voxtral 3, a family of speech-to-text and text-to-speech models plus a real-time voice agent SDK (built on LiveKit) combining transcription, reasoning/tool-calling, and speech synthesis into one streaming pipeline, EU-hosted or self-deployable.

## card

**Що сталося:** Mistral представляє Voxtral 3 — нове сімейство моделей розпізнавання (STT) та синтезу мовлення (TTS), а також SDK для голосових агентів у реальному часі (на базі LiveKit), що об'єднує розпізнавання, розмірковування/виклик інструментів і синтез мовлення в один потоковий конвеєр.

**Контекст:** Це наступна версія лінійки Voxtral; SDK позиціюється як інструмент для побудови голосових агентів з підтримкою дзвінків по SIP (телефонія) та WebRTC (браузер/застосунки), з можливістю як хмарного (EU/US/глобальні endpoints), так і повністю самостійного розгортання для контролю над обробкою та зберіганням аудіо.

**Деталі:**
- Voxtral Small Transcribe 3 ($0.004/хв) — флагманська модель розпізнавання, 50+ мов, діаризація мовців, контекстне зміщення (context biasing), визначення кінця репліки; за заявою Mistral — SOTA на FLEURS та бенчмарках діаризації, попереду Whisper large-v3 і Scribe v2.
- Voxtral Mini Transcribe 3 ($0.0035/хв, batch) — 4B-параметрова модель для швидкого й дешевшого розпізнавання, 50+ мов.
- Voxtral Mini Transcribe Realtime 3 ($0.008/хв) — для агентів, латентність менше 500 мс, 35-40+ мов.
- Context biasing: на бенчмарку Earnings 22 — приблизно 94% keyphrase recall з підказаними термінами.
- Voxtral Speech 3 / Voxtral Mini TTS 3.0 — $13 за 1M символів, 35+ мов і 50+ діалектів, контроль емоції/темпу/акценту, клонування голосу (30+ хвилин зразків).
- Voice agent SDK: $0.04/хв з Mistral Small 4 як моделлю розмірковування, $0.08/хв з іншими моделями; заявлена латентність відповіді — менше 1 секунди на реплік.
- Доступно вже зараз через API (EU/US/глобальні endpoints) та в Studio playgrounds; повне on-premises/private-cloud розгортання — через продажі Mistral.
