# Companies — human/Obsidian view of `sources.json`

The machine-readable truth is [`sources.json`](sources.json); this page mirrors it for
browsing in Obsidian. Tiers: **rss** = TIER-1 (fetched by `scripts/fetch_feeds.py` every
run), **fetch** / **jina** = gap-scrape ladder (used only when a company has zero fresh
TIER-1 candidates).

> [!warning] TRAP URLs — never add these to config
> - `https://cursor.com/rss.xml` — returns 200 with an **HTML page**, not a feed. Use `cursor.com/changelog/rss.xml`.
> - `https://cohere.com/blog/rss.xml` — returns 200 with an **HTML page**, not a feed. Cohere has no working feed; use `fetch` on `cohere.com/blog`.

## OpenAI

- Topics page: [[openai]]
- rss: <https://openai.com/news/rss.xml>

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
- rss: <https://news.microsoft.com/source/feed/> — fresher than `blogs.microsoft.com/feed/`

## NVIDIA

- Topics page: [[nvidia]]
- rss: <https://blogs.nvidia.com/feed/>

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

## Cohere

- Topics page: [[cohere]]
- fetch: <https://cohere.com/blog> — see TRAP warning above
