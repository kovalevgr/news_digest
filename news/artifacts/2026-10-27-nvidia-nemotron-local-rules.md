---
company: nvidia
title: "Fine-Tuning NVIDIA Nemotron to Know Local Rules, Not Just Local Languages"
url: https://developer.nvidia.com/blog/fine-tuning-nvidia-nemotron-to-know-local-rules-not-just-local-languages/
date: 2026-10-27
found_via: rss (TIER-1)
---

NVIDIA publishes a post-training workflow fine-tuning Nemotron 3.5 Lightning via LoRA on synthetic persona-grounded conversations (Nemotron-Personas datasets) to teach local administrative rules rather than just language, with persona data now covering France, Belgium and 12 countries total.

## card

**Що сталося:** NVIDIA публікує методику донавчання Nemotron 3.5 Lightning (LoRA + NeMo) на синтетичних діалогах, прив'язаних до наборів даних Nemotron-Personas — синтетичних "жителів", збудованих на регіональних демографічних і культурних даних — щоб модель знала не лише мову, а й локальні адміністративні правила.

**Контекст:** Приклад з публікації: на запитання про оформлення паспорта людиною, яка не може подорожувати, базова модель радить поштову заявку, якої офіційно не існує, тоді як донавчена модель описує реальну процедуру виїзного візиту.

**Деталі:**
- Дані персон випущено для Франції та Бельгії; ширша відкрита програма даних охоплює 12 країн.
- У прикладі використано 2000 персон і 2000 згенерованих записів; для DGX Spark або хостованого API рекомендується починати з 500-1000.
- Регіональна деталь з прикладу: вартість марки на паспорт — €43 у Французькій Гвіані проти €86 у метрополії.
- Pleias використовує набори даних Франції та Бельгії для свого асистента Lamina з питань спинної хірургії.
- Кількісних бенчмарків немає — оцінка якісна; репозиторій Nemotron v0.2.0 на GitHub, моделі й дані — на Hugging Face.
