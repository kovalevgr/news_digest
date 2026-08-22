---
category: research-institutes
updated: 2026-08-22
---

# Radar: research-institutes

Technical-radar items for this category (sources in [`config/radar.json`](../config/radar.json)).
Appended by the daily routine under weekly headings; format matches topics files.

## 2026-W34

- **2026-08-18** — [When a model reads a drug's class from its name—not its knowledge](https://allenai.org/blog/olmo-drug-morphology) — Ai2 used Olmo 3 and its open training data to show models can infer a drug's class from surface-level name morphology instead of actual pharmacological knowledge, and traced the shortcut to how often each drug appeared in training — an open-data interpretability finding, not just a black-box observation.
- **2026-08-21** — [How a Georgia Tech team used the open Olmo stack to trace social reasoning](https://allenai.org/blog/olmo-capability-tracing) — Verified via WebFetch: using influence functions across five open Olmo-ecosystem components (Olmo 3, Dolma 3's 1.26B documents, WebOrganizer categorization, OlmoEval, OLMES scoring), the team sampled 5.68M documents across 576 categories to trace which training data shaped social reasoning vs. STEM/general knowledge on SocialIQA, ARC-Challenge and MMLU. Finding: most social-science knowledge behaves like STEM knowledge except SocialIQA, which draws heavily on narrative/interpersonal categories (literature, social life, customer support, Q&A threads); confirmed causally by having Olmo 3 "unlearn" the most-influential literature documents, which measurably hurt social-reasoning performance. Code and results public (GitHub, HF Spaces).
