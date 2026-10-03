---
company: Hugging Face
title: "Open-sourcing AstaBrief, the fast report-generation model in Asta"
url: https://huggingface.co/blog/allenai/astabrief
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-02
fetched: 2026-10-03
---

Allen Institute for AI open-sources AstaBrief, an 8B-parameter (Qwen3-8B base) model fine-tuned via SFT+DPO to generate complete cited scientific reports in one pass; 51.1s average generation time vs. 178.5s for a Claude-powered Thinking-mode baseline (~3.5x faster), trained on 47K SFT examples + 6K DPO pairs derived from 90K real user queries, weights and data released on Hugging Face. Note: this same announcement is also covered by today's radar run as a highlight in `radar/community.md` (added 2026-10-03) — kept here too per the Hugging Face company feed's normal scope (third-party-org posts hosted on huggingface.co/blog are routinely included in this topics file).

## card

**Що сталося:** Allen Institute for AI (AI2) відкрив ваги AstaBrief — моделі для швидкої генерації цитованих наукових звітів у платформі Asta, яка створює повний звіт за один прохід замість покрокового підсумовування.

**Контекст:** Продовжує серію відкритих релізів AI2 (Olmo, Asta); відповідає на потребу дослідників у швидшому, локально розгортуваному та водночас перевірюваному (з посиланнями на джерела) синтезі звітів без залежності від пропрієтарних API.

**Деталі:**
- Базова модель: Qwen3-8B (8 млрд параметрів), донавчання SFT + DPO
- Швидкість генерації: 51.1 с у середньому проти 178.5 с у режимі Thinking на базі Claude — приблизно у 3.5 рази швидше
- Дані для навчання: 47 000 SFT-прикладів і 6 000 DPO-пар, отриманих з 90 000 реальних запитів користувачів
- У тестуванні 29.1% з 374 користувачів обрали швидкий режим на кілька днів поспіль, 23% повністю відмовились від режиму Thinking на користь AstaBrief
- Ваги та дані для навчання відкриті на Hugging Face
