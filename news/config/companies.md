# Companies — human/Obsidian view of `sources.json`

The machine-readable truth is [`sources.json`](sources.json); this page mirrors it for
browsing in Obsidian. Tiers: **rss** = TIER-1 (fetched by `scripts/fetch_feeds.py` every
run), **fetch** / **jina** = gap-scrape ladder (used only when a company has zero fresh
TIER-1 candidates).

> [!note] 2026-08-08 technical-first refocus
> The company core was re-pointed at technical channels (audit in
> `news/research/2026-08-08-technical-sources.md`): OpenAI got a category filter,
> Microsoft and NVIDIA were swapped to their research/developer blogs, Cohere was cut.
> Everything beyond company news lives in the **radar** — see [`radar.json`](radar.json).

> [!warning] TRAP URLs — never add these to config
> - `https://cursor.com/rss.xml` — returns 200 with an **HTML page**, not a feed. Use `cursor.com/changelog/rss.xml`.
> - `https://cohere.com/blog/rss.xml` — returns 200 with an **HTML page**, not a feed. Cohere has no working feed; use `fetch` on `cohere.com/blog`.

## OpenAI

- Topics page: [[openai]]
- rss: <https://openai.com/news/rss.xml> — category filter `{Product, Engineering, Research, Publication, Release}`, fail-closed (uncategorized = customer stories / influence-ops reports)

## Anthropic

- Topics page: [[anthropic]]
- fetch: <https://www.anthropic.com/news> — no feed exists

## Google DeepMind

- Topics page: [[google-deepmind]]
- rss: <https://deepmind.google/blog/rss.xml>

## Google Research

- Topics page: [[google-research]]
- rss: <https://research.google/blog/rss/> — trailing slash REQUIRED (`/blog/rss.xml` is 404)

## Microsoft

- Topics page: [[microsoft]]
- rss: <https://www.microsoft.com/en-us/research/feed/> — Microsoft Research blog (swapped 2026-08-08 from the Source newsroom; needs full browser headers, configured in sources.json)

## NVIDIA

- Topics page: [[nvidia]]
- rss: <https://developer.nvidia.com/blog/feed> — NVIDIA Technical Blog (swapped 2026-08-08 from the corporate newsroom; high volume — agent keeps only genuine announcements/major posts)

## xAI

- Topics page: [[xai]]
- jina: <https://x.ai/news> — Cloudflare blocks direct fetch; Jina-only

## Mistral AI

- Topics page: [[mistral]]
- rss: <https://mistral.ai/rss.xml>

## Hugging Face

- Topics page: [[huggingface]]
- rss: <https://huggingface.co/blog/feed.xml> — do NOT use Jina for HF (451)

## Cursor

- Topics page: [[cursor]]
- rss: <https://cursor.com/changelog/rss.xml> — see TRAP warning above

## Perplexity

- Topics page: [[perplexity]]
- jina: <https://www.perplexity.ai/hub/blog> — anonymous Jina → 403 AbuseAlleviation; needs `JINA_API_KEY`, else WebSearch fallback

## Cohere — REMOVED 2026-08-08

- Cut in the technical-first audit (0.0 technical ratio — pure enterprise/policy PR).
- [[cohere]] topics page stays as history. The rss TRAP warning above still applies —
  never re-add `cohere.com/blog/rss.xml`.
