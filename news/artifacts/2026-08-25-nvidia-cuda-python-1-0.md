---
company: NVIDIA
title: "CUDA Python 1.0: Stable APIs, One Foundation, Full Platform Access"
url: https://developer.nvidia.com/blog/cuda-python-1-0-stable-apis-one-foundation-full-platform-access/
published: 2026-08-25
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-26
---

NVIDIA ships CUDA Python 1.0 alongside CUDA 13.3, unifying cuda.core, cuda.compute, cuda.bindings, cuda-pathfinder, and nvmath-python under semantic versioning — the first stable, officially supported way to access the full CUDA platform from Python.

## card

**Що сталося:** NVIDIA випустила CUDA Python 1.0 разом із CUDA 13.3 — офіційно підтримуваний і стабільний спосіб отримати доступ до повної платформи CUDA з Python без написання C++-розширень.

**Контекст:** Раніше екосистема Python-біндингів для CUDA була фрагментована через кілька несумісних шарів; 1.0 об'єднує їх під єдиним фундаментом із гарантіями стабільності.

**Деталі:**
- Компоненти релізу: cuda.core 1.0.0 (pythonic runtime API для пристроїв/потоків/пам'яті), cuda.compute 1.0.0 (паралельні алгоритми CCCL), cuda.bindings 13.3.0 (низькорівневі 1:1 біндинги до CUDA C API), cuda-pathfinder, nvmath-python 1.0
- Перехід на семантичне версіонування — зворотньо несумісні зміни тепер лише в major-релізах, з чіткими шляхами депрекації
- Бібліотеки тепер сумісні між собою: ядра й структури даних передаються між ними без копіювання і workaround'ів
- Прямий доступ з Python до можливостей на кшталт green contexts (розбиття SM), чекпоінтингу процесів, міжпроцесного розподілу пам'яті GPU
