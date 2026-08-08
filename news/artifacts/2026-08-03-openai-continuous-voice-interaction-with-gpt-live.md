---
company: OpenAI
title: "How we built a realtime system for responsive voice AI in six months"
url: https://openai.com/index/continuous-voice-interaction-with-gpt-live
published: 2026-08-03
source_url: https://openai.com/news/rss.xml
fetched: 2026-08-04
---

GPT-Live enables continuous voice interaction with AI, using a turnless speech model
and low-latency architecture for faster, more natural conversations.

## card

**Що сталося:** OpenAI опублікувала інженерний розбір того, як за шість місяців побудувала realtime-систему для GPT-Live — голосової системи третього покоління. Ключова зміна: full-duplex голосова модель, що слухає і говорить одночасно, тож окремий turn detector прибрано з аудіошляху — розмова стає безперервною і природнішою.

**Контекст:** GPT-Live — третє покоління голосового стека OpenAI (після каскадних систем і speech-to-speech моделей з turn-based архітектурою); спирається на попередню перебудову голосової інфраструктури для низьколатентного стрімінгу. Ця архітектура живить ChatGPT Voice, включно з нещодавно запущеним керуванням комп'ютером у desktop-застосунку ChatGPT.

**Деталі:**
- Full-duplex модель контролює розмову; глибше мислення й тули делегуються frontier-моделям (напр. GPT-5.5) асинхронно, без переривання потоку розмови
- Медіапотік відокремлено від бізнес-логіки: аудіо йде виділеним fast path, делегація і тули — за асинхронною RPC-межею, тож повільний tool call не зупиняє аудіо
- Media frontend та inference-логіку переписали з Python asyncio на Go: p95 плавності доставки кадрів нової системи дорівнює p50 старої
- Транспорт — WebRTC: переживає втрату пакетів і clock drift, розтягує аудіо при запізненні пакетів і прискорює відтворення, щоб наздогнати realtime
- Seamless handoff між інстансами моделі: прогрів заміни з префілом контексту сесії, паралельний інференс на обох, безшовне перемикання; той самий механізм використовується для компакції контексту в довгих розмовах
- Систему побудували за шість місяців
