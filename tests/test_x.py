"""X adapter — pure transforms over saved user-lookup + timeline JSON fixtures, plus the
two-step poll path (handle->id lookup, then timeline) with a stubbed httpx client.

No network, no DB, no live X API calls. Exercises:
  - parse_tweets: Item count, status-permalink url, whole-text title, tz-aware UTC
    created_at, public_metrics carried as engagement, stable/distinct item ids;
  - newest_since_id: numeric (int) max across data ids / meta.newest_id / previous cursor,
    and that an empty payload preserves the previous since_id;
  - poll end-to-end: caches the user id on first poll (lookup happens), reuses the cached id
    on the next poll (no lookup), passes since_id, and the empty-result case yields no items
    with the cursor preserved;
  - the env-token contract (RuntimeError naming X_BEARER_TOKEN when unset);
  - the registry wiring (x_user implemented, reddit_sub the only deferred type).
"""
from __future__ import annotations

import json
from datetime import timezone
from pathlib import Path

import httpx
import pytest

from app.adapters import XAdapter, available_types, get_adapter, is_implemented
from app.adapters import _DEFERRED
from app.adapters.base import item_id
from app.adapters.x import (
    XAdapter as XAdapterDirect,
    newest_since_id,
    parse_tweets,
    status_url,
)

FIXTURES = Path(__file__).parent / "fixtures"
_TOKEN = "test-bearer-token"


def _lookup() -> dict:
    return json.loads((FIXTURES / "x_user_lookup.json").read_text())


def _tweets() -> dict:
    return json.loads((FIXTURES / "x_user_tweets.json").read_text())


# --- pure: parse_tweets -------------------------------------------------------------------

def test_parse_tweets_count_and_urls():
    items = parse_tweets(_tweets(), "karpathy")
    assert len(items) == 3
    urls = [i.url for i in items]
    assert urls[0] == "https://x.com/karpathy/status/1799999999999999999"
    # Retweet is kept (exclude=replies only — see adapter docstring).
    assert urls[1] == "https://x.com/karpathy/status/1799000000000000010"
    assert urls[2] == "https://x.com/karpathy/status/1798500000000000005"


def test_status_url_builder():
    assert status_url("simonw", "42") == "https://x.com/simonw/status/42"


def test_title_is_whole_tweet_text():
    items = parse_tweets(_tweets(), "karpathy")
    assert items[0].title.startswith("New post: a from-scratch walkthrough")
    # Retweet text is preserved verbatim (still usable pass-1 content).
    assert items[1].title.startswith("RT @simonw:")


def test_engagement_carries_public_metrics():
    items = parse_tweets(_tweets(), "karpathy")
    assert items[0].engagement == {
        "retweet_count": 412,
        "reply_count": 88,
        "like_count": 5230,
        "quote_count": 37,
        "impression_count": 410233,
        "bookmark_count": 901,
    }


def test_published_at_is_tz_aware_utc():
    item = parse_tweets(_tweets(), "karpathy")[0]
    assert item.published_at is not None
    assert item.published_at.tzinfo is not None
    assert item.published_at.utcoffset() == timezone.utc.utcoffset(None)
    assert item.published_at.year == 2026
    assert item.published_at.hour == 9 and item.published_at.minute == 15


def test_item_ids_stable_and_distinct():
    items = parse_tweets(_tweets(), "karpathy")
    ids = [i.id for i in items]
    assert len(set(ids)) == 3  # distinct
    # Stable: id is the sha256 of the canonical status url.
    assert items[0].id == item_id("https://x.com/karpathy/status/1799999999999999999")


def test_parse_tweets_skips_missing_id():
    payload = {"data": [{"text": "no id here"}, {"id": "5", "text": "ok"}]}
    items = parse_tweets(payload, "karpathy")
    assert len(items) == 1
    assert items[0].url == "https://x.com/karpathy/status/5"


def test_parse_tweets_empty_payload():
    assert parse_tweets({"meta": {"result_count": 0}}, "karpathy") == []
    assert parse_tweets({}, "karpathy") == []


# --- pure: newest_since_id ----------------------------------------------------------------

def test_newest_since_id_picks_numeric_max():
    # The first data id is the largest numerically; meta.newest_id agrees.
    assert newest_since_id(_tweets()) == "1799999999999999999"


def test_newest_since_id_int_compare_not_string():
    # "9" < "1000" as ints; a naive string compare would pick "9". data ids only, no meta.
    payload = {"data": [{"id": "9"}, {"id": "1000"}, {"id": "300"}]}
    assert newest_since_id(payload) == "1000"


def test_newest_since_id_respects_previous_cursor():
    # Previous cursor is already ahead of everything in this (older) payload.
    payload = {"data": [{"id": "100"}], "meta": {"newest_id": "100"}}
    assert newest_since_id(payload, prev_since_id="999") == "999"


def test_newest_since_id_empty_preserves_previous():
    empty = {"data": [], "meta": {"result_count": 0}}
    assert newest_since_id(empty, prev_since_id="555") == "555"
    assert newest_since_id(empty, prev_since_id=None) is None


# --- token contract -----------------------------------------------------------------------

def test_missing_token_raises_named_error(monkeypatch):
    monkeypatch.delenv("X_BEARER_TOKEN", raising=False)
    client = _StubXClient(_lookup(), _tweets())
    adapter = XAdapterDirect(client=client)
    with pytest.raises(RuntimeError, match="X_BEARER_TOKEN"):
        adapter.poll(_source(), cursor=None)


# --- stubbed poll path --------------------------------------------------------------------

class _StubResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("err", request=None, response=None)

    def json(self):
        return self._payload


class _StubXClient:
    """Serves the user-lookup response for /2/users/by/username/<handle> and the timeline
    response for /2/users/<id>/tweets. Records calls so tests can assert lookup-skipping and
    the since_id param."""

    def __init__(self, lookup, timeline):
        self._lookup = lookup
        self._timeline = timeline
        self.calls: list[tuple[str, dict, dict]] = []

    def get(self, url, params=None, headers=None):
        self.calls.append((url, params or {}, headers or {}))
        if "/users/by/username/" in url:
            return _StubResponse(self._lookup)
        if url.endswith("/tweets"):
            return _StubResponse(self._timeline)
        raise AssertionError(f"unexpected url {url}")

    @property
    def urls(self) -> list[str]:
        return [c[0] for c in self.calls]


def _source(handle="karpathy"):
    from app.config import Source, derive_source_key

    identity = {"handle": handle}
    return Source(
        type="x_user",
        identity=identity,
        cadence_s=172800,
        owner="person:test",
        source_key=derive_source_key("x_user", identity),
    )


def test_poll_first_time_looks_up_then_fetches_timeline(monkeypatch):
    monkeypatch.setenv("X_BEARER_TOKEN", _TOKEN)
    client = _StubXClient(_lookup(), _tweets())
    adapter = XAdapterDirect(client=client)
    result = adapter.poll(_source(), cursor=None)

    # Two calls on a cold cursor: lookup, then timeline.
    assert client.urls[0] == "https://api.x.com/2/users/by/username/karpathy"
    assert client.urls[1] == "https://api.x.com/2/users/33836629/tweets"
    # Bearer auth header present.
    assert client.calls[0][2]["Authorization"] == f"Bearer {_TOKEN}"
    # Timeline query params: cap, fields, exclude=replies; no since_id on the first poll.
    tl_params = client.calls[1][1]
    assert tl_params["tweet.fields"] == "created_at,public_metrics"
    assert tl_params["exclude"] == "replies"
    assert "since_id" not in tl_params

    assert result.not_modified is False
    assert len(result.items) == 3
    assert result.cursor == {"user_id": "33836629", "since_id": "1799999999999999999"}


def test_poll_with_cached_user_id_skips_lookup(monkeypatch):
    monkeypatch.setenv("X_BEARER_TOKEN", _TOKEN)
    client = _StubXClient(_lookup(), _tweets())
    adapter = XAdapterDirect(client=client)
    cursor = {"user_id": "33836629", "since_id": "1700000000000000000"}
    result = adapter.poll(_source(), cursor=cursor)

    # Only ONE call — the timeline; the lookup is NOT re-billed.
    assert len(client.calls) == 1
    assert client.urls[0] == "https://api.x.com/2/users/33836629/tweets"
    # since_id from the cursor is forwarded so we fetch only new tweets.
    assert client.calls[0][1]["since_id"] == "1700000000000000000"

    assert len(result.items) == 3
    assert result.cursor["user_id"] == "33836629"
    assert result.cursor["since_id"] == "1799999999999999999"


def test_poll_empty_timeline_preserves_cursor(monkeypatch):
    monkeypatch.setenv("X_BEARER_TOKEN", _TOKEN)
    empty = {"data": [], "meta": {"result_count": 0}}
    client = _StubXClient(_lookup(), empty)
    adapter = XAdapterDirect(client=client)
    cursor = {"user_id": "33836629", "since_id": "1799999999999999999"}
    result = adapter.poll(_source(), cursor=cursor)

    assert result.items == []
    assert result.not_modified is False
    # Cursor preserved unchanged on an empty poll.
    assert result.cursor == cursor


def test_poll_is_idempotent_on_repeat(monkeypatch):
    """Re-polling with the cursor returned by a prior poll, against a timeline that no longer
    has anything newer (empty since_id window), yields no items and the same cursor."""
    monkeypatch.setenv("X_BEARER_TOKEN", _TOKEN)
    first_client = _StubXClient(_lookup(), _tweets())
    adapter = XAdapterDirect(client=first_client)
    first = adapter.poll(_source(), cursor=None)

    # Second poll: the API now returns nothing newer than since_id.
    empty = {"data": [], "meta": {"result_count": 0}}
    second_client = _StubXClient(_lookup(), empty)
    adapter2 = XAdapterDirect(client=second_client)
    second = adapter2.poll(_source(), cursor=first.cursor)

    assert second.items == []
    assert second.cursor == first.cursor


# --- registry -----------------------------------------------------------------------------

def test_registry_exposes_x_user():
    assert "x_user" in available_types()
    assert is_implemented("x_user") is True
    assert isinstance(get_adapter("x_user"), XAdapter)


def test_reddit_sub_is_the_only_deferred_type():
    assert set(_DEFERRED) == {"reddit_sub"}
