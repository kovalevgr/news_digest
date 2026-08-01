"""NiceGUI test entrypoint (the `main_file` the `user` fixture runs via runpy).

NiceGUI's headless `user` fixture (nicegui.testing.user_plugin) builds its test app by executing
a "main file" that registers the pages and calls `ui.run()`. The real app mounts the pages onto
FastAPI with `ui.run_with(...)` (see app/web/routes.py), but the user-fixture path wants a plain
`ui.run()` app — so this tiny file imports the page builders (registering `@ui.page` on the global
NiceGUI app) and runs them.

`storage_secret` is a throwaway here: tests never exercise auth (there is none — Caddy fronts the
real surface) and the secret is only cookie signing. Importing app.web.ui_pages calls its
`ensure_registered()`, which is guarded against double-registration when runpy re-execs this file.
"""
from nicegui import ui

from app.web import ui_pages

# Register the pages on the (freshly reset) global NiceGUI app. We call register_pages()
# DIRECTLY rather than relying on the import-time `ensure_registered()` guard: the user fixture
# clears NiceGUI's page registry between tests but the Python module stays import-cached (so its
# `_REGISTERED` flag would still be True), which would skip re-registration and 404 the pages.
# register_pages() re-runs the `@ui.page` decorators unconditionally against the current registry.
ui_pages.register_pages()

ui.run(storage_secret="test-secret")
