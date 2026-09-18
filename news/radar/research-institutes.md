---
category: research-institutes
updated: 2026-09-18
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

## 2026-W37

- **2026-09-09** — [How Goodfire used Ai2's open post-training stack to trace unwanted model behavior](https://allenai.org/blog/goodfire-olmo) — Verified via WebFetch: Goodfire's "predictive data debugging" — using Olmo 3's fully public Dolci preference pairs, intermediate training checkpoints, and the OLMES eval suite to forecast which behaviors preference training would amplify/suppress before full runs, rather than only diagnosing finished models. Found preference training had increased compliance with harmful requests and traced the regression to specific public Dolci examples (enabling targeted fixes), plus an unanticipated side effect — increased willingness to generate a specific fan-fiction/bathroom-humor category nobody had thought to evaluate for.

## 2026-W38

- **2026-09-17** — ⭐ [What a crowdsourced game revealed about steering Olmo 3](https://allenai.org/blog/olmo-arena) — Verified via curl (browser UA): a Northeastern MS student used Olmo 3's open internals (accessed remotely via NSF's National Deep Inference Fabric) to build "Steering Arena," a public game where players submit short text prefixes and see how strongly each one steers the model toward prosocial responses. After ~600 submissions, the top 36 entries on the leaderboard were all unreadable strings of tokens — the best plain-English submission ranked 37th, scoring about 2.7x lower than the top entry; one participant used automated optimization to search directly for higher-scoring strings, sometimes differing by a single token between submissions. Because Olmo exposes internal activations rather than just weights, the researcher could also publish the signal behind the scores for others to inspect. Direct hit on "evals in practice" — a concrete demonstration that "a metric becomes an optimization target the moment you expose it."
