"""GitHub adapter (source type `github`, identity `{user}`).

v1 choice: the PUBLIC per-user Atom feed at https://<user>.atom equivalent
    https://github.com/<user>.atom
which needs NO auth and NO new dependency. It is an Atom feed of the user's public
activity (pushes, releases, stars, etc.), so the entry parsing is identical to RSS — we
REUSE `app.adapters.rss.parse_feed` and differ only in how the feed URL is built, and in
carrying an etag/last-modified conditional GET exactly like the RSS adapter.

FUTURE OPTION (not v1): the authenticated GitHub Events API gives richer, typed events and
higher rate limits, but it requires a token (a secret) and bespoke event parsing. For a
single-user pass-1 poll the unauthenticated Atom feed is sufficient and dependency-free.

`url` = each activity entry's link (a commit/release/repo page). engagement = {} — the Atom
activity feed carries no native ratings.

Cursor: etag / last-modified, so an unchanged feed returns 304 and transfers nothing —
the same conditional-GET contract as RSS.

Pass 1 only — metadata. No full-text fetch here.
"""
from __future__ import annotations

import logging

import httpx

from app.adapters.base import Adapter, PollResult
from app.adapters.rss import parse_feed

log = logging.getLogger("adapter.github")

_USER_AGENT = "news-digest/0.1 (+https://github.com/) personal-feed-reader"
_TIMEOUT = httpx.Timeout(20.0, connect=10.0)


def build_feed_url(user: str) -> str:
    """Pure: the public GitHub activity Atom feed URL for a user."""
    return f"https://github.com/{user}.atom"


def _conditional_headers(cursor: dict | None) -> dict:
    headers = {"User-Agent": _USER_AGENT}
    if cursor:
        if cursor.get("etag"):
            headers["If-None-Match"] = cursor["etag"]
        if cursor.get("last_modified"):
            headers["If-Modified-Since"] = cursor["last_modified"]
    return headers


class GithubAdapter(Adapter):
    """Fetch a user's public activity Atom feed with a conditional GET and parse it with
    the shared RSS parser; carry an etag/last-modified cursor like RSS."""

    type = "github"

    def __init__(self, client: httpx.Client | None = None):
        # Injectable client keeps the adapter testable; default created per-poll.
        self._client = client

    def poll(self, source, cursor: dict | None) -> PollResult:
        user = source.identity["user"]
        url = build_feed_url(user)
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

        new_cursor: dict = {}
        etag = resp.headers.get("ETag")
        last_modified = resp.headers.get("Last-Modified")
        if etag:
            new_cursor["etag"] = etag
        if last_modified:
            new_cursor["last_modified"] = last_modified

        items = parse_feed(resp.content)
        log.info("github %s -> %d entries (etag=%s)", user, len(items), bool(etag))
        return PollResult(items=items, cursor=new_cursor, not_modified=False)
