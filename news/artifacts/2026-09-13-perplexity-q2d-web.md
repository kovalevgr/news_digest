---
company: Perplexity
title: "Q2D-Web: Evaluating First-Stage Retrievers at Scale"
url: https://www.perplexity.ai/hub/blog/q2d-web
published: 2026-09-09
source_url: https://www.perplexity.ai/hub/blog
fetched: 2026-09-13
---

Perplexity releases Q2D-Web, a large-scale benchmark and public leaderboard for evaluating first-stage retrievers in agentic RAG systems: 190 million web documents and ~69,721 agent-reformulated queries across ten languages (English 65.8%, then Spanish, Russian, German, French, Portuguese, Italian, Korean, Japanese, Chinese), sampled over nine months of PII-free production search traffic. Extends the earlier Q2D benchmark with three independent relevance-judgment sets (agent citations, production web rankings, additional LLM judgments for unjudged pairs) rather than treating one source as ground truth; 13 retrievers (lexical, dense, late-interaction) evaluated so far, with public submissions accepted and the leaderboard hosted on Hugging Face. Backfilled: primary source blocked on every transport tried today (WebFetch EGRESS_BLOCKED, anonymous Jina 403 AbuseAlleviation); confirmed via WebSearch, corroborated by Perplexity's own community-forum announcement thread and independent coverage (AlphaSignal).

## card

**Що сталося:** Perplexity випускає Q2D-Web — великий бенчмарк і публічний лідерборд для оцінки ретріверів першого етапу (first-stage retrievers) в агентних RAG-системах.

**Контекст:** Розширює попередній бенчмарк Q2D до значно більшого корпусу — 190 млн веб-документів і майже 70 тисяч агентних запитів, зібраних за дев'ять місяців production-трафіку пошуку (без PII). Замість одного джерела істини бенчмарк дає три незалежні набори релевантності: за цитуваннями агента, за продакшн-рейтингами вебсторінок і за додатковими LLM-оцінками.

**Деталі:**
- 190 млн веб-документів, ~69 721 запит агента
- 10 мов (англійська — 65.8%, далі іспанська, російська, німецька, французька, португальська, італійська, корейська, японська, китайська)
- 13 оцінених ретріверів (лексичні, dense, late-interaction)
- Лідерборд розміщено на Hugging Face, приймаються публічні заявки на оцінку моделей
