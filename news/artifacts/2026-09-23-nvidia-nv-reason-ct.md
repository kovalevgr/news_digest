---
company: NVIDIA
title: "Introducing NV-Reason-CT: Open 3D CT VLM for Radiologist Chain-of-Thought Reasoning"
url: https://developer.nvidia.com/blog/introducing-nv-reason-ct-open-3d-ct-vlm-for-radiologist-chain-of-thought-reasoning
published: 2026-09-23
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-24
---

NVIDIA releases NV-Reason-CT, an open vision-language model that processes full 3D CT volumes natively (built on a 3D vision transformer + Qwen3.5-4B) and generates radiologist-style chain-of-thought diagnostic reports.

## card

**Що сталося:** NVIDIA випускає NV-Reason-CT — відкриту vision-language модель, що нативно обробляє повні 3D-об'єми КТ (замість окремих 2D-зрізів) і генерує структуровані діагностичні звіти з ланцюжком міркувань у стилі рентгенолога.

**Контекст:** Модель поєднує повний 3D vision transformer encoder із мовною моделлю Qwen3.5-4B, обробляючи об'єми КТ нативно у роздільності 192³ вокселі (патчі 8×8×8). Клінічну правдоподібність висновків та ланцюжків міркувань перевірили радіологи NIH.

**Деталі:**
- Покриває 30 грудних та 29 абдомінальних патологій у структурованих звітах
- CT-RATE: Macro-F1 = 0.614, Macro-AUROC = 0.871 — перевершує опубліковані базові моделі (VoxelFM, Pillar-0, ClinFusion-8B)
- Навчання у два етапи: SFT на ~550 000 структурованих QA-прикладів з анотаціями міркувань радіологів, потім RL (GRPO) з anatomy-aware винагородами
- Дані навчання: CT-RATE, набори NIH, CancerVerse
- Відкритий доступ на Hugging Face + GitHub (скрипти інференсу, post-training рецепти); дослідницька модель, не клінічний продукт
