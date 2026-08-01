"""Engine + session factory. DATABASE_URL is REQUIRED — it must be set explicitly
in the environment. There is no default: Compose injects it per-service, and the test
conftest sets a dev default (content_test). A missing DATABASE_URL fails fast at import
rather than silently connecting to the prod-named 'content' DB."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Set it explicitly — e.g. export "
        "DATABASE_URL=postgresql+psycopg2://app:app@localhost:5432/content_test "
        "for local dev, or postgresql+psycopg2://app:<pw>@db:5432/content under "
        "Docker Compose. There is no silent default (it used to fall back to the "
        "prod-named 'content' DB, which is a footgun)."
    )

engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False, future=True
)


def get_session():
    """Return a new Session. Caller is responsible for closing it."""
    return SessionLocal()
