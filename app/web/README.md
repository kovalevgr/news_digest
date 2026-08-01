# `app/web` — the editor web app (admin + chat-drafting UI)

The one always-on HTTP surface: a **minimal admin dashboard** + a **chat-driven editor** where
the owner turns an approved story into a grounded draft, **iterates on it conversationally
(Phase 4, edit-in-place)**, **switches piece type mid-stream**, and **approves it at Gate 2**.

## What we built & what we used

The UI is built with **[NiceGUI](https://nicegui.io/)** — a pure-Python UI framework — chosen
deliberately as a **ready SDK so we don't hand-roll templates/JS**. (An earlier Phase-3 skeleton
used FastAPI + Jinja2 + vanilla JS; it was replaced by NiceGUI for the admin + chat experience.)

| Concern | What we used |
| --- | --- |
| UI framework | **NiceGUI** (`nicegui>=3.13`) — pages, components (`ui.card`, `ui.table`, `ui.splitter`, `ui.chat_message`, `ui.markdown`, `ui.textarea`), notifications |
| HTTP host | **FastAPI** — NiceGUI is *mounted onto* the existing app via `ui.run_with(app, mount_path="/", storage_secret=…)`, so `uvicorn app.web:app` and the compose `web` service are unchanged |
| Off-loop work | `nicegui.run.io_bound(...)` — the blocking writer-agent draft runs in a worker thread so the UI never freezes |
| Markdown preview | `ui.markdown` (built-in) — no custom renderer, no CDN |
| Tests | `nicegui.testing.User` fixture (headless, no browser) |
| Auth | **None in-app** — Caddy fronts `web` with HTTP basic auth (`docs/02_infra.md §5`); NiceGUI's `storage_secret` is cookie-signing only, not authentication |

**No new service.** `from app.web import app` still returns the FastAPI instance (now also serving
the NiceGUI pages), so deployment is unchanged.

## Files

| File | Role |
| --- | --- |
| `routes.py` | Owns the FastAPI `app`; keeps the JSON endpoints `GET /healthz` and `GET /status`; imports `ui_pages` and mounts NiceGUI with `ui.run_with(...)`. |
| `ui_pages.py` | **The UI layer** — the two NiceGUI pages and all their handlers. |
| `queries.py` | Read-only DB helpers (dashboard counts, ready-to-draft list, recent clusters/articles, one article). Returns detached dataclasses — no ORM leaks into the UI. |
| `chat.py` | The **Phase-4 iterate seam** (`handle_editor_message` → `app.editor.iterate.iterate_article`, returns `IterateResult`) — backend-owned; the editor chat + piece-type switcher route through it. The UI only **calls** it. |

(The old `templates/` dir and the `/`, `/article/{id}`, `POST /article/draft/{id}`, `WS /ws/editor/{id}`
routes were removed — NiceGUI owns the UI + its transport now.)

## Pages

### Dashboard — `@ui.page("/")`
- Pipeline counts: clusters by Gate-1 status (`new/sent/approved/skipped`) and articles by
  lifecycle status (`approved/drafting/pre_publish/published`).
- **Ready to draft** — approved clusters (title · topic · score) each with a **Draft** button.
  Clicking it runs `create_article_for_cluster` + `draft_article` (the writer-agent) via
  `run.io_bound`, behind a spinner, then navigates to the editor. A grounding refusal
  (cluster has no pass-2 source text yet → `ValueError`) surfaces as a clear notify.
- A minimal read-only browse of recent clusters and articles (article ids link to their editor).

### Editor — `@ui.page("/editor/{article_id}")`
A header (status chip + piece-type switcher + Gate-2 approve) over a `ui.splitter` two-pane:

**Header controls (Phase 4)**
- **Status chip** (`.mark("article-status")`) — the article's lifecycle status; updates in place
  after a successful Gate-2 approve.
- **Piece-type switcher** (`ui.select`, `.mark("piece-type-select")`) — defaults to the article's
  current `piece_type`; on change runs a **structural reformat** through the iterate seam with
  `new_piece_type=…` (behind a spinner), refreshes the preview/textarea, and posts a chat note.
- **Approve (pre-publish)** button (`.mark("approve-gate2")`) — **Gate 2**: calls
  `app.editor.approve_article` (drafting → `pre_publish`) via `run.io_bound`, updates the status
  chip, and disables itself once `pre_publish`. This is **owner approval, NOT publishing** —
  `pre_publish` is the last status this UI sets; mark-as-published (→ `published`) is Phase 5.

**Panes**
- **Left — chat** (`ui.chat_message` list + input + send). An *empty* draft routes the first
  instruction to the writer-agent **initial draft** (`draft_article`); a *non-empty* draft routes
  follow-ups to the **Phase-4 iterate seam** `chat.handle_editor_message`. The chat passes the
  **live raw-textarea value as `base_draft`** so the owner's *unsaved* hand-edits are the base the
  agent edits in place (manual edits are sacred). On return the preview + textarea refresh from the
  full revised draft (`IterateResult.draft`) — **edit-in-place, never regeneration** — and the
  agent's terse `reply` renders as a bubble. A `ValueError` surfaces as a red bubble + negative
  notify.
- **Right — live preview + hand-edit**: a `ui.markdown` of the current draft, plus a raw
  `ui.textarea` with **Save edits** that persists the textarea verbatim to `articles.current_draft`
  (the owner's direct hand-edit channel — manual edits are sacred).

## How it stays inside the project's hard rules
- **Never publishes** — preview/editing/admin only; no posting path. `pre_publish` (Gate 2) is the
  **last status this UI sets**; the mark-as-published transition (→ `published` + the article
  embedding) is Phase 5 bookkeeping of an external manual act, not in this UI.
- **Edit-in-place, never regeneration** — chat iterate routes through the seam and applies the full
  revised `IterateResult.draft`; the owner's **unsaved** hand-edits are passed as `base_draft` so
  they survive (manual edits are sacred). The `edit_log` append lives in the backend agent.
- **Grounding stays in the backend** — the UI *calls* `draft_article` / `handle_editor_message`; it
  never weakens its provenance / flag-unverified / propose-not-assert enforcement, and it surfaces
  the refusal.
- **Postgres-only coordination** — every read/write is a short-lived DB session; the UI never calls
  the poller/bot/researcher. It reads clusters/articles, writes `current_draft` (Save edits), and
  calls shared components (`app.editor` for create/draft/**approve**, `app.web.chat` for iterate)
  which own their own sessions + writes.
- **Secrets from env** — `WEB_STORAGE_SECRET` (cookie-signing) comes from the environment
  (`.env.example`); none in code.

## Run & test

```bash
# Run locally (needs a migrated Postgres in DATABASE_URL)
DATABASE_URL=postgresql+psycopg2://app:pass@localhost:5432/content \
  WEB_STORAGE_SECRET=change-me \
  uvicorn app.web:app --host 127.0.0.1 --port 8000
# → http://127.0.0.1:8000/  (dashboard) ,  /editor/{article_id}  (editor) ,  /healthz

# Tests (NiceGUI User fixture; pytest.ini sets asyncio_mode=auto + the nicegui test plugin)
pytest -q tests/test_web.py
```

In production the `web` service runs this image with `uvicorn app.web:app` behind Caddy
(basic auth). `WEB_STORAGE_SECRET` flows in via the existing `.env` / `env_file` — no compose
change was needed.
