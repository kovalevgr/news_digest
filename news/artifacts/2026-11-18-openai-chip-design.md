---
company: openai
title: "Advancing chip design with OpenAI models"
url: https://openai.com/index/advancing-chip-design-with-our-models/
date: 2026-11-18
found_via: gap-scrape (WebFetch — openai.com/news listing)
---

OpenAI reports using its models to optimize its own Jalapeño inference chip and AMD's GPU/CPU IP, plus benchmarks five models on RISC-V core design tasks, and announces a partnership with Synopsys to train "GPT-Synopsys" for EDA tool use.

## card

**Що сталося:** OpenAI описує три напрямки застосування своїх моделей у дизайні чипів: оптимізація власного інференс-чипа Jalapeño за допомогою GPT-o3 mini, співпраця з AMD з переписування SystemVerilog RTL для флагманського GPU IP, і бенчмарк п'яти моделей на задачах покращення відкритих RISC-V ядер (PicoRV32, Ibex).

**Контекст:** Jalapeño — перший власний інференс-чип OpenAI, анонсований раніше (серпень 2026); зміни вже перевірені в силіконі під час bring-up. Напрямок продовжується партнерством із Synopsys для тренування моделі "GPT-Synopsys", що використовуватиме інструменти EDA як досвідчений інженер-дизайнер.

**Деталі:**
- Jalapeño: зміни зменшили площу стандартних осередків у matrix unit на ~10% і у vector unit на ~13%; окремий редизайн мультиплексора зменшив площу на ~15% і latency з 2 тактів до 1.
- Співпраця з AMD: до 14% покращення PPA на флагманському GPU IP порівняно з уже оптимізованими базовими варіантами; частина змін уже в дизайні AMD, відправленому на виробництво. AMD також повідомила про однозначні (single-digit) покращення PPA на ключових блоках майбутнього флагманського CPU.
- RISC-V бенчмарк (~112K токенів на прогон): GPT-6.2 Astra — найкращий результат на PicoRV32 і Ibex; при дизайні ядра "з нуля" за специфікацією всі п'ять моделей показали вищі результати (GPT-6.2 Astra ≈0.7 на PicoRV32, ≈0.75 на Ibex); загалом 9881 оцінений прогін.
- Застереження: дизайн "з нуля" за специфікацією може пропускати функції (напр. performance counters), що може роздувати оцінки — потрібні жорсткіші тести.
