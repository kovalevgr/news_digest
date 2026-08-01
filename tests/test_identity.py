"""URL canonicalization + content identity (app.adapters.base) — pure, no DB, no network.

These pin the dedup invariant at the URL level: the same article shared with different
tracking tags / fragments / trailing-slash variants must hash to ONE item id, while
genuinely distinct paths must stay distinct.
"""
from __future__ import annotations

from app.adapters.base import canonical_url, item_id


def test_strips_tracking_params():
    base = "https://example.com/posts/first"
    tracked = "https://example.com/posts/first?utm_source=rss&utm_medium=email&ref=hn"
    assert canonical_url(tracked) == base


def test_strips_fragment():
    assert canonical_url("https://example.com/a/b#section-2") == "https://example.com/a/b"


def test_strips_trailing_slash():
    assert canonical_url("https://example.com/a/b/") == "https://example.com/a/b"
    # but the bare-host root "/" is preserved (only paths longer than "/" are stripped)
    assert canonical_url("https://example.com/") == "https://example.com/"


def test_lowercases_scheme_and_host_only():
    # scheme + host fold to lowercase; the path is case-sensitive and preserved.
    assert canonical_url("HTTPS://Example.COM/Path/To") == "https://example.com/Path/To"


def test_keeps_meaningful_query_params():
    # non-tracking params identify content and must survive canonicalization.
    url = "https://example.com/search?q=rag&page=2"
    assert canonical_url(url) == url


def test_same_url_different_tracking_same_id():
    a = item_id("https://example.com/posts/first?utm_source=feedburner&utm_medium=rss")
    b = item_id("https://example.com/posts/first")
    c = item_id("https://example.com/posts/first/#comments")
    assert a == b == c


def test_distinct_paths_distinct_ids():
    first = item_id("https://example.com/posts/first")
    second = item_id("https://example.com/posts/second")
    assert first != second


def test_id_is_sha256_hex():
    h = item_id("https://example.com/x")
    assert len(h) == 64
    assert all(ch in "0123456789abcdef" for ch in h)
