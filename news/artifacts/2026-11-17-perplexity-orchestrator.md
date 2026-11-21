---
company: perplexity
title: "Orchestrator: one API for reliable inference"
url: https://www.perplexity.ai/hub/blog/orchestrator-one-api-for-reliable-inference
date: 2026-11-17
found_via: gap-scrape (Jina worked cleanly this run; backfilled after being missed by prior runs)
---

Perplexity launches Orchestrator, a unified API for open-weight and proprietary models with automatic provider failover and unified billing, plus a preview "automatic routing" feature that assigns each request to a model based on a plain-language task profile.

## card

**Що сталося:** Perplexity запускає Orchestrator — єдиний API для відкритих та проприєтарних моделей з єдиним білінгом. Він автоматично обирає провайдера за доступністю, навантаженням і затримкою та повторює невдалі запити на іншому доступному деплойменті тієї ж моделі. Приймає OpenAI Chat Completions/Responses та Anthropic Messages формати запитів.

**Контекст:** За вимірюваннями 4 жовтня — 2 листопада 2026, запити до Claude й GPT через Orchestrator були успішними частіше, ніж до будь-якого окремого провайдера; найшвидший провайдер для однієї моделі змінювався з дня на день (напр. Claude Opus 5.5: Anthropic лідирував 15 з 30 днів, AWS Bedrock — решту 15).

**Деталі:**
- Preview-функція "automatic routing" (`perplexity/auto`): модель-рішення читає розмову й зіставляє її з описами маршрутів без бачення назв моделей; маршрутизація за замовчуванням, якщо немає відповідності.
- Тест на 63-задачному підмножині Terminal-Bench 4.1: маршрутизація навколо відмов безпеки Claude Fable 5.2 (на GPT-6/6.1) підняла результат з 38 до 41 з 63 задач при вищій оцінній вартості.
- Білінг: кожен запит тарифікується за ставкою моделі-відповідача незалежно від провайдера, що обслужив запит; використовує ті ж передплачені кредити, що й решта API-проєкту.
- Доступ через існуючий OpenAI/Anthropic SDK + Orchestrator base URL і ключ Perplexity API.
