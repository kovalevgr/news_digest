---
company: NVIDIA
title: "How to Carry User Identity Across Federated Kubernetes and AI Platforms"
url: https://developer.nvidia.com/blog/how-to-carry-user-identity-across-federated-kubernetes-and-ai-platforms/
published: 2026-09-03
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-04
---

NVIDIA describes a centralized identity-gateway pattern for federated Kubernetes/AI platforms — a single gateway owns OIDC login/refresh/logout while stateless regional gateways delegate validation via a shared session store, cutting repeated logins 55% internally.

## card

**Що сталося:** NVIDIA описав архітектурний паттерн централізованого identity-gateway для федеративних Kubernetes/AI-платформ: замість того, щоб кожен регіональний шлюз вів власний OIDC-потік, єдиний центральний шлюз керує логіном, оновленням токенів і логаутом, а регіональні шлюзи лише валідують сесію через спільне сховище.

**Контекст:** Патерн побудований на публічно доступних інструментах — OAuth2 Proxy, Istio, OPA Envoy plugin, Authorino — і застосований NVIDIA внутрішньо на платформах AWS та OCI.

**Деталі:**
- 55% зменшення повторних подій логіну на внутрішніх платформах розробників (AWS, OCI)
- Сесії — за непрозорим session ID з HTTP-only cookie, короткий час життя access-токена, явний TTL сесії
- Взаємна TLS або workload identity між шлюзами; вхідні identity-заголовки очищуються перед підстановкою довірених
- Навантаження на upstream identity provider масштабується переважно з кількістю активних користувачів, а не комбінацій користувач×інструмент
