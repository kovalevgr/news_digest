---
category: technical-newsletters
updated: 2026-08-31
---

# Radar: technical-newsletters

Technical-radar items for this category (sources in [`config/radar.json`](../config/radar.json)).
Appended by the daily routine under weekly headings; format matches topics files.

## 2026-W33

- **2026-08-10** — [Ultra-High Interactivity on NVIDIA GPUs? - TileRT InferenceX](https://newsletter.semianalysis.com/p/ultra-high-interactivity-on-nvidia) — TileRT compiles the entire decode graph into a single persistent GPU kernel instead of launching separate kernels, hitting 494 tok/s/user at 1k/1k on B200 (~3.6x prior FP8 engines at 136 tok/s/user) and 340 tok/s/user at 8k/1k (~1.9x prior best); closes much of NVIDIA's interactivity gap with Cerebras/Groq/SambaNova in software, at the cost of batch-size-1-only support today.
- **2026-08-10** — [Notes on Midtraining](https://cameronrwolfe.substack.com/p/midtraining-notes) — Explainer on midtraining/continual pretraining as a technique for producing better specialized LLMs.

## 2026-W34

- **2026-08-21** — [Are Open Models Catching Up?](https://newsletter.semianalysis.com/p/are-open-models-catching-up) — Verified via WebFetch: capability-trend analysis (not a finance/hardware piece) tracking open- vs. closed-model gaps across three eras with era-appropriate benchmarks — basic knowledge (Era 1: GPT-3.5 Turbo 75.7 vs. Llama-2-70B 39.9 normalized), reasoning (Era 2: o1-preview led, DeepSeek R1 trailed by 12.1 pts initially), and agentic/coding work (Era 3: Kimi K2.6 passed Opus 4.5 in 4.8 months, GLM-5.2 passed GPT-5.2 in 6 months). Central claim: each era's open models take roughly half as long to catch the first closed-source model of that era as the era before.

## 2026-W35

- **2026-08-24** — [AgentX - InferenceXv3: Does CUDA Moat Hold up in Agentic Inferencing?](https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat) — Verified via WebFetch: open-source (Apache 2.0) inference benchmark suite adds AgentX, a multi-turn agentic-coding scenario built from 393 anonymized Claude Code traces (up to 1M-token context), complementing the existing fixed-length 8k1k/1k1k/1k8k scenarios; run across ~2MW of continuously operated compute on 1000+ chips (NVIDIA GB300/GB200 NVL72, B300, B200, H200; AMD MI355X/MI325/MI300X; RTX Pro Servers, TPUs incoming). Reports KV-cache hit rates >95% for sub-agent bursts (B300 vLLM DEP8: 91% HBM hit rate under 384 concurrent traces) and a DeepSeek V4 Pro p50 input length of 88k tokens. Full dashboard, dataset and REST API published with CI-verified accuracy provenance per benchmark point.
- **2026-08-24** — [Reinforcement Learning for LLMs: The Complete Guide](https://cameronrwolfe.substack.com/p/llm-rl) — Explainer tracing the evolution of RL for LLMs from first principles through to frontier post-training practice.
- **2026-08-30** — [Most Neoclouds Suck At Security](https://newsletter.semianalysis.com/p/most-neoclouds-suck-at-security) — SemiAnalysis security piece on GPU-cloud ("neocloud") providers: container escapes, kernel bypass, network-policy gaps, exposed security keys, multi-tenant Grafana dashboards leaking across tenants, and a preview of ClusterMAX 3.0 (their neocloud security-rating framework). Not independently verified today (kept on feed summary) — out of highlight consideration.
