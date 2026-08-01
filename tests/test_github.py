"""GitHub adapter — pure parsing over a saved activity Atom fixture, plus the feed-URL
builder and the conditional-GET poll path with a stubbed httpx client.

No network, no DB. GitHub reuses app.adapters.rss.parse_feed, so this asserts the shared
parser yields the right activity links/titles/tz-aware timestamps and engagement == {},
that build_feed_url targets the public <user>.atom feed, and that a 304 short-circuits to
not_modified with the cursor preserved (same conditional-GET contract as RSS).
"""
from __future__ import annotations

from datetime import timezone
from pathlib import Path

import httpx

from app.adapters import GithubAdapter, available_types, get_adapter, is_implemented
from app.adapters.github import GithubAdapter as GithubAdapterDirect
from app.adapters.github import build_feed_url
from app.adapters.rss import parse_feed

FIXTURES = Path(__file__).parent / "fixtures"


def _read(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


def test_parse_github_activity_links_and_titles():
    items = parse_feed(_read("github_user.atom"))
    assert len(items) == 2
    urls = {i.url for i in items}
    assert "https://github.com/simonw/datasette/commit/abc123" in urls
    assert "https://github.com/simonw/llm/releases/tag/0.20" in urls


def test_github_has_no_engagement_and_tz_aware():
    for item in parse_feed(_read("github_user.atom")):
        assert item.engagement == {}
        assert item.published_at is not None
        assert item.published_at.tzinfo is not None
        assert item.published_at.utcoffset() == timezone.utc.utcoffset(None)


def test_build_feed_url():
    assert build_feed_url("karpathy") == "https://github.com/karpathy.atom"


class _StubResponse:
    def __init__(self, status_code, content=b"", headers=None):
        self.status_code = status_code
        self.content = content
        self.headers = headers or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("err", request=None, response=None)


class _StubClient:
    def __init__(self, response):
        self._response = response
        self.last_headers = None
        self.last_url = None

    def get(self, url, headers=None):
        self.last_url = url
        self.last_headers = headers or {}
        return self._response


def _source(user="simonw"):
    from app.config import Source, derive_source_key

    identity = {"user": user}
    return Source(
        type="github",
        identity=identity,
        cadence_s=86400,
        owner="person:test",
        source_key=derive_source_key("github", identity),
    )


def test_poll_200_returns_items_and_etag_cursor():
    resp = _StubResponse(
        200,
        content=_read("github_user.atom"),
        headers={"ETag": '"gh-etag"', "Last-Modified": "Sat, 14 Jun 2026 09:00:00 GMT"},
    )
    client = _StubClient(resp)
    adapter = GithubAdapterDirect(client=client)
    result = adapter.poll(_source(), cursor=None)

    assert client.last_url == "https://github.com/simonw.atom"
    assert result.not_modified is False
    assert len(result.items) == 2
    assert result.cursor == {
        "etag": '"gh-etag"',
        "last_modified": "Sat, 14 Jun 2026 09:00:00 GMT",
    }


def test_poll_304_short_circuits_with_cursor_preserved():
    client = _StubClient(_StubResponse(304))
    adapter = GithubAdapterDirect(client=client)
    cursor = {"etag": '"gh-etag"'}
    result = adapter.poll(_source(), cursor=cursor)

    assert client.last_headers.get("If-None-Match") == '"gh-etag"'
    assert result.not_modified is True
    assert result.items == []
    assert result.cursor == cursor


def test_registry_exposes_github():
    assert "github" in available_types()
    assert is_implemented("github") is True
    assert isinstance(get_adapter("github"), GithubAdapter)
