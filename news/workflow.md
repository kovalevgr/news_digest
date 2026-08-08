# news workflow — the routine's single source of truth

- **Status:** active
- **Owner:** news routine (scheduled Claude Code cloud agent; its live prompt is just
  "Run the daily research using news/workflow.md")
- **Scope:** everything under `news/` only. Never touch `app/`, `tests/`, `migrations/`,
  `config.yaml`, `content/`, or anything outside `news/`.

## GOAL

Daily per-company AI-news collection into `news/topics/` AND technical-radar
collection into `news/radar/` (practitioner signal: builds, techniques, trends),
plus a weekly digest on Sunday with a radar-ideas section.

- Agent-facing instructions (this file, run-log entries, item summaries in topics files)
  are in **ENGLISH**.
- All reader-facing TEXT — `weeks/<ISO-week>/summary.md`, the `## card` block in
  artifacts, Linear card descriptions — is in **UKRAINIAN**.

## THE DAILY RUN

1. **Read state.** Read `config/sources.json` + `config/companies.md` + each
   `topics/<company>.md` (the dedup base). Determine the window = since the last
   successful run (see `run-log.md`; default **26h** if no prior entry).

2. **TIER-1 fetch.** Run `python3 news/scripts/fetch_feeds.py` (deterministic, stdlib-only,
   no tokens). Output: JSON candidates per company from all TIER-1 (`kind: "rss"`) feeds.
   Every company from config appears in the output — an empty `fresh` list is the
   gap-scrape signal. The script maintains its own HTTP cursors (ETag / Last-Modified /
   last_run) in `state/cursors.json` — leave that file to the script; never edit it by hand.

3. **GAP SCRAPE** — ONLY for companies with zero fresh candidates. Walk the fetch ladder
   for that company as configured in `sources.json`:
   - tier `"fetch"` → WebFetch the page;
   - tier `"jina"` → bash `curl https://r.jina.ai/<url>` (add header
     `"Authorization: Bearer $JINA_API_KEY"` if the env var exists);
   - last resort → WebSearch `"<company> announcement news <current month year>"`.

   **MAX ONE fallback attempt per company** (no loops). On timeout/error: record it in
   `run-log.md`, move on to the next company.

4. **DEDUP + CONFIRM.**
   - First pass (deterministic): canonical-URL match vs items already in `topics/`.
   - Second pass (judgement): "is this the same story?" vs this week's titles.
   - Cross-company same-URL: keep the item in the company that **OWNS** the announcement;
     mark the other with `[duplicate]` + a wikilink to the owning company.
   - Confirm each candidate is a real announcement — not ads, hiring posts, or a
     roundup-of-others.
   - **NEVER invent facts; carry the source URL on every item.**

5. **WRITE STATE.**
   - Append confirmed items to `topics/<company>.md` under this week's heading
     (`## YYYY-Www`), using the item format in OBSIDIAN CONVENTIONS below.
   - Write one raw artifact file per NEW item to
     `artifacts/YYYY-MM-DD-<company>-<slug>.md`: frontmatter + a one-two sentence
     English excerpt (feeds the topics line), then a `## card` block IN UKRAINIAN
     (feeds the Linear card and the weekly digest):
       - `**Що сталося:**` 2–3 sentences — the story itself;
       - `**Контекст:**` 1–2 sentences of FACTUAL context only (related prior
         announcements, what this supersedes or continues) — no opinions, no takes;
       - `**Деталі:**` bullet list of key facts (numbers, dates, availability, pricing).
     Everything in the card block must come from the fetched source — never pad.
   - **LINEAR CARDS** (if the Linear connector is available; else skip silently).
     Search project "News digest" by URL/title first — never duplicate. Then create
     one issue per NEW story (team "Kovalevgr", project "News digest", status Todo):
       - title: `[<Company>] <original English title>`;
       - description: the artifact's `## card` block verbatim, then a footer line
         `Джерело: <url> · Опубліковано: YYYY-MM-DD · Артефакт: news/artifacts/<file>`;
       - priority: High(2) = major model/product launch or major org news,
         Medium(3) = regular announcement, Low(4) = minor update;
       - exactly ONE type label: `model-release` | `product` | `research` |
         `policy-safety` | `business` | `infra`;
       - `[duplicate]` stories → status Duplicate, marked duplicateOf the owning card.
     Never move cards out of In Progress / Done / Canceled — those are the owner's.

6. **LOG + COMMIT.**
   - Append a run entry to `run-log.md`: per company — searched / found / fell-back /
     errors; plus totals.
   - Then make **ONE** git commit:
     `news: daily run YYYY-MM-DD (+N items, M companies fresh)` — and push.

## THE RADAR (daily, after the company core)

The radar collects TECHNICAL practitioner signal (what people build, techniques to
try, trends) — a different content type from company news, kept in separate files.
Config: `config/radar.json`. Volume budget: **≤ ~15 confirmed items/day total** —
when in doubt, drop.

1. **Fetch.** Run `python3 news/scripts/fetch_radar.py` (deterministic, stdlib-only).
   Output: JSON with `fresh` candidates per source, grouped by category. The script
   owns `state/radar-cursors.json` — never edit it by hand. Source errors are
   reported in-band; **NO gap-scrape ladder for radar sources** — a silent radar
   source today just means no items today (log and move on).

2. **TRIAGE (judgement).** For each candidate keep it only if a technical builder
   would care: real engineering/technique/benchmark/release content. Drop: product
   marketing that survived the config filters, memes/appreciation posts (Reddit),
   consumer-app launches (HN), finance/markets posts (SemiAnalysis), tutorial-grade
   Copilot education (GitHub). GPU MODE videos appear twice (livestream + edited
   cut) — keep one. smol.ai issues titled "not much happened today" → skip that day.

3. **DEDUP.** By canonical URL vs the target `radar/<category>.md` file, then
   judgement vs this week's radar titles ("same story?"). An item already covered in
   a COMPANY topics file is not re-added to radar (link the company page instead if
   the radar angle adds something).

4. **WRITE.** Append confirmed items to `radar/<category>.md` under this week's
   `## YYYY-Www` heading, uniform item format (same as topics) with an optional
   signal suffix: `(123 pts)` for HN, `(45 upvotes)` for HF papers. Категорії:
   `lab-engineering`, `inference-infra`, `oss-ml-systems`, `bigtech-eng`,
   `research-institutes`, `technical-newsletters`, `practitioner-blogs`, `youtube`,
   `community`, `mistral-watch`. No artifacts and NO Linear cards for daily radar
   items — the radar surfaces weekly (see below).

5. **LOG.** Add a `radar:` line to the run-log entry: per-category counts + errors.

Expected/known behaviors (do not treat as failures): `karpathy-blog` is disabled
(Cloudflare; needs JINA_API_KEY); Reddit 429 → skip, never retry-loop; first run of
a seen-dedup source seeds silently and yields nothing; `mistral-docs-changelog`
emits a single "page updated" item — fetch the page for what actually changed
before writing the item line.

## THE WEEKLY DIGEST (Sunday run)

After the daily run on Sunday:

1. Read this week's sections of all `topics/*.md`.
2. Write `weeks/<ISO-week>/summary.md` **IN UKRAINIAN**:
   - Frontmatter: `week`, `items`, `companies_fresh`, `companies_tracked`, `generated`.
   - Header `Підсумок тижня` with counts (items, companies).
   - `## Що це означає` — a short narrative tying the week's stories into threads;
     factual only, no invented takes.
   - Per-company sections (ordered by item count, desc): each item —
     `- **date** — [title](url)` + the artifact's `**Що сталося:**` text as an
     indented paragraph. High-priority stories (per the Linear priority rubric)
     get a `⭐` marker and their `**Деталі:**` bullets (trim to the 3–4 most
     telling). Items without a card block fall back to the one-line topics
     summary. `[duplicate]` markers preserved.
   - A coverage line:
     `Покриття: <companies with fresh items>. Без свіжого: <silent companies>.`
   - **NO stale filler** — a silent company is REPORTED silent, never padded with old
     or invented items.
3. **RADAR IDEAS (the week's harvest).** Read this week's sections of all
   `radar/*.md`. Select **5–10 ideas** worth the owner's hands-on time — favor items
   that are reproducible (code available, clear technique) and could seed an article.
   Add a `## Radar: ідеї тижня` section to `weeks/<ISO-week>/summary.md` — each idea
   IN UKRAINIAN as a card:
   - `**Що це:**` 1–2 sentences — the thing itself;
   - `**Чому цікаво:**` 1 sentence — the technical hook (facts only, no invented takes);
   - `**Мінімальний експеримент:**` 1–2 sentences — the smallest hands-on try;
   - `**Тип статті:**` `tech_explainer` | `project_post`;
   - source link(s) on every card — **never invent; every claim carries its URL**.
4. **RADAR LINEAR CARDS** (if the Linear connector is available; else skip silently).
   Project "Radar" (team "Kovalevgr") — search by title first, never duplicate. One
   issue per idea card, status Todo: title `[Idea] <short name>`, description = the
   idea card verbatim + `Джерела:` links. Board semantics: Todo = idea backlog;
   In Progress / Done / Canceled are the OWNER's states — never move cards out of
   them. Cards not taken by the owner just stay in Todo (no auto-close for Radar).
5. **Close the news board week** (if the Linear connector is available; else skip
   silently): every card in project "News digest" still in status Todo whose story is
   in this week's digest → status Done. Leave In Progress / Canceled / Duplicate
   cards untouched — those are the owner's states.
6. Commit + push.
7. Delivery to Telegram / a Linear doc: a later step — **TODO**, not part of this run.

## PRINCIPLES

1. timeout/error → one fallback, then log and move on;
2. duplicates are marked, never re-added;
3. the agent NEVER invents anything — every item carries its source URL; opinions are
   never added.

## OBSIDIAN CONVENTIONS

- Every item line links its company as `[[<company-slug>]]` (the wikilink lives in the
  week-section context of the topics/digest files; topic pages themselves are the targets).
- `topics/<company>.md` **IS** the company MOC page — no separate index pages.
- Uniform item format (one line per item):

  `- **YYYY-MM-DD** — [<title>](<url>) — <one-line summary in English>. <optional [duplicate] → [[other-company]]>`

- Topics file frontmatter: `company`, `aliases`, `sources` (list), `updated`.

## FAILURE MODES

| Failure | Symptom | Action |
| --- | --- | --- |
| Feed 4xx/5xx | fetch_feeds.py reports the source in `source_errors` | One fallback via the company's ladder; log in run-log; move on |
| Radar source error | fetch_radar.py reports it in `errors` | NO fallback ladder for radar — log in run-log, move on (a quiet radar source is normal) |
| Reddit 429 | fetch_radar reports HTTP 429 | Skip for this run; never retry-loop; never add a second reddit call |
| microsoft.com 403 | company feed error despite headers in config | The edge rotated its bot rules — do NOT strip the headers; log and move on |
| Feed content-type trap | URL returns 200 but body is HTML, not RSS/Atom (known: `cursor.com/rss.xml`, `cohere.com/blog/rss.xml`) | fetch_feeds.py logs "TRAP/not-a-feed" and skips; never add these URLs to config |
| Jina 403 AbuseAlleviation | Perplexity via anonymous Jina | Needs `JINA_API_KEY`; if absent → WebSearch fallback |
| WebFetch target-403 | Site blocks the direct fetch | Retry ONCE via Jina (`https://r.jina.ai/<url>`) |
| Empty week | No fresh items anywhere on Sunday | Still write the digest: counts of zero + full "Без свіжого" list; never pad |
