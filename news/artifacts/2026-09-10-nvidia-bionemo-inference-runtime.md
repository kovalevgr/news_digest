---
company: NVIDIA
title: "High-Throughput Structure Prediction with BioNeMo Inference Runtime"
url: https://developer.nvidia.com/blog/high-throughput-structure-prediction-with-bionemo-inference-runtime/
published: 2026-09-10
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-11
---

NVIDIA's BioNeMo Inference Runtime (BioIR) accelerates GPU biomolecular structure prediction while keeping PyTorch compatibility; on 1,000 human dimer targets, BioIR-accelerated Boltz-2 delivers 58.5K folded residues per GPU-hour vs. 20.2K for open-source implementations — a 2.90x throughput gain and ~69% lower energy use at scale.

## card

**Що сталося:** NVIDIA представляє BioNeMo Inference Runtime (BioIR) — рантайм для прискорення передбачення структури білків на GPU, сумісний з PyTorch, орієнтований на обробку в масштабі цілого протеому.

**Контекст:** Вирішує проблему ефективної обробки великих списків задач передбачення структури (proteome-scale), де важлива пропускна здатність усього конвеєра, а не лише швидкість однієї інференс-ітерації.

**Деталі:**
- Тест на 1000 людських димерних мішенях: Boltz-2 на BioIR — 58 500 успішно згорнутих залишків на GPU-годину проти 20 200 у відкритих реалізаціях
- 2.90x приріст пропускної здатності
- Оцінка економії енергії — близько 69% при обробці мільйона порівнянних мішеней
