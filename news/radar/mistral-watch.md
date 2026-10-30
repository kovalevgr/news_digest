---
category: mistral-watch
updated: 2026-10-30
---

# Radar: mistral-watch

Technical-radar items for this category (sources in [`config/radar.json`](../config/radar.json)).
Appended by the daily routine under weekly headings; format matches topics files.

## 2026-W42

- **2026-10-16** — [mistralai/Timestral](https://www.reddit.com/r/LocalLLaMA/comments/1x6ouoy/mistralaitimestral/) — Reddit self-text post quoting Mistral's own HF model card (content already in hand): Timestral is Mistral's family of time-series foundation models for zero-shot forecasting (univariate + multivariate, past-only and past+future-covariate inputs), released in 5M/28M/123M/209M-parameter sizes — this thread covers the 209M checkpoint. **First item in this file** — not caught by the 3 dedicated mistral-watch sources this run (`mistral-hf-org`/`mistral-releases`/`mistral-docs-changelog` all returned zero fresh), surfaced instead via the general community/reddit source and filed here per `interests.md`'s "Mistral: everything" special watch (so the run-log's mistral-watch raw-candidate count, which reflects only the dedicated sources' JSON output, reads 0 against this 1 confirmed item — the discrepancy is this cross-filing, not an error). "Mistral: everything" HIGH fit — a new model family, not yet checked against `topics/mistral.md` (today's company-core run, 06:00 UTC, hasn't happened yet).

## 2026-W44

- **2026-10-30** — ⭐ [mistralai/Mistral-Large-4-1T-A52B](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) — Verified via WebFetch (model card): Mistral Large 4 ("Le Chonk") weights are live on Hugging Face — the ~1T-parameter/49B-active (52B incl. embeddings/output) natively-multimodal MoE Mistral teased in its 2026-10-21 NVIDIA-engineering post ("weights planned end of October," see [[mistral]]) has now actually shipped. Architecture: 128 routed experts (4 active/token) + 1 shared expert, Pixtral-style vision encoder, 1M-token context, text+image input/text output, trained from scratch on 3,800 NVIDIA Grace Blackwell GPUs in Mistral's own EU datacenters. Benchmarks on the card: Artificial Analysis Coding Agent Index 48% (tied with GLM-5.3, using 47% fewer tokens/task); AA Intelligence Index v5: 26, highest among western open-weight models (some Chinese open-weight models score higher). Ships an embedded DSpark speculative-decoding draft head (3 dense MLA layers, up to 1.9x throughput). License: Mistral Ecosystem Open-Weight License (modified MIT) — commercial and non-commercial use is free; a separate license is needed only to resell it as a hosted Model-as-a-Service. Also live on the Mistral API as `mistral-large-4`; NVFP4-quantized checkpoint and llama.cpp GGUF builds already up; recommended serving via vLLM (SGLang/Transformers/llama.cpp also supported); fine-tunable with Axolotl/Unsloth/TRL. "Mistral: everything" — direct hit on the dedicated special-watch bucket, and today's single biggest radar story: confirms the release yesterday's company-core daily run found only an unconfirmed secondhand public-preview-date claim about and declined to add.
