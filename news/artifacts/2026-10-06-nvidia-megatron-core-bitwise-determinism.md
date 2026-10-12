---
company: NVIDIA
title: "Scale Bitwise-Deterministic Pretraining with NVIDIA Megatron Core"
url: https://developer.nvidia.com/blog/scale-bitwise-deterministic-pretraining-with-nvidia-megatron-core/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-10-06
fetched: 2026-10-12
---

NVIDIA details a Megatron Core workflow (Megatron-LM PR #7262) for making large-scale LLM pretraining bitwise deterministic — independent and checkpoint-resumed runs produce identical numerical trajectories — while keeping determinism overhead low at scale. Found via gap-scrape (WebFetch of developer.nvidia.com/blog — TIER-1 RSS showed zero fresh; sibling Oct 6 posts on the same page were already captured, this one was missed).

## card

**Що сталося:** NVIDIA публікує методику Megatron Core (Megatron-LM PR #7262) для бітово-детермінованого пре-тренування великих LLM: незалежні запуски та запуски, відновлені з чекпоінта, дають ідентичну числову траєкторію. Детермінізм перевіряють впорядкованими per-rank тензорними відбитками (`torch.hash_tensor`), звужуючи пошук розбіжностей від метрик до фаз, модулів, операцій і, нарешті, кернелів.

**Контекст:** Приклад кернела — grouped-GEMM writers отримують приватні вихідні слоти, що комбінуються у фіксованому порядку редукції, збергаючи паралелізм і відновлюючи детермінізм.

**Деталі:**
- Nemotron 3 Ultra: оверхед детермінізму впав з ~17% до 2%, а на 3072 GPU — до 1.5%
- Hybrid Triton proxy: оверхед впав з ~60% до 37%, потім до 2%
- CuTeDSL weight-gradient шлях: ~3.6% оверхед на 256 GPU, ~2% на 2432 GPU за 800 кроків
- Гіпотетичний приклад: зниження оверхеду з 15% до 5% на 100-денному запуску на 10 000 GPU заощадило б 100 000 GPU-днів
