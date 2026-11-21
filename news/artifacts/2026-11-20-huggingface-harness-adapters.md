---
company: huggingface
title: "Introducing harness adapters: adapt your favorite model to your harness to improve performance and cost"
url: https://huggingface.co/blog/harness-adapters-at-scale
date: 2026-11-20
found_via: gap-scrape (WebFetch — huggingface.co/blog/feed.xml returned zero fresh in-window entries this run)
---

Hugging Face introduces "harness adapters" — LoRA adapters RL-trained inside a specific agent harness (Qwen3.8-27B base, frozen weights) — raising Terminal-Bench 2.1 pass@1 from ~39% to 55% with Pi while cutting average tokens per task from ~2.9K to ~1.5K.

## card

**Що сталося:** Hugging Face представляє "harness adapters" — LoRA-адаптери, натреновані через reinforcement learning безпосередньо всередині конкретного агентного харнесу, аргументуючи, що модель загального призначення залишає продуктивність і ефективність невикористаними для конкретного харнесу й набору задач.

**Контекст:** Базова модель — Qwen3.8-27B із замороженими вагами, по одному LoRA-адаптеру на харнес (Pi 1.5.2, OpenCode 2.2.7, Hermes Agent v0.22.6). Тренування — TRL's AsyncGRPOTrainer (GRPO), rollout виконуються у реальному харнесі через Harbor і OpenEnv; 871 агентна задача з 35 репозиторіїв (SWE-smith, SWE-Gym через TaskTrove, Tasksmith), 598 кумулятивних кроків, кожен адаптер — на 2×B200.

**Деталі:**
- Головний результат: Terminal-Bench 2.1 з Pi — pass@1 зростає з ~39% до ~55%, середня кількість токенів на задачу падає з ~2.9K до ~1.5K.
- "Супер-адаптер" (три LoRA об'єднані конкатенацією, ранг 96, масштаб ½): середній pass@1 по шести парах харнес-бенчмарк зростає з 39.5% до 49.0% (без "thinking").
- Застереження: частина приросту без "thinking" пояснюється короткими текстовими міркуваннями перед викликами інструментів ("reasoning leakage"); на позабенчмарковому AutomationBench результати переважно в межах шуму, адаптер Hermes на 5.3 п.п. гірший за базову модель.
- Доступні на Hugging Face Hub: адаптери, GGUF-збірки, датасет RL-задач, плагін safeagents (колекція "Qwen3.8-27B Harness adapters"); траєкторії — у відкритому бакеті; повний рецепт опубліковано для відтворення.
