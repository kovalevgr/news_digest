---
company: NVIDIA
title: "Run NVIDIA BioNeMo NIM Microservices for Protein Structure Prediction in Claude Science"
url: https://developer.nvidia.com/blog/run-nvidia-bionemo-nim-microservices-for-protein-structure-prediction-in-claude-science/
published: 2026-08-31
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-01
---

NVIDIA and Anthropic integrated the BioNeMo Agent Toolkit into Claude Science, letting AI agents orchestrate protein-structure-prediction workflows (OpenFold3, Boltz-2) via NVIDIA NIM microservices as callable skills.

## card

**Що сталося:** NVIDIA та Anthropic інтегрували BioNeMo Agent Toolkit у Claude Science, дозволяючи AI-агентам оркеструвати робочі процеси передбачення структури білків через мікросервіси NVIDIA NIM.

**Контекст:** Toolkit пакує понад десятиліття напрацювань NVIDIA BioNeMo (моделі, бібліотеки, воркфлоу для наук про життя) у виклики-навички для біології та розробки ліків.

**Деталі:**
- Моделі OpenFold3 і Boltz-2: interface confidence 0.85 і 0.82 з вирівнюванням послідовностей (MSA), падає до 0.14 і 0.19 без нього
- Точність виконання завдань зростає з 60% до 100% при використанні повного workflow
- Локальний деплой: ~700 ГБ дискового простору + NVIDIA L40S або H100
- Доступно на GitHub
