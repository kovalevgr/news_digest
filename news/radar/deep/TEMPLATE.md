# Deep-dive template — radar/deep/<YYYY-MM-DD>-<slug>.md

Agent-facing spec for THE DEEP DIVE routine (see workflow.md). The document serves
three readers in this order: (1) the owner on a phone deciding in 30 seconds
whether to invest time, (2) the owner at a laptop reproducing the thing, (3) the
owner as an article author a week later. Front-load the verdict; never bury it.

Reader-facing text is UKRAINIAN. Numbers go in TABLES, never buried in prose.
**Never invent — every claim carries its URL; community reactions are quoted from
real threads, not imagined.** Unverifiable claims are flagged, not asserted.

```markdown
---
title: "<original title>"
source_url: <url>
card: KOV-<NN>
date: YYYY-MM-DD
verdict: try-now | try-later | read-only
effort: S | M | L
hardware: "<конкретно: M-series 32GB+ / NVIDIA 24GB+ / CPU-only / тільки API / нічого>"
article_odds: high | med | low
type_hint: tech_explainer | project_post
---

# <Назва людською мовою>

> **TL;DR:** 2–3 речення — що це і чому (не) варте часу owner-а. Читається з
> телефона за 15 секунд. Без жаргону, який потребує самого документа.

## Вердикт

| | |
| --- | --- |
| Що це | одним рядком |
| Зрілість | прототип / робочий інструмент / продакшн-грейд |
| Effort експерименту | S/M/L + одне речення чому |
| Залізо | що реально треба |
| Шанс на статтю | high/med/low + який кут найсильніший |

## Що це насправді

2–4 абзаци: що АВТОР стверджує vs що Є при близькому читанні коду/повного тексту.
Розриви між заявкою і реальністю — головна цінність цієї секції.
Якщо є червоні прапорці — окремим списком з 🚩 (невідтворювані числа,
клікбейт-розрив, мертвий код, cherry-picked бенчмарки).

## Як воно працює

Механізм/техніка, з технічним м'ясом: кроки процесу списком, ключові числа
ТАБЛИЦЕЮ (throughput, розміри, вартість, латентність — з одиницями і джерелом),
короткі код-фрагменти лише якщо вони пояснюють суть (≤10 рядків).

## Контекст

- Prior art: що це продовжує, з лінками.
- Конкуренти/альтернативи: порівняльна ТАБЛИЦЯ, якщо їх 2+.
- Що каже спільнота: реальні заперечення з HN/Reddit-тредів (цитата + лінк) —
  шукати чинні контраргументи, не тільки захоплення.

## Експеримент

- **Мета:** яке ЧИСЛО або перевірюваний висновок хочемо отримати (не "спробувати
  X", а "виміряти Y до/після").
- **Кроки:** нумерований чекліст; команди — де можливо, дослівно.
- **Що зафіксувати:** метрики, які стануть таблицею в статті.
- **Ризики/блокери:** що найімовірніше не заведеться і як обійти.

## Кути для статті

2–3 варіанти, кожен: чернетка заголовка + 1 речення чому цей кут зайде + тип
(`tech_explainer` / `project_post`). Це ПРОПОЗИЦІЇ owner-у — ніколи не
формулювати як його думку чи готовий тейк.

## Джерела

Кожен використаний URL з one-line анотацією (що саме звідти взято).
```

## Card comment (Linear)

The comment on the hot card is the PHONE-SIZED cut, not the full document:
TL;DR + the Вердикт table + the experiment's **Мета** line + footer
`Файл: news/radar/deep/<file>`. The full analysis lives in the repo file only.
