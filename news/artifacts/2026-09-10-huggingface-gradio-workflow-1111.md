---
company: Hugging Face
title: "Rebuilding AUTOMATIC1111 with Gradio Workflow"
url: https://huggingface.co/blog/gradio-workflow-1111
published: 2026-09-10
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-11
---

Hugging Face releases Workflow1111, a Gradio-based reconstruction of AUTOMATIC1111's stable-diffusion-webui with 73 nodes across 11 media pipelines (text-to-image, editing, upscaling, object detection, video generation), exposed as a browser-based node canvas that becomes a REST endpoint with no hand-written routes.

## card

**Що сталося:** Hugging Face випускає Workflow1111 — переосмислення AUTOMATIC1111 (stable-diffusion-webui) на базі Gradio, з 73 вузлами для 11 медіа-пайплайнів.

**Контекст:** Продовжує серію Gradio-орієнтованих релізів Hugging Face для конструювання AI-пайплайнів через візуальний інтерфейс без написання коду вручну.

**Деталі:**
- 73 вузли (nodes), що покривають 11 медіа-пайплайнів: text-to-image, редагування зображень, апскейлінг, детекція об'єктів, генерація відео та інші
- Єдине робоче полотно (canvas) у браузері, яке автоматично стає REST-ендпоінтом без ручного написання маршрутів
- Побудований поверх Gradio
