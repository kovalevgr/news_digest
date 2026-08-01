"""Persistence for pass-1 ingest: the items/sightings dedup invariant + cursor I/O.

The headline rule (docs/01_technical.md §3, decision 4): an item is content identity
(one canonical URL); a sighting is one source's observation of it. Re-seeing the same URL
from a different source inserts a *sighting*, never a duplicate item, and never overwrites
the first source's item row. We enforce this with Postgres ON CONFLICT:

  - items: INSERT ... ON CONFLICT (id) DO NOTHING  — first source wins, content identity
    is immutable here (embedding/full_text are filled by later stages, not by re-ingest).
  - sightings: INSERT ... ON CONFLICT (item_id, source_key) DO UPDATE — refresh that one
    source's engagement + seen_at; re-polling the same source is idempotent.

`upsert_item_and_sighting` returns True iff a *new* item row was created — the future
signal that this item still needs an embedding (the dedup-into-clusters slice consumes it).

No commit happens here: the poll runner owns the transaction boundary so a whole source's
items + cursor land atomically (or roll back together).
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.adapters.base import Item
from app.db.models import Cursor, Item as ItemModel, Sighting


def upsert_item_and_sighting(session, item: Item, source_key: str) -> bool:
    """Upsert one item + this source's sighting of it. Returns True iff a new item row
    was created (i.e. this URL had never been seen by any source before).

    The item insert is DO NOTHING on the PK, so a URL already ingested by another source
    keeps its original title/url/published_at — the first source's content identity wins.
    """
    item_stmt = (
        pg_insert(ItemModel)
        .values(
            id=item.id,
            url=item.url,
            title=item.title,
            published_at=item.published_at,
        )
        .on_conflict_do_nothing(index_elements=["id"])
        .returning(ItemModel.id)
    )
    # RETURNING yields a row only when the INSERT actually wrote one; a conflict (existing
    # item) returns nothing. That is exactly the "new item?" signal we want.
    inserted_id = session.execute(item_stmt).scalar_one_or_none()
    is_new_item = inserted_id is not None

    seen_at = datetime.now(timezone.utc)
    sighting_stmt = (
        pg_insert(Sighting)
        .values(
            item_id=item.id,
            source_key=source_key,
            engagement=item.engagement or {},
            seen_at=seen_at,
        )
        .on_conflict_do_update(
            index_elements=["item_id", "source_key"],
            set_={
                "engagement": item.engagement or {},
                "seen_at": seen_at,
            },
        )
    )
    session.execute(sighting_stmt)
    return is_new_item


def load_cursor(session, source_key: str) -> dict | None:
    """Return the persisted cursor dict for a source, or None if it has never polled."""
    row = session.execute(
        select(Cursor.cursor).where(Cursor.source_key == source_key)
    ).scalar_one_or_none()
    return row


def save_cursor(session, source_key: str, cursor: dict) -> None:
    """Upsert a source's cursor (JSONB). Touches updated_at on every save."""
    stmt = (
        pg_insert(Cursor)
        .values(
            source_key=source_key,
            cursor=cursor or {},
            updated_at=datetime.now(timezone.utc),
        )
        .on_conflict_do_update(
            index_elements=["source_key"],
            set_={"cursor": cursor or {}, "updated_at": datetime.now(timezone.utc)},
        )
    )
    session.execute(stmt)
