---
company: Hugging Face
aliases:
  - HF
  - HuggingFace
sources:
  - https://huggingface.co/blog/feed.xml
updated: 2026-09-05
---

MOC page for **Hugging Face** — AI-news items collected daily by the news routine (see [[workflow]]); newest week on top, one line per item.

## 2026-W36

- **2026-09-03** — [NeoMME: an efficient Multimodal-native and Multilingual Encoder](https://huggingface.co/blog/Hcompany/neomme) — H Company releases NeoMME (260M/800M), a unified encoder processing image patches and text in one transformer; the retrieval variant sets a new SOTA among sub-800M models on ViDoRe v3 with a 255x smaller index.
- **2026-09-03** — [Give Your Coding Agents a Memory You Own](https://huggingface.co/blog/funes) — Hugging Face introduces funes, a local-first memory layer indexing coding-agent session traces into searchable datasets synced via private HF datasets; recall measured 4-8x cheaper than a written handoff. Backfilled: missed by the 2026-09-04 gap-scrape (feed showed 304-not-modified), confirmed today.
- **2026-09-03** — [Fine-tuning a 350M Model for Better Structured Outputs in 100 GRPO Steps](https://huggingface.co/blog/grpo-with-trl-ifstruct) — Hugging Face and Liquid AI show GRPO fine-tuning of LFM2.5-350M lifting IFStruct accuracy 22.6%→29.7% in 100 steps on ~500 samples via a ~1.66%-of-model LoRA adapter. Backfilled: missed by the 2026-09-04 gap-scrape (feed showed 304-not-modified), confirmed today.
- **2026-09-03** — [Training a coding model to paint watercolours with TRL and OpenEnv](https://huggingface.co/blog/train-to-paint-with-code) — Hugging Face reproduces an RL pipeline (TRL GRPO) training a 35B Qwen coding model to paint watercolours via p5.brush, scored against 178 curated reference paintings with a multi-component reward. Backfilled: missed by the 2026-09-04 gap-scrape (feed showed 304-not-modified), confirmed today.
- **2026-09-02** — [Real-Time Intelligence with IBM Time Series Models on Confluent](https://huggingface.co/blog/ibm-research/real-time-intelligence) — IBM Research and Confluent launch early access integrating IBM's Granite Time Series foundation models (PatchTST-FM, FlowState, TTM, TSPulse) into Confluent Cloud via Apache Flink SQL functions for real-time forecasting/anomaly detection.
- **2026-09-01** — [BenchMIRT: What are LLM benchmarks actually measuring?](https://huggingface.co/blog/allenai/benchmirt) — Allen Institute for AI applies multidimensional Item Response Theory to 100 LLMs across 16 benchmarks (34,000+ questions), finding benchmarks often measure safety vs. general-reasoning dimensions differently than labeled (e.g. WMDP tracks reasoning, not safety); predicts held-out question performance 79% vs. 70% for baseline.
- **2026-08-31** — [VLANeXt: A Simple and Research-Oriented Codebase for Robotics Research](https://huggingface.co/blog/cavanloy/vlanext) — A research-oriented vision-language-action (VLA) codebase distilling design recipes from 500+ experiments, with six baselines hitting SOTA on LIBERO and real-world manipulation benchmarks.
- **2026-08-31** — [Technical writing in the agentic era](https://huggingface.co/blog/joelniklaus/technical-writing-in-the-agentic-era) — An essay arguing that as AI agents generate content quickly, editorial judgment — what to highlight, how to present it, which evidence to include — becomes the scarce, valuable work.

## 2026-W35

- **2026-08-26** — [Training and Finetuning Multi-Vector Embedding Models with Sentence Transformers](https://huggingface.co/blog/train-multi-vector-encoder) — Hugging Face publishes a guide to training ColBERT-style multi-vector embedding models, with a medical-retrieval model beating 50+ general-purpose models after 14.5 hours of finetuning on a single RTX 3090.
- **2026-08-25** — [Granite 4.2 LLMs: How They're Built](https://huggingface.co/blog/ibm-granite/granite-4-2) — IBM releases Granite 4.2, its first family of dense decoder-only reasoning LLMs (3B/8B/30B) with a thinking/non-thinking toggle, agentic RL training, and native tool calling, under Apache 2.0.
- **2026-08-25** — [Quantization-Aware Healing: a compressed, 4-bit model that outperforms its full-precision original](https://huggingface.co/blog/MultiverseComputingCAI/quantization-aware-healing) — Multiverse Computing distills a 4-bit MXFP4 student directly from the full-precision teacher, compressing GPT-OSS 120B to 60B while beating its own 16-bit original on 7 of 9 benchmarks.
- **2026-08-25** — [Wire It, Run It, Deploy It: AI Workflows in Gradio](https://huggingface.co/blog/gradio-workflow-guide) — Hugging Face announces gr.Workflow, a new Gradio feature turning multi-step AI pipelines into a visual drag-and-drop interface with automatic REST-endpoint generation and one-command Spaces deployment.

## 2026-W34

- **2026-08-20** — [Up to 3.2x Faster Inference with LFM2.5-DSpark](https://huggingface.co/blog/LiquidAI/lfm25-dspark) — Liquid AI releases LFM2.5-DSpark draft-model checkpoints using speculative decoding, speeding up decoding up to 2.87x on H100 and 2.54x on MacBook M4 Max with identical output quality.
- **2026-08-19** — [LFM2.5 Q4_0 Checkpoints from Quantization-Aware Distillation](https://huggingface.co/blog/LiquidAI/qad) — Liquid AI releases QAD Q4_0 checkpoints for four LFM2.5 models (230M–2.6B), recovering ~96.5–97.4% of BF16 accuracy at 3–33% higher decode throughput on MacBook Pro, NucBox EVO-X2, Galaxy S26 Ultra, and Raspberry Pi 5.
- **2026-08-18** — [How Much Memory Does Your Agent Actually Need?](https://huggingface.co/blog/ibm-research/altk-evolve-hmm) — IBM Research's ALTK-Evolve framework finds optimal agent memory strategy depends on model strength: curated retrieval helps weak models most, full guideline injection helps strong models, saturated models see no gain.

- **2026-08-17** — [Same Cluster, 33 Points More Utilization: What Changed Was the Order](https://huggingface.co/blog/Dharma-AI/gpu-management-pt2) — Dharma AI's constraint-aware GPU allocator lifts cluster utilization by up to 33pp over FIFO scheduling and priority-weighted output by 52% on average, part 2 of a GPU-management series.

## 2026-W33

- **2026-08-14** — [State of Open Models: Summer 2026 Observations](https://huggingface.co/blog/state-of-open-models-summer-2026) — Hugging Face publishes a data-driven ecosystem analysis: Chinese labs now dominate frontier-scale releases, Qwen dominates the Hub's derivative ecosystem (151K+ derivatives), and small/quantized models capture the overwhelming majority of real-world downloads.
- **2026-08-13** — [Record, train, and deploy from one place with Strands Agents, LeRobot, and Hugging Face Storage Buckets](https://huggingface.co/blog/amazon/strands-lerobot-streaming-data-loop) — AWS Strands Robots SDK closes the full robot-learning data loop with Hugging Face Storage Buckets and streaming LeRobot training.
- **2026-08-12** — [LFM2.5-VL-3B for Better and Faster Vision Capabilities for the Edge](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-3b) — Liquid AI releases LFM2.5-VL-3B, a 3.1B-parameter vision-language model for edge deployment with strong screen/UI understanding and 228 tok/s on M5 Max.
- **2026-08-12** — [Introducing OlmoEarth embeddings: Custom embedding exports from OlmoEarth Studio for downstream analysis](https://huggingface.co/blog/allenai/olmoearth-embeddings) — Allen AI adds custom embedding exports (Nano/Tiny/Base encoders) to OlmoEarth Studio for downstream satellite-imagery analysis.
- **2026-08-11** — [Thinking of ACE? We Can Do It with Fewer Tokens](https://huggingface.co/blog/ibm-research/altk-evolve-sldd) — IBM Research compares its ALTK-Evolve agentic-memory framework against ACE, reaching comparable-or-better accuracy at 15-40% of ACE's inference token cost.

## 2026-W32

- **2026-08-07** — [TutorMoments: Do AI tutors know when to help and when to hold back?](https://huggingface.co/blog/allenai/tutormoments) — Allen Institute for AI publishes TutorMoments, an evaluation framework measuring whether LLMs appropriately balance giving instructional help versus encouraging students to think independently during math tutoring.
- **2026-08-06** — [Baseten on Hugging Face Inference Providers](https://huggingface.co/blog/baseten) — Baseten becomes an integrated inference provider on Hugging Face Hub, letting developers access frontier language models through the Hub's website and client SDKs.
- **2026-08-04** — [Deploy local agents everywhere with LFM2.5-2.6B](https://huggingface.co/blog/LiquidAI/lfm2-5-2-6b) — A guide to deploying local agents everywhere using the LFM2.5-2.6B model, published on the Hugging Face blog.

## 2026-W31
