---
company: Hugging Face
title: "Getting the Source Right, Not Just the Fact: Source-Aware Verification for MCP Agents"
url: https://huggingface.co/blog/MultiverseComputingCAI/getting-the-source-right-not-just-the-fact-source
source_url: https://huggingface.co/blog/feed.xml
published: 2026-09-29
fetched: 2026-09-30
---

Multiverse Computing introduces ProvenanceGuard, a verification technique for multi-tool LLM agents that checks whether each claim is attributed to the correct source tool, not merely supported somewhere in the evidence pool.

## card

**Що сталося:** Multiverse Computing представила ProvenanceGuard — техніку верифікації для multi-tool LLM-агентів, що розкладає відповідь на окремі твердження, визначає, який виклик інструменту підтверджує кожне з них, і перевіряє правильність атрибуції джерела (а не лише наявність підтвердження десь у пулі доказів).

**Контекст:** Розроблена для MCP-агентів; тестувалась на трасах медичного агента.

**Деталі:**
- 0.802 F1 у блокуванні непідтверджених тверджень
- Дає per-claim вердикти джерела
- Перевершує "сліпу до джерела" верифікацію
