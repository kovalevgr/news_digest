---
company: huggingface
title: "An Indic Voice Agent with CUGA"
url: https://huggingface.co/blog/ibm-research/an-indic-voice-agent-with-cuga
date: 2026-11-25
found_via: TIER-1 rss
---

IBM Research builds a voice-based farm assistant on its open-source CUGA agent harness, answering spoken questions in several Indic languages by searching an English agricultural handbook via multilingual embeddings.

## card

**Що сталося:** IBM Research створює голосового "Farm Assistant" на основі власного відкритого агентного фреймворку CUGA. Фермери задають питання голосом своєю мовою, а агент відповідає, спираючись виключно на англійський аграрний довідник, показуючи використані сторінки джерела для перевірки.

**Контекст:** Пост опубліковано 25 листопада 2026 на блозі Hugging Face від IBM Research; CUGA — агентний харнес з відкритим кодом під ліцензією Apache 2.0.

**Деталі:**
- Мови: хінді, таміл, телугу, гуджараті, маратхі та інші; відповідь дається тією мовою, якою задано питання.
- База знань: 154-сторінковий англійський аграрний довідник, пошук через мультимовну embedding-модель `intfloat/multilingual-e5-large`.
- Формат відповіді: 2–4 вимовлених речення, обґрунтованих довідником.
- Доступність: спробувати можна в CUGA Apps на Hugging Face Spaces без додаткового налаштування.
