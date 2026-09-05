---
company: NVIDIA
title: "Frontier Reasoning Reaches the Edge: How to Deploy and Optimize Models on NVIDIA Jetson"
url: https://developer.nvidia.com/blog/frontier-reasoning-reaches-the-edge-how-to-deploy-and-optimize-models-on-nvidia-jetson/
published: 2026-09-04
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-05
---

NVIDIA shows how NVFP4 quantization plus speculative decoding (DSpark, DFlash2) deploy reasoning models — Nemotron 3.5 Lightning (30B MoE, 3B active) and Qwen3.8-27B (dense) — on Jetson edge hardware, reaching up to 6.28x decode-throughput speedup over BF16.

## card

**Що сталося:** NVIDIA опублікувала гайд з розгортання та оптимізації reasoning-моделей на едж-пристроях Jetson, показавши, що моделі 2026 року досягають рівня інтелекту фронтирних моделей 2025-го при значно меншій кількості параметрів.

**Контекст:** Технічна стаття в серії NVIDIA Developer Blog про едж-інференс; фокус на двох моделях — Nemotron 3.5 Lightning (MoE) та Qwen3.8-27B (dense).

**Деталі:**
- Nemotron 3.5 Lightning: 30 млрд параметрів загалом, активних лише 3 млрд на токен (MoE); Qwen3.8-27B: щільна модель, всі 27 млрд активні
- NVFP4-квантизація сама по собі: прискорення 2.2–2.33x
- NVFP4 + спекулятивне декодування: до 6.28x прискорення пропускної здатності декодування проти BF16
- Пропускна здатність: Nemotron 3.5 Lightning 123.01–138.02 ток/с; Qwen3.8-27B 27.69–34.44 ток/с
- Найкращі методи спекулятивного декодування: DSpark для Nemotron, DFlash2 для Qwen3.8
