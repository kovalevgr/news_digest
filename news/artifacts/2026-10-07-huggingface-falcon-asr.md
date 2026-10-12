---
company: Hugging Face
title: "Introducing Falcon ASR"
url: https://huggingface.co/blog/tiiuae/falcon-asr
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-07
fetched: 2026-10-12
---

The Technology Innovation Institute (TII) releases Falcon-ASR, a 1.6B-parameter speech-recognition model covering Arabic (especially Emirati dialect) plus English, French, Spanish, and Portuguese with one set of weights. Found via gap-scrape (WebFetch of huggingface.co/blog — TIER-1 RSS never surfaced this post; same-day sibling posts from TII were already captured, this one was missed).

## card

**Що сталося:** TII (Абу-Дабі) випускає Falcon-ASR — модель розпізнавання мови на 1.6B параметрів, що розпізнає арабську (з фокусом на емірадський діалект), а також англійську, французьку, іспанську та португальську одним набором ваг, без прапорця мови; підтримує word-level timestamps.

**Контекст:** Модель побудована на архітектурі та підході до тренування Falcon3-Audio; тренувальні дані включають симульований фоновий шум, перекриту мову, музику, реверберацію та ефекти телефонії.

**Деталі:**
- Арабська: середній WER 20.92% на 6 тестових наборах Open Universal Arabic ASR Leaderboard (на 2.25 п.п. краще за найкращий опублікований результат 23.17%)
- Емірадський діалект (внутрішня оцінка): WER 22.73%, CER 10.19% — найкращий серед порівнюваних систем, на 4.07 п.п. краще за Qwen3-Omni
- Англійська: середній WER 5.74% на 7 публічних тестових наборах HF Open ASR Leaderboard
- Доступна демо-Space на Hugging Face; API та нативні застосунки заплановані
