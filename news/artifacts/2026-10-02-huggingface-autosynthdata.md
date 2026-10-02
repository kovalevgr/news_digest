---
company: Hugging Face
title: "AutoSynthData: Generating Training Data for Enterprise Agents"
url: https://huggingface.co/blog/ServiceNow-AI/autosynthdata
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-02
fetched: 2026-10-02
---

ServiceNow CoreAI releases AutoSynthData, a pipeline that evaluates agent failures, synthesizes and validates new training tasks targeting those capability gaps, then fine-tunes on the successes; +7.2pp Pass@1 (35% relative) on a hybrid-domain benchmark and 18.77%→27.18% on ITSM; publishes the EnterpriseOps-Gym dataset on the Hub.

## card

**Що сталося:** ServiceNow CoreAI випустила AutoSynthData — систему генерації тренувальних даних, що цілеспрямовано закриває конкретні прогалини у можливостях enterprise-агентів, знайдені через оцінювання моделі.

**Контекст:** Підхід: знайти провали моделі через оцінку → витягнути специфікацію бракуючої здатності → згенерувати нові синтетичні завдання, що її тренують → перевірити завдання в реальному середовищі → донавчити на вдалих прикладах; багаторівневий контроль якості (перевірка кожного завдання + мета-огляд батчів на покриття й різноманітність).

**Деталі:**
- Домен Hybrid: Pass@1 +7.2 в.п. (відносне покращення 35%), закрито 59% розриву з референсними моделями; згенеровано 2000 прикладів за 18 годин
- Домен ITSM: Pass@1 зріс з 18.77% до 27.18%; згенеровано 1994 приклади за 66 годин
- Датасет EnterpriseOps-Gym опубліковано у відкритому доступі на Hugging Face Hub
- Код і повні релізи моделей окремо не анонсовані
