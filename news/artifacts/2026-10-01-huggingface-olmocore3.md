---
company: Hugging Face
title: "Introducing Olmo-core 3: Open, scalable training infrastructure for large MoEs"
url: https://huggingface.co/blog/allenai/olmocore3
source_url: https://huggingface.co/blog/feed.xml
published: 2026-10-01
fetched: 2026-10-02
---

Allen Institute for AI releases Olmo-core 3, an open MoE training framework replacing FSDP-based weight-gathering with a DDP-style design keeping experts resident on GPU; 2.7x throughput (52,000 vs. 19,400 tok/s/GPU) on a 47B-parameter/128-expert config, tested to 1.2T parameters across 512 GPUs; code on GitHub. Note: also covered by today's radar run under `radar/research-institutes.md` via AI2's own `allenai.org/blog/olmocore3` post (same announcement, different canonical URL/platform) — kept here too per the Hugging Face company feed's normal scope (third-party-org posts hosted on huggingface.co/blog are routinely included in this topics file).

## card

**Що сталося:** Allen Institute for AI (AI2) випустив Olmo-core 3 — перероблений, повністю відкритий фреймворк для тренування MoE-моделей, що замінює попередній підхід на основі FSDP дизайном у стилі DDP, який тримає експертів резидентними на GPU замість повторного збирання ваг.

**Контекст:** Продовжує серію відкритих релізів екосистеми Olmo (код, дані, ваги); інфраструктурний фундамент для майбутніх MoE-моделей Olmo.

**Деталі:**
- 2.7x пропускна здатність: 52 000 проти 19 400 токенів/с/GPU на конфігурації 47B параметрів / 128 експертів (8x NVIDIA B300)
- Протестовано масштабування до 1.2T параметрів (58.36B активних) на 512 GPU, пікова продуктивність 858 TFLOP/с/GPU
- Тест ємності до 2.38T параметрів
- Точність MXFP8 знизила пікове активне споживання пам'яті зі 103 до 95 GiB при на 21% вищій пропускній здатності порівняно з BF16
- Код відкритий на GitHub
