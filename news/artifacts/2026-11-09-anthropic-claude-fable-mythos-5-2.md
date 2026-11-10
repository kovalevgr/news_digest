---
company: anthropic
title: "Introducing Claude Fable 5.2 and Claude Mythos 5.2"
url: https://www.anthropic.com/claude-fable-and-mythos-5-2
date: 2026-11-09
found_via: fetch (confirmed via WebFetch on anthropic.com/news; Jina 401'd, same as xAI/Perplexity this run)
---

Anthropic releases Claude Fable 5.2 (available to all users) and Claude Mythos 5.2 (verified organizations only) — the same underlying model with coding/reasoning/vision gains, outputs up to 30% faster than 5.1, an optional fast mode up to 2.5x faster, and cyber/bio safeguards with ~55% fewer false-positive blocks than 5.1; priced at $8/$40 per million input/output tokens standard, $16/$80 in fast mode.

## card

**Що сталося:** Anthropic випустила Claude Fable 5.2 (доступна всім користувачам) та Claude Mythos 5.2 (доступна лише верифікованим організаціям) — це одна й та сама базова модель із покращеннями в кодингу, міркуванні та зорі, виводом до 30% швидшим за 5.1 та опційним fast mode (до 2.5x швидше генерація токенів).

**Контекст:** Наступна версія після Fable/Mythos 5.1; Anthropic і далі рекомендує Claude Opus 5.5 як основну модель для щоденних задач, а Fable/Mythos — для найскладніших. Cyber- та bio-захист залишається на рівні 5.1, але з ~55% менше фолс-позитивних блокувань (−60% у кібербезпеці, −40% у біології); заблоковані запити Fable тепер обслуговує Opus 4.8 (кібер) чи Opus 5 (біо). Fable 5.2 отримала найсильніший на сьогодні захист від дистиляції (−90–99% зібраних даних).

**Деталі:**
- Ціна: $8/$40 за млн вхідних/вихідних токенів (стандартний режим), $16/$80 у fast mode.
- Бенчмарки Fable 5.2 vs Fable 5.1 vs Opus 5.5: FrontierCode 2.0 — 49.1% / 32.4% / 45.5%; FrontierSWE v2 — 69.9% / 56.3% / 62.3%; Humanity's Last Exam (з тулами) — 74.2% / 65.6% / 67.7%; Remote Labor Index — 41.3% / 17.9% / 21.3%.
- Mythos 5.2: 89.6% на CVE Rediscovery (було 78.3% у 5.1, 81.3% у Opus 5.5 без захисних механізмів).
- Доступність: Fable 5.2 — на всіх платформах (AWS, GCP, Azure), API ID `claude-fable-5-2`; Mythos 5.2 — через Cyber Verification Program і Life Sciences Verification Program.
- Зовнішнє тестування: UK AI Security Institute, Frontier Design, METR (без рецензування самого посту).
