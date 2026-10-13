---
company: Microsoft
title: "Simulating student learning for better AI tutoring"
url: https://www.microsoft.com/en-us/research/blog/simulating-student-learning-for-better-ai-tutoring/
source_url: https://www.microsoft.com/en-us/research/feed/
published: 2026-10-12
fetched: 2026-10-13
---

Microsoft Research introduces StudentSim, a system that builds personalized AI simulators of individual students (trained on de-identified learner records) to test AI tutors before they reach real learners, evaluated across chess, second-language writing, and mathematics.

## card

**Що сталося:** Microsoft Research представляє StudentSim — систему персоналізованих AI-симуляторів окремих учнів для тестування AI-репетиторів до їх використання реальними учнями; кожен симулятор тренується на деідентифікованих записах учня (спільне тренування в межах домену + спеціалізація на даних конкретного учня).

**Контекст:** Дослідники оцінюють симулятори через StudentSimEval — метрику поведінкової точності (відповідність записаним відповідям учня) та чутливості до підказок (чи змінює симулятор відповідь після підказки репетитора); протестовано на трьох доменах: шахи, письмо англійською як другою мовою, математика.

**Деталі:**
- У шахах StudentSim: 0.5150 поведінкової точності / 0.9067 чутливості до підказок — проти GPT-5.4 (0.2316 / 0.7186) і шахової моделі Maia2 (0.4535 / 0.2721)
- У дослідженні з RL-тренуванням шахового репетитора: репетитор, винагороджений StudentSim, досяг 90.5% точності проти 75.7% без RL і 71.6% для репетитора, винагородженого GPT-5.4
- Люди-експерти з шахів також оцінили цього репетитора вище за якість підказок і персоналізацію
- Автори наголошують: потрібні дослідження з реальними людьми щодо навчальних результатів, безпеки та придатності для класу; статтю й код опубліковано відкрито
