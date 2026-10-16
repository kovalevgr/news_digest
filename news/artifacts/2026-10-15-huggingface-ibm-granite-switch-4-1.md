---
company: Hugging Face
title: "Granite Switch 4.1: Chat, Decisions, and Speech from One Endpoint"
url: https://huggingface.co/blog/ibm-granite/granite-switch-4-1
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-15
fetched: 2026-10-16
---

IBM releases Granite Switch 4.1 (8B and 30B), bundling a general-purpose Decision aLoRA, a Guardian safety aLoRA, and a speech-recognition model so one hosted endpoint handles chat, decision tasks, and speech-to-text with near-zero extra VRAM.

## card

**Що сталося:** IBM випустив Granite Switch 4.1 — моделі на 8B і 30B параметрів, що об'єднують загальний Decision aLoRA, Guardian aLoRA для безпекових рішень і модель розпізнавання мови Granite-Speech-5.0-Turbo-CTC. Мета — дати одній хостинговій точці доступу обробляти чат, задачі прийняття рішень і розпізнавання мови.

**Контекст:** Продовжує проєкт Granite Switch, представлений "минулої весни", і будується на попередньому релізі Granite Libraries — наборі спеціалізованих decision/task-адаптерів, які можна комбінувати в кастомні моделі.

**Деталі:**
- Моделі: Granite-Switch-4.1-8B і -30B; базова модель + усі 3 компоненти займають приблизно стільки ж VRAM, скільки сама базова модель
- Адаптери — Activated LoRA, тож KV-кеш базової генерації можна повторно використовувати для наступних adapter-рішень
- За даними IBM: Guardian aLoRA в середньому перевершує кілька названих decision-моделей на safety-задачах; 30B-модель із 4 спеціалізованими aLoRA швидше завершує 5-кроковий RAG-воркфлоу за Jev-27B; 3B кастомна модель робить 60–100 рішень/сек у демо на Doom проти ≈10 у Jev
- Доступність: карти моделей у колекції Granite Switch на Hugging Face, Speech-to-Decisions Space, репозиторій на GitHub, Colab-ноутбук; Adapter SDK для тренування адаптерів у Mellea запланований, але ще не випущений
