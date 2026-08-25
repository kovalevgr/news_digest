---
company: Hugging Face
title: "Wire It, Run It, Deploy It: AI Workflows in Gradio"
url: https://huggingface.co/blog/gradio-workflow-guide
published: 2026-08-25
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-25
---

Hugging Face announces gr.Workflow, a new Gradio feature turning multi-step AI pipelines into a visual, drag-and-drop interface with automatic REST-endpoint generation and one-command deployment to Spaces.

## card

**Що сталося:** Hugging Face випустила `gr.Workflow` — нову можливість Gradio, що перетворює багатокрокові AI-пайплайни на візуальний drag-and-drop інтерфейс, де кожен вузол — це крок обробки.

**Контекст:** Розширення екосистеми Gradio (частина Hugging Face) для побудови складніших агентних/мультимодальних застосунків без окремого фронтенду.

**Деталі:**
- Автоматична генерація API: кожен вихід workflow стає REST-ендпоінтом (Python або curl)
- Типи вузлів: references (вхідні дані), operators (кроки обробки), subjects (виходи)
- Підтримка GPU через інтеграцію з ZeroGPU для локального інференсу моделей
- Розгортання в Hugging Face Spaces однією командою
- Мінімальний код для старту: `gr.Workflow(bind=[your_function]).launch()`
- У пості показано 6 прикладів: редагування зображень за текстовими інструкціями, багатокрокова медіа-студія, паралельна генерація зображень, аналіз датасетів, анімація відео на локальній GPU, приклад з кількома API-ендпоінтами
