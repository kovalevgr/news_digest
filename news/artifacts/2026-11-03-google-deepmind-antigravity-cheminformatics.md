---
company: google-deepmind
title: "Agentic cheminformatics with Google Antigravity"
url: https://deepmind.google/blog/agentic-cheminformatics-with-google-antigravity/
date: 2026-11-03
found_via: rss
---

Google DeepMind introduces Cheminformatics Skills for Google Antigravity, its agentic development platform, turning it into a workbench for computational/experimental chemists — demonstrated on a lung-cancer kinase-inhibitor drug-discovery workflow — with free access for 10,000 scientists for six months.

## card

**Що сталося:** Google DeepMind представили Cheminformatics Skills для Google Antigravity (агентна платформа розробки), що перетворює її на робочий інструмент для хіміків-дослідників. На прикладі пошуку інгібіторів кіназ для раку легень (аналоги крізотинібу та лорлатінібу) агент знайшов тисячі сполук у літературі й патентах, відфільтрував нерелевантні, провів matched molecular pair аналіз, побудував моделі потенції та запропонував нові макроцикли з маршрутами синтезу — весь процес зайняв близько години.

**Контекст:** Пост продовжує серію про науковий workflow на Antigravity — попередній був про протимікробні пептиди (жовтень 2026). Skills побудовані на RDKit з інтеграцією ChEMBL та PubChem.

**Деталі:**
- Відфільтрований набір для аналізу — 568 сполук.
- Доступно вже сьогодні: встановлення Science plugin в застосунку Antigravity; enterprise-користувачі — через Google Cloud credentials.
- Google пропонує 10 000 науковцям найвищий тарифний рівень безкоштовно на 6 місяців (ролінговий onboarding, заявка через форму в пості).
- Застереження: обчислювальні дизайни — лише гіпотези, що потребують експериментальної перевірки; розріджені дані та шум аналізів обмежують точність моделей.
