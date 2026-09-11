---
company: Google Research
title: "ToolGrad: Efficient tool-use dataset generation with textual \"gradients\""
url: https://research.google/blog/toolgrad-efficient-tool-use-dataset-generation-with-textual-gradients/
published: 2026-09-10
source_url: https://research.google/blog/rss/
fetched: 2026-09-11
---

Google Research introduces ToolGrad, an "answer-first" framework that generates tool-use training data by first constructing valid API-call workflows and then generating matching user queries; models fine-tuned on ToolGrad data (e.g. Gemma-3-12B at 83.1) match or exceed proprietary models like Gemini 2.5-pro on tool-use benchmarks.

## card

**Що сталося:** Google Research представляє ToolGrad — фреймворк для генерації датасетів з використання інструментів (tool-use), що інвертує звичний підхід: спочатку будує робочий ланцюжок викликів API, а вже потім генерує відповідний запит користувача.

**Контекст:** Відповідає на проблему традиційних методів генерації tool-use даних (спочатку запит, потім пошук розв'язку), які дають нижчий відсоток успішних траєкторій; ToolGrad названо "answer-first paradigm".

**Деталі:**
- Майже 100% успішних (valid) згенерованих траєкторій проти нижчих показників попередніх методів
- Моделі, дотюнені на даних ToolGrad, зрівнюються або перевершують проприєтарні моделі рівня Gemini 2.5-pro
- Gemma-3-12B, дотюнена на ToolGrad-даних, показує 83.1 на бенчмарку tool-use
