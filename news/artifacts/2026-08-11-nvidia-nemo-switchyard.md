---
company: NVIDIA
title: "Route AI Agent Workloads Across Models with NVIDIA NeMo Switchyard"
url: https://developer.nvidia.com/blog/route-ai-agent-workloads-across-models-with-nvidia-nemo-switchyard/
published: 2026-08-11
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-12
note: "TIER-1 rss."
---

NVIDIA open-sources NeMo Switchyard, a provider-agnostic SDK that routes agent workloads across models (tuning-free and tunable routers) based on capability, cost, and infrastructure signals; a LangChain benchmark reports a 74% cost reduction vs. a frontier-only baseline at comparable accuracy.

## card

**Що сталося:** NVIDIA випустила у відкритий доступ NeMo Switchyard — SDK для динамічної маршрутизації задач AI-агентів між різними моделями, відокремлюючи логіку роутингу від конкретних реалізацій моделей.

**Контекст:** Публікується одночасно з моделлю Nemotron 3.5 Lightning (окремий артефакт) — Switchyard і Lightning разом формують NVIDIA-пропозицію для мультимодельних агентних систем: "дешева спеціалізована модель + розумний роутер".

**Деталі:**
- Provider-agnostic SDK, сумісний з OpenAI-, Anthropic- та іншими стандартними API
- Роутери "без тюнінгу": LLM classifier, stage router (для coding-агентів), escalation router (починає з дешевших моделей, ескалує за потреби)
- "Тюнюваний" роутер: prefill router, що навчається на реальних даних передбачати точність моделі
- Враховує три категорії сигналів: можливості моделі, вартісний профіль (латентність/ціна), інфраструктурні сигнали (навантаження, помилки)
- Тест з LangChain: зниження вартості на 74% порівняно з baseline "тільки фронтирна модель" при збереженні точності
- Інтегрується з наявними agent-фреймворками й гейтвеями без переписування застосунку
