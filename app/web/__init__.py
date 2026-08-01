"""Editor web app — the one always-on HTTP surface (docs/01_technical.md §2.6).

`uvicorn app.web:app` is the docker-compose `web` command, so this package MUST expose a
module-level `app` FastAPI instance. That instance lives in app.web.routes, which keeps the
API/health JSON routes (`/healthz`, `/status`) and MOUNTS the NiceGUI UI onto itself via
`ui.run_with(...)`. We re-export `app` here so `app.web:app` resolves unchanged — it is now a
FastAPI app that also serves the NiceGUI pages.

Layout of the package:
  - app.web.routes   — the FastAPI `app`, /healthz + /status, and the NiceGUI mount.
  - app.web.ui_pages — the NiceGUI pages: `@ui.page('/')` admin/dashboard and
                       `@ui.page('/editor/{article_id}')` the chat-drafting editor.
  - app.web.queries  — read-only DB query helpers (reused by the pages).
  - app.web.chat     — the Phase-4 iterate seam the editor chat routes through.

The UI is built on NiceGUI (the ready SDK; we don't hand-roll templates). v1 is lean: a status/
admin dashboard with a "ready to draft" action, and a two-pane editor (chat + live preview +
hand-edit). No auth (Caddy basic-auth fronts this), no publishing — the system never posts.
"""
from app.web.routes import app

__all__ = ["app"]
