"""Pass-2 full-text extraction (app.fetcher).

Two layers, tested at the right level:
  - extract_main_text / fetch_full_text are exercised PURELY + with an injected httpx
    MockTransport (no network), against a realistic article fixture with nav/script/style
    chrome to prove main-content isolation.
  - fetch_cluster_full_text is DB-backed (guarded by RUN_PG_TESTS) and proves it persists
    full_text for a cluster's items, isolates a per-item fetch failure, and is idempotent.
"""
from __future__ import annotations

import os
import uuid
from pathlib import Path

import httpx
import pytest

from app.fetcher import extract_main_text, fetch_cluster_full_text, fetch_full_text

FIXTURE = (Path(__file__).parent / "fixtures" / "article.html").read_text(encoding="utf-8")


# --- pure extraction -----------------------------------------------------------------------


def test_extract_main_text_keeps_article_drops_chrome():
    text = extract_main_text(FIXTURE, url="https://example.com/rag")
    # The article body survives...
    assert "retrieval-augmented generation" in text.lower()
    assert "learned" in text.lower() and "relevance head" in text.lower()
    # ...but script/style payloads never leak into the text (we drop those tags).
    assert "TRACKINGPIXEL" not in text
    assert "console.log" not in text
    assert "font-family" not in text


def test_extract_main_text_empty_inputs():
    assert extract_main_text("") == ""
    assert extract_main_text("   \n  ") == ""


def test_extract_main_text_falls_back_on_minimal_html():
    # No clear "article" container — readability may bail; we still salvage the text.
    text = extract_main_text("<html><body><p>Just one short paragraph here.</p></body></html>")
    assert "short paragraph" in text


# --- fetch_full_text over an injected transport (no network) --------------------------------


def _client_returning(status: int, body: str) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, text=body)

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_fetch_full_text_200_extracts():
    with _client_returning(200, FIXTURE) as client:
        text = fetch_full_text("https://example.com/rag", client=client)
    assert text is not None
    assert "relevance head" in text.lower()


def test_fetch_full_text_404_returns_none():
    with _client_returning(404, "nope") as client:
        assert fetch_full_text("https://example.com/missing", client=client) is None


def test_fetch_full_text_propagates_transport_errors():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(httpx.ConnectError):
            fetch_full_text("https://example.com/down", client=client)


# --- DB-backed: fetch_cluster_full_text -----------------------------------------------------

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"


@pytest.fixture()
def session():
    from app.db.session import engine, SessionLocal

    conn = engine.connect()
    outer = conn.begin()
    sess = SessionLocal(bind=conn, join_transaction_mode="create_savepoint")
    try:
        yield sess
    finally:
        sess.close()
        outer.rollback()
        conn.close()


def _routing_client(routes: dict) -> httpx.Client:
    """An httpx.Client whose MockTransport maps url -> (status, body) or to an exception."""
    def handler(request: httpx.Request) -> httpx.Response:
        outcome = routes[str(request.url)]
        if isinstance(outcome, Exception):
            raise outcome
        status, body = outcome
        return httpx.Response(status, text=body)

    return httpx.Client(transport=httpx.MockTransport(handler))


@pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")
def test_fetch_cluster_full_text_persists_isolates_and_is_idempotent(session):
    from app.adapters.base import Item as AdapterItem, item_id
    from app.db.models import Cluster, Item as ItemModel
    from app.researcher.cluster import new_cluster_id
    from app.researcher.store import upsert_item_and_sighting

    cid = new_cluster_id()
    session.add(Cluster(id=cid, status="approved"))
    session.flush()

    good_url = f"https://example.com/good/{uuid.uuid4().hex}"
    bad_url = f"https://example.com/bad/{uuid.uuid4().hex}"
    for url in (good_url, bad_url):
        upsert_item_and_sighting(session, AdapterItem(url=url, title="t"), "rss:a")
        session.flush()
        session.get(ItemModel, item_id(url)).cluster_id = cid
    session.flush()

    routes = {
        good_url: (200, FIXTURE),
        bad_url: httpx.ConnectError("down", request=httpx.Request("GET", bad_url)),
    }
    with _routing_client(routes) as client:
        stats = fetch_cluster_full_text(session, cid, client=client)

    assert stats["considered"] == 2
    assert stats["fetched"] == 1
    assert stats["failed"] == 1
    # The good item got full text; the failed one stays NULL (isolated, not poisoned).
    assert session.get(ItemModel, item_id(good_url)).full_text is not None
    assert "relevance head" in session.get(ItemModel, item_id(good_url)).full_text.lower()
    assert session.get(ItemModel, item_id(bad_url)).full_text is None

    # Idempotent: the already-fetched item is not reconsidered; only the still-empty one is.
    with _routing_client(routes) as client:
        stats2 = fetch_cluster_full_text(session, cid, client=client)
    assert stats2["considered"] == 1
    assert stats2["fetched"] == 0
    assert stats2["failed"] == 1
