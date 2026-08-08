# news workflow — the routine's single source of truth

- **Status:** active
- **Owner:** news routine (scheduled Claude Code cloud agent; its live prompt is just
  "Run the daily research using news/workflow.md")
- **Scope:** everything under `news/` only. Never touch `app/`, `tests/`, `migrations/`,
  `config.yaml`, `content/`, or anything outside `news/`.

## GOAL

Daily per-company AI-news collection into `news/topics/`, plus a weekly digest on Sunday.

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

## THE WEEKLY DIGEST (Sunday run)

After the daily run on Sunday:

1. Read this week's sections of all `topics/*.md`.
2. Write `weeks/<ISO-week>/summary.md` **IN UKRAINIAN**:
   - Header `Підсумок тижня` with counts (items, companies).
   - Per-company sections: date + title + one-line `Коротко:` + link;
     `[duplicate]` markers preserved.
   - A coverage line:
     `Покриття: <companies with fresh items>. Без свіжого: <silent companies>.`
   - **NO stale filler** — a silent company is REPORTED silent, never padded with old
     or invented items.
3. **Close the board week** (if the Linear connector is available; else skip silently):
   every card in project "News digest" still in status Todo whose story is in this
   week's digest → status Done. Leave In Progress / Canceled / Duplicate cards
   untouched — those are the owner's states.
4. Commit + push.
5. Delivery to Telegram / a Linear doc: a later step — **TODO**, not part of this run.

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
| Feed content-type trap | URL returns 200 but body is HTML, not RSS/Atom (known: `cursor.com/rss.xml`, `cohere.com/blog/rss.xml`) | fetch_feeds.py logs "TRAP/not-a-feed" and skips; never add these URLs to config |
| Jina 403 AbuseAlleviation | Perplexity via anonymous Jina | Needs `JINA_API_KEY`; if absent → WebSearch fallback |
| WebFetch target-403 | Site blocks the direct fetch | Retry ONCE via Jina (`https://r.jina.ai/<url>`) |
| Empty week | No fresh items anywhere on Sunday | Still write the digest: counts of zero + full "Без свіжого" list; never pad |
