---
company: NVIDIA
title: "How to Evaluate AI Agents From Tool Calls to Task Completion"
url: https://developer.nvidia.com/blog/how-to-evaluate-ai-agents-from-tool-calls-to-task-completion/
published: 2026-09-21
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-22
---

NVIDIA lays out a two-layer AI-agent evaluation framework (step-level tool-call scoring plus end-to-end outcome scoring across a Benchmark→Trial→Task→Turn→Step hierarchy) emphasizing paired accuracy/consistency reporting over 3–5 trials rather than single-point success rates; illustrated with Nemotron 3.5 Lightning reaching 86% accuracy on PinchBench, 30% faster than Qwen3.6 35B at comparable accuracy.

## card

**Що сталося:** NVIDIA публікує фреймворк оцінювання AI-агентів із двома рівнями: поопераційна (process) перевірка окремих викликів інструментів на релевантність і корисність, та наскрізна (outcome) перевірка відповідності кінцевого стану середовища меті задачі.

**Контекст:** Ієрархія оцінювання — Benchmark → Trial → Task → Turn → Step, з метриками за трьома осями (точність, багатослівність, вартість); автори наголошують, що "рівень успіху без міри узгодженості — це точкова оцінка стохастичної системи", тож рекомендують парну звітність (task success rate + діапазон узгодженості на 3–5 прогонах, точність tool-call + точність аргументів, кроки на успіх + вартість на успіх).

**Деталі:**
- Порівнюваність бенчмарків залежить від складності задачі, статefulності середовища та методології (перевага виконуваній верифікації над LLM-as-judge)
- Приклад: Nemotron 3.5 Lightning — 86% точності на PinchBench, на 30% швидше за Qwen3.6 35B за порівнянної точності
- Документація відтворюваності на GitHub, ваги моделі на Hugging Face, розгортання через NVIDIA NIM, пробний доступ на build.nvidia.com
