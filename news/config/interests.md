# Owner interest profile — radar triage weights

Used by the daily radar (TRIAGE pass 2 and HIGHLIGHT selection in
[`workflow.md`](../workflow.md)). **The owner edits this file freely; the routine
reads it and never rewrites it.** Drafted 2026-08-09 from the radar design
conversation — owner: adjust weights and add/remove topics as taste sharpens.

## HIGH (highlight-worthy)

- AI agents in practice: coding agents, agent harnesses, context engineering,
  agent memory, multi-agent orchestration
- Local / self-hosted models: inference engines (vLLM, SGLang, llama.cpp),
  quantization, serving cost/perf, "runs on my hardware" stories
- MCP and the agent-tool ecosystem
- Evals in practice: how people actually measure agents and models
- **Mistral: everything** (models, tooling, API changes) — special watch
- Reproducible techniques WITH CODE that could become a small own experiment

## MEDIUM

- RAG / retrieval engineering, embeddings
- GPU / kernel engineering (CUDA, Triton) — deep interest, higher effort to act on
- Training & fine-tuning practice (LoRA, RL for LLMs, distillation)
- Engineering post-mortems and "how we built X" from big-tech AI systems

## LOW (rarely a highlight, still radar-file-worthy if technically strong)

- Pure academic papers without released code
- Robotics / 3D / video generation
- Hardware-market and business analysis (SemiAnalysis finance posts etc.)

## The article lens

When scores tie, prefer the item that could seed a piece the owner writes:
a `tech_explainer` (how X actually works) or a `project_post` (I built / tried X).
