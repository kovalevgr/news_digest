from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base; all ORM models register on Base.metadata."""
    pass
