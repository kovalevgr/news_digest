"""DB package. Importing it registers all models on Base.metadata so Alembic and
create_all see the full schema."""
from app.db.base import Base
from app.db import models  # noqa: F401  (side effect: register tables)

__all__ = ["Base", "models"]
