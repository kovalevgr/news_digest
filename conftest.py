"""Ensure the repo root is importable so `import app.*` works regardless of the cwd
pytest is launched from. The runtime image already sets PYTHONPATH=/app; this makes
local `python -m pytest` runs work too."""
import os

# Provide a dev default for DATABASE_URL BEFORE any app import can happen, so a bare
# `pytest` imports app.db.session cleanly (it now requires DATABASE_URL — no silent
# default). Using content_test (not the prod-named 'content') means a stray test
# connection can never hit live data. PG tests override DATABASE_URL via the run command.
os.environ.setdefault(
    "DATABASE_URL", "postgresql+psycopg2://app:app@localhost:5432/content_test"
)

import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
