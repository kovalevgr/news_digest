---
company: NVIDIA
title: "NVIDIA Nemotron 3.5 Super VL Powers Specialized Agents with Multimodal Reasoning"
url: https://developer.nvidia.com/blog/nvidia-nemotron-3-5-super-vl-powers-specialized-agents-with-multimodal-reasoning/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-10-15
fetched: 2026-10-16
---

NVIDIA releases Nemotron 3.5 Super VL, an open multimodal model (120B MoE, 12B active) combining reasoning, tool use, and text/image/document/video understanding, distilled from Nemotron 3 Ultra and outperforming Nemotron 3 Super on SWE-bench and Terminal-Bench.

## card

**Що сталося:** NVIDIA випустив Nemotron 3.5 Super VL — відкриту мультимодальну модель, що поєднує міркування, виклик інструментів та розуміння тексту, зображень, документів і відео в одній моделі, як альтернативу запуску окремих текстових і vision-language моделей.

**Контекст:** Дистильована з Nemotron 3 Ultra; перевершує Nemotron 3 Super на SWE-bench і Terminal-Bench, а також Nemotron 3 Ultra на Hermes Bench і LangChain Evals. Позиціонується поряд із меншою Nemotron 3.5 Lightning та більшою Nemotron 3 Ultra.

**Деталі:**
- Архітектура: mixture-of-experts, 120B параметрів загалом, 12B активних на токен
- Пропускна здатність: до 5× вища за відкриті моделі того ж класу на агентних задачах на одному GPU; понад 600 токенів/сек на агентному бенчмарку Artificial Analysis (через Baseten)
- Бенчмарки: Hermes Bench 63.44% (Nemotron 3 Ultra: 56.33%); LangChain Evals 87.05% (84.3%); CharXiv 80.8% (Nemotron 3 Nano Omni: 63%), 84% з Python-інтерпретатором
- Партнерські результати (за даними партнерів): Scale AI — 40× нижча вартість inference; Ramp — до 50% вища пропускна здатність і 10× нижча латентність; AI21/Alice — +41% точності в задачах threat intelligence
- Доступність: базові, post-trained та NVFP4-квантовані чекпоінти, ваги на Hugging Face і ModelScope, хостинг на OpenRouter, контейнер NVIDIA NIM
