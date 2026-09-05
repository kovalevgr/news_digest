---
company: NVIDIA
title: "Building a Memory-Driven Agent with NVIDIA NemoClaw"
url: https://developer.nvidia.com/blog/building-a-memory-driven-agent-with-nvidia-nemoclaw/
published: 2026-09-04
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-05
---

NVIDIA details a memory-driven "Chief of Staff" agent built on NemoClaw, separating evidence/knowledge/governed-execution layers with a Markdown self-model and SQLite audit ledger; against an agentic-RAG baseline it lifted overall accuracy 82.8%→90.9% and changed-facts tracking 60.0%→100%.

## card

**Що сталося:** NVIDIA описала побудову агента-«керівника апарату» на базі NemoClaw з постійною пам'яттю про людей, проєкти та пріоритети, використовуючи трирівневу архітектуру: докази → знання → підконтрольне виконання.

**Контекст:** Порівняння з базовим агентним RAG-підходом на тих самих enterprise-сценаріях; частина серії NVIDIA про агентні системи з пам'яттю.

**Деталі:**
- "Self model" зберігає структуровані знання у Markdown-сторінках; SQLite-журнал фіксує зобов'язання, пріоритети, виправлення та аудит-події
- Intent gating: пріоритет заявленим користувачем цілям над сприйнятою терміновістю
- Пісочниця виконання через NVIDIA OpenShell (файлова система, процеси, мережа)
- Загальна точність: 82.8% → 90.9%; відстеження змінених фактів: 60.0% → 100% (+40 п.п.); складні питання: 67.7% → 87.1%
