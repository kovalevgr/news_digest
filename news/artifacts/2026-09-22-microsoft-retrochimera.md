---
company: Microsoft
title: "Improving synthesis prediction of small molecules at scale with RetroChimera"
url: https://www.microsoft.com/en-us/research/blog/improving-synthesis-prediction-of-small-molecules-at-scale-with-retrochimera/
published: 2026-09-21
source_url: https://www.microsoft.com/en-us/research/feed/
fetched: 2026-09-22
---

Microsoft Research introduces RetroChimera, a retrosynthesis-prediction framework combining a Transformer (R-SMILES 2) and a graph neural network (NeuralLoc) with a learned ranking strategy; published in Nature, RetroChimera routes reached a 90% expert-chemist acceptance rate versus 20–50% for either sub-model alone, and is available open-source (MIT) and via Microsoft Foundry.

## card

**Що сталося:** Microsoft Research публікує в Nature RetroChimera — фреймворк для передбачення ретросинтезу (планування синтезу молекул "у зворотному напрямку" до простіших будівельних блоків), що поєднує дві доповнюючі одна одну моделі глибокого навчання через навчену стратегію ранжування.

**Контекст:** Система об'єднує R-SMILES 2 (Transformer, гнучкий, але схильний до "галюцинацій") та NeuralLoc (графова нейромережа, точна, але слабка на незнайомих реакціях), вирішуючи типові проблеми планування хімічного синтезу — рідкісні реакції, слабку стійкість поза межами навчальних даних і невідповідність очікуванням хіміків.

**Деталі:**
- На повних маршрутах синтезу RetroChimera успішно впорався з 9 цілями проти 5 (de novo модель), 4 (editing модель) і 2 (NeuralSym)
- Рівень прийняття експертами-хіміками — 90% для маршрутів RetroChimera проти 20–50% для окремих підмоделей
- Опубліковано в Nature 21 вересня 2026
- Доступно як open-source під ліцензією MIT на GitHub, а також через Microsoft Foundry (ai.azure.com)
