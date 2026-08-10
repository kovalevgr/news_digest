---
category: technical-newsletters
updated: 2026-08-10
---

# Radar: technical-newsletters

Technical-radar items for this category (sources in [`config/radar.json`](../config/radar.json)).
Appended by the daily routine under weekly headings; format matches topics files.

## 2026-W33

- **2026-08-10** — [Ultra-High Interactivity on NVIDIA GPUs? - TileRT InferenceX](https://newsletter.semianalysis.com/p/ultra-high-interactivity-on-nvidia) — TileRT compiles the entire decode graph into a single persistent GPU kernel instead of launching separate kernels, hitting 494 tok/s/user at 1k/1k on B200 (~3.6x prior FP8 engines at 136 tok/s/user) and 340 tok/s/user at 8k/1k (~1.9x prior best); closes much of NVIDIA's interactivity gap with Cerebras/Groq/SambaNova in software, at the cost of batch-size-1-only support today.
