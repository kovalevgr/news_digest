---
kind: source
title: "Tencent Hy4-preview model card (Hugging Face)"
url: https://huggingface.co/tencent/Hy4-preview
fetched: 2026-09-05
note: WebFetch-verified 2026-09-05; weights dropped 2026-08-27
---

- 770B total / 49B active MoE (78 layers: 1 dense + 77 MoE, 256 routed + 1 shared expert, top-8), Apache 2.0, 1M context, Gated DeepSeek Sparse Attention with IndexCache, native MTP layer for speculative decoding.
- SWE-Bench Pro 65.7%; SWE-Bench Multilingual 82.9%; Deep-SWE 64.3%; Terminal-Bench 2.1 85.4%; SkillsBench V1.1 62.9%; GPQA Diamond 92.3%; Toolathlon Verified 74.1%; Apex Agents 37.1%.
- Blind human eval, 163 internal Tencent experts, 203 engineering tasks: Hy4-preview 2.99 avg vs GLM 5.3 2.92 (46.8% wins / 12.8% ties / 40.4% losses) and vs Kimi K3 2.94 (51.2% / 7.9% / 40.9%).
