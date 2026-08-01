# AI Content Engine — Build Plan

> The phased implementation roadmap. This is the document to work through. Assumes `00_overview.md`, `01_technical.md`, `02_infra.md`, and the authoritative `config.yaml` (repo root) are read.

## How to use this plan

- Build in **vertically testable slices**, in the order below. Each phase should be runnable and verifiable on its own before moving on.
- Several technical decisions are **intentionally open** (listed at the end). Where a phase touches one, build a clean seam (an interface, a config value, a single function to swap later) and pick a reasonable default — **do not block** on getting it perfect.
- Single user, no scale requirements. Prefer the simple implementation every time.
- Respect the non-negotiables in `00_overview.md` at every step — especially: never publish anything, keep drafting grounded, config in a file, Postgres as the single source of truth, swappable model.

## Suggested repo layout

```
app/
  llm/          # model abstraction: generate(messages, role, tools), embed(texts); role->model config
  db/           # schema, migrations, query helpers
  adapters/     # one module per source type (rss, reddit, x, hn, github), common interface -> Item
  fetcher/      # full-text extraction (readability + optional headless): pass-2 and the editor's fetch_source
  researcher/   # scheduler, polling, dedup/clustering, ranking, topic tagging
  editor/       # the writer-agent (draft + iterate), tools, context assembly, grounding
  variants/     # per-platform single-call formatters
  digest/       # scheduled digest query
  bot/          # Telegram triage (Gate 1) + digest delivery
  web/          # editor web app (chat + live preview + admin/status)
config.yaml     # sources/people/topics/cadences/digest — authoritative shape (mounted read-only)
content/        # owner-authored voice files: style_guide.md, anti_patterns.md, projects/ (mounted read-only)
migrations/     # DB migrations
docker-compose.yml, Dockerfile, Caddyfile, .env (gitignored)
```

## Suggested stack (defaults — adjust if you have a better reason)

- Python. Web: FastAPI + Uvicorn. Realtime chat in the editor: WebSocket (or SSE).
- DB access: SQLAlchemy; migrations: Alembic. Postgres with the `pgvector` extension.
- Scheduler: APScheduler, in the `poller` process.
- Telegram: `aiogram` or `python-telegram-bot` (long-polling by default).
- Model transport: Vertex (ADC, no API key) or the Anthropic SDK — see `02_infra.md` §6.

## External-account prerequisites (start these during Phase 0 — they have lead time)

- **Reddit:** subreddit reading uses the official OAuth JSON API (free non-commercial tier; unauthenticated RSS is blocked from datacenter IPs and carries no scores). Register a script-type app and submit the API access request **immediately** — approval can take 2–4 weeks, which should overlap Phases 0–1, not block them. Secrets: `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET`.
- **X:** read access is pay-per-use only (the free read tier closed in early 2026) — a developer account with prepaid credits, ~$2–5/month at this config's volume (see `02_infra.md` §9). Set up the account and credits before the X adapter lands in Phase 1. Secret: `X_BEARER_TOKEN`.

## Phases

### Phase 0 — Foundation
**Goal:** an empty but runnable skeleton with config, DB, and model access.
**Scope:** repo layout; YAML config loader validating the **authoritative** shape in `config.yaml` at the repo root — exactly the source types `x_user` / `github` / `rss` / `reddit_sub` / `hn` / `arxiv` and their field names, per that file's header (the sketch in `02_infra.md` §4 is an illustrative excerpt, not the spec); Postgres + pgvector with migrations for all eight tables (`items`, `sightings`, `clusters`, `articles`, `article_clusters`, `edit_log`, `variants`, `cursors`); the `app/llm` abstraction with role→model mapping and the chosen transport; `.env` secrets; Docker Compose (`db`, `web`, `bot`, `poller`, `proxy`), with Caddy fronting `web` behind basic auth from day one (`WEB_AUTH_USER`/`WEB_AUTH_HASH`, see `02_infra.md` §5).
**Done:** `docker compose up` runs; the schema exists; a trivial `generate` and `embed` round-trip works; config loads.

### Phase 1 — Researcher (ingest → clusters)
**Goal:** real items flowing in and forming ranked clusters.
**Scope:** the RSS-family adapter first, then Reddit (OAuth JSON API) / X / HN / GitHub — there is no pollable web source type; the web fetcher is pass-2 machinery (Phase 2); the common `Item` interface; the scheduler firing per-source polls on cadence; pass-1 metadata fetch with cursors, recording a **sighting** per (item, source) — a canonical URL already seen from another source upserts a sighting, never a duplicate item and never an overwrite; embedding each new item and deduplicating into clusters; topic tagging (source-default + a `cheap`-role classifier for ambiguous items); cluster ranking (normalized native ratings from sightings' `engagement` + cross-source frequency counted over distinct sighting sources + recency).
**Done:** the poller pulls real configured sources on cadence; items land; the same URL arriving from two sources yields one item with two sightings; clusters form, carry a topic, and get a blended `score`. Inspect via DB/logs (no triage yet).

### Phase 2 — Triage (Gate 1)
**Goal:** the owner can approve/skip stories from the phone.
**Scope:** the triage-summary single call in the poller for clusters selected by the triage rule, writing `clusters.triage_title` / `triage_summary` (the selection knobs — top-N / threshold / daily cap — are an open decision: pick defaults behind a seam); the Telegram bot polling the DB for summarized, unsent clusters, delivering title + summary with approve/skip buttons to `TELEGRAM_OWNER_CHAT_ID` and accepting commands/callbacks **only** from that chat (anyone else is ignored), marking each delivered cluster `sent`; approve/skip updates `clusters.status`; pass-2 full-text fetch triggered for approved clusters only, via `app/fetcher` (readability extraction; headless browser only as a fallback — paywall/JS handling is an open decision).
**Done:** the owner receives each top story in Telegram exactly once — restarting the bot or the poller resends nothing; approving a story fetches full text for its items.

### Phase 3 — Editor: draft (the agent)
**Goal:** an approved story becomes a grounded canonical draft.
**Scope:** the web app skeleton; on approval create an `article` (link clusters via `article_clusters`); the writer-agent draft phase with context assembly (the `content/` voice files — `style_guide.md` and `anti_patterns.md`, **bootstrapped together with the owner as part of this phase**, even as short stubs — plus KB retrieval of past published articles via pgvector) and on-demand tools (`kb_search`, `fetch_source` backed by `app/fetcher`, optional `web_search`); enforce grounding (provenance links, flag unverified claims, no injected opinions); `piece_type` parameter.
**Done:** approving a story yields a grounded canonical long-read visible in the web app; the assembled draft context demonstrably includes the style-guide rules.

### Phase 4 — Editor: iterate + Gate 2
**Goal:** the owner refines the draft conversationally and approves it.
**Scope:** real-time chat in the web app with live preview; **edit-in-place, never full regeneration**; hybrid instruct + direct hand-edit (respect manual edits); append every instruction to `edit_log`; piece-type switchable mid-stream; Gate 2 approval moves `articles.status` to `pre_publish`.
**Done:** the owner iterates a draft via chat, edits are logged, and the canonical can be approved.

### Phase 5 — Variants
**Goal:** platform-ready text to copy and post.
**Scope:** single-call per-platform formatters — Medium (format/markdown), Reddit (format + tone), LinkedIn (condense to a short post); generated on demand for the chosen platform; stored in `variants`; optional hand-tune by dropping the variant into the same chat editor; a **mark-as-published** control in the web app — after posting manually, the owner clicks it: `articles.status` → `published`, the article embedding is computed and stored (role `embedding`), and the article thereby enters the voice/continuity knowledge base that `kb_search` retrieves from (bookkeeping of an external manual act — not publishing).
**Done:** the owner gets a platform-ready variant and copies it out (no publishing — manual); after marking the article published, it is retrievable via `kb_search` when drafting the next piece.

### Phase 6 — Digest
**Goal:** the weekly digest.
**Scope:** a scheduled digest job in the bot per topic's `digest.schedule`: rolling window → **exclude clusters already linked via `article_clusters`** (covered by hot-news pieces or previous digests; `skipped` clusters stay eligible) → rank → top N → summarize; the job creates the `digest` article up front, links its clusters (the linkage is the covered-marker that stops the next run from repeating them) and stores the dense rollup as its initial `current_draft`; the dense version delivered to Telegram; the digest article flows through the editor on demand.
**Done:** the weekly digest is delivered to Telegram; a digest post can be drafted through the editor; two consecutive runs over overlapping windows (e.g. a 14d window on a weekly schedule) do not repeat a story.

### Phase 7 — Hardening & deploy
> **Deferred to last (revised 2026-06-21).** Runs only when the project is *fully ready* — after Phases 9 → 10 and a settled Phase 8 UI. Cheap hardening (prompt caching, error handling on flaky source/model calls) may land opportunistically earlier; the VM deploy + TLS + backups are the final step.
**Goal:** running in production, durably.
**Scope:** deploy on the GCP VM with Caddy/TLS (`02_infra.md`); verify the editor is unreachable without basic auth and the bot ignores non-owner chats; enable prompt caching on repeated context; nightly `pg_dump` backup (local + GCS); logging and `restart: unless-stopped`; reasonable error handling for flaky source fetches and model calls.
**Done:** the system runs on the VM, survives reboots, and is backed up.

### Phase 8 — UI polish (minimal, iterative; owner-driven)
**Goal:** incrementally improve the web UI for the owner's daily use — small, reviewable presentation changes, one surface at a time (dashboard first, then editor, then digests/variants).
**Scope:** presentation only — NiceGUI layout/styling/affordances in `app/web/ui_pages.py` plus read-only view helpers in `app/web/queries.py`. NO schema, NO pipeline/agent changes, NO new posting path (hard rule 1 holds). Each change is kept minimal and verified visually in the local preview.
**Done:** each increment runs, looks right in the preview, and the suite stays green. Increments are logged under "Phase 8 increments" below.

### Phase 9 — Morning brief (batched triage roundup)
**Added 2026-06-21** as part of reframing the project as a **personal-brand engine, not a news site**. **Revised execution order from here:** Phase 9 → Phase 10 → Phase 8 (UI polish, ongoing) → Phase 7 (deploy, last). **Audited 2026-06-21** (multi-agent, grounded in code): the design is architecturally sound and covered-marker-safe *by construction* (triage/delivery never write `ArticleCluster`), but the seams below are **net-new, not "just reuse"** — four of them are correctness-critical.

**Goal:** one consolidated morning roundup in Telegram of new top stories — low-friction to skim for an owner with little time, each story still approve/skip → draft.
**Scope:**
- **Daily batched delivery** in the bot at a configured time, **replacing** the per-cluster Phase-2 drip: batch all summarized-but-unsent clusters in the window, rank, take top-N, send ONE message (chunked if needed) — each story = `triage_title` + one-line summary + approve/skip buttons.
- **Atomic send (correctness-critical).** Do NOT claim-all-then-send: on a partial-chunk failure or crash the unsent chunks' clusters are left marked `sent`-but-never-shown — silent Gate-1 loss, never re-selected (`select_deliverable` only re-selects `new`). Tie each cluster to its chunk(s), send sequentially, mark a chunk's clusters `sent` only AFTER that chunk's send returns; on failure stop, leave the rest `new`. Worst case re-shows the in-flight batch (at-most-once-per-cluster), never silent loss.
- **Retire the drip (correctness-critical).** `_delivery_loop`/`_deliver_once` is started **unconditionally** in `_post_init` (`app/bot/__main__.py:407`) and draws from the same `select_deliverable` pool — gate or remove it so the brief is the only consumer when a brief is configured; else the drip empties the pool between briefs and the roundup arrives empty.
- **Window / anti-starvation (correctness-critical).** Use a fixed rolling lookback (reuse the digest `created_at >= now - window` mechanism) + top-N, and age out clusters older than the window that were never sent — so below-top-N stories don't sit `new+summarized` forever, perpetually out-ranked (the drip used to trickle the tail).
- **Covered-marker untouched:** the brief MUST NOT create a `digest` article and MUST NOT link `article_clusters`. The publishable weekly digest (Phase 6) stays a separate path.
- Optional `cheap`-role "what's notable today" preamble — **deferred to a fast-follow**; if built, it's the bot's first model call (logical role, never a model id), grounded only in the batched triage summaries, no opinions, degrades to none on failure, isolated so it never blocks delivery.
**Builds:** backend. **Config seam is net-new and must land FIRST (before editing `config.yaml`, or the `/config-edit` PostToolUse hook rejects it):** (a) add `brief` to the top-level allow-list in BOTH `app/config.py:193` AND `.claude/skills/config-edit/validate_config.py` (kept in lockstep — both raise `ConfigError` on unknown top-level keys); (b) a `Brief` dataclass + `_check_brief` mirroring `Digest`/`_check_digest`; (c) a NEW daily-time grammar + parser (bare `HH:MM`, no weekday — `SCHEDULE_RE`/`parse_digest_schedule` require a day-of-week token; `CronTrigger` already accepts `day_of_week='*'`). One daily brief across all topics (one cron job, parallel to `digest`). Delivery logic itself is small.
**Done:** at the configured morning time the owner gets ONE roundup of new top stories; approving one fetches full text and makes it draftable (as Phase 2); restarting the bot/poller resends nothing AND a simulated mid-batch send failure strands nothing at `sent`; `articles`/`article_clusters` counts are unchanged by a brief run; no throwaway digest articles; the weekly digest is unaffected.

### Phase 10 — Flagship intake (own-material → canonical draft)
**Added 2026-06-21. The brand-builder mode** — the owner's own research/experiments become polished articles; the system's actual purpose, today under-served (the editor only starts from a researcher cluster). **Audited 2026-06-21** (multi-agent, grounded in code). The single-seam framing is correct and Phase 4/5 already tolerate zero linked clusters (`iterate.py` builds a bundle only `if cluster_id`; `fetch_source` is cluster-free; KB/publish/version-history all work). But the flagship draft is **blocked today by three hard-coded "every article has a cluster" assumptions** that must be relaxed **together, without relaxing `GROUNDING_RULES`**.
**Goal:** the owner starts a grounded canonical draft from his OWN material (repo / notebook / results / notes / link), bypassing the researcher, in his voice — technical but accessible, ready for his primary surfaces (X / LinkedIn / Medium).
**Core seam:** owner material is a **first-class grounding source attachable to any article** — standalone (no cluster → flagship) or alongside a news cluster (→ fusion: react to news *through* his own work).

**Scope — core (must land together):**
- **Storage — `article_sources` (DECIDED, not open).** A dedicated 9th table (`article_id` FK **`ON DELETE CASCADE`** — the first cascading FK, deliberate: owner material dies with its article; `kind`, `title`, `url` nullable, `content` text, `created_at`). New Alembic revision (`down_revision='0001_initial'`) + ORM model. The synthetic-owner-cluster alternative is **rejected** — it provably pollutes `select_digest_clusters` (no provenance filter → summarized as a "news story"), `load_stories` (phantom Gate-1 row), and dedup/ranking (origin-agnostic). Note the name collision with the read-only `ArticleSource` view dataclass in `app/web/queries.py`.
- **Grounding-guard relaxation.** `draft_article` raises *before any model call* on no-linked-cluster (`draft.py:149-153`) and on `not bundle.has_full_text` (`:158-165`, cluster-items-only). Redefine grounding as **"has any grounding corpus"**: load owner sources + (cluster full_text if linked), refuse ONLY on the empty union, extend `has_full_text` (`context.py:162`) to count owner-source text. `GROUNDING_RULES` (`context.py:263-277`) **unchanged** — it already covers owner material once it's in the bundle. The `draft.py` fix and the intake path ship together (the empty-draft chat entry point dead-ends otherwise).
- **Context assembly:** fold owner `SourceItem`s into the **SAME cached SOURCE BUNDLE block** (single `cache_control` breakpoint, `context.py:322`) — NOT a separate post-cache block, or prompt caching (which iteration depends on) breaks.
- **Cluster-less creation:** add `create_flagship_article(session, *, piece_type='tech_explainer', sources=[...])` → inserts an Article at `status='drafting'` with NO `article_clusters` row; leave `create_article_for_cluster` (approved-cluster contract + covered-marker) untouched.
- **`tech_explainer` piece_type (DECIDED).** Add a brief (motivation → mechanism → worked example → when-to-use → caveats) as the default register for own-material; keep `project_post` for building-in-public build logs. One `PIECE_TYPES` tuple entry + one `_PIECE_TYPE_BRIEFS` dict entry, switchable mid-stream.
- **Provenance posture:** render owner sources as a distinct **OWNER ARTIFACT** class (vs external SOURCE), provenance handle = file name / upload time / URL; the agent treats owner results as authoritative-but-don't-fabricate-beyond — it must NOT flag the owner's own experimental numbers as `[unverified]` the way it would an external claim.
- **Web intake:** a "New piece from my material" entry creating a flagship article from pasted text / an uploaded file / a URL; same attach affordance on an existing cluster article (→ fusion). Uploaded-file parsing is net-new (md/txt/log pass-through, `.ipynb` cell-concat, cap at `FETCH_MAX_CHARS`); `fetch_source` covers the URL sub-case only.
- **Read-layer:** teach `load_article_sources` (`queries.py:539`, joins `article_clusters→clusters→items` only, returns `[]` for flagship) to UNION `article_sources`; source the flagship Story row's topic/source/open-original from owner material (today degrade to —/[]/None) + an "owner material" indicator. Ship `tests/test_stories.py` (field-set assertion) + `tests/test_web.py` (StoryRow construction) updates in the same change.
- Then reuse Phase 4/5 unchanged for iterate → Gate 2 → publish.

**Scope — increments (each a separately verifiable slice; all folded in per owner 2026-06-21):**
- **10a — X/Twitter variant.** Add an `x` platform brief (single post + thread) to `app/variants`; `variants.platform` is a plain String → additive, **no migration**. The named #1 brand surface; `PLATFORMS=('medium','reddit','linkedin')` omits it, so "reuse Phase 5 unchanged" is inaccurate without this.
- **10b — Fusion-discovery UX.** On the New-piece-from-material flow, a "find related news" affordance: embed the owner's material → surface top-k related clusters via the existing dedup vector index, so the owner works **from a result toward news** (the natural direction), not only from an already-open cluster.
- **10c — Diagrams / code rendering ("beautiful").** A rendering/insertion seam: fenced-code syntax highlighting + diagram (mermaid/svg) in the editor preview and the variants. Heaviest item; v1 may be rendered-markdown + code fences with diagram/image authoring as a sub-step (`docs/01_technical.md` §2.6 promises "image insertion", unimplemented).

**Done — core:** the owner pastes/uploads/links his own material and gets a grounded canonical long-read in his voice with NO researcher cluster (drafted via `tech_explainer`); the same material attaches to a news-cluster article → a fused piece; the draft flows through iterate → Gate 2 → publish; the editor Sources panel + dashboard Story row show the owner material; the suite (incl. updated `test_stories`/`test_web`) is green. **Done — increments:** 10a a flagship piece formats to an X post + thread; 10b "find related news" returns relevant clusters for pasted material; 10c code blocks render and a diagram can be embedded.
**Builds:** backend (article_sources migration+model, grounding-guard relax, create_flagship_article, context assembly, tech_explainer brief, X/fusion backends, read-layer) ∥ frontend (intake UI, fusion affordance, diagram/code rendering).

## Phase 8 increments (owner-requested UI changes, logged)

Each is additive: it reuses the existing schema (no migration), adds no agent and no model call, and is covered by the test suite.

- **Editor version history + restore + source links** (2026-06-20). Every draft records a genesis snapshot, and each owner instruction records its resulting snapshot, in `edit_log`. The editor shows a **Version history** panel (per-version unified diff + restore-to-version; append-only — a restore is itself a logged version) and a **Sources** panel linking each linked cluster's item URLs (the original articles) so the owner can reopen and re-read them. Restore is bookkeeping only: it never publishes and refuses on a `published` canonical (the live KB entry). Files: `app/editor/article.py` (`_ensure_genesis`, `restore_article_version`), `app/editor/{draft,iterate}.py` + `app/digest/run.py` (genesis capture), `app/web/queries.py` (`load_article_versions`, `load_article_sources`), `app/web/ui_pages.py` (panels).

- **Unified "Stories" dashboard** (SPEC — increment in progress). FULL dashboard refactor: REMOVE every current section (cluster-status count cards, article-lifecycle count cards, "Ready to draft", "Recent clusters" table, "Recent articles" table) and leave ONLY one filterable, paginated **Stories** list. A *Story* is a derived aggregate (no schema change): one cluster + its 0..1 own draft, with digests as their own rows.
  - **Effective status** = the status of the cluster's OWN draft (a `hot_news`/`project_post` article, ~1:1) if it has one, else the cluster's Gate-1 status: `new → sent → approved → skipped → drafting → pre_publish → published`. DERIVED (a COALESCE over a LEFT JOIN `clusters → article_clusters → articles`), never a stored column. A cluster with its own 1:1 draft is shown as that article (no double row). A **digest** is its OWN Story row; the clusters it merely *covers* keep their OWN status + an "in digest" badge — a digest covering a `new`/`skipped` cluster must NOT relabel it `drafting`/`published` (that would corrupt the Gate-1 funnel and the digest covered-marker). The derivation therefore distinguishes a cluster's own draft from a digest that only covers it. (Schema rework was analysed and rejected: a clusters+articles merge is structurally impossible because a digest is 1 article : N clusters via `article_clusters`, and a stored unified-status column is unsafe; the aggregate is a read-layer projection only.)
  - **Title** = article → first `#` heading of `current_draft` (fallback: a linked cluster's `triage_title`); cluster → `triage_title`, fallback to a representative `item.title` (fixes the `(untitled)` rows), final fallback `(untitled)`.
  - **Layout**: the dashboard becomes JUST a status **filter** + the paginated Stories list (client-side pagination, ~260 rows; server-side deferred). **Columns**: status chip · title · topic · **source** (source-type chips — hn/x_user/rss/arxiv/github, from the cluster's items' sightings) · **open original ↗** (a representative item URL, new tab). **No score/ratio is shown** — the owner finds the blended score noise on the list; it STAYS in the model for ranking/triage, it is simply not displayed. A status filter (with optional per-status counts) replaces the old count cards. Per-row actions: un-drafted → **Approve / Skip** (Gate-1, reuse `app.bot.triage.decide`; **Approve also runs `fetch_cluster_full_text`** so the story is immediately draftable) / **Draft**; drafted/digest → **Open** (→ `/editor/{id}`).
  - **Backend**: new read-only `app/web/queries.py` helpers (`load_stories(...)` + `unified_status_counts(...)`) producing the aggregate; row actions reuse existing functions (`decide`, `fetch_cluster_full_text`, `create_article_for_cluster`, `draft_article`) via `run.io_bound`. Approve-from-web is a 2nd Gate-1 surface alongside Telegram — same guarded `decide()`, so exactly-once/idempotency holds and the bot's claim model is unaffected. No new agent, no model call in the list path.
  - **Vectors / series decision (recorded after analysis)**: keep the two existing vector uses AS-IS — *dedup* (item-title vectors → cluster grouping; CORE, no series replacement) and *KB retrieval* (`articles.embedding`; a dormant near-free seam — pgvector is already mandatory for dedup, KB is one embed per publish and returns `[]` until the corpus grows). Do NOT add an explicit `series` table now (premature at 1 published article + a per-piece curation tax). "Threads" are delivered cheaply by grouping published pieces by their cluster's `topic` (next increment). Both KB→topic-filter and explicit-series stay behind clean seams (`kb_search(session, query, top_k)`; a future nullable `articles.series_id`) for a cheap later revisit.
  - **Then (following increment)**: a topic filter + a "Threads" view = published pieces grouped by cluster `topic`, chronological ("show all my GPT pieces"), zero migration.
  - **Done**: one filterable/paginated Stories list with correct effective status; Approve/Skip/Draft/open-original work from a row; drafted stories open the editor; `(untitled)` replaced by the item-title fallback; suite green; verified in the preview.

## Open technical decisions (intentionally unspecified)

Pick a reasonable default behind a clean seam; revisit with real data.

- **Dedup similarity threshold** — the cosine threshold (and any title/URL heuristics) for grouping items into one cluster.
- **Topic classifier** — the prompt and label set for tagging ambiguous items.
- **Paywall / JS pages** — how the web fetcher (`app/fetcher`) handles member-only or JS-rendered pages in pass-2 extraction (Medium member posts truncate to preview, etc.).
- **Feed-URL verification** — confirm the exact feed/endpoint URLs for each configured source.
- **Ranking weights** — the blend weights for native rating vs cross-source frequency vs recency.
- **Triage selection & delivery rule** — which clusters get a triage summary and a Telegram push (top-N per topic, score threshold, daily cap) and the bot's DB-check interval.
- **Per-piece-type templates** — the structural templates/prompts for `hot_news`, `digest`, `project_post`, refined by experiment.
- **Embedding dimensions / storage** — vector dimension and index choice in pgvector.
- **Morning-brief defaults (Phase 9) — DECIDED 2026-06-21 (behind seams):** fixed rolling lookback (reuse the digest window) + top-N + age-out for the tail; ONE daily `HH:MM` brief across all topics; at-most-once-per-cluster send (claim-after-confirmed-chunk, never claim-all-then-send); the `cheap` preamble deferred to a fast-follow. Still tunable with real data: exact window length, top-N, delivery time.
- **Owner-material storage (Phase 10) — DECIDED 2026-06-21:** a dedicated `article_sources` table (`article_id` FK `ON DELETE CASCADE`, `kind`, `title`, `url` nullable, `content`, `created_at`). The synthetic-owner-cluster alternative is REJECTED (pollutes digest/dedup/ranking). Still open: parse depth for large notebooks/logs — cap at the bundle item char limit; any summarize step stays **strictly extractive** (never drop the owner's own numbers).
- **Flagship piece_type (Phase 10) — DECIDED 2026-06-21:** add a `tech_explainer` brief (motivation → mechanism → worked example → when-to-use → caveats), default for the own-material explainer register; keep `project_post` for build logs.
- **Diagram / code rendering depth (Phase 10c)** — v1 = rendered markdown + fenced-code highlighting only, vs full diagram (mermaid/svg) + image authoring. Decide at 10c.

## Testing notes (single user)

- Each phase is validated by the owner exercising it directly; there is no need for load testing.
- Phases 0–1 are inspected via the DB and logs. Phase 2 onward is exercised through Telegram and the web app.
- Keep a small set of fixture sources/items for repeatable local runs so the researcher and editor can be tested without waiting on live feeds.
