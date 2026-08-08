---
company: Hugging Face
title: "Baseten on Hugging Face Inference Providers"
url: https://huggingface.co/blog/baseten
published: 2026-08-06
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-08-07
note: "Found via gap-scrape WebFetch (RSS TIER-1 feed had zero fresh candidates)."
---

Baseten becomes an integrated inference provider on Hugging Face Hub, letting developers
access frontier language models and other AI capabilities through the Hub's website and
client SDKs.

## card

**Що сталося:** Baseten став офіційно підтримуваним Inference Provider на Hugging Face Hub. Розробники отримують serverless-доступ до frontier-моделей прямо зі сторінок моделей на Hub і через клієнтські SDK (Python та JavaScript).

**Контекст:** Розширення чинної програми Hugging Face Inference Providers — Baseten додається до наявної екосистеми сторонніх провайдерів serverless-інференсу на Hub.

**Деталі:**
- На старті підтримуються conversational- і text-generation-задачі; підтримка інших типів задач — згодом
- Серед доступних моделей: Kimi K3, DeepSeek V4 Flash, GLM-5.2 (повний список — на сторінці моделей Hub з фільтром за провайдером Baseten)
- Два режими роутингу: із власним API-ключем Baseten (білінг напряму в Baseten) або через Hugging Face без ключа провайдера — за стандартними тарифами провайдера, без націнки
- PRO-передплатники отримують $2 інференс-кредитів щомісяця (діють для всіх провайдерів); безкоштовні користувачі мають невелику квоту
- OpenAI-сумісний API через роутер https://router.huggingface.co/v1; інтеграція вже є в більшості агентних harness'ів, зокрема Pi, OpenCode і Hermes Agents
