---
company: nvidia
title: "Inside NVIDIA Sentry: Secure AI Agents at Runtime"
url: https://developer.nvidia.com/blog/inside-nvidia-sentry-secure-ai-agents-at-runtime/
date: 2026-10-21
found_via: TIER-1 rss (developer.nvidia.com/blog/feed)
---

NVIDIA introduces Sentry, a runtime security framework that monitors AI agents from an isolated hardware domain on BlueField-4 DPUs, using DOCA Tower (an Envoy-based proxy enforcing Open Policy Agent rules) and DOCA Argus (agentless memory introspection) to contain misbehaving agents in silicon within milliseconds; planned availability early next year.

## card

**Що сталося:** NVIDIA представляє Sentry — фреймворк безпеки для AI-агентів у реальному часі, що моніторить агентів з ізольованого апаратного домену на DPU BlueField-4, частина довідкової архітектури NVIDIA OpenShell.

**Контекст:** Sentry використовує два компоненти DOCA: Tower — проксі на основі Envoy, що завершує TLS і оцінює запити агентів за правилами Open Policy Agent, та Argus — безагентна інтроспекція пам'яті середовища виконання агента. Мета — блокувати неправомірну поведінку агента на рівні кремнію за мілісекунди та вести незмінні (tamper-evident) журнали активності.

**Деталі:**
- Запланована доступність — на початок наступного року.
- Розробники вже можуть експериментувати з пов'язаними бібліотеками DOCA: Argus, Flow, OVS-DOCA.
- Ізоляція реалізована на апаратному рівні (BlueField-4 DPU), окремо від основного обчислювального домену агента.
