# AI Content Engine — Technical

> Architecture, components, data model, and the LLM/agent specification. Assumes `00_overview.md` has been read. Hosting and deployment are in `02_infra.md`; build order and open decisions are in `03_build_plan.md`.

## 1. Architecture

The system is a **staged pipeline**, not a multi-agent system. Each stage does its work and writes its state and output to Postgres; the next stage reads from Postgres. Stages do not call each other directly and do not run concurrently in any coordinated way — Postgres is the only integration point.

There is **one agentic component** (the writer/editor, used in the draft and iterate phases). Every other model use is a single-shot call. The researcher is deterministic code.

End-to-end flow:

1. The **researcher** wakes on a schedule, pulls new items from each configured source, normalizes them, embeds them, deduplicates them into **clusters**, tags each cluster with a topic, and computes a blended ranking score per cluster.
2. For top-ranked clusters, a single model call produces a **triage summary** (title + short blurb). These are sent to the owner in Telegram — **Gate 1**.
3. When the owner approves a cluster, full text is fetched for its items (pass 2), an **article** record is created, and the **writer-agent** drafts a canonical long-read grounded in the sources.
4. The owner iterates the draft in the **web editor** (real-time chat). Each instruction is logged. The agent edits in place.
5. The owner approves the canonical draft — **Gate 2**.
6. On demand, a single model call formats a **variant** for a chosen platform (LinkedIn / Medium / Reddit).
7. The owner copies the variant and posts it manually — the system never publishes. Afterwards the owner clicks **mark as published** in the web app: this flips `articles.status` to `published` and computes and stores the article's embedding (role: `embedding`). That click is what populates the knowledge base used when drafting future pieces (§3, decision 3); it is owner bookkeeping of an external manual act, not publishing.

A weekly **digest** is a scheduled query over the rolling store rather than a fresh poll; see §2.5.

## 2. Components

### 2.1 Researcher (deterministic)

- **Scheduler.** A single scheduler drives polling. Each source has a `cadence` (poll interval) coming from config; a person's cadence cascades to their sources unless a source overrides it. Cadence is how often we *check*, set by freshness need and cost — not by how often the author posts.
- **Source adapters.** One adapter per source *type*, all exposing a common interface that returns a normalized `Item`. One RSS-family adapter covers RSS, blogs, Substack, arXiv, Medium, dev.to, Lobsters, HF papers, GitHub trending feeds. Separate adapters: Reddit (the official OAuth JSON API, **not** RSS — unauthenticated Reddit is blocked from datacenter IPs, and RSS carries no scores, while the API returns the `score`/`num_comments` the ranking needs), X (pay-per-use read API), Hacker News, and GitHub (events/Atom). There is deliberately **no pollable "web page" source type**: the generic web fetcher (readability extraction, headless browser as a fallback) is not an adapter but a shared component (`app/fetcher`) — the pass-2 full-text extractor and the backend of the editor's `fetch_source` tool.
- **Pull, with cursors.** Everything is polled; nothing is pushed. Each source keeps a cursor (`since_id`, last-seen id, or `ETag`/`If-Modified-Since`) so each poll fetches only what is new.
- **Two-pass fetch.** Pass 1 fetches cheap metadata for everything (title, url, engagement, published_at). Full text is fetched in pass 2 **only after Gate 1**, for approved stories — this keeps extraction cost low.
- **Two input streams.** (a) *People*: posts from followed authors, spanning their X, blog/RSS, GitHub, and arXiv — not just X. (b) *Topic*: the top items on a topic, independent of author.
- **Dedup → clusters.** Two layers. (a) Same canonical URL seen by several sources: one **item**, one **sighting** per source — a plain PK upsert, no embeddings involved (HN and Reddit items link to the external article, so identical URLs across sources are the norm, not an edge case). (b) Different URLs about the same story (across HN, Reddit, X, blogs): each new item is embedded and grouped into one **cluster** by vector similarity. The exact similarity threshold is a build-time decision (see build plan).
- **Topic tagging.** Default tag comes from the source; a light classifier (cheap model) tags only ambiguous items (e.g. general blogs, HN front page). See §4.
- **Cluster ranking.** Ranking happens at the **cluster** level. Compute a blended `score`: normalize native ratings where they exist (e.g. percentile within a platform for Reddit `/top`, HN points — taken from each sighting's `engagement`), add cross-source frequency (the strongest signal — the same story surfacing in many sources; counted as **distinct sighting sources** across the cluster's items, so one URL seen by three sources counts as three), and factor in recency. Sources without native ratings (arXiv, blogs) contribute via cross-source frequency.
- **Triage summary.** At the end of a poll cycle, for clusters selected by the triage rule (status `new`, no summary yet, ranked high enough — the exact top-N / threshold / daily cap is an open decision, see build plan), a single model call produces a title + short blurb, written to `clusters.triage_title` / `triage_summary`. This is the researcher's last step; delivery belongs to the bot, and the cluster row is the hand-off (Postgres is the stages' only channel).

Comment threads are not content; comment counts are only a ranking signal.

### 2.2 Triage — Gate 1 (Telegram bot)

The Telegram bot exists for triage only (it is the convenient mobile surface). Mechanics: the bot checks Postgres every few minutes (default: 5 min) for clusters with a triage summary and `status = 'new'`, sends each to `TELEGRAM_OWNER_CHAT_ID` as title + summary with approve/skip buttons, and immediately sets `status = 'sent'` — so nothing is ever delivered twice, including across bot or poller restarts. Approve sets `approved` (which triggers pass-2 fetch); skip sets `skipped`; both are terminal for triage. The bot delivers summaries, it never generates them. Triage is at the **cluster (story) level**, never per item — the owner decides once per story, not once per duplicate.

### 2.3 Editor — the one agent (web app)

A grounded-RAG ghostwriter with the owner in the loop. Three phases:

**Draft.** Input: the approved cluster's source bundle, the chosen `piece_type`, and an assembled context. Context assembly is the quality crux: the voice style-guide rules + relevant past published articles retrieved via pgvector (these do double duty — voice few-shot and continuity / non-repetition). Output: one grounded canonical draft (a long-read). Grounding is mandatory — stick to the source text, carry provenance links into the draft, and flag any uncertain claim for the owner to verify. The drafter may call tools on demand (see §4); tools are not always-on.

**Iterate.** Real-time chat in the web app with a live preview. The core principle is **edit-in-place on the working draft — never full regeneration** (regeneration would undo the owner's refinements). It is hybrid: the owner can both instruct in chat and hand-edit the draft directly; the agent must respect manual edits. Each instruction is appended to `edit_log` (this is the voice training signal over time).

**Posture.** Default is *grounded-knowledgeable*: the model understands the domains well enough not to garble technical content, but does **not** inject outside facts or opinions; any addition beyond the sources is flagged. The owner can request more on demand in chat ("explain RAG for beginners", "add a take here"). Authenticity guard: opinions and takes are the owner's — the agent may propose a position, but the owner approves or edits it.

**Piece type.** A switchable parameter — `hot_news`, `digest`, or `project_post` — chosen at draft start (with a default and an override) and switchable mid-stream. Switching piece type is a structural reformat, not a point edit. Templates per type are refined by experiment (build plan).

**Canonical.** The canonical text is one long-read. After Gate 2, variants are derived from it on demand (compressing is easier and better-grounded than expanding).

### 2.4 Variants (single calls, on demand)

After Gate 2, a per-platform version is produced by a **single model call per platform**, on demand for the platform being posted to — not an agent.

- **Medium** — formatting: the long-read plus markdown (headers, code, bold); roughly passthrough, length preserved.
- **Reddit** — formatting plus light tone adjustment for the target subreddit; markdown.
- **LinkedIn (feed post)** — a *condense*: the long-read does not fit the short feed format, so the call rewrites it down to a short, hook-first, plain-text post (decide what to keep and what to cut). Still one call.

Each generated variant is shown in an **editable** copy-out field. The owner can **regenerate** it (re-run the single-shot, system-prompt formatter — no agent conversation) or **hand-tune it inline** and **save** the edit back; a save appends a new `variants` row (history preserved, latest wins), so the tweaked text survives a reload and feeds the copy-out. The save is a plain DB write — no model call, and nothing is ever posted. (v1 deliberately uses this inline edit + regenerate instead of routing a variant through the chat editor: the canonical is what the chat agent co-writes; a variant is a downstream platform reformat the owner finishes by hand. Chat-based per-variant iteration is a deferred, optional convenience.)

### 2.5 Digest

A weekly **scheduled query** over the rolling store — not a fresh poll and not a raw dump. The job runs in the **bot** process at each topic's configured `digest.schedule`. For each topic: take the rolling window, **exclude clusters already linked to any article via `article_clusters`** (covered by a hot-news piece or a previous digest), rank the rest by blended score, take the top N, summarize. The exclusion is what prevents repeats: with a window longer than the schedule interval (e.g. dotnet's 14d window on a weekly schedule) re-scanning the overlap is guaranteed, so "already covered" must be filtered out, not re-ranked. A Gate-1 `skipped` cluster stays eligible — skip means "no standalone post", not "omit from the weekly awareness rollup". It is cheap because clusters are built incrementally during polling.

The digest is dual-purpose from a single artifact — the `digest` **article record, created by the run itself**. The job creates the article (`piece_type = digest`), links its clusters via `article_clusters` (this linkage is the persistent "covered" marker future runs filter on), and writes the dense rollup as the article's initial `current_draft`. Then: (a) the bot delivers that dense version to the owner in Telegram for personal awareness, and (b) the same article is the basis for a published digest post — the owner takes it through the editor like any other article. If the owner never drafts it, the record simply remains as the covered-marker.

### 2.6 Surfaces

- **Telegram bot** — triage (Gate 1) plus the scheduled digest job and its delivery (§2.5). Mobile convenience.
- **Web app** — the editor: real-time chat + live preview + image insertion, plus any status/admin views, plus the **mark-as-published** control that closes an article's lifecycle and adds it to the knowledge base. This is the one always-on HTTP surface. v1 is a lean chat + preview; a rich drag-and-drop "constructor" editor is deferred.

## 3. Data model (Postgres + pgvector)

Principles:

- Postgres + pgvector is the single source of truth and the coordination bus.
- **Config is not in the database.** People, sources, topics, cadences, and digest schedules live in `config.yaml` at the repo root, loaded at startup (authoritative for source types and field names; see `02_infra.md` §4). The only mutable poll state persisted in the DB is per-source cursors.
- **Two embedding purposes:** item embeddings are for deduplication; article embeddings are for voice/continuity retrieval once published.

Four decisions baked into the schema:

1. **Clusters are a first-class table**, not a `cluster_id` field on items. The cluster holds the blended cross-source score and the Gate-1 status — these cannot live on one of N duplicate items. All "top on topic" and triage logic operates on clusters.
2. **Triage and ranking are at the cluster level** (consequence of dedup-before-triage).
3. **There is no separate "finals" table.** A published article plus its embedding *is* the knowledge base retrieved from when drafting new pieces. Storing finals separately would be duplication.
4. **Sightings are separate from items.** An item is content identity (one canonical URL, one text, one embedding); a sighting records that a particular source surfaced it, with that platform's engagement. Re-seeing a URL from a new source inserts a sighting — never a duplicate item, and never an overwrite of the first source's observation.

Tables (types are indicative; `vector` = pgvector):

**items** — raw pool of findings; one row per canonical URL (content identity: text + embedding).
- `id` TEXT PK — hash of the canonical URL
- `cluster_id` TEXT FK → clusters.id, nullable until clustered
- `title` TEXT, `url` TEXT
- `full_text` TEXT, nullable — populated in pass 2, only for approved stories
- `embedding` vector — for dedup
- `published_at` TIMESTAMPTZ, `fetched_at` TIMESTAMPTZ — first time seen

**sightings** — one source's observation of an item. The same canonical URL surfacing via the HN poll, a Reddit poll, and a blog RSS poll is *one* item with *three* sightings; cross-source frequency counts sightings, so collapsing them into the item row would silently destroy the strongest ranking signal.
- `item_id` TEXT FK → items.id
- `source_key` TEXT — references a source defined in the YAML config (a plain string, **not** a DB foreign key, because sources live in the file)
- `engagement` JSONB — that platform's signals (points, comments, etc.)
- `seen_at` TIMESTAMPTZ
- composite PK (`item_id`, `source_key`)

**clusters** — stories.
- `id` TEXT PK
- `topic` TEXT — tag
- `score` FLOAT — blended cross-source ranking score
- `status` TEXT — Gate 1 lifecycle: `new` → `sent` (delivered to Telegram, awaiting decision) → `approved` / `skipped`
- `triage_title` TEXT, nullable — written by the researcher's triage-summary call
- `triage_summary` TEXT, nullable — same; the bot reads these for delivery (the cluster row is the poller → bot hand-off)
- `created_at`, `updated_at` TIMESTAMPTZ

**articles** — the working record through the lifecycle, and (when published) the knowledge base.
- `id` TEXT PK
- `piece_type` TEXT — `hot_news` / `digest` / `project_post`
- `status` TEXT — `approved` → `drafting` → `pre_publish` → `published`
- `current_draft` TEXT — the canonical long-read
- `embedding` vector, nullable — populated when `published`, for KB retrieval
- `created_at`, `updated_at` TIMESTAMPTZ

**article_clusters** — many-to-many join. A `hot_news` article maps to one cluster; a `digest` article aggregates many.
- `article_id` TEXT FK → articles.id
- `cluster_id` TEXT FK → clusters.id
- composite PK (`article_id`, `cluster_id`)

**edit_log** — iteration trail and voice signal.
- `id` PK
- `article_id` TEXT FK → articles.id
- `instruction` TEXT — the owner's edit instruction
- `draft_snapshot` TEXT, nullable — optional snapshot of the draft at that point
- `created_at` TIMESTAMPTZ

**variants** — per-platform formatted outputs.
- `id` PK
- `article_id` TEXT FK → articles.id
- `platform` TEXT — `linkedin` / `medium` / `reddit`
- `formatted_text` TEXT
- `created_at` TIMESTAMPTZ

**cursors** — per-source poll state (the only config-adjacent thing that must persist).
- `source_key` TEXT PK — derived deterministically from the source's config entry: `<type>:` plus a stable serialization (or short hash) of its **identity fields**, i.e. every field except `cadence`. Two same-type sources differing only in params (e.g. the two `hn` entries) get distinct cursors; tuning `cadence` keeps the cursor; changing an identity field deliberately resets it (safe — re-polling is idempotent thanks to the items/sightings upsert).
- `cursor` TEXT or JSONB — `since_id` / last-seen id / `etag` + `last_modified`, depending on source type
- `updated_at` TIMESTAMPTZ

The voice style-guide / anti-patterns and any project notes (for `project_post`) are **files**, not tables — `content/style_guide.md`, `content/anti_patterns.md`, `content/projects/`, mounted read-only into the editor — consistent with the config-in-file principle.

## 4. LLM / agent specification

### Model roles

Steps declare a logical **role**; config maps roles to concrete models so models stay swappable. No step hardcodes a model.

- `generation` — the workhorse for all text: triage summaries, drafting, iteration, variant formatting. Default: Claude Sonnet 4.6.
- `generation_high` — optional higher-quality tier, used for the draft step only if Sonnet's writing is not good enough. Default: Claude Opus 4.8.
- `cheap` — optional low-cost tier for high-volume bounded tasks (topic classification, and triage summaries if cost matters). Default: Claude Haiku 4.5. At expected volume this tiering is optional — a single `generation` model can do everything.
- `embedding` — text → vectors for dedup and retrieval. Default: `gemini-embedding-001` via Vertex (native to the GCP host); Voyage is an alternative if best-in-class code/technical retrieval is wanted.

### Model abstraction

A thin interface, e.g. `generate(messages, role, tools=None) -> response` and `embed(texts) -> vectors`. The implementer chooses the transport (Anthropic API directly, or Claude via Vertex Model Garden so model and embeddings bill to one GCP account — see infra). Enable prompt caching on the repeated parts of the context (style guide, retrieved context, the working draft during iteration) — this materially cuts input cost because iteration resends the same context each turn.

### The writer-agent (draft + iterate)

This is the only loop-with-tools component. Tools, all on-demand (called only when needed, never always-on):

- `kb_search(query)` — retrieve relevant past **published** articles via pgvector (for voice few-shot and continuity / non-repetition).
- `fetch_source(url)` — fetch the full text of a source (readability or headless) for grounding and detail.
- `web_search(query)` — optional, used sparingly for long-form pieces that need extra context.

Grounding rules (enforced in the draft and iterate phases):

- Use only facts present in the approved source bundle plus anything explicitly fetched via the tools. Do not introduce outside facts.
- Carry provenance links through into the draft.
- Flag any claim that is uncertain or not supported by a source, for the owner to verify.
- Opinions and takes are the owner's. The agent may propose a position, clearly marked as a proposal; it never asserts a judgement as the owner's own.
- During iteration: edit in place, never regenerate the whole draft; respect any manual edits the owner has made.

### Single-shot calls (not agents)

Each is one model call, input → output, no tools, no loop:

- **Topic classification** — input: an ambiguous item's metadata; output: a topic tag. Role: `cheap`.
- **Triage summary** — input: a cluster's items; output: title + short blurb for Gate 1. Role: `generation` (or `cheap`).
- **Variant formatting** — input: the approved canonical + the target platform; output: the platform version (format for Medium/Reddit, condense for a LinkedIn post). Role: `generation`. One call per platform.

### Voice

Cold start, no existing corpus. Three ingredients, growing over time:

- A light **style guide** plus **anti-patterns**, kept as a file, with two modes: *news-commentary* and *personal-project*.
- **Retrieval** of past published articles (pgvector) as voice few-shot and for continuity.
- The **edit log**: every owner instruction is captured; over time it informs the voice (it can be periodically distilled back into the style guide). Chat iteration is the main training signal.

## 5. Deferred technical decisions

Settled here; *unspecified on purpose* and to be decided during the build (tracked in `03_build_plan.md`): the dedup similarity threshold, the exact topic-classifier prompt/labels, paywall and JS-page extraction handling, exact feed-URL verification, and the per-piece-type templates. The agent should implement clean seams for these and not block on them.
