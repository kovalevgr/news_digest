---
company: openai
title: "Perplexity and Intelligence"
url: https://openai.com/index/perplexity-and-intelligence/
date: 2026-11-22
found_via: gap-scrape (WebFetch — openai.com/news listing)
---

OpenAI Chief Scientist Jakub Pachocki argues perplexity (cross-entropy loss) should become a shared metric across labs for tracking capability and grounding safety pacing agreements, and publishes OpenAI's own internal perplexity curve from GPT-3.5 onward.

## card

**Що сталося:** Головний науковець OpenAI Якуб Пахоцький пропонує зробити perplexity (cross-entropy loss) спільною метрикою індустрії для порівняння прогресу лабораторій і прив'язки до неї узгоджених "лімітів" розробки — межі, яку розробники домовляються не перетинати, поки не буде досягнуто конкретної віхи моніторингу (наприклад, наступника chain-of-thought-моніторів).

**Контекст:** Пост публікує внутрішню криву log-perplexity OpenAI на кодовому датасеті, починаючи з GPT-3.5, і прив'язує історичні зрушення здібностей (chain-of-thought reasoning, кібербезпека, математика) до конкретних значень цієї метрики; посилається на есе Даріо Амодея "We must pace the frontier" як мотивацію для спільного темпу розробки.

**Деталі:**
- Log-perplexity: GPT-3.5 ≈ 0.99, GPT-4 ≈ 0.91, останні моделі < 0.8.
- Трансформативні можливості з кібербезпеки та математики з'явилися нижче позначки 0.8; модель на рівні ≈0.76 почала давати результати на відкритих математичних задачах.
- Автор очікує нових трансформативних можливостей у діапазоні ≈0.68–0.7, можливо вже з 2027 року.
- Обмеження: лабораторії використовують різні дані, perplexity не напряму відображає реальні задачі й не враховує пост-тренувальні техніки (напр. CoT reasoning).
