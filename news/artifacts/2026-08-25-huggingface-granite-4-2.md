---
company: Hugging Face
title: "Granite 4.2 LLMs: How They're Built"
url: https://huggingface.co/blog/ibm-granite/granite-4-2
published: 2026-08-25
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-26
---

IBM releases Granite 4.2, its first family of dense decoder-only reasoning LLMs (3B/8B/30B) with a thinking/non-thinking toggle, agentic RL training, and native OpenAI-compatible tool calling, under Apache 2.0.

## card

**Що сталося:** IBM випустила Granite 4.2 — першу серію щільних (dense) decoder-only reasoning-моделей (3B, 8B, 30B параметрів) із перемикачем режимів "думати / не думати" та вбудованим agentic-тренуванням.

**Контекст:** Продовження лінійки Granite від IBM з фокусом на мультимовність, код і агентні сценарії; 8B і 30B моделі пройшли RL у реальних пісочницях (виклик інструментів, редагування коду, термінал, веб-пошук).

**Деталі:**
- Розміри: 3B, 8B, 30B параметрів; ліцензія Apache 2.0
- Архітектура: Grouped Query Attention (40 голів уваги), Rotary Position Embeddings, SwiGLU
- Претрейн на ~15 трильйонах токенів у 5 фаз, контекст розширено до 512K токенів
- ~7.2 млн SFT-прикладів (~100 млрд токенів); багатоетапне RL через GRPO (базове RL, skill boosters, agentic RL, RLHF-вирівнювання)
- Нативний tool calling у форматі, сумісному з OpenAI, для інтеграції з існуючими агентними фреймворками
- Бенчмарки: AIME25 — 78%/87%/89% (3B/8B/30B); SWE-Bench Verified — 48%/57% (8B/30B); MMLU-Pro — 68%/74%/78% (3B/8B/30B)
