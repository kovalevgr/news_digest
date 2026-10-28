---
company: google-research
title: "The Sleep framework: A new way for LLMs to retain knowledge in continual learning"
url: https://research.google/blog/the-sleep-framework-a-new-way-for-llms-to-retain-knowledge-in-continual-learning
date: 2026-10-27
found_via: rss (TIER-1)
---

Google Research introduces Sleep, a continual-learning framework that alternates "wake" interaction with offline "sleep" consolidation into new MoE low-rank experts, reporting near-zero forgetting on continual-translation and strong results on BABILong, SQuAD/CPT, and math-reasoning benchmarks versus SFT/GRPO/SEAL baselines.

## card

**Що сталося:** Google Research представляє фреймворк Sleep для безперервного навчання LLM: модель чергує активну взаємодію ("wake") з офлайн-консолідацією ("sleep"), під час якої нові знання записуються в low-rank експерти MoE-архітектури (на основі Hope) без перезапису старих параметрів.

**Контекст:** Фреймворк вирішує класичну проблему безперервного навчання — catastrophic forgetting при донавчанні та обмеженість in-context learning вікном контексту; порівнюється з Cartridges, SEAL, SFT, GRPO та OPSD, а також з архітектурою довгострокової пам'яті Titans.

**Деталі:**
- Переклад невідомих мов (маньчжурська, каламанг): майже нульова втрата якості проти значного забування у in-context learning, Cartridges та SFT.
- BABILong (довгий контекст): майже ідеальне масштабування до 10M токенів, краще за GPT-4 та Titans.
- Фактичні знання (SQuAD/CPT): 48.9% (single-task) і 46.2% (CPT) — попереду базової моделі, SFT та SEAL.
- Математика: 79.2% AIME 24, 69.0% AIME 25, 46.1% HMMT 25 — попереду SFT, GRPO та OPSD.
- Показники авторські, незалежної перевірки немає.
