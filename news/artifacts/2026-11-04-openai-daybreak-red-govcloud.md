---
company: openai
title: "Daybreak Red is now available in AWS GovCloud (US-East)"
url: https://openai.com/index/daybreak-red-aws-govcloud
date: 2026-11-04
found_via: jina (WebFetch 403'd, one retry per failure-mode table)
---

OpenAI extends Daybreak Red — its purpose-trained cybersecurity model access (GPT‑5.6 Cyber) for authorized vulnerability research and exploit validation — to approved customers in AWS GovCloud (US-East) via Amazon Bedrock, building on existing Daybreak-on-Bedrock availability.

## card

**Що сталося:** OpenAI відкрила доступ до Daybreak Red (спеціально навчена кіберверсія GPT‑5.6 Cyber) для авторизованих команд у AWS GovCloud (US-East) через Amazon Bedrock — раніше Daybreak на Bedrock був доступний поза GovCloud-регіонами.

**Контекст:** Це розширення вже наявної інтеграції Daybreak-моделей (Daybreak Blue, Daybreak Red) з Amazon Bedrock для enterprise security-команд, представленої раніше. Daybreak Red дає верифікованим захисникам менше відмов на задачі пошуку вразливостей за рахунок посиленої верифікації ідентичності, моніторингу та контролю доступу.

**Деталі:**
- Доступ — лише для схвалених клієнтів після заявки на Daybreak Red та окремого провіщення в AWS; схвалення Daybreak Red не вмикає доступ до моделі в AWS автоматично.
- Дані інференсу в Bedrock не використовуються для тренування моделей; клієнти не повинні передавати свої дані Daybreak Red OpenAI.
- Призначення: дослідження вразливостей, валідація експлойтів, security testing у контрольованих умовах; кваліфіковані фахівці мають перевіряти знахідки та запропоновані фікси перед застосуванням.
