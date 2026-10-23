---
company: huggingface
title: "OlmoEarth v1.3: State-of-the-art embeddings for the whole planet"
url: https://huggingface.co/blog/allenai/olmoearth-v1-3
date: 2026-10-22
found_via: TIER-1 rss (huggingface.co/blog/feed.xml)
---

Ai2 releases OlmoEarth v1.3, satellite embeddings (Sentinel-1/2, Landsat) at 10m resolution with precomputed global coverage shared on Source Cooperative (~150TB/year), a no-login Embeddings Explorer, and a new tropical crop-mapping benchmark (PLANTEUR); v1.3 wins 20/27 (128-dim) and 18/27 (64-dim) evaluation tasks against AlphaEarth Foundations and Tessera v2, at 18% of v1's pretraining compute/cost.

## card

**Що сталося:** Ai2 випустив OlmoEarth v1.3 — модель супутникових ембедингів (Sentinel-1/2, Landsat) з роздільною здатністю 10 метрів, з готовими глобальними ембедингами, опублікованими на Source Cooperative (~150 ТБ на рік), та безкоштовним браузерним інструментом Embeddings Explorer без реєстрації.

**Контекст:** Продовжує лінійку OlmoEarth; у цій версії додано новий бенчмарк PLANTEUR для класифікації типів тропічних культур, а також записи провенансу вихідних супутникових знімків для кожного тайлу 20×20 км.

**Деталі:**
- У оцінці на 27 завданнях проти AlphaEarth Foundations і Tessera v2: 128-вимірна версія перемагає у 20 з 27, 64-вимірна — у 18 з 27.
- Обчислення для передтренування — 53% від v1.2 і 18% від v1; викиди вуглецю — 50% і 22% відповідно.
- Орієнтовна вартість відтворення фінального прогону передтренування v1.3 Base — близько $2720 в оренді H100 (проти $5100 для v1.2 і $15 060 для v1).
- Глобальні ембединги покривають 2023-2025 роки, вибрані країни — 2017-2022.
- Ваги моделі, дані передтренування та код опубліковані під ліцензією OlmoEarth Artifact License.
