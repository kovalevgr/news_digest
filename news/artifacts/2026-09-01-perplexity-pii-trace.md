---
company: Perplexity
title: "PII-TRACE: Detecting Personal Data Before It Leaves the Device"
url: https://www.perplexity.ai/hub/blog/pii-trace-detecting-personal-data-before-it-leaves-the-device
published: 2026-09-01
source_url: https://www.perplexity.ai/hub/blog
fetched: 2026-09-02
---

Perplexity released PII-TRACE, a 13-language benchmark for consistent PII detection across long conversations, plus PII-Tracer, a compact 0.6B-parameter local detector that scored highest among 12 evaluated systems.

## card

**Що сталося:** Perplexity випустила PII-TRACE — бенчмарк на 13 мовах для виявлення персональних даних у багатоходових розмовах, та PII-Tracer — компактний детектор на 0.6B параметрів (на базі Qwen3) для локального запуску.

**Контекст:** Бенчмарк вирішує проблему послідовного виявлення одного й того ж ідентифікатора, що повторюється кілька разів у довгому діалозі; обидва компоненти планують випустити у відкритий доступ найближчим часом.

**Деталі:**
- 13 мов, 10 систем письма; 13 148 синтетичних розмов, 37 431 згадка ідентифікаторів 9 типів PII
- PII-Tracer — 0.6B модель на базі Qwen3, навчена на ~714 000 прикладах
- Найкращий character F1 (0.629) серед 12 оцінених систем, знаходить кожну згадку у 79.4% повторюваних ідентифікаторів
- Дата релізу PII-TRACE і PII-Tracer не вказана — "плануємо випустити незабаром"
