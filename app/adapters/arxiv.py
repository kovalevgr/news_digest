"""arXiv adapter (source type `arxiv`, identity `{category}`).

Why a thin adapter: the arXiv Atom API returns a standard Atom feed, so the entry
parsing is identical to RSS — we REUSE `app.adapters.rss.parse_feed` and only differ in
how the feed URL is built. This keeps one Atom parser, not two.

Endpoint: the public Atom query API, newest-first by submission date:
    https://export.arxiv.org/api/query?search_query=cat:<category>
        &sortBy=submittedDate&sortOrder=descending&max_results=<N>
No auth, no new dependency.

`url` is the arXiv abs link (`entry.link`, which feedparser yields as the abstract page).
engagement = {} — arXiv carries no native ratings; cross-source frequency + recency rank
these in clusters.

Cursor: the arXiv API does not honor conditional GET reliably, so we keep a simple
last-seen marker (the newest entry's URL) purely as a "last polled" breadcrumb. We do NOT
use it to filter — persistence dedups by content id, so re-yielding seen items is harmless
and re-polling stays idempotent. Keeping it markerless-but-recorded means no fragile
since/offset bookkeeping for a single-user pass-1 poll.

Pass 1 only — metadata (title, abs url, published_at). Full text (the PDF/HTML) is pass 2.
"""
from __future__ import annotations

import logging
from urllib.parse import urlencode

import httpx

from app.adapters.base import Adapter, PollResult, get_with_retry
from app.adapters.rss import parse_feed

log = logging.getLogger("adapter.arxiv")

_API = "https://export.arxiv.org/api/query"
_USER_AGENT = "news-digest/0.1 (+https://github.com/) personal-feed-reader"
_TIMEOUT = httpx.Timeout(20.0, connect=10.0)

# How many newest papers to pull per poll. A seam: enough to catch a day's submissions in
# an active category at a daily cadence, small enough to stay polite. Override-able later.
_DEFAULT_MAX_RESULTS = 50

# Seconds slept between retry attempts on a transient GET failure. A seam (injectable) so tests
# pass 0 and don't actually sleep; production keeps a polite half-second.
_DEFAULT_RETRY_BACKOFF = 0.5


def build_query_url(category: str, max_results: int = _DEFAULT_MAX_RESULTS) -> str:
    """Pure: build the arXiv Atom query URL for a category, newest-first."""
    query = urlencode(
        {
            "search_query": f"cat:{category}",
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": max_results,
        }
    )
    return f"{_API}?{query}"


class ArxivAdapter(Adapter):
    """Fetch a category's newest Atom entries and parse them with the shared RSS parser."""

    type = "arxiv"

    def __init__(self, client: httpx.Client | None = None,
                 max_results: int = _DEFAULT_MAX_RESULTS,
                 retry_backoff: float = _DEFAULT_RETRY_BACKOFF):
        # Injectable client + cap + retry backoff keep the adapter testable; defaults per-poll.
        self._client = client
        self._max_results = max_results
        self._retry_backoff = retry_backoff

    def poll(self, source, cursor: dict | None) -> PollResult:
        category = source.identity["category"]
        url = build_query_url(category, self._max_results)
        headers = {"User-Agent": _USER_AGENT}
        client = self._client or httpx.Client(timeout=_TIMEOUT, follow_redirects=True)
        try:
            # Retry a transient blip before the per-source isolation kicks in (the arXiv API can
            # flake under load); a persistent failure still raises and the runner isolates it.
            resp = get_with_retry(client, url, headers=headers, backoff=self._retry_backoff)
        finally:
            if self._client is None:
                client.close()

        items = parse_feed(resp.content)

        # Last-seen breadcrumb only (not used to filter — persistence dedups). Seed from the
        # prior cursor so a successful empty poll preserves the existing breadcrumb instead of
        # wiping it to {} (save_cursor is a wholesale replace, not a merge).
        new_cursor: dict = dict(cursor or {})
        if items:
            new_cursor["last_seen_url"] = items[0].url

        log.info("arxiv cat:%s -> %d entries", category, len(items))
        return PollResult(items=items, cursor=new_cursor, not_modified=False)
