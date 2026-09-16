---
company: NVIDIA
title: "How NVIDIA NVLink 6 Delivers Multi-Layer Resiliency for AI Factories"
url: https://developer.nvidia.com/blog/how-nvidia-nvlink-6-delivers-multi-layer-resiliency-for-ai-factories/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-09-15
fetched: 2026-09-16
---

NVIDIA details NVLink 6's four-layer resiliency architecture (physical, link, application, system) for AI factories built on Vera Rubin NVL72's 72-GPU domain: lightweight FEC + Physical Layer Retry for near-zero-latency error correction, credit-based flow control to mathematically eliminate packet loss, an NMX Controller with High Availability plus Shadow Engine Recovery, and rack-level serviceability with CUDA checkpointing. Shadow Engine Recovery restores inference capacity in 7.3s vs. 283s cold restart (39x faster); NVLink 6 delivers 3x lower end-to-end latency and 10x higher packet rates than generic Ethernet.

## card

**Що сталося:** NVIDIA описує чотирирівневу архітектуру відмовостійкості NVLink 6 — мережевої фабрики масштабування для AI-фабрик на базі Vera Rubin NVL72 (домен на 72 GPU).

**Контекст:** Кожен рівень вирішує свій клас збоїв: фізичний — легка Forward Error Correction і Physical Layer Retry з майже нульовою затримкою плюс відновлення UPHY при серйозній деградації лінку; лінковий — credit-based flow control математично усуває втрату пакетів і автономно перебалансовує лінки; прикладний — NMX Controller з High Availability і Shadow Engine Recovery для inference; системний — сервісованість на рівні стійки, розподілена резервність керування, підтримка CUDA checkpointing.

**Деталі:**
- Shadow Engine Recovery відновлює inference-потужність за 7.3с проти 283с холодного рестарту (у 39 разів швидше)
- У 3 рази нижча наскрізна затримка і у 10 разів вища частота пакетів проти звичайного Ethernet
- Відновлення NMX Controller — за секунди
- Корекція помилок на фізичному рівні — менше 1 мс
