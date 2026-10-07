---
company: NVIDIA
title: "Control How Your GPU Shares Work with Green Contexts"
url: https://developer.nvidia.com/blog/control-how-your-gpu-shares-work-with-green-contexts/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-10-06
fetched: 2026-10-07
---

NVIDIA expands Green Contexts — explicit GPU resource partitioning (SMs and workqueues) within a single process — from the Driver API to the Runtime API starting with CUDA 13.1, making the feature more accessible to developers.

## card

**Що сталося:** NVIDIA розширює Green Contexts — явне партиціонування ресурсів GPU (SM та workqueues) в межах одного процесу — з Driver API на Runtime API, починаючи з CUDA 13.1, роблячи фічу доступнішою для розробників.

**Контекст:** Green Contexts існували в Driver API з CUDA 12.4; це розширення додає підтримку в Runtime API. Фіча опціональна й зворотньо сумісна з існуючими CUDA-воркфлоу.

**Деталі:**
- Тест на Blackwell GPU: латентність критичного ядра впала з 0.140 мс до 0.007 мс (у 20 разів) при виділених SM-партиціях
- Покращення перевищує ефект лише від stream priority
- Можна впроваджувати інкрементально, поряд з існуючими воркфлоу
