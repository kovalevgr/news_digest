---
company: Hugging Face
title: "Safety for Whom? Refusing the Right Subset of a Topic, Not the Whole Topic"
url: https://huggingface.co/blog/MultiverseComputingCAI/safety-for-whom
published: 2026-09-08
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-09
---

Multiverse Computing proposes "boundary-aware self-distillation": training refusal on paired prompts that differ only in intent, so a model refuses only the harmful subset of a topic instead of the whole topic. On Qwen3-8B (political persuasion testbed), political refusal rose from 9.47% to 84.75% and harmful-response rate fell from 26.26% to 0.14%, while boundary-pair training kept over-refusal on safe prompts at 4.16% instead of 74%.

## card

**Що сталося:** Multiverse Computing опублікувала дослідження "Safety for Whom?" — метод "boundary-aware self-distillation" для навчання LLM відмовляти лише на шкідливій підмножині запитів у межах теми, а не на всій темі загалом, використовуючи парні промпти, що відрізняються лише наміром.

**Контекст:** Традиційний підхід до безпеки трактує шкоду як властивість теми загалом (наприклад, відмова на весь політичний контент), що на практиці означає надмірні відмови на легітимні запитання в тій самій темі. Автори прямо показують: сама лише частка відмов маскує небезпечний компроміс між безпекою та корисністю моделі.

**Деталі:**
- Тестовий стенд: Qwen3-8B, тема — політичне переконання (political persuasion)
- Відмова на шкідливі політичні запити зросла з 9.47% до 84.75%
- Частка шкідливих відповідей за бенчмарками впала з 26.26% до 0.14%
- Без парних граничних прикладів надмірні відмови на безпечні запити сягали 74%; з ними — впали до 4.16% при збереженні 87.72% відмов на шкідливі запити
- Технічні компоненти: відновлення покриття (escalating retry повернув 99.8% невдалих тренувальних прикладів замість відкидання 20%), додавання 11,955 "на вигляд небезпечних, але безпечних" прикладів у тренувальні дані, оцінка за парами меж (boundary pairs)
