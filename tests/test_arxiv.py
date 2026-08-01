"""arXiv adapter — pure parsing over a saved Atom fixture, plus the query-URL builder.

No network, no DB. arXiv reuses app.adapters.rss.parse_feed, so this asserts the shared
parser yields the right abs links/titles/tz-aware timestamps and the engagement == {}
invariant, and that build_query_url encodes category + newest-first sort + max_results.
"""
from __future__ import annotations

from datetime import timezone
from pathlib import Path

import httpx

from app.adapters import ArxivAdapter, available_types, get_adapter, is_implemented
from app.adapters.arxiv import ArxivAdapter as ArxivAdapterDirect, build_query_url
from app.adapters.base import item_id
from app.adapters.rss import parse_feed

FIXTURES = Path(__file__).parent / "fixtures"


def _read(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


def test_parse_arxiv_abs_links_and_titles():
    items = parse_feed(_read("arxiv_query.xml"))
    assert len(items) == 2
    titles = {i.title for i in items}
    assert "Scaling Laws for Retrieval-Augmented Language Models" in titles
    assert "Efficient Sparse Attention for Long Contexts" in titles
    urls = {i.url for i in items}
    # url is the arXiv abs link (feedparser picks the alternate text/html link).
    assert "http://arxiv.org/abs/2606.00001v1" in urls
    assert "http://arxiv.org/abs/2606.00002v1" in urls
    paper = next(i for i in items if i.url == "http://arxiv.org/abs/2606.00001v1")
    assert paper.id == item_id("http://arxiv.org/abs/2606.00001v1")


def test_arxiv_has_no_engagement_and_tz_aware():
    for item in parse_feed(_read("arxiv_query.xml")):
        assert item.engagement == {}
        assert item.published_at is not None
        assert item.published_at.tzinfo is not None
        assert item.published_at.utcoffset() == timezone.utc.utcoffset(None)


def test_build_query_url_encodes_category_and_sort():
    url = build_query_url("cs.LG", max_results=25)
    assert url.startswith("https://export.arxiv.org/api/query?")
    assert "search_query=cat%3Acs.LG" in url
    assert "sortBy=submittedDate" in url
    assert "sortOrder=descending" in url
    assert "max_results=25" in url


def test_registry_exposes_arxiv():
    assert "arxiv" in available_types()
    assert is_implemented("arxiv") is True
    assert isinstance(get_adapter("arxiv"), ArxivAdapter)


# --- Phase 7: flaky-fetch resilience (retry the single query GET on a transient blip) --------


def _arxiv_source(category="cs.LG"):
    from app.config import Source, derive_source_key

    identity = {"category": category}
    return Source(
        type="arxiv",
        identity=identity,
        cadence_s=86400,
        owner="topic:test",
        source_key=derive_source_key("arxiv", identity),
    )


class _TransientThenOkArxivClient:
    """Fails the single query GET transiently ONCE, then serves the Atom fixture. Proves the
    query GET is retried before the per-source isolation would kick in."""

    def __init__(self, content: bytes, *, fail_exc=None):
        self._content = content
        self._fail_exc = fail_exc  # default: a transient 503 on the first attempt
        self._calls = 0
        self.urls: list[str] = []

    def get(self, url, headers=None):
        self.urls.append(url)
        self._calls += 1
        request = httpx.Request("GET", url)
        if self._calls == 1:
            if self._fail_exc is not None:
                raise self._fail_exc
            return httpx.Response(503, request=request)  # transient -> retried
        return httpx.Response(200, content=self._content, request=request)


def test_query_get_retries_a_transient_5xx_then_succeeds():
    client = _TransientThenOkArxivClient(_read("arxiv_query.xml"))
    adapter = ArxivAdapterDirect(client=client, retry_backoff=0)  # backoff=0 -> no real sleep
    result = adapter.poll(_arxiv_source(), cursor=None)

    urls = {i.url for i in result.items}
    assert "http://arxiv.org/abs/2606.00001v1" in urls
    assert "http://arxiv.org/abs/2606.00002v1" in urls
    assert len(client.urls) == 2  # one transient failure + one success


def test_query_get_retries_a_transport_error_then_succeeds():
    client = _TransientThenOkArxivClient(
        _read("arxiv_query.xml"), fail_exc=httpx.ConnectTimeout("connect timed out")
    )
    adapter = ArxivAdapterDirect(client=client, retry_backoff=0)
    result = adapter.poll(_arxiv_source(), cursor=None)

    assert len(result.items) == 2
    assert len(client.urls) == 2
