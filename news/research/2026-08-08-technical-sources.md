# Technical-first source analysis — verified 2026-08-08

Second research pass (after [[2026-08-08-inspiration-sources]]): the owner wants a
**technical-first** focus — engineering/how-it-works/benchmarks content, not business PR.
An 11-track workflow (1 local audit + 8 new technical categories + 2 re-scores) verified
every endpoint live and sampled real recent titles. `tech` = technical_ratio: share of
the ~10 most recent items that are genuinely technical.

## Audit of the current 12 sources (from collected topics/*.md, W31–W32)

Overall: only ~40% of collected items are technical. The skew comes from WHICH page is
tracked, not which company.

| Company | tech | Verdict |
| --- | --- | --- |
| OpenAI /news | 0.25 | **Keep + filter**: feed items carry `<category>` tags (Research 194 / Engineering 18 / Publication 30 / Release 7 vs Product/Company/Global Affairs). Filtering to {Engineering, Research, Publication, Release} → clean ~0.25/day technical stream. `openai.com/research/rss.xml` does NOT exist (404 that looks 200 — HTML error page). |
| Anthropic /news | 0.5 (n=2) | Keep (only release channel) + **add** anthropic.com/engineering |
| DeepMind blog | 0.5 | Keep — effectively their technical blog |
| Google Research | n/a | Keep — **0 items in 8 days; investigate cursor/feed silence** |
| Microsoft Source | 0.5 | **Swap** → Microsoft Research feed (Source's technical items are syndicated from there) |
| NVIDIA corporate | 0.29 | **Swap** → developer.nvidia.com Technical Blog |
| xAI /news | 0.5 | Keep (coverage; model launches only) |
| Mistral | 1.0 (n=1) | Keep |
| Hugging Face blog | 0.67 | Keep — technical gem |
| Cursor changelog | n/a | Keep — 0 items in 8 days; check cadence |
| Cohere blog | 0.0 | **Cut**. Candidate replacement: Cohere Labs research (unverified) |
| Perplexity hub | 0.0 | **Cut** |

## New technical sources — ADOPT (verified endpoints)

### Lab engineering / research
- fetch `https://www.anthropic.com/engineering` — tech 1.0, ~2–3/mo. No feed; grep `href="/engineering/..."` slugs, dedup by slug. Exactly the owner's genre (postmortems, agent-building, context engineering).
- rss `https://developer.nvidia.com/blog/feed` — tech ~1.0, ~1.45/day (needs topic filter: feed has category tags; pick genAI/agents/inference). TRAP: 736KB, 100 entries, ordered by `<updated>` not `<published>` — sort yourself.
- rss `https://www.microsoft.com/en-us/research/feed/` — tech 1.0, ~0.25/day. TRAP: 403 with simple UA; needs full browser headers (Chrome UA + Accept + Accept-Language).
- rss `https://openai.com/news/rss.xml` — existing source, add category filter (see audit).
- rss `https://machinelearning.apple.com/rss.xml` — tech 1.0 but academic paper drops, ~0.9/day. OPTIONAL if research quadrant feels thin.
- SKIP: Meta AI blog (no feed, curl 400, Jina-only, glacial cadence, product-skewed); OpenAI Cookbook (feed chain 404s; developers.openai.com/rss.xml is an undated docs catalog); Google Developers Blog (works but ZERO date fields → breaks cursor fetching).

### Inference / GPU infra
- rss `https://modal.com/blog/atom.xml` — tech 0.65, ~0.3/day. Filter title pattern "now available on Modal".
- rss `https://www.together.ai/blog/rss.xml` — tech 0.7, ~0.55/day. Filter titles starting "Together AI announces/partners".
- fetch `https://www.baseten.co/blog/` — tech 0.65, ~0.8/day, deepest content in the niche (18x tokenization speedup). NO feed (real 404s); titles in h3/h4 server-side, plain WebFetch works. OPTIONAL (fetch-tier cost).
- SKIP: Groq (0.05 — pure funding/partnership PR), Fireworks (no feed + ~half noise), Cerebras (no feed, coin-flip ratio), Lambda (feed fine, generalist thought-leadership, wrong depth), Replicate (dormant since May, acquired by Cloudflare).

### OSS ML systems
- rss `https://vllm.ai/blog/rss.xml` — tech 0.9, ~0.45/day. Must-have. TRAP: old blog.vllm.ai serves 404-as-200 for /feed.xml; site moved.
- fetch `https://lmsys.org/blog/` — tech 0.9, ~0.4/day. IS the SGLang blog (SpecForge, Miles RL, SGL-Diffusion). NO feed; posts array embedded as escaped JSON in Next.js flight data — regex the raw HTML (do NOT strip script tags).
- rss `https://pytorch.org/blog/feed/` — tech 0.5 raw → ~0.9 filtered, ~0.34/day. Drop Foundation/conference/community items by WordPress category + keywords.
- rss `https://blog.eleuther.ai/index.xml` — tech 0.9 but alignment/interp flavor, ~6 posts/yr. OPTIONAL passive slot.
- SKIP: Ollama blog (thin release notes; working path is /blog/rss.xml, /blog/rss is a trap; CDATA titles need real XML parser), Modular (corporate drift post-Qualcomm-acquisition).

### Big-tech engineering
- rss `https://github.blog/ai-and-ml/feed/` — tech 0.6, ~2–3/wk, 100% AI by construction. Filter "for Beginners"/"guide to" Copilot-education titles.
- rss `https://netflixtechblog.com/feed` — tech 1.0, ~1.4/wk total, ~40% AI (LLM serving, GenRec). Medium feed truncates content:encoded.
- rss `https://blog.cloudflare.com/tag/ai/rss/` — tech 0.4 (measured during Agents Week burst of ~5/day; normal weeks <1/day, deeper). OPTIONAL with per-source daily cap (Innovation Weeks flood).
- SKIP: Uber (406/404 bot-blocked), Shopify (blog.atom = 200→HTML redirect trap, no feed), LinkedIn (no feed, client-rendered), Discord (blog-wide feed ~90% patch notes).

### Research institutes
- rss `https://bair.berkeley.edu/blog/feed.xml` — tech 0.9, ~1/mo, author-written deep dives.
- rss `https://allenai.org/rss.xml` — tech 0.8, ~0.24/day. TRAP: /blog 302s to /research app shell; use /rss.xml. Dedup by URL (feed contained a literal "(duplicate)" title).
- rss `https://www.answer.ai/index.xml` — tech 0.6, exactly the owner's genre, but dormant since 2026-03. Zero-cost passive slot.
- SKIP: Sakana (half Japanese corporate PR), Epoch (no RSS; astro-island JSON scrape; macro-analysis genre), CMU ML (1-item feed, quiet), Stanford CRFM (no feed, ~5 posts/yr, HELM-centric).

### Technical newsletters (beyond wave-1 Raschka/Interconnects)
- rss `https://cameronrwolfe.substack.com/feed` — tech 1.0, ~1/mo, full post bodies free. Unconditional adopt.
- rss `https://semianalysis.substack.com/feed` — tech 0.4 (~5/12 technical: NVL72 TCO, HBM4, CUDA-moat; rest finance/markets). OPTIONAL with per-item finance filter. **TRAP: `semianalysis.com/feed/` is 11 months STALE but returns valid-looking RSS and homepage autodiscovery still points there — never adopt that URL.**
- SKIP (dormant): The Gradient (1 post/6mo), Davis Blalock (dead since 2024-08), Ruder NLP News (dead since 2024-05). The Sequence: active but 0.75/day at ~50% depth — would eat the budget.

### Technical YouTube (channel RSS, no auth)
- `https://www.youtube.com/feeds/videos.xml?channel_id=UCJgIbYl6C5no72a0NUAPcTA` — GPU MODE, tech 1.0. TRAP: lectures appear twice (livestream + edited cut) — dedup by title similarity.
- `https://www.youtube.com/feeds/videos.xml?channel_id=UCfzlCWGWYyIQ0aLC5w48gBQ` — sentdex, tech 0.7, local-inference experimentation arc (matches "I tried X" format). OPTIONAL.
- `https://www.youtube.com/feeds/videos.xml?channel_id=UCtAcpQcYerN8xxZJYTfWBMw` — Umar Jamil, tech 1.0, DORMANT 19 mo; zero-cost passive slot.
- Wave-1 adopts still stand: AI Engineer `UCLKPca3kwwd-B59HNr-_lvA`, Karpathy, Latent Space.
- SKIP: Trelis (pivoted to ASR self-releases), 3Blue1Brown (math puzzles; watch as a human), Welch Labs (~50% merch/Shorts noise, no duration field to filter).

## Community layer — tuned for technical (re-scored)

- **HN via Algolia** (replaces hnrss for the radar — same data, better filtering; keeping both double-counts):
  union of 4–6 keyword queries at `points>10` (inference, quantization, RAG, MCP, fine-tuning, agents) + one `query=AI` at `points>50`; dedup on `objectID`. Expected ~1.5–2.5/day at ~0.85 tech. Proven: `query=inference` lifted tech from 0.5 → 0.9. TRAPS: query matches post BODY too (sanity-check downstream); points are snapshot-at-query — re-query a 2-day window to catch late risers.
- **Reddit**: narrow to `https://www.reddit.com/r/LocalLLaMA+LLMDevs/top/.rss?t=day&limit=25` — r/LocalLLaMA is ~0.8 tech (benchmarks, llama.cpp PRs, inference builds); r/ClaudeAI is ~0.25 tech (memes) and r/ChatGPTCoding contributed 0 — dropped. One fetch/day, browser UA mandatory.
- **Lobsters** `https://lobste.rs/t/ai.json` — tech 0.8, ~0.6/day. Do NOT filter by score (high scores select opinion essays); drop items co-tagged culture/philosophy/video; dedup by URL.
- **HF daily papers** `https://huggingface.co/api/daily_papers` — ~13/day raw. Take top 2–3/day by upvotes, REQUIRE `paper.githubRepo` non-empty (the try-it guarantee), keyword-bias agent/LLM/inference/retrieval over robotics/3D. Score yesterday's batch, not today's (upvotes lag).
- **Aggregator: exactly one** — `https://news.smol.ai/rss.xml` (tech 0.85): full-content weekday digest with an engineer's structure (benchmarks, architecture, "practical implications for engineers", /r/LocalLlama recap). Parse ONLY the first item (feed = 2.1MB full archive). **TRAP: all pubDates carry an identical regenerated time — cursor/dedup by issue URL slug, never pubDate.** Self-triages with "not much happened today" titles.
- SKIP: TLDR AI (0.6 but redundant vs smol.ai + company feeds; title-only RSS needs second fetch), Ben's Bites (0.2 — lifestyle), Import AI (0.5 — policy lens; owner weekend reading, not radar).

## Expected volume of the full adopted set

Roughly 10–15 items/day pre-triage: community ~4–6, OSS/infra blogs ~2.5, lab
engineering ~2 (with OpenAI filter + NVIDIA topic filter), big-tech ~0.7, institutes
~0.5, newsletters/YouTube ~0.5, smol.ai 1. Fits the ≤15–20/day lean budget with
headroom for burst days.
