"""Hacker News adapter (source type `hn`, identity `{listing, min_points?, match?}`).

Source: the official Firebase HN API (no auth, no new dependency):
    listing ids:  https://hacker-news.firebaseio.com/v0/<listing>stories.json
                  where <listing> is best | top | new  ->  beststories / topstories / newstories
    one item:     https://hacker-news.firebaseio.com/v0/item/<id>.json

Two-step poll: fetch the ranked id list, then fetch the first N item objects (cap behind a
seam — we don't need the whole 500-long list for a single-user pass-1 poll). Filtering from
identity is applied to the fetched items:
  - min_points: keep only items whose `score` >= min_points.
  - match: case-insensitive substring keyword match on the title (keep if ANY keyword hits);
    absent/empty match means no title filter.

`url`: for link submissions use `item['url']` (the external article). For Ask HN / text
posts (no `url`), use the HN discussion permalink https://news.ycombinator.com/item?id=<id>
so there is always a content identity.
engagement = {"points": score, "comments": descendants} — HN's native signals.
published_at: `item['time']` (unix seconds) -> tz-aware UTC.

Cursor: the largest story id observed this poll, recorded as an idempotent breadcrumb (not
necessarily the newest story — best/top listings are rank-ordered, not id-ordered). It is
NOT used to filter — persistence dedups by content id, so re-yielding seen items is harmless
and re-polling stays idempotent.

The pure transforms (`select_story_ids`, `story_to_item`, `stories_to_items`) take
already-fetched JSON and do all filtering/normalization with no network, so they unit-test
without hitting the API. Pass 1 only — metadata; no full-text fetch here.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

import httpx

from app.adapters.base import Adapter, Item, PollResult, get_with_retry

log = logging.getLogger("adapter.hn")

_API = "https://hacker-news.firebaseio.com/v0"
_USER_AGENT = "news-digest/0.1 (+https://github.com/) personal-feed-reader"
_TIMEOUT = httpx.Timeout(20.0, connect=10.0)

# Map the config listing to the Firebase endpoint stem.
_LISTING_ENDPOINT = {
    "best": "beststories",
    "top": "topstories",
    "new": "newstories",
}

# How many of the ranked stories to fetch+inspect per poll. A seam: the listing returns up
# to ~500 ids; we only fetch the top slice (cost = one item GET each), enough to catch the
# fresh high-rankers for a single user without hammering the API.
_DEFAULT_ITEM_CAP = 50

# Seconds slept between retry attempts on a transient GET failure. A seam (injectable) so tests
# pass 0 and don't actually sleep; production keeps a polite half-second.
_DEFAULT_RETRY_BACKOFF = 0.5


def _hn_permalink(item_id_: int) -> str:
    return f"https://news.ycombinator.com/item?id={item_id_}"


def _matches_keywords(title: str | None, keywords: list[str] | None) -> bool:
    """True if no keyword filter, else case-insensitive substring match on ANY keyword."""
    if not keywords:
        return True
    if not title:
        return False
    low = title.lower()
    return any(kw.lower() in low for kw in keywords)


def select_story_ids(id_list: list[int], cap: int = _DEFAULT_ITEM_CAP) -> list[int]:
    """Pure: take the top `cap` ids off the ranked listing (the list is rank-ordered)."""
    return list(id_list[:cap])


def story_to_item(
    story: dict,
    min_points: int | None = None,
    match: list[str] | None = None,
) -> Item | None:
    """Pure: one HN item-JSON -> Item, or None if it is filtered out / unusable.

    Drops dead/deleted items and anything failing min_points or the keyword match. For link
    posts uses the external url; for Ask/text posts uses the HN discussion permalink.
    """
    if not story or story.get("deleted") or story.get("dead"):
        return None

    sid = story.get("id")
    if sid is None:
        return None

    score = story.get("score")
    if min_points is not None and (score is None or score < min_points):
        return None

    title = story.get("title")
    if not _matches_keywords(title, match):
        return None

    # Link submission -> external article; otherwise the HN discussion permalink.
    url = (story.get("url") or "").strip() or _hn_permalink(sid)

    published_at = None
    ts = story.get("time")
    if isinstance(ts, (int, float)):
        published_at = datetime.fromtimestamp(int(ts), tz=timezone.utc)

    engagement: dict = {}
    if score is not None:
        engagement["points"] = score
    descendants = story.get("descendants")
    if descendants is not None:
        engagement["comments"] = descendants

    return Item(
        url=url,
        title=title.strip() if isinstance(title, str) else title,
        published_at=published_at,
        engagement=engagement,
    )


def stories_to_items(
    stories: list[dict],
    min_points: int | None = None,
    match: list[str] | None = None,
) -> list[Item]:
    """Pure: a batch of HN item-JSONs -> filtered, normalized Items (order preserved)."""
    items: list[Item] = []
    for story in stories:
        item = story_to_item(story, min_points=min_points, match=match)
        if item is not None:
            items.append(item)
    return items


class HnAdapter(Adapter):
    """Fetch a ranked HN listing, pull the top slice of item objects, filter by
    min_points/match from identity, and normalize to Items with native engagement."""

    type = "hn"

    def __init__(
        self,
        client: httpx.Client | None = None,
        item_cap: int = _DEFAULT_ITEM_CAP,
        retry_backoff: float = _DEFAULT_RETRY_BACKOFF,
    ):
        # Injectable client + cap + retry backoff keep the adapter testable; defaults per-poll.
        self._client = client
        self._item_cap = item_cap
        self._retry_backoff = retry_backoff

    def poll(self, source, cursor: dict | None) -> PollResult:
        listing = source.identity["listing"]
        endpoint = _LISTING_ENDPOINT.get(listing)
        if endpoint is None:
            raise ValueError(f"unknown hn listing {listing!r}; expected best|top|new")
        min_points = source.identity.get("min_points")
        match = source.identity.get("match")

        client = self._client or httpx.Client(timeout=_TIMEOUT, follow_redirects=True)
        headers = {"User-Agent": _USER_AGENT}
        try:
            # The listing GET is retried on a transient blip; if it still fails the poll raises and
            # the runner isolates this one source for the tick (one source failing a tick is fine).
            ids_resp = get_with_retry(
                client, f"{_API}/{endpoint}.json", headers=headers, backoff=self._retry_backoff
            )
            id_list = ids_resp.json() or []
            ids = select_story_ids(id_list, self._item_cap)

            stories: list[dict] = []
            for sid in ids:
                # Each per-item fetch+parse is isolated: a persistently-bad /item/<id>.json
                # (still failing after retries) skips THAT story, not the whole batch — one flaky
                # item must not abort the poll for the source.
                try:
                    item_resp = get_with_retry(
                        client, f"{_API}/item/{sid}.json", headers=headers,
                        backoff=self._retry_backoff,
                    )
                    story = item_resp.json()
                except Exception as exc:  # noqa: BLE001 — isolate one bad item; keep the batch.
                    log.warning("hn item %s fetch failed (%s); skipping it", sid, exc)
                    continue
                if story:
                    stories.append(story)
        finally:
            if self._client is None:
                client.close()

        items = stories_to_items(stories, min_points=min_points, match=match)

        # Idempotent breadcrumb: the newest (max) story id ever seen. Not a filter. Seed from
        # the prior cursor and only RAISE it, so a successful poll over an empty/null listing
        # (ids == []) keeps the existing breadcrumb instead of wiping it to {} (save_cursor is a
        # wholesale replace, not a merge) — the breadcrumb stays monotonic.
        new_cursor: dict = dict(cursor or {})
        if ids:
            prev_max = new_cursor.get("max_id")
            new_cursor["max_id"] = max(ids) if prev_max is None else max(prev_max, max(ids))

        log.info(
            "hn %s -> %d/%d items pass filters (min_points=%s, match=%s)",
            listing, len(items), len(stories), min_points, match,
        )
        return PollResult(items=items, cursor=new_cursor, not_modified=False)
