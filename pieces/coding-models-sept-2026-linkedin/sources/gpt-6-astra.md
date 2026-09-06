---
kind: source
title: "GPT-6 Astra — Latent Space hands-on + Simon Willison pelican grid (openai.com page itself returned 403 to WebFetch)"
url: https://www.latent.space/p/astra
url2: https://simonwillison.net/2026/Sep/4/astra-pelicans/
url3: https://openai.com/index/gpt-6-astra/
fetched: 2026-09-05
note: latent.space and simonwillison.net WebFetch-verified 2026-09-05; openai.com facts below come from web-search snippets only and are flagged
---

## Latent Space (verified)
- Launched 2026-09-03; authors had early access, burned 20B+ tokens of Astra in testing.
- Described as a "lightly looped" model; "fully capable AI Engineers in their own right".
- OpenAI-claimed: FrontierMath 97.6%, ARC-AGI-3 99.9%; "cleanly beating Fable 5.1 on many metrics" (authors' phrasing).
- Authors' measured: under $6/hour for practical engineering tasks with their parallel-agent usage; 33 tokens/s; $50 per million output tokens; $10/M input mentioned.
- More token-efficient than Sol and Fable (authors say confirmed by Artificial Analysis).
- Caveats: authors say they are "not qualified to talk about" standard OpenAI benchmarks; $6/hr is their own usage pattern.

## Simon Willison, 2026-09-04 (verified)
- Pricing: Astra $10/M input, $50/M output; GPT-5.6 Sol $5/M input, $30/M output.
- Pelican SVG benchmark across 5 effort levels vs GPT-5.6 Sol/Terra/Luna.
- Exact quote: "Astra low produces a better pelican than ANY of the GPT-5.6 Sol models at any level, for 9.55 cents."
- Astra/Luna use 16 input tokens for the prompt vs 26 for Sol/Terra (tokenizer difference).

## openai.com announcement (NOT fetched — search snippets only) [unverified — owner to check]
- API id `gpt-6-astra`, 1M-token context.
- DeepSWE v1.1 74.1%; OSWorld 2.0 72.6% at ~40 min/task vs GPT-5.6 Sol 65.7% at ~75 min; FrontierMath Tier 4 "98%".
- Staged rollout; cyber-sensitive capabilities gated behind a trusted-access program.
