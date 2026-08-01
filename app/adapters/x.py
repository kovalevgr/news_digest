"""X adapter (source type `x_user`, identity `{handle}`) — a person's X timeline.

People-only source: we follow specific authors' original posts (config.yaml lists
`x_user` under `people:` — karpathy, simonw, rasbt, lilianweng). X is **pay-per-use**: the
free read tier closed in early 2026, so each billed request costs prepaid credits. The whole
adapter is built to minimize calls — read the cost note below before changing the poll path.

API: X API v2, app-only Bearer auth (Authorization: Bearer <X_BEARER_TOKEN>).
Host: https://api.x.com (the current host; api.twitter.com is a legacy alias — use api.x.com).
The token is read from the env **at call time** (not import), so the module imports cleanly
in tests / on hosts where the token is not set yet; a missing token raises a clear
RuntimeError naming X_BEARER_TOKEN.

Two steps per source, but the user-id is cached in the cursor so the lookup is paid ONCE:
  1. handle -> user id:  GET /2/users/by/username/{handle}
     Called ONLY when the cursor has no cached `user_id`. The id is then stored in the
     cursor and reused forever (handles are stable; if a handle is ever reassigned the owner
     re-keys the source in config, which changes source_key and resets the cursor).
  2. timeline:           GET /2/users/{id}/tweets
     Query: max_results=<cap>, tweet.fields=created_at,public_metrics, exclude=replies,
     and since_id=<cursor.since_id> when present so we fetch ONLY tweets newer than the last
     poll. One timeline call per poll — no pagination (pass-1 only; we don't need history).

exclude= decision: `exclude=replies` only (NOT retweets).
  - replies are excluded: a reply is conversation noise, not the author's own post/story.
  - retweets are KEPT: a retweet is a deliberate signal from a followed author that they
    endorse a piece — exactly the "what is this person amplifying" signal this people-stream
    is for. A retweet's `text` is the retweeted content and its `url` resolves to a real
    status, so it still maps to a usable pass-1 Item; cross-source frequency + the author's
    other sightings sort out duplicates. (If retweet volume ever drowns originals, flip to
    `exclude=replies,retweets` here — it is a one-line change behind this comment.)

Mapping each tweet -> Item (pass-1 metadata only — NO linked-article full text; that is
pass-2, app/fetcher, after Gate 1):
  - url          = https://x.com/{handle}/status/{tweet_id}  (the canonical status permalink)
  - title        = the tweet `text`, whole (a tweet is short — it IS the pass-1 snippet)
  - published_at = `created_at` (ISO 8601) -> tz-aware UTC
  - engagement   = the tweet's `public_metrics` dict (like_count, retweet_count, reply_count,
                   quote_count, and impression_count / bookmark_count when present) — X's
                   native ratings, fed straight into cluster ranking.

Cursor (JSONB): {"user_id": <str>, "since_id": <str>}.
  - user_id: cached so step 1 is never re-billed.
  - since_id: the max tweet id seen so far. X ids are numeric strings ordered by id, so the
    max is computed by comparing as int (string compare would mis-order different lengths).
    Passing it as since_id makes each subsequent poll fetch only new tweets. Idempotent:
    re-polling with the same cursor yields nothing new, and persistence dedups by content id
    regardless. An empty timeline (meta.result_count == 0) returns an empty PollResult with
    the cursor preserved unchanged.

Cost note: pay-per-use. user-id caching collapses step 1 to a single lifetime charge per
handle, and since_id keeps each poll to ONE billed timeline request that transfers only new
posts. There is intentionally no pagination and no full-text fetch in this adapter.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone

import httpx

from app.adapters.base import Adapter, Item, PollResult

log = logging.getLogger("adapter.x")

# Current API host. api.twitter.com is a legacy alias; use api.x.com.
_API = "https://api.x.com"
_BEARER_ENV = "X_BEARER_TOKEN"
_USER_AGENT = "news-digest/0.1 (+https://github.com/) personal-feed-reader"
_TIMEOUT = httpx.Timeout(20.0, connect=10.0)

# Tweet fields we request. exclude=replies (keep originals + retweets) — see module docstring.
_TWEET_FIELDS = "created_at,public_metrics"
_EXCLUDE = "replies"

# How many newest tweets to pull per poll. A seam: the API allows 5-100. For a SINGLE
# followed author polled on a multi-day cadence, ~10-20 new posts between polls is plenty;
# we pick 10 to keep each billed request small (cost-minimization is the whole point of this
# adapter) while still catching a normal poster's gap. Bump it for very prolific handles.
_DEFAULT_MAX_RESULTS = 10


def _require_token() -> str:
    """Read the Bearer token from the env at call time; raise a clear error if unset."""
    token = os.environ.get(_BEARER_ENV)
    if not token:
        raise RuntimeError(
            f"{_BEARER_ENV} is not set — the x_user adapter needs an X API Bearer token "
            f"(set it in the environment; never in config.yaml or code)."
        )
    return token


def _parse_created_at(value: str | None) -> datetime | None:
    """X `created_at` is ISO 8601 UTC (e.g. 2024-01-01T12:00:00.000Z) -> tz-aware UTC."""
    if not value or not isinstance(value, str):
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def status_url(handle: str, tweet_id: str) -> str:
    """Pure: the canonical status permalink for a tweet."""
    return f"https://x.com/{handle}/status/{tweet_id}"


def parse_tweets(payload: dict, handle: str) -> list[Item]:
    """Pure: a `GET /2/users/{id}/tweets` JSON payload -> normalized Items. No network.

    Drops entries with no id (an id is the content identity). The whole tweet `text` is the
    title (pass-1 snippet); `public_metrics` is carried as engagement verbatim. Order is
    preserved (the API returns newest-first).
    """
    items: list[Item] = []
    for tweet in (payload or {}).get("data") or []:
        tid = tweet.get("id")
        if tid is None:
            continue
        tid = str(tid)
        text = tweet.get("text")
        metrics = tweet.get("public_metrics")
        engagement = dict(metrics) if isinstance(metrics, dict) else {}
        items.append(
            Item(
                url=status_url(handle, tid),
                title=text.strip() if isinstance(text, str) else text,
                published_at=_parse_created_at(tweet.get("created_at")),
                engagement=engagement,
            )
        )
    return items


def newest_since_id(payload: dict, prev_since_id: str | None = None) -> str | None:
    """Pure: the new `since_id` = max tweet id across the payload and the previous cursor.

    X ids are numeric strings; compare as int so a longer (larger) id wins regardless of
    digit count. Returns the previous since_id unchanged when the payload is empty, so an
    empty poll preserves the cursor. Prefers meta.newest_id when present (the API's own max),
    falling back to scanning data ids.
    """
    candidates: list[int] = []
    if prev_since_id is not None:
        try:
            candidates.append(int(prev_since_id))
        except (TypeError, ValueError):
            pass

    meta = (payload or {}).get("meta") or {}
    newest = meta.get("newest_id")
    if newest is not None:
        try:
            candidates.append(int(newest))
        except (TypeError, ValueError):
            pass

    for tweet in (payload or {}).get("data") or []:
        tid = tweet.get("id")
        if tid is None:
            continue
        try:
            candidates.append(int(tid))
        except (TypeError, ValueError):
            continue

    if not candidates:
        return prev_since_id
    return str(max(candidates))


class XAdapter(Adapter):
    """Poll a followed author's X timeline (pass-1). Caches the user id and carries a
    since_id so each poll is a single billed request fetching only new posts."""

    type = "x_user"

    def __init__(self, client: httpx.Client | None = None,
                 max_results: int = _DEFAULT_MAX_RESULTS):
        # Injectable client + cap keep the adapter testable; defaults created per-poll.
        self._client = client
        self._max_results = max_results

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {_require_token()}",
            "User-Agent": _USER_AGENT,
        }

    def _lookup_user_id(self, client: httpx.Client, handle: str) -> str:
        """Step 1 (billed once per handle): resolve handle -> user id."""
        resp = client.get(
            f"{_API}/2/users/by/username/{handle}",
            headers=self._headers(),
        )
        resp.raise_for_status()
        data = (resp.json() or {}).get("data") or {}
        user_id = data.get("id")
        if not user_id:
            raise RuntimeError(f"x_user: no id returned for handle {handle!r}")
        return str(user_id)

    def poll(self, source, cursor: dict | None) -> PollResult:
        handle = source.identity["handle"]
        cursor = dict(cursor or {})
        user_id = cursor.get("user_id")
        prev_since_id = cursor.get("since_id")

        client = self._client or httpx.Client(timeout=_TIMEOUT, follow_redirects=True)
        try:
            # Step 1: only if we have not cached the user id yet (avoid re-billing the lookup).
            if not user_id:
                user_id = self._lookup_user_id(client, handle)

            # Step 2: one timeline request, newest-only via since_id.
            params: dict = {
                "max_results": self._max_results,
                "tweet.fields": _TWEET_FIELDS,
                "exclude": _EXCLUDE,
            }
            if prev_since_id:
                params["since_id"] = prev_since_id
            resp = client.get(
                f"{_API}/2/users/{user_id}/tweets",
                params=params,
                headers=self._headers(),
            )
            resp.raise_for_status()
            payload = resp.json() or {}
        finally:
            if self._client is None:
                client.close()

        items = parse_tweets(payload, handle)
        new_since_id = newest_since_id(payload, prev_since_id)

        new_cursor: dict = {"user_id": user_id}
        if new_since_id is not None:
            new_cursor["since_id"] = new_since_id

        result_count = (payload.get("meta") or {}).get("result_count")
        log.info(
            "x_user @%s -> %d new tweets (result_count=%s, since_id=%s)",
            handle, len(items), result_count, new_since_id,
        )
        return PollResult(items=items, cursor=new_cursor, not_modified=False)
