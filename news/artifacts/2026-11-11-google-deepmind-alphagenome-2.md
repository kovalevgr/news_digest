---
company: google-deepmind
title: "AlphaGenome 2: Deciphering how cells read DNA to better understand disease"
url: https://deepmind.google/blog/alphagenome-2-deciphering-how-cells-read-dna-to-better-understand-disease/
date: 2026-11-11
found_via: rss (confirmed; the TIER-1 feed's own TRAP/not-a-feed flag this run was a false positive — raw curl confirmed valid application/xml with this item at the top)
---

Google DeepMind releases AlphaGenome 2, a next-generation DNA sequence model that — unlike the original AlphaGenome's parallel tissue-average predictions — is conditional on a single target cell type or state and can adapt to new single-cell data without retraining; it identifies nearly twice as many expression-changing variants as the prior state of the art and is available for non-commercial research via API, with commercial research in private preview.

## card

**Що сталося:** Google DeepMind випустив AlphaGenome 2 — модель нового покоління для передбачення впливу послідовностей і варіантів ДНК на активність генів у конкретних типах/станах клітин людини. На відміну від оригінального AlphaGenome, який паралельно передбачав усереднені показники по тканинах, нова модель є умовною — працює з одним цільовим типом клітини за раз і адаптується до нових single-cell даних без перенавчання.

**Контекст:** Наступне покоління AlphaGenome; модель натренована на понад 100 млн профілів окремих клітин із 68 тканин. Доступна для некомерційних дослідницьких задач через API, для комерційних досліджень — у приватному перегляді (private preview).

**Деталі:**
- Виявляє майже вдвічі більше варіантів, що змінюють експресію генів, ніж попередній найкращий метод.
- На датасеті TenK10K: точність виявлення каузальних варіантів — 30% проти 16% в оригінального AlphaGenome, донавченого на single-cell даних, та інших спеціалізованих інструментів.
- Визначення напрямку ефекту на гени: 43% проти 23%.
- Тренувальні дані: понад 100 млн профілів окремих клітин, 68 тканин.
