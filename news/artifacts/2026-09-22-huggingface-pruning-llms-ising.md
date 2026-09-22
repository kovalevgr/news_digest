---
company: Hugging Face
title: "Pruning LLMs Like a Physicist: Block Removal as an Ising Optimization Problem"
url: https://huggingface.co/blog/MultiverseComputingCAI/pruning-llms-like-a-physicist-block-removal-as-an
published: 2026-09-21
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-22
---

Multiverse Computing reframes transformer depth-pruning (block removal) as a constrained binary optimization problem mapped onto an Ising spin-glass model, using a Hessian from a single calibration pass to capture pairwise block dependencies that mean-field/independent-ranking methods miss; on Llama-3.3-70B-Instruct at 50% depth compression, their CBO method scores 76.9 MMLU versus 54.0 for a block-influence baseline (~23pp gain), tested also on Llama-3.1-8B-Instruct, Qwen3-14B, and NVIDIA-Nemotron-3-Nano-30B.

## card

**Що сталося:** Multiverse Computing публікує метод обрізання блоків трансформера (depth pruning), переформульований як задача бінарної оптимізації з обмеженнями, відображена на модель спінового скла Ізінга — фізичну систему з взаємодіями "усі з усіма" між блоками.

**Контекст:** На відміну від методів, що ранжують блоки незалежно (mean-field), підхід обчислює матрицю Гессе (діагональ — важливість окремого блоку, недіагональні елементи — парні взаємозв'язки між блоками) за один калібрувальний прохід, після чого підбір конфігурації зведений до пошуку станів мінімальної енергії; перевірено на Llama-3.1-8B-Instruct, Qwen3-14B, Llama-3.3-70B-Instruct та гібридній NVIDIA-Nemotron-3-Nano-30B (Mamba2 + attention + MoE).

**Деталі:**
- Llama-3.3-70B-Instruct, видалено 40 із 80 блоків (50% компресія по глибині): CBO — 76.9 MMLU проти 54.0 у бейзлайну block-influence (приріст ≈23 п.п.)
- Qwen3-14B, видалено 12 із 40 блоків: CBO випереджає бейзлайн приблизно на 10 пунктів MMLU
- Обчислення матриці Гессе потребує лише одного калібрувального проходу — це дозволяє перебирати мільярди конфігурацій на одній GPU
- Збуджені (не лише основні) стани спінової системи часто дають кращі результати після донавчання
