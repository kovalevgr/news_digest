---
company: perplexity
title: "Open-sourcing SPACE, the sandbox platform behind Computer"
url: https://www.perplexity.ai/hub/blog/open-sourcing-space
date: 2026-10-15
found_via: gap-scrape (anonymous Jina — perplexity.ai is DNS-blocked for direct WebFetch)
---

Perplexity open-sources SPACE, its in-house sandbox platform that has powered all Computer agent sessions since July, after security testing found it resilient against network-bypass techniques like the OpenAI/Hugging Face incident.

## card

**Що сталося:** Perplexity відкриває код SPACE — власної sandbox-платформи, яка з липня обслуговує всі сесії агента Computer; репозиторій доступний на GitHub (perplexityai/SPACE).

**Контекст:** SPACE замінив комерційного провайдера sandbox у липні 2026. Незалежне тестування безпеки ("Escaping SPACE: Part I", 2026-09-23) показало стійкість до мережевих обходів на зразок інциденту OpenAI/Hugging Face; виявлені тоді вразливості мережевих обмежень виправлені й не відтворюються при повторному тестуванні.

**Деталі:**
- Кожен sandbox SPACE працює у власній віртуальній машині з окремою ОС; SPACE вважає sandbox недовіреним середовищем і керує мережевим доступом та обліковими даними зовні.
- Створення sandbox у 3–5 разів швидше за попереднього провайдера на тому ж продакшн-трафіку.
- Обробляє мільйони створень sandbox на день із липня 2026.
- Тестування на злам: 0 успішних виходів із VM на хост за 108 спроб; виявлені обходи мережевих обмежень — виправлені, повторні спроби не вдалися.
- Частина серії відкритих security-інструментів Perplexity: BrowseSafe, Numbat (липень), Bumblebee (травень).
