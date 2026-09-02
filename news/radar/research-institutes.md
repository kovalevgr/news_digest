---
category: research-institutes
updated: 2026-08-27
---

# Radar: research-institutes

Technical-radar items for this category (sources in [`config/radar.json`](../config/radar.json)).
Appended by the daily routine under weekly headings; format matches topics files.

## 2026-W34

- **2026-08-18** — [When a model reads a drug's class from its name—not its knowledge](https://allenai.org/blog/olmo-drug-morphology) — Ai2 used Olmo 3 and its open training data to show models can infer a drug's class from surface-level name morphology instead of actual pharmacological knowledge, and traced the shortcut to how often each drug appeared in training — an open-data interpretability finding, not just a black-box observation.
- **2026-08-21** — [How a Georgia Tech team used the open Olmo stack to trace social reasoning](https://allenai.org/blog/olmo-capability-tracing) — Verified via WebFetch: using influence functions across five open Olmo-ecosystem components (Olmo 3, Dolma 3's 1.26B documents, WebOrganizer categorization, OlmoEval, OLMES scoring), the team sampled 5.68M documents across 576 categories to trace which training data shaped social reasoning vs. STEM/general knowledge on SocialIQA, ARC-Challenge and MMLU. Finding: most social-science knowledge behaves like STEM knowledge except SocialIQA, which draws heavily on narrative/interpersonal categories (literature, social life, customer support, Q&A threads); confirmed causally by having Olmo 3 "unlearn" the most-influential literature documents, which measurably hurt social-reasoning performance. Code and results public (GitHub, HF Spaces).

## 2026-W35

- **2026-08-26** — [How researchers adapted Dolma for better Thai language models](https://allenai.org/blog/thai-llm-dolma) — Verified via WebFetch: the Mangosteen project modified Ai2's open Dolma data-curation pipeline for Thai — Thai lacks clear sentence boundaries, so sentence/paragraph-level dedup "removed almost all" the data; the team kept document/URL-level dedup and added Thai-specific quality filters and web-pattern rules instead. Result: a 47-billion-token Thai pretraining corpus (eliminating >80% of Common Crawl and ~50% of FineWeb2 input) that matched or improved model performance, with stronger results on Thai cultural-knowledge evals — evidence that Dolma's open toolkit lets communities build their own locally-curated corpora rather than relying on generic multilingual scraping.

## 2026-W36

- **2026-09-01** — ⭐ [BenchMIRT: What are LLM benchmarks actually measuring?](https://allenai.org/blog/benchmirt) — Verified via WebFetch: extends multidimensional Item Response Theory (MIRT) from psychometrics to audit benchmarks question-by-question, run across 100 LLMs on 16 benchmarks (34,000+ questions). Without being told what each benchmark measures, it independently recovered two dominant dimensions (safety, general reasoning) and found real misalignments: BBQ (bias testing) tracks general reasoning more than safety; WMDP (dual-use knowledge) correlates -0.89 with reasoning, meaning it measures absence of knowledge rather than safety behavior; HarmBench's copyright questions show weaker safety alignment than its other harm categories. Using just 10% of questions preserved nearly the same capability picture, and held-out-question prediction hit 79% accuracy vs. 70% for baseline methods.
- **2026-09-01** — [The hard parts of AI-assisted science](https://allenai.org/blog/swedish-autodiscovery-recap) — Verified via WebFetch: recap of an Ai2 event (with Providence Swedish) on the hardest open problems in AI-assisted science — keeping systems steerable, grounded in human judgment and sound methods, and responsive to new evidence; discussion/framing piece, no new method or numbers.
