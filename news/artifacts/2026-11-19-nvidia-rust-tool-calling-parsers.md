---
company: nvidia
title: "Build Tool-Calling Parsers in Rust with AI Agents"
url: https://developer.nvidia.com/blog/build-tool-calling-parsers-in-rust-with-ai-agents/
date: 2026-11-19
found_via: rss (developer.nvidia.com/blog/feed)
---

NVIDIA open-sources reusable Rust tool-call parsers (frontend-crates, behind Dynamo's parsers) plus a shared cross-model-family conformance test corpus, built with an AI-agent workflow that drafts tests and implementation for human review.

## card

**Що сталося:** NVIDIA відкрила вихідний код frontend-crates — набору Rust-парсерів для розбору потокового виводу LLM (reasoning, текст, tool calls) на основні компоненти, що лежать в основі парсерів tool-calling у NVIDIA Dynamo.

**Контекст:** Проблема: вивід LLM може надходити частинами, обриватися посередині аргументу або "протікати" специфічною для моделі розміткою у видиму відповідь; парсер має розділяти ці потоки без втрати даних чи дублювання викликів.

**Деталі:**
- Спільний "Conformance Corpus" — мовно-нейтральні YAML-фікстури з парами вхід/очікуваний "GOLDEN" вихід, що повторно використовуються для різних сімей моделей (Beam, GPT-OSS, Muse Spark, NVIDIA Nemotron 3).
- Робочий процес: AI-агент готує набір GOLDEN-тестів (людина перевіряє), потім реалізує парсер, прогонає тести й формує звіт про відповідність.
- Протестовано на Rust 1.96.1 та dynamo-parsers-v2 0.10.3; окремих даних про пропускну здатність чи затримку в пості немає.
- Доступно на GitHub (ai-dynamo/frontend-crates) та як crate dynamo-parsers-v2 на crates.io; парсери використовуються і в самій NVIDIA Dynamo.
