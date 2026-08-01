# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal, non-commercial AI/IT content engine for a single user (the **owner**): it researches tech news, drafts commentary in the owner's voice grounded in the sources, and produces platform-ready variants for LinkedIn / Medium / Reddit. The owner publishes manually — the system never posts.

## Current state

**Phases 0–4 are implemented.** Phase 0 (foundation: config loader, DB schema/migrations for all eight tables, `app/llm` role→model seam, Docker Compose), Phase 1 (researcher: source adapters except Reddit, scheduler, ingest → embed/dedup → ranked, topic-tagged clusters), Phase 2 (triage / Gate 1: the triage-summary stage, `app/fetcher` pass-2 full-text, and the Telegram bot), Phase 3 (editor draft: the `app/web` editor skeleton + the `app/editor` writer-agent draft phase — context assembly over the `content/` voice files, on-demand tools, grounding, `piece_type`), and Phase 4 (editor iterate + Gate 2: `app/editor/iterate.py` edit-in-place iteration — the same writer-agent extended, respects manual hand-edits via `base_draft`, appends every instruction to `edit_log`, piece-type switchable mid-stream; `approve_article` Gate-2 → `pre_publish`; the `app/web/chat.handle_editor_message` seam + the NiceGUI chat / piece-switch / approve controls) are done and verified. **Next is Phase 5** (variants + mark-as-published) in `docs/03_build_plan.md`. Reddit (`reddit_sub`) remains a deferred, owner-credential-gated adapter seam.

## Read order

1. `docs/00_overview.md` — purpose, the pipeline, principles.
2. `docs/01_technical.md` — architecture, components, data model, LLM/agent spec.
3. `docs/02_infra.md` — hosting, Docker Compose, config, secrets, deploy.
4. `docs/03_build_plan.md` — the phased plan to work through, plus the list of intentionally open decisions.
5. `config.yaml` (repo root) — the **authoritative** config shape: use exactly these source types (`x_user`, `github`, `rss`, `reddit_sub`, `hn`, `arxiv`) and field names; do not invent new ones. It is the runtime file, not documentation — on any divergence from a doc, `config.yaml` wins.

## Architecture (the big picture)

A **staged pipeline, not a multi-agent system**. Stages coordinate only through Postgres — each stage writes its state/output to the DB and the next stage reads it; stages never call each other.

```
researcher (poller) → clusters ranked in Postgres
  → Gate 1: owner approves/skips a story in Telegram (bot)
  → writer-agent drafts canonical long-read (web app)
  → owner iterates via chat, edit-in-place (web app)
  → Gate 2: owner approves the canonical
  → per-platform variant on demand (single model call)
  → owner copies and posts manually
```

- **Researcher** is deterministic code: scheduler + source adapters + cursors + embed/dedup into clusters + blended ranking. Two-pass fetch: metadata for everything (pass 1), full text only after Gate 1 approval (pass 2).
- **Clusters are first-class**: dedup groups items into one cluster per story; triage, ranking, and approval all operate at the cluster level, never per item.
- **Eight tables**: `items`, `sightings`, `clusters`, `articles`, `article_clusters`, `edit_log`, `variants`, `cursors`. An item is one canonical URL; a sighting is one source's observation of it (with that platform's engagement) — cross-source frequency counts distinct sighting sources. A published article + its embedding *is* the knowledge base for voice/continuity retrieval — there is no separate "finals" table.
- **Writer-agent** (the only agent) gets on-demand tools: `kb_search`, `fetch_source`, optional `web_search`. Iteration is edit-in-place on the working draft — never full regeneration — and must respect the owner's manual edits. Every owner instruction is appended to `edit_log` (the voice training signal).
- **Digest** is a weekly scheduled query over the rolling store run by the bot (window → exclude clusters already linked via `article_clusters` → rank → top N → summarize), not a fresh poll. The run creates the `digest` article up front and links its clusters — that linkage is what keeps overlapping windows from repeating stories.

## Hard rules (never violate)

- **Never publish anything.** No auto-posting and no publishing/posting API integration. Output is text plus per-platform formatting for the owner to copy and post.
- **Drafting is grounded.** Use only facts from the approved sources plus anything explicitly fetched via the tools; carry provenance links; flag unverified claims; never invent facts. Opinions and takes are the owner's — propose them, never assert them as the owner's own.
- **Config is a file, not the DB.** Sources, people, topics, cadences, and digest schedules live in `config.yaml` (read-only mount). Only poll cursors persist in the database. Secrets come from the environment — never in YAML or git.
- **Postgres + pgvector is the single source of truth** and the only way stages coordinate. Stages do not call each other.
- **One agent only:** the writer/editor (draft + iterate, with on-demand tools). Everything else is a single-shot model call or deterministic code. Do not turn the researcher, triage, or variant formatting into agents.
- **The model is swappable.** Steps use a logical role (`generation` / `generation_high` / `cheap` / `embedding`); never hardcode a specific model. The role→model mapping lives in config.

## Stack & repo layout (targets, from the build plan)

Python; FastAPI + Uvicorn (web); the editor UI is **NiceGUI mounted on FastAPI** (`ui.run_with(app, …)`) — a minimal admin dashboard + a chat-drafting editor; see [`app/web/README.md`](app/web/README.md); SQLAlchemy + Alembic; Postgres with pgvector (`pgvector/pgvector:pg16` image); APScheduler in the poller; `python-telegram-bot` (long-polling default); model transport via Vertex (ADC) or the Anthropic SDK.

```
app/
  llm/          # generate(messages, role, tools), embed(texts); role->model config
  db/           # schema, migrations, query helpers
  adapters/     # one module per source type (rss, reddit, x, hn, github) -> common Item
  fetcher/      # full-text extraction (readability + optional headless): pass-2 + fetch_source
  researcher/   # scheduler, polling, dedup/clustering, ranking, topic tagging
  editor/       # writer-agent (draft + iterate), tools, context assembly, grounding
  variants/     # per-platform single-call formatters
  digest/       # scheduled digest query
  bot/          # Telegram triage (Gate 1) + digest delivery
  web/          # editor web app (chat + live preview + admin/status)
config.yaml     # mounted read-only
content/        # owner voice files: style_guide.md, anti_patterns.md, projects/ (read-only mount)
migrations/
docker-compose.yml, Dockerfile, Caddyfile, .env (gitignored)
```

The `web`, `bot`, and `poller` services are the **same Python image** run with different commands.

## Run

`docker compose up -d --build` — services `db`, `web`, `bot`, `poller`, `proxy`. On first run, ensure the `vector` extension and the migrations are applied. See `docs/02_infra.md` §3 and §8.

## How to work here

- Build in **vertical, testable slices** in the order in `docs/03_build_plan.md`. Each phase must run and be verifiable before starting the next.
- Some decisions are **intentionally open** (dedup threshold, classifier prompt/labels, paywall extraction, feed-URL verification, ranking weights, piece-type templates, embedding dimensions — see the build plan). Build a clean seam, pick a sensible default, and do not block on them.
- Single user, no scale requirements. When two designs are equally correct, choose the simpler one.
- Keep a small set of fixture sources/items for repeatable local runs, so the researcher and editor can be tested without waiting on live feeds.
- Enable prompt caching on repeated context (style guide, retrieved context, the working draft during iteration) — iteration resends the same context each turn.

## Claude tooling (.claude/)

- **Agents:** `backend`, `frontend`, `devops`, `rules-reviewer`. Run `rules-reviewer` on every completed slice and before closing a phase. Natural parallel pairs: backend ∥ devops (Phase 0), backend ∥ frontend (Phases 3–4).
- **Skills:** `/config-edit` (safe `config.yaml` edits; its bundled validator also runs automatically as a PostToolUse hook on every config.yaml edit), `/phase-check` (run the current phase's Done criteria), `/db-inspect` (canned pipeline queries), `/deploy` (owner-run VM runbook; manual-only).

## When unsure

Prefer the simplest correct option, keep the seam swappable, and leave a clear note rather than guessing on an open decision.
