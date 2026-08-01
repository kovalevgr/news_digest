"""RSS-family adapter (source type `rss`): blogs, Substack, dev.to, Lobsters, etc.

Pass 1 only — feed metadata (title, link, published_at). No full-text fetch; that is
pass 2 (app/fetcher), and only for Gate-1-approved stories.

Two responsibilities, kept apart so parsing stays unit-testable without a network:
  - `parse_feed(content) -> list[Item]` is pure: bytes/str in, normalized Items out.
  - `RssAdapter.poll` does the I/O: a conditional GET (If-None-Match / If-Modified-Since
    from the cursor), returning `not_modified=True` on a 304, or a fresh etag/last-modified
    cursor plus parsed items on a 200.

feedparser handles RSS 2.0 and Atom transparently, so arXiv and GitHub Atom feeds (later
slices) reuse `parse_feed` via thin URL-builders — they only differ in how the feed URL is
constructed, not in how the entries are parsed.

RSS carries no engagement signals, so every Item here has `engagement == {}`; cross-source
frequency (distinct sighting sources) is what ranks these in clusters.
"""
from __future__ import annotations

import logging
from calendar import timegm
from datetime import datetime, timezone
from time import struct_time

import feedparser
import httpx

from app.adapters.base import Adapter, Item, PollResult

log = logging.getLogger("adapter.rss")

# A real UA — some feed hosts 403 the default httpx/python agent.
_USER_AGENT = "news-digest/0.1 (+https://github.com/) personal-feed-reader"
_TIMEOUT = httpx.Timeout(20.0, connect=10.0)


def _struct_to_dt(st: struct_time | None) -> datetime | None:
    """feedparser's *_parsed fields are UTC struct_time; make them tz-aware UTC."""
    if not st:
        return None
    return datetime.fromtimestamp(timegm(st), tz=timezone.utc)


def parse_feed(content: bytes | str) -> list[Item]:
    """Pure parse: feed bytes/text -> normalized Items. No network, no cursor.

    Drops entries with no link (a link is the content identity — no link, no item).
    Prefers `published`, falls back to `updated` for the timestamp. Engagement is always
    empty for RSS/Atom; it has no native ratings.
    """
    parsed = feedparser.parse(content)
    items: list[Item] = []
    for entry in parsed.entries:
        link = (entry.get("link") or "").strip()
        if not link:
            continue
        published = _struct_to_dt(
            entry.get("published_parsed") or entry.get("updated_parsed")
        )
        title = entry.get("title")
        items.append(
            Item(
                url=link,
                title=title.strip() if isinstance(title, str) else title,
                published_at=published,
                engagement={},
            )
        )
    return items


def _conditional_headers(cursor: dict | None) -> dict:
    headers = {"User-Agent": _USER_AGENT}
    if cursor:
        if cursor.get("etag"):
            headers["If-None-Match"] = cursor["etag"]
        if cursor.get("last_modified"):
            headers["If-Modified-Since"] = cursor["last_modified"]
    return headers


class RssAdapter(Adapter):
    """Fetch a feed with a conditional GET, parse it, and carry an etag/last-modified
    cursor so the next poll transfers nothing when the feed is unchanged (304)."""

    type = "rss"

    def __init__(self, client: httpx.Client | None = None):
        # An injectable client keeps the adapter testable; default is created per-poll.
        self._client = client

    def poll(self, source, cursor: dict | None) -> PollResult:
        url = source.identity["url"]
        headers = _conditional_headers(cursor)
        client = self._client or httpx.Client(timeout=_TIMEOUT, follow_redirects=True)
        try:
            resp = client.get(url, headers=headers)
        finally:
            if self._client is None:
                client.close()

        if resp.status_code == 304:
            # Nothing changed — keep the cursor exactly as it was.
            return PollResult(items=[], cursor=cursor or {}, not_modified=True)

        resp.raise_for_status()

        # Seed from the prior cursor so a 200 that omits ETag/Last-Modified (RFC 7232 makes
        # both optional; CDNs/origins drop them on some 200s) does not DISCARD validators we
        # already hold — overwrite only when the response actually provides one. Otherwise the
        # next poll would send no conditional headers and silently fall back to a full transfer
        # every cycle. (The 304 path already preserves the cursor; this matches it on 200.)
        new_cursor: dict = dict(cursor or {})
        etag = resp.headers.get("ETag")
        last_modified = resp.headers.get("Last-Modified")
        if etag:
            new_cursor["etag"] = etag
        if last_modified:
            new_cursor["last_modified"] = last_modified

        items = parse_feed(resp.content)
        log.info("rss %s -> %d entries (etag=%s)", url, len(items), bool(etag))
        return PollResult(items=items, cursor=new_cursor, not_modified=False)
