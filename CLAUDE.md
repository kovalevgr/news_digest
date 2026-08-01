# CLAUDE.md

This file guides Claude Code when working in this repository.

## What this is

A personal, file-based **AI-news engine + article-writing studio** for a single user (the **owner**). There is **no database, no web app, no deploy** — markdown files + git ARE the system. Two loosely-coupled halves:

1. **News core (`news/`)** — a daily scheduled Claude Code cloud routine follows `news/workflow.md`: fetches 12 AI-company sources (deterministic feed script first, agentic gap-scrape only for holes), dedups, appends items to per-company `news/topics/*.md`, logs, commits, pushes. Weekly (Sunday) it writes a Ukrainian per-company digest to `news/weeks/`.
2. **Writing studio (`pieces/`, `published/`)** — the owner drafts interactively in Claude Code via skills: `/draft-piece` → iterate in-session → `/approve-piece` (Gate 2) → platform variants (`/linkedin-variant`, `/x-variant`, `/medium-variant`, `/reddit-variant`) → `/publish-piece` (bookkeeping only). `published/` is the voice knowledge base future drafts read.

Viewers: **Obsidian** (this repo is the vault; wikilinks + frontmatter are load-bearing), **Linear** (board, written by the routine via connector), **GitHub** (sync hub — the cloud routine clones/pushes).

## Hard rules (never violate)

- **Never publish anything, anywhere.** No posting, no publishing APIs. Every output is text the owner copies and posts manually. `/publish-piece` only records that the owner already posted.
- **Grounded, always.** Never invent facts. Every news item and every draft claim carries its source URL. Unverified claims are flagged. Takes/opinions are proposed to the owner, never asserted as theirs.
- **Files + git are the single source of truth.** State lives in markdown/JSON in this repo; history lives in git. No hidden state.
- **The owner's hand-edits are sacred.** Always re-read a file before editing it; edit in place; never regenerate a draft wholesale.
- **Every meaningful edit is a commit.** Draft iterations commit with the owner's instruction as the message (that history is the voice-training signal).

## Layout

```
news/            # news core: workflow.md (THE recipe), config/, scripts/, topics/, artifacts/, weeks/, state/, run-log.md
pieces/          # working drafts: <slug>/{draft.md, meta.yaml, sources/, variants/}
published/       # frozen published canonicals (the voice KB)
content/         # owner voice files: style_guide.md, anti_patterns.md (read-only reference)
.claude/skills/  # the writing skills (draft/approve/4 variants/publish)
```

## Read order

1. `news/workflow.md` — the routine's full recipe (daily + weekly), principles, failure modes.
2. `news/config/companies.md` + `news/config/sources.json` — tracked companies, verified source URLs, fetch tiers (rss → WebFetch → Jina), trap warnings.
3. `.claude/skills/*/SKILL.md` — the writing flow and its gates.

## Operational notes

- The daily routine runs in Anthropic cloud, in the custom-network environment **"Test"** (allowlisted domains; the Default env blocks all bash egress). Model: Sonnet daily, Opus for the weekly digest.
- `news/scripts/fetch_feeds.py` is stdlib-only (runs in a bare cloud sandbox). Its HTTP cursors live in `news/state/cursors.json` — committed, never hand-edited.
- Perplexity needs an authenticated Jina call (`JINA_API_KEY`); anonymous Jina 403s it. Until the key is set, cover it via WebSearch or skip.
- Digest/summary text for the owner is **Ukrainian**; agent-facing instructions stay English.

## Legacy

The original system (Python staged pipeline: Postgres + pgvector, FastAPI/NiceGUI editor, Telegram bot, Docker — feature-complete through Phase 10, 505+ tests) lives intact in git history at the root commit `1775fc5` ("Initial commit"). Restore any part with `git checkout 1775fc5 -- <path>`. Do not resurrect it casually — the file-based flow above replaced it deliberately (2026-08-01).
