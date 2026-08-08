# Inspiration-sources scout — verified 2026-08-08

Research artifact for the planned **radar** expansion (practitioner signal: what people
build, trends, ideas to try hands-on → articles). Every endpoint below was fetched live
on 2026-08-08 by a 10-agent scout; `verified` means an actual 200 with genuine
feed/JSON content (not an HTML trap). Fit scores: how well the category feeds
*ideas-to-try* / *trends*, 1–5.

## TL;DR ranking

| Category | Ideas | Trends | Verdict |
| --- | --- | --- | --- |
| Hacker News + Lobsters | 5 | 4 | Adopt. Show HN = "what builders ship"; Algolia JSON for keyword filtering |
| Reddit (practitioner subs) | 5 | 4 | Adopt via ONE multireddit RSS call/day (rate limits!) |
| GitHub | 5 | 5 | Adopt. Search API (new rising repos) + trending RSS mirror + releases.atom |
| Practitioner blogs | 5 | 4 | Adopt as TIER-1 group. 12 working no-auth feeds; also style references |
| YouTube talks | 5 | 4 | Adopt 3–5 hardcoded channel feeds (AI Engineer = highest value) |
| Newsletters/aggregators | 4 | 5 | Adopt AINews (smol.ai) daily; TLDR AI; Import AI weekly |
| HF papers/trending | 4 | 5 | Adopt daily_papers (upvote≥15–20) + trending snapshot-diff |
| X/Twitter | 4 | 5 | Direct = dead without $200/mo API. Proxy via AINews; nitter.net best-effort only |
| Launch trackers (PH) | 3 | 3 | Optional weekly scan; tagline-only, no vote filtering via feed |
| arXiv raw | 3 | 3 | Skip raw firehose (~300/day). HF daily papers IS the curation layer |

## Verified endpoints by category

### Hacker News + Lobsters (`hnrss.org`, `hn.algolia.com`, `lobste.rs`)

- rss `https://hnrss.org/show?points=100` — Show HN ≥100pts, ~3/day, all topics; body carries points/comments/self-text.
- api `https://hn.algolia.com/api/v1/search_by_date?tags=show_hn&query=AI&numericFilters=points%3E10&hitsPerPage=50` — ~4/day; has `created_at_i` → supports `numericFilters=created_at_i>UNIXTIME` cursor fetching; `objectID` = dedup key.
- api `https://hn.algolia.com/api/v1/search_by_date?query=%22LLM%22&tags=story&numericFilters=points%3E100&restrictSearchableAttributes=title&hitsPerPage=30` — title-exact trending stories, ~0.5/day/keyword; run per keyword (LLM, agent, RAG, MCP…). Quoted query + `restrictSearchableAttributes=title` kills typo-fuzz.
- api `https://lobste.rs/t/ai.json` — ~0.6/day, heavily curated; `.rss` twin exists (pick one). Related tag: `/t/vibecoding` (unverified).
- **TRAP:** `hnrss.org` `q=` param is flaky (502s/timeouts observed) — keyword filtering via Algolia only.
- **DEAD END:** Algolia `tags=front_page` = point-in-time snapshot, not a stream; use `points>100` on `tags=story` instead.

### Reddit (`www.reddit.com`)

- rss `https://www.reddit.com/r/LocalLLaMA+LLMDevs+ChatGPTCoding+ClaudeAI/top/.rss?t=day&limit=40` — BEST PICK: one call, 4 subs, valid Atom, `<category term="Sub">` per entry. Score-ranked across subs → big subs crowd out small; run a 2nd multireddit for small subs (r/MachineLearning+LLMDevs+ChatGPTCoding).
- r/MachineLearning: filter titles on `[P]` (project posts = the gems).
- **Constraints (verified):** browser User-Agent REQUIRED; anonymous bursts of 3–4 requests → 429 (back off 60s); keep to 1–2 multireddit calls per run total.
- **DEAD END:** anonymous JSON API (`.json`) → 403 block page since API changes; RSS delivers the same items.

### GitHub (`api.github.com`, `github.com`, `mshibanami.github.io`, opt. `api.ossinsight.io`)

- api `https://api.github.com/search/repositories?q=topic:llm+created:%3E2026-08-01+stars:%3E100&sort=stars&order=desc&per_page=10` — fast-rising NEW repos; unauth 10 req/min (confirmed in headers). Run 3–4 topic queries (llm/rag/agents/mcp), union+dedup. NEVER omit the `stars:` floor (without it: 5,474 repos/2wk).
- rss `https://mshibanami.github.io/GitHubTrendingRSS/daily/all.xml` — trending mirror, ~17 repos/day snapshot, today ~80% AI. **Quirks:** no per-item pubDate → dedup by repo link across days; item description embeds full README (470–714KB) → parse titles+links only. Language/weekly variants exist (`daily/python.xml`, `weekly/rust.xml`).
- rss `https://github.com/<owner>/<repo>/releases.atom` — verified: vllm (~2/mo, perfect), ollama (~5/wk, filter `-rc`), langchain (monorepo bumps, low-priority). Candidates: sglang, transformers, litellm.
- **NOISE WARNING:** `llama.cpp/releases.atom` = auto build releases (~6/day, titles `b6xxx`) — skip.
- Optional api `https://api.ossinsight.io/v1/trends/repos/?period=past_24_hours&language=Python` — richer event-score ranking, extra hostname.
- Fallback only: `https://github.com/trending?since=daily` HTML (575KB, no timestamps).

### Hugging Face extra (`huggingface.co` — same hostname as existing blog feed)

- api `https://huggingface.co/api/daily_papers?date=YYYY-MM-DD&limit=100` — ~25–35 papers/day; `paper.upvotes` → client-side threshold ≥15–20 leaves ~5–10/day. `paper.id` = arXiv id.
- api `https://huggingface.co/api/models?sort=trendingScore&limit=20` — leaderboard SNAPSHOT, not a feed → diff vs yesterday's top-20, report new entrants (~3–8/day). `&pipeline_tag=` scoping works. Dedup quant/LoRA derivatives by base name.
- api `https://huggingface.co/api/spaces?sort=trendingScore&limit=20` — same pattern; strong "try the demo" material.
- **Confirmed again:** r.jina.ai on huggingface.co → 403/451. Never route HF through Jina.

### arXiv (skip raw; precision tool only)

- Raw `https://rss.arxiv.org/rss/cs.AI` = 137 items on a single weekday (cs.LG 105, cs.CL 60, cross-listed), empty Sat/Sun, no quality signal → do not track.
- api `https://export.arxiv.org/api/query?search_query=cat:cs.CL+AND+abs:%22context+engineering%22&sortBy=submittedDate&sortOrder=descending&max_results=10` — usable for narrow standing queries on owner topics (~1 req/3s etiquette).
- **DEAD ENDS:** alphaXiv (no public API/feed; guessed endpoints 404); paperswithcode.com → 302 to HF papers (defunct).

### Practitioner blogs (11 hostnames, all no-auth, all verified)

- `https://simonwillison.net/atom/entries/` — long-form only, ~2/wk (RECOMMENDED over `/atom/everything/` which is ~3.8/day link-blog).
- `https://www.latent.space/feed` — filter out titles starting `[AINews` (cross-posts); ~0.2/day after filter.
- `https://www.interconnects.ai/feed` — ~1.3/wk, open-model landscape.
- `https://magazine.sebastianraschka.com/feed` — ~1.5/mo, deep explainers (~2.5MB body, full articles inline).
- `https://eugeneyan.com/rss/` — exact path required (`/feed` 404s); full archive in feed → date-filter on first ingest.
- `https://huyenchip.com/feed.xml` — DORMANT (~19 mo); passive slot.
- `https://lilianweng.github.io/index.xml` — 2–4/yr, every item High; guard bogus year-0001 date at feed tail.
- `https://hamel.dev/index.xml` — exact path required; ~1/mo, LLM evals.
- `https://karpathy.bearblog.dev/feed/` — sporadic; posted 2026-08-08.
- Bonus finds: `https://jxnl.co/feed_rss_created.xml` (~1–2/mo, agent/structured-output engineering), `https://vickiboykis.com/index.xml` (~1.5/mo, opinionated hands-on).

### Newsletters / aggregators

- rss `https://news.smol.ai/rss.xml` — **crown jewel**: 1 digest/weekday aggregating 12 subreddits + X + Discords; full content. **TRAP:** feed contains the ENTIRE archive (693 items, 2.1MB) → conditional GET (ETag/Last-Modified) or parse first 1–2 items only. Also the recommended X-proxy.
- rss `https://tldr.tech/api/rss/ai` — teaser-only feed (1/weekday); full issue plain-fetchable at item link. Only `/api/rss/<vertical>` works (`/ai/rss` = trap).
- rss `https://importai.substack.com/feed` — weekly, full content, research/policy.
- rss `https://www.bensbites.com/feed` — 2–3/wk practitioner essays (beehiiv-subdomain URL is a 404 trap).
- **DEAD ENDS:** The Batch (no feed anywhere; Ghost backend 402), The Rundown (beehiiv RSS disabled; email-only).

### YouTube talks (`www.youtube.com`, single hostname; no auth)

Pattern: `https://www.youtube.com/feeds/videos.xml?channel_id=<ID>` — Atom, 15 latest, includes full description (`media:description`) + views (`media:statistics`) → summarizable WITHOUT transcripts.

- AI Engineer `UCLKPca3kwwd-B59HNr-_lvA` — conference-burst (9 videos in 2 days post-conf); highest value.
- Karpathy `UCXUPKJO5MZQN11PqgIvyuvQ` — rare, always worth it.
- Latent Space `UCxBcwypKK-W3GHd_RZ9FZrQ` — ~2/wk.
- MLST `UCMLtBahI5DMrt0NPvDSoIRQ` — ~1/wk, research-flavored (drop first if trimming).
- Yannic Kilcher `UCZHmQk67mSJgfCCTn7xBfew` — quiet since 2026-03.
- **TRAP:** channel `@handle` pages 302 to consent.youtube.com with empty body (EU geo) — hardcode channel_ids; never discover at runtime. Deep talk summarization needs transcript tooling (not stdlib) — agentic fallback territory.

### X/Twitter (direct = dead)

- **DEAD:** X API v2 read = $200/mo Basic tier (verified 401 anon); r.jina.ai blocked domain-wide on x.com (403 AbuseAlleviation); syndication endpoints empty/429; xcancel needs per-reader email whitelist.
- Best-effort only: `https://nitter.net/<handle>/rss` — WORKS today, fresh, ~20 items/fetch; replies `R to` / RTs `RT by` prefixed (filterable). Aggressively rate-limited (search RSS 429'd same run), historically unstable. Tiny handpicked list, once daily, graceful skip on 429. NEVER TIER-1.
- Primary recommendation: AINews (above) as the X-proxy.

### Launch trackers (optional)

- rss `https://www.producthunt.com/feed?category=artificial-intelligence` (~6–9/day) and `?category=developer-tools` (~5/day, better builder fit) — genuine Atom, `?category=` honored, but NO vote counts in feed (API v2 = OAuth only). Old stragglers appear → dedup by entry `<id>`, not date. Weekly scan at best.
- **DEAD ENDS:** theresanaiforthat (Cloudflare JS challenge), devhunt.org (Next.js error shell), BetaList (~12/day consumer spam — skip).

## Domain allowlist delta (cloud env "Test")

Core set: `hnrss.org`, `hn.algolia.com`, `lobste.rs`, `www.reddit.com`, `api.github.com`,
`github.com`, `mshibanami.github.io`, `huggingface.co`*, `news.smol.ai`, `tldr.tech`,
`www.youtube.com`.
Blogs group: `simonwillison.net`, `www.latent.space`, `www.interconnects.ai`,
`magazine.sebastianraschka.com`, `eugeneyan.com`, `huyenchip.com`, `lilianweng.github.io`,
`hamel.dev`, `karpathy.bearblog.dev`, `jxnl.co`, `vickiboykis.com`.
Optional: `importai.substack.com`, `www.bensbites.com`, `www.producthunt.com`,
`api.ossinsight.io`, `nitter.net`, `export.arxiv.org`.
(* already allowlisted for the existing HF blog feed.)
