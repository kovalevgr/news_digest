---
company: huggingface
title: "ALTK-Evolve: How learned memory tops the τ²-bench leaderboard on customer service tasks without a frontier model"
url: https://huggingface.co/blog/ibm-research/altk-evolve-bc
date: 2026-10-20
found_via: TIER-1 rss (huggingface.co/blog/feed.xml)
---

IBM Research releases ALTK-Evolve, a library that distills behavioral guidelines from an agent's own past task attempts and injects them into its system prompt (no weight updates), lifting τ²-bench accuracy for both gpt-4.1 and gpt-5.5 agents while raising per-conversation cost.

## card

**Що сталося:** IBM Research публікує ALTK-Evolve — бібліотеку, що вилучає поведінкові рекомендації з власних минулих спроб агента виконати задачу та додає їх до системного промпту, без оновлення ваг моделі.

**Контекст:** Та сама модель (`gpt-4.1`) виконує роль і агента, і екстрактора рекомендацій; рекомендації виводяться з успіхів і невдач на тренувальній частині бенчмарку Sierra τ²-bench (стандартний ReAct-скаффолд, `gpt-5.5` як симулятор клієнта, 4 спроби на задачу) і без змін застосовуються до відкладеної тестової частини. Код — на GitHub (AgentToolkit/altk-evolve).

**Деталі:**
- На відкладеному тесті для агента `gpt-4.1`: Retail (40 задач) — точність 78.1%→82.5% (lossless-конфігурація), Pass^4 57.5%→67.5%; Airline (20 задач) — точність 57.5%→65.0%, Pass^4 35.0%→40.0%.
- Вартість розмови зростає: Retail +65% ($0.084→$0.139), Airline +32% ($0.081→$0.107) — переважно через більші вхідні промпти; кількість ходів агента трохи скорочується (~0.3-0.4 менше реплік на співставних прогонах).
- З frontier-моделлю (`gpt-5.5` як агент і екстрактор) на Airline: точність 72.5%→82.5%, Pass^4 55.0%→70.0%.
- На повному базовому спліті лідерборду (Pass^4, знімок 12 жовтня 2026): Retail — 67.5% (#1), випереджає frontier-моделі та RAFT-30B-A3B (61.4%, модель, донавчена на синтетичних даних τ²-bench retail); Airline — агент на `gpt-5.5` досяг 82.0% (#1), агент на `gpt-4.1` — 44% (#8).
- Автори зазначають обмеження: малі тестові вибірки (40 Retail, 20 Airline), а показники лідерборду — це власні подання авторів.
