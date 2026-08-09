# news workflow — the routine's single source of truth

- **Status:** active
- **Owner:** THREE scheduled Claude Code cloud routines, each running its section of
  this file: **daily-ai-news** (06:00 UTC — THE DAILY RUN), **daily-radar**
  (05:00 UTC — THE RADAR), **weekly-ai-digest** (Sunday 07:00 UTC — THE WEEKLY
  DIGEST). Live prompts are one-liners pointing here; format details live ONLY here.
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

## THE RADAR (its own daily routine — **daily-radar**, 05:00 UTC)

The radar runs in a SEPARATE cloud routine from the company core (live prompt:
"Run the daily radar using news/workflow.md") — either routine can be disabled
without touching the other. It collects TECHNICAL practitioner signal (what people
build, techniques to try, trends) into `radar/*.md` and surfaces **0–3 daily
highlights**. Config: `config/radar.json`; interest profile: `config/interests.md`.
Volume budget: **≤ ~15 confirmed items/day total** — when in doubt, drop.

1. **Fetch.** Run `python3 news/scripts/fetch_radar.py` (deterministic, stdlib-only).
   Output: JSON with `fresh` candidates per source, grouped by category. The script
   owns `state/radar-cursors.json` — never edit it by hand. Source errors are
   reported in-band; **NO gap-scrape ladder for radar sources** — a silent radar
   source today just means no items today (log and move on).

2. **TRIAGE (judgement, two passes).**
   - Pass 1 — technical bar: keep only items a technical builder would care about
     (real engineering/technique/benchmark/release content). Drop: product marketing
     that survived the config filters, memes/appreciation posts (Reddit),
     consumer-app launches (HN), finance/markets posts (SemiAnalysis),
     tutorial-grade Copilot education (GitHub). GPU MODE videos appear twice
     (livestream + edited cut) — keep one. smol.ai issues titled "not much happened
     today" → skip that day.
   - Pass 2 — owner fit: score each survivor **high / medium / low** against
     `config/interests.md` ("is this THE OWNER's material and could it seed an
     article?"). The score drives highlight selection; low-fit items still land in
     the radar files if they cleared pass 1.

3. **VERIFY SUBSTANCE (highlight candidates only).** For up to 5 highest-scored
   candidates, read the actual content and confirm it delivers what the title
   promises (real technique, numbers, code — not clickbait or a marketing shell).
   **Transport per platform — WebFetch is BLOCKED for github.com and reddit.com in
   the cloud env (verified 2026-08-09):**
   - reddit.com → bash `curl -sS -A "Mozilla/5.0 ..."` on the post URL (browser UA
     mandatory, same as the fetcher); the feed entry's own body text is also a
     valid basis if curl 429s;
   - github.com repos → read the README via the git proxy:
     `git clone --depth 1 <repo-url> /tmp/verify-<name>` (REST API and web pages
     are gateway-blocked; anonymous git reads of public repos work);
   - everything else → WebFetch, with ONE curl retry on failure.
   A candidate that fails verification stays a regular radar item but is out of
   highlight consideration. Transport error → same: keep item, skip highlight.

4. **DEDUP.** By canonical URL vs the target `radar/<category>.md` file, then
   judgement vs this week's radar titles ("same story?"). An item already covered in
   a COMPANY topics file is not re-added to radar (link the company page instead if
   the radar angle adds something).

5. **WRITE.** Append confirmed items to `radar/<category>.md` under this week's
   `## YYYY-Www` heading, uniform item format (same as topics) with an optional
   signal suffix: `(123 pts)` for HN, `(45 upvotes)` for HF papers. Категорії:
   `lab-engineering`, `inference-infra`, `oss-ml-systems`, `bigtech-eng`,
   `research-institutes`, `technical-newsletters`, `practitioner-blogs`, `youtube`,
   `community`, `mistral-watch`. No artifacts for radar items.

6. **DAILY HIGHLIGHTS (0–3).** From the verified candidates pick at most 3 the
   owner should see TODAY. **Zero on quiet days — never pad.** When ≥1:
   - Write `radar/daily/YYYY-MM-DD.md` **IN UKRAINIAN**: per highlight —
     `- **[<title>](<url>)**` + `**Що це:**` 1–2 sentences + `**Чому сьогодні:**`
     1 sentence (the hook — factual, no invented takes). No file on zero-highlight
     days (run-log records the quiet day).
   - **Linear cards** (if the connector is available; else skip silently): project
     "Radar" (team "Kovalevgr"), status Todo, label `highlight` **plus exactly ONE
     source label from the `src` group** (`reddit`, `hn`, `github`, `hf`, `blog`,
     `newsletter`, `youtube`, `lobsters`, `smolai`, `docs` — pick by the item's
     source platform; if none fits, create the missing label INSIDE the `src`
     group, never at top level), title `[Highlight] <original title>`, description
     = the Ukrainian highlight card + `Джерело: <url>`. Search the project by
     URL/title first — never duplicate (an item already carded as a highlight or
     an `[Idea]` is skipped).
   - Highlight cards are ephemeral attention pointers — the Sunday run closes the
     stale ones (see THE WEEKLY DIGEST).

7. **LOG + COMMIT.** Append a radar run entry to `run-log.md`: per-category table
   with `raw candidates` = the EXACT count of items in fetch_radar.py's `fresh`
   arrays for that category (count from the JSON — the table and the triage prose
   must agree on the same numbers), `confirmed`, errors; then triage detail prose
   (what was dropped and WHY — this is the conversion audit trail), highlight
   count. Then ONE git commit:
   `news: radar run YYYY-MM-DD (+N items, H highlights)` — and push.

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
   idea card verbatim + `Джерела:` links, **exactly ONE source label from the `src`
   group** (`reddit`, `hn`, `github`, `hf`, `blog`, `newsletter`, `youtube`,
   `lobsters`, `smolai`, `docs`; if none fits, create it INSIDE the `src` group).
   Board semantics: Todo = idea backlog; In Progress / Done / Canceled are the
   OWNER's states — never move cards out of them. Cards not taken by the owner just
   stay in Todo (no auto-close for `[Idea]` cards).
5. **DIGEST CARD** (if the Linear connector is available; else skip silently).
   Project "News digest" (team "Kovalevgr"): search by title
   `📰 Тижневий дайджест <ISO-week>` first — **update it if it exists, create it
   otherwise, never duplicate**. Status Todo; description = the full digest text
   from `weeks/<ISO-week>/summary.md` (drop the frontmatter, keep everything else
   including the Radar section) + a footer line `Артефакт: news/weeks/<ISO-week>/summary.md`.
   This card IS the owner's phone-readable delivery of the digest — it is not
   optional. The card stays in Todo until the owner reads it (owner's state).
6. **Close the news board week** (if the Linear connector is available; else skip
   silently): every card in project "News digest" still in status Todo whose story is
   in this week's digest → status Done (the digest card itself from step 5 stays
   Todo). Also in project "Radar": cards with label `highlight` still in Todo →
   Done (attention pointers expire with the week); NEVER touch `[Idea]` cards or
   anything in owner states (In Progress / Done / Canceled).
7. Commit + push.
8. Delivery to Telegram: a later step — **TODO**, not part of this run.

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
