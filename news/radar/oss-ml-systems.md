---
category: oss-ml-systems
updated: 2026-08-19
---

# Radar: oss-ml-systems

Technical-radar items for this category (sources in [`config/radar.json`](../config/radar.json)).
Appended by the daily routine under weekly headings; format matches topics files.

## 2026-W33

- **2026-08-10** — [SGLang Adds Day-0 Support for Muse Glimmer](https://lmsys.org/blog/2026-08-10-meta-muse-glimmer) — SGLang ships day-0 inference support for Meta's new 30B open-weight Muse Glimmer model, built for local agentic workflows.
- **2026-08-10** — [Fast, On Device Agentic AI with Muse Glimmer on ExecuTorch](https://pytorch.org/blog/fast-ondevice-agentic-ai-with-executorch/) — ExecuTorch adds end-to-end support for running Meta's 30B Muse Glimmer model on-device (including NVIDIA backends) for local agentic workflows.
- **2026-08-10** — [vLLM v0.27.0](https://github.com/vllm-project/vllm/releases/tag/v0.27.0) — Routine vLLM release (tag v0.27.0); no release-note text available at fetch time.
- **2026-08-11** — [SGLang Adds Day-0 Support for NVIDIA Nemotron 3.5 Lightning](https://lmsys.org/blog/2026-08-11-nemotron-3-5-lightning) — SGLang ships day-0 inference support for NVIDIA's Nemotron 3.5 Lightning model.
- **2026-08-11** — [Unified Radix Cache: One Tree for Hybrid Model Prefix Caching](https://lmsys.org/blog/2026-08-11-unified-radix-cache) — A component-based radix tree unifies prefix caching across full attention, sliding-window attention, and Mamba recurrent state under one tree (replacing per-mechanism cache classes), with native multi-tier GPU/host/external caching; on DeepSeek-V4-Flash (4×H200) the L3 tier hit 98% cache rate at 145.5K tok/s vs 9.4K tok/s L1-only, and cut TTFT 2.9–16.6% on SWE-bench workloads vs an LRU baseline.
- **2026-08-12** — [vllm release v0.27.1](https://github.com/vllm-project/vllm/releases/tag/v0.27.1) — Routine vLLM release (tag v0.27.1); no release-note text available at fetch time.
- **2026-08-12** — [SGLang and Miles Add Day-0 Support for Qwen3.8-2.4T-A95B](https://lmsys.org/blog/2026-08-12-qwen3-8-day0-support) — Verified via WebFetch: SGLang plus Miles (a colocated-LoRA-training RL framework sharing hardware with inference) ship day-0 support for Qwen's largest open model (2.4T total / 95B active params), handling its hybrid architecture's three state types (KV cache, GDN recurrent state, conv windows) via a ReplaySSM mechanism for speculative-decode state recovery, plus prefill-decode disaggregation and Radix/HiCache prefix caching; on GB300, peak 5,126 tok/s/GPU (NVFP4), 334 tok/s per-user at low latency, 346 tok/s with MTP speculative decode.
- **2026-08-13** — [FP8 Training on AMD GPUs with TorchTitan and TorchAO: Upstreaming Performance Improvements](https://pytorch.org/blog/fp8-training-on-amd-gpus-with-torchtitan-and-torchao-upstreaming-performance-improvements/) — PyTorch upstreamed the AMD Instinct optimizations demonstrated at PyTorch Conference 2025 (linear scaling beyond 1,000 GPUs via AMD's Primus-Turbo library) directly into `pytorch/AO` and `pytorch/TorchTitan`, giving TorchTitan native AMD Instinct support with competitive FP8 training performance out of the box.

## 2026-W34

- **2026-08-18** — [Advanced CUDA Graph Techniques in SGLang](https://lmsys.org/blog/2026-08-17-advanced-cuda-graph) — Verified via WebFetch: SGLang's three CUDA-graph backends — full-graph capture, Breakable CUDA Graph (BCG, segments capture with eager breaks around incompatible ops instead of paying torch.compile cost), and TC Piecewise (torch.compile trace+split) — with measured numbers: BCG builds 3.8–5.2× faster than compiler-based piecewise (torch.compile alone was 78–86% of prefill-graph prep time), replay-latency speedups of 1.93× (full capture), 1.70× (BCG) and 1.45× (TC piecewise) vs eager, activation-memory peaks cut from 0.56GB to 0.001GB via chunked-prefill-size capture, and end-to-end diffusion latency down from 6.48s to 2.45s.
- **2026-08-18** — [Miles v0.1: Production-level Post-training](https://lmsys.org/blog/2026-08-18-miles-v0-1) — Verified via WebFetch: full-stack RL post-training system (rollout via SGLang, training via Megatron-LM/FSDP) with Token-In-Token-Out fidelity, Rollout Routing Replay for MoE numerical stability, NVFP4/MXFP8/FP8 training, and NVMe optimizer-state offload. Concrete numbers: GLM-5.2 744B trains on 64 GB300 GPUs at 96% prefix-cache hit rate; on-policy distillation cut Qwen3.5-35B rollout length 18.6K→~6K tokens while improving held-out accuracy 84.6%→89.5%; P2P weight sync for Kimi-K2 1T cut update time 53.3s→7.2s (disk-delta payload 62.4GB→0.69–0.83GB); day-0 support across NVIDIA A100–GB300 and AMD MI300X–MI355X.
