---
company: Hugging Face
title: "TutorMoments: Do AI tutors know when to help and when to hold back?"
url: https://huggingface.co/blog/allenai/tutormoments
published: 2026-08-07
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-08
---

Allen Institute for AI publishes TutorMoments, an evaluation framework that measures
whether large language models can appropriately balance providing instructional support
versus encouraging students to think independently during math tutoring sessions.

## card

**Що сталося:** Allen Institute for AI (Ai2) опублікував TutorMoments — фреймворк оцінки того, чи вміють LLM-тьютори балансувати між наданням допомоги учневі та заохоченням до самостійного мислення, тобто розуміти, коли втрутитися, а коли стриматися, під час математичного тьюторингу.

**Контекст:** Дослідницька публікація Ai2 у блозі Hugging Face, створена за підтримки Gates Foundation і Learning Commons; реліз відкритий (датасет, код, техзвіт).

**Деталі:**
- Датасет TutorMoments-Preview: 462 деідентифіковані транскрипти математичного тьюторингу учнів 2–7 класів шкіл Title I у США
- Понад 1500 анотованих педагогічних "моментів"; анотації від 27 досвідчених учителів математики
- Вимірює три поведінки в точках педагогічних рішень: scaffolding (спрощення задачі), push for rigor (заохочення глибшого мислення), over-scaffolding (надмірна допомога)
- Ключовий висновок: моделі за замовчуванням над-допомагають; "evaluation-aware" промпти про trade-off scaffolding vs rigor значно покращують результат — для всіх семи оцінених моделей
- Навіть із покращеними промптами моделі суттєво різняться за надійністю та використовують менше стратегій, ніж люди-тьютори; детекція push-for-rigor лишається менш надійною за scaffolding
- Техзвіт, датасет і код опубліковані на Hugging Face та GitHub
