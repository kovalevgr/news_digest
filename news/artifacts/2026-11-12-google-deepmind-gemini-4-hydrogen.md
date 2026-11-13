---
company: google-deepmind
title: "Introducing Gemini 4 Hydrogen"
url: https://deepmind.google/blog/introducing-gemini-4-hydrogen/
date: 2026-11-12
found_via: rss (confirmed; the TIER-1 feed's own TRAP/not-a-feed flag this run was a false positive again — raw curl confirmed valid application/xml with this item at the top, pubDate 2026-11-12T18:00:50Z; full content read via anonymous Jina since the DeepMind page 302-redirects to blog.google, which this session's network does not allow)
---

Google DeepMind introduces Gemini 4 Hydrogen, a fast/efficient member of the Gemini 4 family built for everyday coding and agentic workflows (vs. Carbon/Argon's deep long-horizon reasoning), rolling out today across AI Studio, the Gemini API, Gemini for business, the Gemini app, Google Search, and Antigravity. It surpasses Argon on the Artificial Analysis Intelligence Index at default thinking (51 vs. 50) and is priced flat at $1.50/$7.50 per million input/output tokens across its 1M-token context window.

## card

**Що сталося:** Google DeepMind представив Gemini 4 Hydrogen — швидку та ефективну модель лінійки Gemini 4, орієнтовану на повсякденний код і агентні робочі процеси (на відміну від Carbon/Argon, які фокусуються на глибокому довгостроковому міркуванні). Модель доступна вже сьогодні в AI Studio, Gemini API, Gemini for business, застосунку Gemini, Google Search та Antigravity.

**Контекст:** Третя модель лінійки Gemini 4 після Carbon і Argon; замінює Gemini 3.8 Flash як стандарт для масових/економних навантажень. Разом з Hydrogen представлено Orchestrator в Google Antigravity — механізм, що динамічно перемикається між Carbon і Hydrogen в межах однієї сесії.

**Деталі:**
- Artificial Analysis Intelligence Index: 51 (high thinking) / 54 (xhigh) проти 50 в Argon.
- Ціна: $1.50 за млн вхідних токенів / $7.50 за млн вихідних, фіксовано по всьому контексту 1M токенів.
- Terminal-Bench 4.1 проти Gemini 3.8 Flash: 57% проти 18.2%; завдання виконуються у 2.5x швидше; вигадані твердження (fabrications) скорочені більш ніж у 5x.
- Orchestrator (Carbon+Hydrogen) на Terminal-Bench 4.0: майже рівень успішності Carbon при −24% витраченої квоти і −19% часу.
- Безпека агентних дій проти 3.8 Flash: overreach −81%, under-service −79%, misaligned actions −12x; стійкість до indirect prompt injection (Gray Swan IPI) — у 2.3x вища; chain-of-thought legibility 99.9% без deceptive edits на 200k+ перевірених turns.
- Чотири рівні "thinking": low/medium/high(default)/xhigh.
