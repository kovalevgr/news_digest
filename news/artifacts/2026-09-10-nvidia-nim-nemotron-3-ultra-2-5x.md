---
company: NVIDIA
title: "How Full-Stack NIM Optimizations Deliver 2.5x More Users on Nemotron 3 Ultra"
url: https://developer.nvidia.com/blog/how-full-stack-nim-optimizations-deliver-2-5x-more-users-on-nemotron-3-ultra/
published: 2026-09-10
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-11
---

NVIDIA details full-stack NIM optimizations for Nemotron 3 Ultra — autotuned kernels, tensor parallelism, prefix/state reuse, scheduler and memory tuning, MTP speculative decoding — reaching 1,997 tokens/sec on a 4xB200 system, a 2.5x throughput gain at the 50 tok/s-per-user target for agentic workloads.

## card

**Що сталося:** NVIDIA описує комплексну (full-stack) оптимізацію NIM для Nemotron 3 Ultra — від автотюнінгу ядер до спекулятивного декодування — яка дозволяє обслуговувати вдвічі-з-половиною більше користувачів на тому ж обладнанні.

**Контекст:** Продовжує серію технічних матеріалів NVIDIA про inference-оптимізацію для агентних навантажень, де важлива саме кількість одночасних користувачів при фіксованій швидкості токенів на користувача, а не лише сира пропускна здатність.

**Деталі:**
- Комбінація технік: автотюновані CUDA-ядра, tensor parallelism, prefix/state reuse, тюнінг планувальника й пам'яті, MTP speculative decoding
- 1997 токенів/сек на системі 4×B200
- 2.5x приріст пропускної здатності відносно baseline при цільових 50 токенів/сек на користувача (типово для агентних сценаріїв)
