---
kind: source
title: "Qwen3.8-27B model card (Hugging Face)"
url: https://huggingface.co/Qwen/Qwen3.8-27B
fetched: 2026-09-05
note: WebFetch-verified 2026-09-05; released 2026-08-14
---

- 27B dense, Apache 2.0, 262,144 native context (extensible to 1M with RoPE scaling).
- Reasoning effort: `xhigh` (default), `medium`, `low`.
- SWE-bench Pro 61.7% ("best among dense models compared"); Terminal-Bench 2.1 73.0%; LiveCodeBench v6 90.3%; QwenSWEBench 79.0%; CoWorkBench 70.7%.
- Community context (radar, r/LocalLLaMA, August): runs at 262K context on a single RTX 5090 (NVFP4), 200k+ context on 16GB VRAM laptops, 124 tok/s single-request on an RTX 3090; Simon Willison noted it "defaults to wildly overthinking" at `xhigh`.
