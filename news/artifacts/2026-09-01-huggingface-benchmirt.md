---
company: Hugging Face
title: "BenchMIRT: What are LLM benchmarks actually measuring?"
url: https://huggingface.co/blog/allenai/benchmirt
published: 2026-09-01
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-02
---

Allen Institute for AI applied multidimensional Item Response Theory (BenchMIRT) to 100 LLMs across 16 benchmarks (34,000+ questions), finding several benchmarks measure different underlying dimensions than their labels suggest.

## card

**Що сталося:** Allen Institute for AI застосував метод BenchMIRT (багатовимірну Item Response Theory) до 100 LLM на 16 бенчмарках (34 000+ питань), щоб виявити, які реальні здібності вимірює кожне окреме питання.

**Контекст:** Метод оцінює здібності моделі та складність/дискримінативність питань без попереднього маркування того, яку здатність вимірює бенчмарк — і показує розбіжності з офіційними ярликами бенчмарків (напр. WMDP насправді корелює з reasoning, а не безпекою).

**Деталі:**
- Проаналізовано 100 LLM на 16 бенчмарках: 6 reasoning-орієнтованих (MMLU-Pro, GPQA) та 10 з safety-набору Olmo 3
- BBQ виявився ближче до general reasoning, ніж до safety; питання HarmBench про копірайт вимірюють reasoning, а не safety
- Лише 10% питань бенчмарку зазвичай зберігають той самий рейтинг моделей; 50% питань часто точніші за повний бенчмарк
- BenchMIRT правильно передбачає результат на прихованих питаннях у 79% випадків проти 70% для базового підходу
