---
company: openai
title: "Scaling Git at OpenAI"
url: https://openai.com/index/scaling-git-at-openai
date: 2026-11-02
found_via: rss (TIER-1)
---

OpenAI built Pando, a new horizontally-scalable, Git-protocol-compatible backend that now powers all development in its monorepo, cutting median push latency by nearly 5x while serving almost a petabyte of Git data per day.

## card

**Що сталося:** OpenAI розробили Pando — новий бекенд для Git, який тепер обслуговує всю розробку в монорепозиторії компанії, повністю зберігаючи сумісність з Git-протоколом і клієнтом (і для людей, і для агентів).

**Контекст:** Потреба виникла через зростання масштабу паралельної роботи, яку уможливив Codex — більше гілок, пушів і fetch'ів одночасно; на старих рішеннях надійність інколи падала нижче 90%.

**Деталі:**
- Pando оптимізований одночасно під горизонтально масштабовані записи (паралельні пуші в різні гілки) і максимальну пропускну здатність читання.
- У продакшені Pando скоротив медіанну латентність пушу майже в 5 разів.
- Система передає майже петабайт Git-даних щодня.
- OpenAI планує передавати покращення клієнта Git у upstream-репозиторій Git-спільноти.
