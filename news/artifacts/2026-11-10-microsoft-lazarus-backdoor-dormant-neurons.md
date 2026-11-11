---
company: microsoft
title: "Lazare, veni foras: Reprogramming Dormant Neurons to Backdoor AI Agents"
url: https://www.microsoft.com/en-us/research/blog/lazare-veni-foras-reprogramming-dormant-neurons-to-backdoor-ai-agents/
date: 2026-11-10
found_via: rss
---

Microsoft Research describes "Lazarus," a backdoor technique that reprograms fewer than 10 rarely-firing ("dormant") neurons — no retraining needed — to make an otherwise normal-passing AI agent execute attacker commands when a hidden trigger appears; the technique was mostly discovered autonomously by Claude Code running on Opus 4.5.

## card

**Що сталося:** Дослідники Microsoft Research описали техніку "Lazarus" — бекдор, який перепрограмовує менше 10 "сплячих" (рідко активних) нейронів моделі, роблячи агента, що проходить стандартні оцінки, здатним виконувати команди атакувальника при появі скритого тригера.

**Контекст:** Техніку класифікують як новий тип загрози в лінії попередніх досліджень бекдор-моделей; робота почалась у березні як експеримент, де Claude Code (на Opus 4.5) попросили бекдорити модель без тренування — і агент самостійно відкрив більшість техніки.

**Деталі:**
- Для атаки достатньо менше 10 перепрограмованих нейронів; лінійний класифікатор на ~50 прикладах відрізняє вхід із тригером від звичайного.
- Один перепрограмований нейрон може форсувати один токен у виводі; ланцюжок нейронів може видати довший payload (напр., термінальні команди).
- Атака потребує лише inference-рівня обчислень і доступу на запис до чекпоінта моделі — тренування не потрібне.
- Приклад тригера — зміна дати: після півночі 2027 року агент завантажує й запускає код атакувальника з доступними йому правами.
- Microsoft Foundry перевіряє походження моделей і скановує супутнє ПЗ; компанія розробляє AI-скан вагів, red-teaming harness і криптографічний підпис моделей з аудиторськими слідами.
