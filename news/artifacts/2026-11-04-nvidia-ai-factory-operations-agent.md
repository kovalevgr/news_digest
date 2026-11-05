---
company: nvidia
title: "How NVIDIA Uses AI Agents to Streamline AI Factory Operations"
url: https://developer.nvidia.com/blog/how-nvidia-uses-ai-agents-to-streamline-ai-factory-operations/
date: 2026-11-04
found_via: rss (TIER-1)
---

NVIDIA open-sources the AI Factory Operations Agent, a multi-agent system (six domain agents: Job Recovery, Hardware, Observability, Research, Kubernetes, Cluster Management) built on the NemoClaw blueprint and OpenShell runtime for operating DGX SuperPOD clusters, read-only-first by design.

## card

**Що сталося:** NVIDIA представила AI Factory Operations Agent — мультиагентну систему з шести доменних агентів (Job Recovery, Hardware, Observability, Research, Kubernetes, Cluster Management) для операцій над DGX SuperPOD-кластерами, побудовану на блюпринті NemoClaw та runtime OpenShell, з локально розгорнутими моделями Nemotron.

**Контекст:** Це ще один приклад застосування NemoClaw/OpenShell для агентної автоматизації інфраструктури AI-фабрик — у тому ж напрямку, що й попередні релізи NVIDIA Mission Control, Minerva та OpenShell reference architecture.

**Деталі:**
- Спільні MCP-інструменти: веб-пошук, виконання коду, дашборди Grafana.
- Мультитенантне обмеження: доступ агентів, інструментів і прав Kubernetes можна звужувати по тенанту.
- Принцип "read-only-first": дослідження інциденту завжди передує автоматичним діям.
- Позначена як "experimental open source software" — API та конфігурація можуть змінюватися між релізами; працює на DGX H100, B200 і GB300.
- Конкретних метрик точності root-cause-аналізу чи згоди з SRE в пості не наведено (NVIDIA каже, що вимірює їх, але цифр не дає).
