"""DB-backed proof of the items/sightings dedup invariant + cursor round-trip.

Guarded: skipped unless RUN_PG_TESTS=1 and DATABASE_URL points at a migrated Postgres
(the poller service provides both). Runs inside a SAVEPOINT-wrapped session and rolls back
at the end, so it leaves no rows behind and is safe to re-run.

The headline invariant (the whole point of separating sightings from items): the same
canonical URL upserted under two different source_keys yields exactly ONE item and TWO
sightings, the item keeps the FIRST source's title, and re-upserting is idempotent.
"""
from __future__ import annotations

import os
import uuid

import pytest

from app.adapters.base import Item, item_id

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"
pytestmark = pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")


@pytest.fixture()
def session():
    """A session wrapped in an outer transaction that is rolled back after the test, so
    nothing persists. Imports are inside the fixture so collection works without a DB."""
    from app.db.session import engine, SessionLocal

    conn = engine.connect()
    outer = conn.begin()
    sess = SessionLocal(bind=conn)
    try:
        yield sess
    finally:
        sess.close()
        outer.rollback()
        conn.close()


def _unique_url() -> str:
    # A fresh URL per test run so we never collide with prior rows in a shared DB.
    return f"https://example.com/story/{uuid.uuid4().hex}"


def test_same_url_two_sources_one_item_two_sightings(session):
    from sqlalchemy import func, select

    from app.db.models import Item as ItemModel, Sighting
    from app.researcher.store import upsert_item_and_sighting

    url = _unique_url()
    iid = item_id(url)

    # Source A sees it first, with a title.
    first = Item(url=url, title="Original title from source A", engagement={"points": 10})
    created_a = upsert_item_and_sighting(session, first, "rss:a")
    assert created_a is True  # brand-new item

    # Source B sees the SAME canonical URL, with a different title + engagement.
    second = Item(url=url, title="DIFFERENT title from source B", engagement={"score": 99})
    created_b = upsert_item_and_sighting(session, second, "reddit_sub:b")
    assert created_b is False  # item already existed — no new item row

    session.flush()

    # Exactly one item...
    item_count = session.execute(
        select(func.count()).select_from(ItemModel).where(ItemModel.id == iid)
    ).scalar_one()
    assert item_count == 1

    # ...and it kept SOURCE A's title (first source wins; B never overwrites it).
    title = session.execute(
        select(ItemModel.title).where(ItemModel.id == iid)
    ).scalar_one()
    assert title == "Original title from source A"

    # Two sightings, one per source, each with its own engagement.
    sightings = session.execute(
        select(Sighting.source_key, Sighting.engagement)
        .where(Sighting.item_id == iid)
        .order_by(Sighting.source_key)
    ).all()
    assert [s.source_key for s in sightings] == ["reddit_sub:b", "rss:a"]
    engagement_by_source = {s.source_key: s.engagement for s in sightings}
    assert engagement_by_source["rss:a"] == {"points": 10}
    assert engagement_by_source["reddit_sub:b"] == {"score": 99}


def test_reupsert_is_idempotent(session):
    from sqlalchemy import func, select

    from app.db.models import Item as ItemModel, Sighting
    from app.researcher.store import upsert_item_and_sighting

    url = _unique_url()
    iid = item_id(url)
    item = Item(url=url, title="t", engagement={"points": 1})

    assert upsert_item_and_sighting(session, item, "rss:a") is True
    # Re-poll the same source: not a new item, and still just one sighting (PK upsert).
    assert upsert_item_and_sighting(session, item, "rss:a") is False
    assert upsert_item_and_sighting(session, item, "rss:a") is False
    session.flush()

    assert session.execute(
        select(func.count()).select_from(ItemModel).where(ItemModel.id == iid)
    ).scalar_one() == 1
    assert session.execute(
        select(func.count()).select_from(Sighting).where(Sighting.item_id == iid)
    ).scalar_one() == 1


def test_reupsert_refreshes_engagement(session):
    from sqlalchemy import select

    from app.db.models import Sighting
    from app.researcher.store import upsert_item_and_sighting

    url = _unique_url()
    iid = item_id(url)

    upsert_item_and_sighting(session, Item(url=url, title="t", engagement={"points": 1}), "rss:a")
    # Same source re-sees it with updated engagement -> the sighting reflects the new value.
    upsert_item_and_sighting(session, Item(url=url, title="t", engagement={"points": 5}), "rss:a")
    session.flush()

    engagement = session.execute(
        select(Sighting.engagement).where(
            Sighting.item_id == iid, Sighting.source_key == "rss:a"
        )
    ).scalar_one()
    assert engagement == {"points": 5}


def test_cursor_round_trip(session):
    from app.researcher.store import load_cursor, save_cursor

    key = f"rss:{uuid.uuid4().hex}"
    assert load_cursor(session, key) is None  # never polled

    save_cursor(session, key, {"etag": '"v1"', "last_modified": "Wed, 04 Jun 2025 00:00:00 GMT"})
    session.flush()
    assert load_cursor(session, key) == {
        "etag": '"v1"',
        "last_modified": "Wed, 04 Jun 2025 00:00:00 GMT",
    }

    # A later poll overwrites the cursor (etag advanced).
    save_cursor(session, key, {"etag": '"v2"'})
    session.flush()
    assert load_cursor(session, key) == {"etag": '"v2"'}
