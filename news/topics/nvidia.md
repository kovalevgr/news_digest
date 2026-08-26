---
company: NVIDIA
aliases:
  - Nvidia
sources:
  - https://blogs.nvidia.com/feed/
updated: 2026-08-26
---

MOC page for **NVIDIA** — AI-news items collected daily by the news routine (see [[workflow]]); newest week on top, one line per item.

## 2026-W35

- **2026-08-25** — [Restore LLM Inference Capacity in Seconds with Shadow Engine Recovery in NVIDIA Dynamo](https://developer.nvidia.com/blog/restore-llm-inference-capacity-in-seconds-with-shadow-engine-recovery-in-nvidia-dynamo/) — NVIDIA introduces Shadow Engine Recovery, a pre-warmed standby inference engine sharing GPU weights via a GPU Memory Service, cutting failover from a 283s cold restart to 7.3s (~39x faster).
- **2026-08-25** — [CUDA Python 1.0: Stable APIs, One Foundation, Full Platform Access](https://developer.nvidia.com/blog/cuda-python-1-0-stable-apis-one-foundation-full-platform-access/) — NVIDIA ships CUDA Python 1.0 with CUDA 13.3, unifying cuda.core/cuda.compute/cuda.bindings/nvmath-python under semantic versioning as the first stable, officially supported way to access the full CUDA platform from Python.
- **2026-08-24** — [NVIDIA Vera Rubin and Blackwell Set a New Standard for Agentic AI Performance per Watt](https://developer.nvidia.com/blog/nvidia-vera-rubin-and-blackwell-set-a-new-standard-for-agentic-ai-performance-per-watt/) — NVIDIA publishes SemiAnalysis AgentX benchmark results: Vera Rubin NVL72 up to 30x higher AI-factory throughput/MW than GB300 NVL72 on DeepSeek V4-Pro; GB300 up to 15x over H200 NVL8.
- **2026-08-24** — [NVIDIA BlueField-4 Powers New Scale-In Network Infrastructure for Agentic AI Factories](https://developer.nvidia.com/blog/nvidia-bluefield-4-powers-new-scale-in-network-infrastructure-for-agentic-ai-factories/) — NVIDIA introduces Scale-In, a fifth AI-networking pillar built on the BlueField-4 DPU (800 Gb/s, 4x memory/2x network bandwidth over BlueField-3), offloading security/storage/telemetry from host CPUs.
- **2026-08-24** — [How NVIDIA Groq 3 LPX Unlocks Ultrafast Interactivity at Long Context on NVIDIA Vera Rubin](https://developer.nvidia.com/blog/how-nvidia-groq-3-lpx-unlocks-ultrafast-interactivity-at-long-context-on-nvidia-vera-rubin/) — NVIDIA publishes benchmarks for its Groq 3 LPX inference accelerator on Vera Rubin NVL72: 3,431 tok/s on Artificial Analysis 100K-context, 4,767 tok/s median on SPEED-Bench.
- **2026-08-24** — [Giga-Scale AI and the Ethernet Evolution: How Spectrum-X Ethernet Rewrites the Rules](https://developer.nvidia.com/blog/giga-scale-ai-ethernet-evolution-spectrum-x-ethernet-rewrites-rules/) — NVIDIA details Spectrum-X Ethernet architecture for giga-scale AI factories, claiming 98% line-rate throughput and 400x faster failover recovery (2.68ms vs 1.08s) at up to 512,000 GPUs.
- **2026-08-24** — [Solving Agentic AI Fleet Challenges with NVIDIA Vera CPU](https://developer.nvidia.com/blog/solving-agentic-ai-fleet-challenges-with-nvidia-vera-cpu/) — NVIDIA details Vera CPU for agentic workloads, citing telemetry from 163,000+ agentic sessions (97%+ unique profiles) and up to 1.5x per-core performance over AMD Venice CPUs.

## 2026-W34

- **2026-08-21** — [NVIDIA AVO Reaches 100% on ARC-AGI-3, Demonstrating a Frontier-Level General-Purpose Architecture for Long-Horizon Autonomous Agents](https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/) — NVIDIA's AVO agent architecture (built on Claude Opus 5) hits a perfect 100.00 RHAE score on ARC-AGI-3's public set, up from Claude Opus 5's 30% baseline alone, showing architecture — not just the model — drives frontier agent performance.
- **2026-08-21** — [Maximizing AI Factory Performance per Watt with NVIDIA DSX MaxLPS](https://developer.nvidia.com/blog/maximizing-ai-factory-performance-per-watt-with-nvidia-dsx-maxlps/) — NVIDIA details DSX MaxLPS, combining dynamic power allocation, perf-per-watt optimization, and 45°C liquid cooling for up to 40% more Rubin GPU capacity in the same power budget.
- **2026-08-20** — [How Generative Recommenders Are Redefining RecSys at Scale](https://developer.nvidia.com/blog/how-generative-recommenders-are-redefining-recsys-at-scale/) — NVIDIA details generative recommenders (HSTU, Semantic IDs) that reframe recommendation as sequence prediction, with production-scale H100 training/inference numbers and two open-source repos.
- **2026-08-19** — [Evaluating AI Agent Skill Performance with NVIDIA SkillEvaluator](https://developer.nvidia.com/blog/evaluating-ai-agent-skill-performance-with-nvidia-skillevaluator/) — NVIDIA releases SkillEvaluator, an open-source three-tier framework (static checks, distinctiveness analysis, live agent evaluation) measuring AI agent skill impact, benchmarked at +31 avg Skill Lift across 300+ verified skills in 30+ NVIDIA products.
- **2026-08-18** — [How AI Coding Agents Can Unlock Materials Simulation with NVIDIA ALCHEMI Toolkit](https://developer.nvidia.com/blog/how-ai-coding-agents-can-unlock-materials-simulation-with-nvidia-alchemi-toolkit/) — NVIDIA pairs its ALCHEMI Toolkit (GPU-accelerated MLIP framework) with an Agent Skills Library so coding agents generate correct atomistic-simulation code, validated across 45 benchmark pipelines.

- **2026-08-17** — [Developing Nemotron 3.5 Lightning NVFP4 with QAD Using NVIDIA Model Optimizer](https://developer.nvidia.com/blog/developing-nemotron-3-5-lightning-nvfp4-with-qad-using-nvidia-model-optimizer/) — NVIDIA details a Quantization-Aware Distillation pipeline compressing Nemotron 3.5 Lightning from 66GB to 22GB (NVFP4) while recovering up to 99.7% of baseline accuracy.

## 2026-W33

- **2026-08-12** — [Serve Qwen3.8-2.4T-A95B, a 2.4T-Parameter Model, with Configurable Reasoning on NVIDIA GB300 NVL72](https://developer.nvidia.com/blog/serve-qwen3-8-2-4t-a95b-a-2-4t-parameter-model-with-configurable-reasoning-on-nvidia-gb300-nvl72/) — NVIDIA details day-0 serving of Alibaba's Qwen3.8-2.4T-A95B (its largest open-weight model) on GB300 NVL72, reaching 4K+ tok/s per GPU in FP8.
- **2026-08-11** — [NVIDIA Nemotron 3.5 Lightning Delivers Fast, Accurate Specialized Task Execution for Long-Running Agents](https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/) — NVIDIA releases Nemotron 3.5 Lightning, an open-weight 30B (3B-active) MoE model built for the fast execution layer of long-running agents.
- **2026-08-11** — [Route AI Agent Workloads Across Models with NVIDIA NeMo Switchyard](https://developer.nvidia.com/blog/route-ai-agent-workloads-across-models-with-nvidia-nemo-switchyard/) — NVIDIA open-sources NeMo Switchyard, a provider-agnostic SDK routing agent workloads across models by capability, cost, and infra signals.
- **2026-08-11** — [NVIDIA JetPack 7.2.1 Adds Agentic Video Skills and T3000 Emulation](https://developer.nvidia.com/blog/nvidia-jetpack-7-2-1-adds-agentic-video-skills-and-t3000-emulation/) — NVIDIA releases JetPack 7.2.1 for Jetson, adding an agentic video-skills layer and T3000-performance emulation on Thor AGX T5000.

## 2026-W32

- **2026-08-08** — [Firebird Launches CIS Region's Largest AI Factory in Armenia](https://blogs.nvidia.com/blog/firebird-ai-factory-armenia-blackwell-rubin-dsx) — Firebird, an emerging AI cloud, launches the CIS region's largest AI factory in Armenia, built on NVIDIA accelerated computing and Dell Technologies infrastructure; NVIDIA to invest in Firebird.
- **2026-08-06** — [Into the Omniverse: How Open World Models Push the Frontier of Physical AI](https://blogs.nvidia.com/blog/open-world-models-physical-ai) — NVIDIA discusses how open world models are pushing the frontier of physical AI, following the "Open Weights and American AI Leadership" letter signed by 200+ companies and organizations.
- **2026-08-05** — [NVIDIA and Partners Build in America, for America](https://blogs.nvidia.com/blog/nvidia-and-partners-build-in-america-for-america/) — NVIDIA and its partners are investing in American manufacturing, supply chains, energy grids, and skilled workforces to build AI infrastructure.
- **2026-08-04** — [NVIDIA Joins NSF State and Regional AI Hubs Program to Expand AI Research and Education Across the US](https://blogs.nvidia.com/blog/nsf-state-regional-ai-hub-program) — NVIDIA joins the NSF's State and Regional AI Infrastructure Hubs program, expanding access to computing, data, and expertise for AI-enabled research and education.
- **2026-08-04** — [NVIDIA Alpamayo 2 Super, the Frontier Open Model for Robotaxis and Autonomous Vehicles, Now Available for Commercial Use](https://blogs.nvidia.com/blog/alpamayo-2-super-open-model-now-available) — NVIDIA releases Alpamayo 2 Super, an open model for robotaxis and autonomous vehicles, for commercial use.
- **2026-08-04** — [As AI Increases Demands on Memory, Storage Steps Up](https://blogs.nvidia.com/blog/ai-storage-fms) — NVIDIA discusses how surging AI demands for datasets and context windows are driving new storage architecture needs.
- **2026-08-04** — [AI Leaders Propose SAFE Guidelines for Cybersecurity Transparency](https://blogs.nvidia.com/blog/open-secure-ai-alliance-contributions) — The Open Secure AI Alliance and Linux Foundation propose SAFE guidelines for agentic AI cybersecurity transparency, coinciding with Black Hat.

## 2026-W31
