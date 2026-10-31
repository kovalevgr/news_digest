---
company: nvidia
title: "Build Specialized Agents on a Stack You Control with NVIDIA NemoClaw"
url: https://developer.nvidia.com/blog/build-specialized-agents-on-a-stack-you-control-with-nvidia-nemoclaw/
date: 2026-10-30
found_via: rss (TIER-1)
---

NVIDIA introduces NemoClaw, a set of open blueprints combining an existing agent harness (OpenClaw, Hermes Agent, or LangChain Deep Agents) with Nemotron open models, NeMo optimization/observability tooling, and OpenShell, a secure runtime governing agent access to files, networks, credentials, and tools.

## card

**Що сталося:** NVIDIA представляє NemoClaw — набір відкритих blueprint'ів, які збирають повний agent-стек навколо вже знайомого харнесу (OpenClaw, Hermes Agent або LangChain Deep Agents), відкритих моделей Nemotron, інструментів NeMo (оптимізація, спостережність) та OpenShell — захищеного runtime, що контролює доступ агента до файлів, мережі, credentials та інструментів.

**Контекст:** NemoClaw подається як не-конкуруючий харнес і не-runtime, а шар, що поєднує tuning моделі/харнесу з runtime-контролем безпеки; один з blueprint'ів — тюнінг LangChain Deep Agents під Nemotron 3 Ultra без перенавчання моделі.

**Деталі:**
- LangChain налаштував свій харнес під Nemotron 3 Ultra (зміна промптів/інструментів/middleware, без перенавчання) — заявлена near-frontier якість за ~10x нижчою вартістю запуску проти провідних закритих моделей.
- Community-рецепт на базі Hermes ("Chief of Staff") використовує персистентну пам'ять у людино-читабельному форматі; OpenShell контролює доступ до файлів/процесів/мережі та тримає облікові дані поза sandbox.
- NemoClaw-агенти можуть працювати в хмарі, дата-центрах, на NVIDIA DGX Spark і RTX PC/workstation, а також поруч із фронтир-агентами (Claude, Codex, Cursor).
- Доступність: тюнений профіль Nemotron 3 Ultra — через LangChain на GitHub (langchain-ai/deepagents); NemoClaw quickstart, GitHub-репозиторій з прикладами та DLI-курс "Deploy Secure Agents with NemoClaw".
