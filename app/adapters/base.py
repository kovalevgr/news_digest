"""Common adapter seam: the normalized Item, URL canonicalization + content identity,
the Adapter base, and the PollResult an adapter returns.

Pass 1 only — adapters return cheap metadata (title, url, engagement, published_at).
Full text is pass 2 (app/fetcher), fetched only after Gate 1 for approved stories.
"""
from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import httpx

log = logging.getLogger("adapter.base")

# Query params that never identify content — stripped before hashing so the same
# article shared with different tracking tags collapses to one item. Heuristic; the
# dedup URL normalization is an intentionally-open decision (see build plan).
_TRACKING_PREFIXES = ("utm_",)
_TRACKING_KEYS = {"ref", "ref_src", "fbclid", "gclid", "mc_cid", "mc_eid", "source"}


def canonical_url(url: str) -> str:
    """Normalize a URL to a stable identity key: lowercase scheme/host, drop the
    fragment and tracking params, strip a trailing slash. Conservative on purpose —
    over-normalizing would merge distinct articles."""
    parts = urlsplit(url.strip())
    scheme = (parts.scheme or "https").lower()
    netloc = parts.netloc.lower()
    if scheme == "http" and netloc.endswith(":80"):
        netloc = netloc[:-3]
    elif scheme == "https" and netloc.endswith(":443"):
        netloc = netloc[:-4]
    query = urlencode([
        (k, v)
        for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if not k.lower().startswith(_TRACKING_PREFIXES) and k.lower() not in _TRACKING_KEYS
    ])
    path = parts.path
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")
    return urlunsplit((scheme, netloc, path, query, ""))


def item_id(url: str) -> str:
    """Stable content id = sha256 of the canonical URL (hex). The same article from any
    source hashes identically, so a cross-source re-sighting upserts, never duplicates."""
    return hashlib.sha256(canonical_url(url).encode("utf-8")).hexdigest()


def get_with_retry(
    client: httpx.Client,
    url: str,
    *,
    headers: dict | None = None,
    retries: int = 2,
    backoff: float = 0.5,
) -> httpx.Response:
    """GET `url` with a small retry on TRANSIENT failures only. Returns the response after a
    successful `raise_for_status()`.

    A single flaky GET (a connect/read/timeout blip or a transient 5xx) should not abort a poll
    when the next attempt would succeed — so this retries those. It does NOT retry 4xx: a client
    error (404, 401, 403, …) is deterministic, not transient, so re-issuing the same request is
    pointless and would just hammer the source.

    Transient = `httpx.TransportError` (connect/read/timeout/etc.) or a 5xx status. `backoff`
    seconds are slept between attempts (a param so tests pass `backoff=0` and don't actually
    sleep). After `retries` extra attempts are exhausted the last exception is re-raised.

    Dependency-free (httpx + stdlib) and synchronous, matching the deterministic adapter seam.
    `retries` is the number of RETRIES, so total attempts = retries + 1."""
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            resp = client.get(url, headers=headers)
            resp.raise_for_status()
            return resp
        except httpx.HTTPStatusError as exc:
            # 4xx is a deterministic client error — do not retry; re-raise immediately.
            status = exc.response.status_code if exc.response is not None else None
            if status is None or status < 500:
                raise
            last_exc = exc
        except httpx.TransportError as exc:
            # connect/read/timeout/etc. — transient; retry.
            last_exc = exc
        if attempt < retries:
            log.warning(
                "transient GET failure for %s (attempt %d/%d): %s; retrying",
                url, attempt + 1, retries + 1, last_exc,
            )
            if backoff:
                time.sleep(backoff)
    # Exhausted: re-raise the last transient error.
    assert last_exc is not None  # the loop only exits here after at least one failure
    raise last_exc


@dataclass
class Item:
    """A normalized pass-1 finding. `url` is the content URL; `id` is its canonical
    hash. `engagement` holds the source's native signals (points/comments/...), {} for
    sources without them (RSS/arXiv). Full text is None here — it is a pass-2 concern."""

    url: str
    title: str | None = None
    published_at: datetime | None = None
    engagement: dict = field(default_factory=dict)

    @property
    def id(self) -> str:
        return item_id(self.url)


@dataclass
class PollResult:
    """What one adapter poll yields: the items found and the cursor to persist for the
    next poll. `not_modified` is True when the source reported nothing changed (e.g. 304)."""

    items: list[Item] = field(default_factory=list)
    cursor: dict = field(default_factory=dict)
    not_modified: bool = False


class Adapter:
    """One adapter per source type. `poll` does pass-1 only and must be idempotent:
    re-polling a source may re-yield items — persistence dedups them by content id."""

    type: str = ""

    def poll(self, source, cursor: dict | None) -> PollResult:  # pragma: no cover
        raise NotImplementedError
