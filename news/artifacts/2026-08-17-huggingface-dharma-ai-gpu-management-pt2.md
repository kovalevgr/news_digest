---
company: Hugging Face
title: "Same Cluster, 33 Points More Utilization: What Changed Was the Order"
url: https://huggingface.co/blog/Dharma-AI/gpu-management-pt2
published: 2026-08-17
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-18
---

Dharma AI presents a constraint-aware GPU allocator (part 2 of a GPU-management series) that lifted cluster utilization by up to 33 percentage points over FIFO scheduling and increased priority-weighted output by an average of 52% across seven benchmark scenarios, without hardware changes.

## card

**Що сталося:** Dharma AI опублікував другу частину серії про GPU-менеджмент, представивши constraint-aware алокатор GPU, який підняв утилізацію кластера до 33 відсоткових пунктів порівняно з FIFO-плануванням і в середньому на 52% збільшив пріоритетно-зважений вихід у семи бенчмарк-сценаріях — без змін заліза.

**Контекст:** Продовження статті "GPU Management: Why Idle GPUs Are the New Grounded Aircraft" (30 липня 2026), яка стверджувала, що саме утилізація, а не інтелект моделей, стає наступним обмеженням enterprise AI; автори зазначають, що усталеної практики GPU-менеджменту в індустрії ще не існує.

**Деталі:**
- Проблема: чотири несумісні типи навантажень (тренування, real-time inference, batch inference, квантизація) конкурують за GPU; FIFO марнує потужність через резервування під пік і погане впорядкування
- Результати бенчмарків: тренувальний сценарій — утилізація з 53.6% до 87.0% (+105.1% цінності); змішаний контроль — з 51.6% до 72.4% (+54.8% цінності); тест масштабу (64 GPU, 30 завдань) — та сама утилізація, але +15.9% пріоритетно-зваженої цінності
- Затримка обробки: 1–15 мс
- Підхід: real-time попит трактується як крива, а не пікове резервування; batch-завдання розміщуються за пріоритетом на весь плановий горизонт; діють 5 обмежень (один GPU на завдання за таймстеп, дотримання попиту, суцільні блоки GPU для batch, ліміти свопів для real-time, без preemption активної роботи)
- Прогнозування попиту: власні естіматори для кожного типу навантаження (22 ознаки для варіантів тренування, специфічна для алгоритму обробка квантизації, тижневі профілі real-time)
