# news/ — file-based news core

This module is the state store + recipe for the daily news researcher: a scheduled
Claude Code cloud routine that clones this repo, collects per-company AI news into
markdown files, and pushes. **There is no database — these files plus git ARE the store.**
All files are Obsidian-native (frontmatter, wikilinks), so the vault doubles as the UI.

How it relates to the rest of the repo:

- `app/` — the legacy Postgres pipeline (poller/bot/web). Read-only reference; being retired.
- `pieces/` + `published/` — article writing, driven by skills downstream of this module.
- `content/` — the owner's voice files (style guide, anti-patterns); used by the writing side.
- `news/workflow.md` — the single source of truth the routine follows every run.

The daily/weekly flow:

- **Daily:** `scripts/fetch_feeds.py` pulls all TIER-1 RSS feeds (deterministic, no tokens).
- **Gap scrape:** companies with zero fresh items get ONE fallback (WebFetch / Jina / WebSearch).
- **Dedup + confirm:** canonical-URL match against `topics/`, then judgement vs this week's titles.
- **Write state:** confirmed items appended to `topics/<company>.md`; one raw artifact per new
  item in `artifacts/`; run logged in `run-log.md`; one commit, one push.
- **Sunday:** weekly digest in Ukrainian → `weeks/<ISO-week>/summary.md`; silent companies are
  reported silent, never padded.
