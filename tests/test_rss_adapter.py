"""RSS adapter parsing (app.adapters.rss.parse_feed) — pure, no network.

Covers RSS 2.0 and Atom (feedparser handles both), correct counts/titles/urls, tz-aware
published_at, and the RSS-has-no-engagement invariant (engagement == {}). Also checks the
conditional-GET path with a stubbed httpx client (304 -> not_modified, no parsing).
"""
from __future__ import annotations

from datetime import timezone
from pathlib import Path

import httpx
import pytest

from app.adapters import get_adapter, available_types, is_implemented
from app.adapters.rss import RssAdapter, parse_feed
from app.adapters.base import item_id

FIXTURES = Path(__file__).parent / "fixtures"


def _read(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


def test_parse_rss_counts_titles_urls():
    items = parse_feed(_read("sample_rss.xml"))
    assert len(items) == 2
    titles = [i.title for i in items]
    assert "First post about LLMs" in titles
    assert "Second post about vector search" in titles
    urls = {i.url for i in items}
    assert "https://example.com/posts/second" in urls
    # the tracked link is carried verbatim on the Item; identity strips tracking via item_id
    tracked = next(i for i in items if i.title == "First post about LLMs")
    assert "utm_source" in tracked.url
    assert tracked.id == item_id("https://example.com/posts/first")


def test_parse_atom_counts_titles_urls():
    items = parse_feed(_read("sample_atom.xml"))
    assert len(items) == 2
    assert {i.title for i in items} == {
        "Atom entry on retrieval",
        "Atom entry on embeddings",
    }
    assert {i.url for i in items} == {
        "https://atom.example.org/entries/retrieval?utm_campaign=newsletter",
        "https://atom.example.org/entries/embeddings",
    }


def test_published_at_is_tz_aware_utc():
    for name in ("sample_rss.xml", "sample_atom.xml"):
        for item in parse_feed(_read(name)):
            assert item.published_at is not None
            assert item.published_at.tzinfo is not None
            assert item.published_at.utcoffset() == timezone.utc.utcoffset(None)


def test_rss_has_no_engagement():
    for name in ("sample_rss.xml", "sample_atom.xml"):
        for item in parse_feed(_read(name)):
            assert item.engagement == {}


def test_entry_without_link_is_dropped():
    feed = b"""<?xml version="1.0"?>
    <rss version="2.0"><channel><title>t</title>
      <item><title>no link here</title></item>
      <item><title>has link</title><link>https://example.com/ok</link></item>
    </channel></rss>"""
    items = parse_feed(feed)
    assert len(items) == 1
    assert items[0].url == "https://example.com/ok"


class _StubResponse:
    def __init__(self, status_code, content=b"", headers=None):
        self.status_code = status_code
        self.content = content
        self.headers = headers or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("err", request=None, response=None)


class _StubClient:
    """Minimal httpx.Client stand-in: records the request, returns a canned response."""

    def __init__(self, response):
        self._response = response
        self.last_headers = None
        self.last_url = None

    def get(self, url, headers=None):
        self.last_url = url
        self.last_headers = headers or {}
        return self._response


def _source(url="https://feed.example.com/rss"):
    from app.config import Source, derive_source_key

    identity = {"url": url}
    return Source(
        type="rss",
        identity=identity,
        cadence_s=86400,
        owner="topic:test",
        source_key=derive_source_key("rss", identity),
    )


def test_poll_200_returns_items_and_cursor():
    resp = _StubResponse(
        200,
        content=_read("sample_rss.xml"),
        headers={"ETag": '"abc123"', "Last-Modified": "Wed, 04 Jun 2025 00:00:00 GMT"},
    )
    client = _StubClient(resp)
    adapter = RssAdapter(client=client)
    result = adapter.poll(_source(), cursor=None)

    assert result.not_modified is False
    assert len(result.items) == 2
    assert result.cursor == {
        "etag": '"abc123"',
        "last_modified": "Wed, 04 Jun 2025 00:00:00 GMT",
    }


def test_poll_sends_conditional_headers_from_cursor():
    client = _StubClient(_StubResponse(304))
    adapter = RssAdapter(client=client)
    cursor = {"etag": '"abc123"', "last_modified": "Wed, 04 Jun 2025 00:00:00 GMT"}

    result = adapter.poll(_source(), cursor=cursor)

    assert client.last_headers.get("If-None-Match") == '"abc123"'
    assert client.last_headers.get("If-Modified-Since") == "Wed, 04 Jun 2025 00:00:00 GMT"
    # 304 -> nothing changed: no items, cursor unchanged, not_modified flag set.
    assert result.not_modified is True
    assert result.items == []
    assert result.cursor == cursor


def test_registry_exposes_rss():
    # rss is implemented and resolves to its adapter; available_types is sorted and
    # contains it (more no-credential adapters have since landed alongside rss).
    assert "rss" in available_types()
    assert available_types() == sorted(available_types())
    assert is_implemented("rss") is True
    assert isinstance(get_adapter("rss"), RssAdapter)


# Only the owner-credential-gated Reddit OAuth adapter remains deferred (the X read-API
# adapter has since landed and is implemented).
@pytest.mark.parametrize("deferred", ["reddit_sub"])
def test_registry_defers_unbuilt_adapters(deferred):
    assert is_implemented(deferred) is False
    with pytest.raises(NotImplementedError):
        get_adapter(deferred)


def test_registry_rejects_unknown_type():
    with pytest.raises(ValueError):
        get_adapter("not_a_type")
