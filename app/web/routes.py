"""FastAPI app + NiceGUI mount for the editor web app (docs/01_technical.md §2.6).

This is the one always-on HTTP surface. The UI is built on **NiceGUI** (the owner picked it as
the ready SDK so we don't hand-roll templates); the FastAPI `app` here keeps the API/health
endpoints and HOSTS the NiceGUI pages, which are mounted onto it via `ui.run_with(...)`. So
`uvicorn app.web:app` and the compose `web` service are unchanged: `from app.web import app`
still returns the FastAPI instance, now serving the NiceGUI shell at `/`.

What lives where:
  - FastAPI JSON routes (here): `GET /healthz` (liveness) and `GET /status` (deep foundation
    probe). These are API/health, not UI — kept as plain FastAPI handlers.
  - NiceGUI pages (app/web/ui_pages.py): `@ui.page('/')` admin/dashboard and
    `@ui.page('/editor/{article_id}')` the chat-drafting editor. Importing that module registers
    the pages; `ui.run_with` below mounts them at the root path.
  - Read helpers (app/web/queries.py) and the Phase-4 iterate seam (app/web/chat.py) are reused
    unchanged by the NiceGUI pages.

House rules honoured here:
  - NO auth in the app — Caddy fronts `web` with HTTP basic auth (docs/02_infra.md §5); no
    login/sessions/user model. The NiceGUI `storage_secret` is only cookie-signing, NOT auth.
  - NEVER publishes — this is a preview/editing/admin surface; no posting/publishing path exists.
  - Postgres is the only coordination channel — the pages read/write the DB and call shared
    components (app.editor, app.web.chat); nothing here calls the poller/bot/researcher.

Heavy/optional imports (the LLM stack used by /status, the editor/agent stack used by the pages)
stay lazy or scoped so importing this module — which `uvicorn app.web:app` does at boot, and
which the tests do — is cheap and has no DB/network side effects beyond registering the pages.
"""
from __future__ import annotations

import logging
import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from nicegui import ui

# Importing ui_pages registers the NiceGUI pages on the global app (its module body calls
# ensure_registered()). Kept as a top-level import so the pages exist before ui.run_with mounts.
from app.web import ui_pages  # noqa: F401  (imported for its page-registration side effect)

log = logging.getLogger("web")

# NiceGUI signs its per-browser storage cookie with this secret. It is NOT authentication (Caddy
# basic-auth fronts the whole surface) — only cookie integrity. From env so no secret lives in
# code; a clear, obviously-non-secret dev fallback keeps a fresh local `uvicorn`/`docker compose`
# boot working with no extra setup (documented in .env.example as WEB_STORAGE_SECRET).
_DEV_STORAGE_SECRET = "dev-only-change-me"


def storage_secret() -> str:
    """NiceGUI cookie-signing secret from env WEB_STORAGE_SECRET, with a dev fallback.

    A blank/absent value falls back to the obvious dev placeholder so a credential-free local boot
    works; production sets WEB_STORAGE_SECRET to a real random value (see .env.example). This is
    cookie signing only — never treat it as auth."""
    raw = os.environ.get("WEB_STORAGE_SECRET")
    if raw is None or not raw.strip():
        return _DEV_STORAGE_SECRET
    return raw.strip()


# --- app + API/health routes ---------------------------------------------------------------

app = FastAPI(title="AI Content Engine — editor")


@app.get("/healthz")
def healthz() -> dict:
    """Liveness: a cheap 200 with no DB/model dependency, for Caddy/compose health checks."""
    return {"status": "ok"}


@app.get("/status")
def status() -> JSONResponse:
    """Foundation check through the running stack (carried over from the Phase-0 skeleton):
    config loads, generate+embed round-trip, and the schema is present. Each probe is wrapped so
    one failing dependency surfaces as an error field rather than crashing the endpoint — useful
    for verifying a fresh deploy behind Caddy. Imports are lazy so importing this module stays
    side-effect-free."""
    out: dict = {}

    try:
        from app.config import load_config

        cfg = load_config()
        out["config"] = {"sources": len(cfg.sources), "digests": sorted(cfg.digests)}
    except Exception as e:  # surface, don't crash the endpoint
        out["config"] = {"error": f"{type(e).__name__}: {e}"}

    try:
        from app import llm

        text = llm.generate([{"role": "user", "content": "ping"}], role="generation")
        vec = llm.embed(["ping"])[0]
        out["llm"] = {"generate_ok": bool(text), "embed_dim": len(vec)}
    except Exception as e:
        out["llm"] = {"error": f"{type(e).__name__}: {e}"}

    try:
        from sqlalchemy import text as sql

        from app.db.session import engine

        with engine.connect() as conn:
            n = conn.execute(
                sql(
                    "select count(*) from information_schema.tables "
                    "where table_schema='public'"
                )
            ).scalar()
        out["db"] = {"public_tables": int(n)}
    except Exception as e:
        out["db"] = {"error": f"{type(e).__name__}: {e}"}

    return JSONResponse(out)


# --- mount NiceGUI onto the FastAPI app -----------------------------------------------------
# `ui.run_with` attaches NiceGUI (its router, static assets, and the Socket.IO transport that
# powers the chat/preview round-trip) to the existing FastAPI instance, mounted at the root path.
# The `@ui.page` functions in app.web.ui_pages (imported above) become routes under `/`. This is
# what makes `from app.web import app` serve the NiceGUI UI while still exposing /healthz + /status
# as plain FastAPI JSON routes. `storage_secret` is from env (cookie signing only, not auth).
ui.run_with(
    app,
    mount_path="/",
    storage_secret=storage_secret(),
    title="AI Content Engine — editor",
)


__all__ = ["app", "storage_secret"]
