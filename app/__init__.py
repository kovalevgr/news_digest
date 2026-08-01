"""AI Content Engine — application package.

A staged pipeline (researcher -> Gate 1 -> writer-agent -> Gate 2 -> variants),
coordinated only through Postgres. See docs/ and CLAUDE.md.
"""

# Local/dev convenience: load .env so non-Compose runs (host scripts, tests, a bare
# `python -m app.poller`) see the same env Compose injects via env_file. In Compose the
# vars are already set and load_dotenv() does not override them, so this is a no-op there.
# Guarded so the package still imports if python-dotenv is absent.
try:
    from dotenv import load_dotenv as _load_dotenv

    _load_dotenv()
except Exception:
    pass

__version__ = "0.0.0"
