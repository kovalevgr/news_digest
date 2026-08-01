"""Hacker News adapter — pure transforms over saved stories-list + item JSON fixtures.

No network, no DB. Exercises the testable functions that take already-fetched JSON:
  - select_story_ids caps the ranked id list,
  - story_to_item / stories_to_items apply min_points + match filtering, pick the link url
    vs the Ask/text HN permalink, drop dead items, and carry {points, comments} engagement
    with a tz-aware UTC published_at.
Also checks the adapter end-to-end with a stubbed client that serves the same fixtures.
"""
from __future__ import annotations

import json
from datetime import timezone
from pathlib import Path

import httpx

from app.adapters import HnAdapter, available_types, get_adapter, is_implemented
from app.adapters.base import item_id
from app.adapters.hn import (
    HnAdapter as HnAdapterDirect,
    select_story_ids,
    stories_to_items,
    story_to_item,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _stories() -> dict:
    return json.loads((FIXTURES / "hn_items.json").read_text())


def _id_list() -> list[int]:
    return json.loads((FIXTURES / "hn_stories.json").read_text())


def _story(sid: int) -> dict:
    return _stories()[str(sid)]


def test_select_story_ids_caps():
    ids = _id_list()
    assert select_story_ids(ids, cap=2) == ids[:2]
    assert select_story_ids(ids, cap=100) == ids  # cap larger than list -> whole list


def test_link_post_uses_external_url():
    item = story_to_item(_story(40001))
    assert item is not None
    assert item.url == "https://example.com/llm-beats-gpt4"
    assert item.id == item_id("https://example.com/llm-beats-gpt4")


def test_ask_post_uses_hn_permalink():
    item = story_to_item(_story(40003))
    assert item is not None
    assert item.url == "https://news.ycombinator.com/item?id=40003"


def test_engagement_carries_points_and_comments():
    item = story_to_item(_story(40001))
    assert item.engagement == {"points": 250, "comments": 88}


def test_published_at_is_tz_aware_utc():
    item = story_to_item(_story(40001))
    assert item.published_at is not None
    assert item.published_at.tzinfo is not None
    assert item.published_at.utcoffset() == timezone.utc.utcoffset(None)


def test_dead_item_is_dropped():
    assert story_to_item(_story(40005)) is None


def test_min_points_filter():
    # 40002 has score 40 -> dropped at min_points=100; 40001 (250) kept.
    assert story_to_item(_story(40002), min_points=100) is None
    assert story_to_item(_story(40001), min_points=100) is not None


def test_match_keyword_filter_case_insensitive():
    # 40001 title mentions LLM/GPT; 40004 "Rust 2.0" does not match the AI keywords.
    kept = story_to_item(_story(40001), match=["llm", "gpt"])
    assert kept is not None
    dropped = story_to_item(_story(40004), match=["LLM", "GPT"])
    assert dropped is None


def test_stories_to_items_applies_both_filters():
    stories = list(_stories().values())
    items = stories_to_items(stories, min_points=100, match=["LLM", "Postgres"])
    urls = {i.url for i in items}
    # 40001 (LLM, 250pts) and 40003 (Ask HN Postgres, 500pts) survive;
    # 40002 (40pts) below min_points, 40004 (Rust) no keyword, 40005 dead.
    assert urls == {
        "https://example.com/llm-beats-gpt4",
        "https://news.ycombinator.com/item?id=40003",
    }


class _StubResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("err", request=None, response=None)

    def json(self):
        return self._payload


class _StubHnClient:
    """Serves the id-list for the listing endpoint and item JSON for /item/<id>.json."""

    def __init__(self, id_list, stories):
        self._id_list = id_list
        self._stories = stories
        self.urls: list[str] = []

    def get(self, url, headers=None):
        self.urls.append(url)
        if url.endswith("stories.json"):
            return _StubResponse(self._id_list)
        # /item/<id>.json
        sid = url.rsplit("/", 1)[-1].removesuffix(".json")
        return _StubResponse(self._stories.get(sid))


def _source(listing="best", min_points=None, match=None):
    from app.config import Source, derive_source_key

    identity: dict = {"listing": listing}
    if min_points is not None:
        identity["min_points"] = min_points
    if match is not None:
        identity["match"] = match
    return Source(
        type="hn",
        identity=identity,
        cadence_s=21600,
        owner="topic:test",
        source_key=derive_source_key("hn", identity),
    )


def test_poll_end_to_end_with_stub_client():
    client = _StubHnClient(_id_list(), _stories())
    adapter = HnAdapterDirect(client=client)
    result = adapter.poll(_source(min_points=100, match=["LLM", "Postgres"]), cursor=None)

    assert result.not_modified is False
    urls = {i.url for i in result.items}
    assert urls == {
        "https://example.com/llm-beats-gpt4",
        "https://news.ycombinator.com/item?id=40003",
    }
    # listing endpoint hit first, then one item GET per id.
    assert client.urls[0] == "https://hacker-news.firebaseio.com/v0/beststories.json"
    assert result.cursor == {"max_id": 40005}


def test_registry_exposes_hn():
    assert "hn" in available_types()
    assert is_implemented("hn") is True
    assert isinstance(get_adapter("hn"), HnAdapter)


# --- Phase 7: flaky-fetch resilience (skip one bad item, retry a transient blip) ------------


def _httpx_response(status_code: int, *, json_body=None) -> httpx.Response:
    """A real httpx.Response carrying a request, so get_with_retry's raise_for_status raises a
    proper HTTPStatusError with .response.status_code."""
    request = httpx.Request("GET", "https://hacker-news.firebaseio.com/v0/x")
    if json_body is not None:
        return httpx.Response(status_code, json=json_body, request=request)
    return httpx.Response(status_code, request=request)


class _FlakyHnClient:
    """Serves the listing + item JSON like _StubHnClient, but a chosen story id ALWAYS fails its
    item GET (persistently, even across retries) — so the adapter must SKIP that one story and
    still return the rest, never abort the batch. Returns real httpx.Responses so the in-adapter
    get_with_retry exercises its real raise_for_status path."""

    def __init__(self, id_list, stories, *, fail_sid, fail_exc=None):
        self._id_list = id_list
        self._stories = stories
        self._fail_sid = str(fail_sid)
        # Default failure is a persistent 503 (transient class -> retried then exhausted).
        self._fail_exc = fail_exc
        self.urls: list[str] = []

    def get(self, url, headers=None):
        self.urls.append(url)
        if url.endswith("stories.json"):
            return _httpx_response(200, json_body=self._id_list)
        sid = url.rsplit("/", 1)[-1].removesuffix(".json")
        if sid == self._fail_sid:
            if self._fail_exc is not None:
                raise self._fail_exc
            return _httpx_response(503)  # persistent server error -> retried, then raises
        return _httpx_response(200, json_body=self._stories.get(sid))


def test_poll_skips_a_persistently_bad_item_keeps_the_rest():
    # 40001 (a kept LLM story) always 503s on its item GET; the poll must skip it and still
    # return the other surviving items — one flaky item never aborts the whole batch.
    client = _FlakyHnClient(_id_list(), _stories(), fail_sid=40001)
    adapter = HnAdapterDirect(client=client, retry_backoff=0)  # backoff=0 -> no real sleep
    result = adapter.poll(_source(min_points=100, match=["LLM", "Postgres"]), cursor=None)

    urls = {i.url for i in result.items}
    # 40001 was skipped (its GET kept failing); 40003 (Ask HN Postgres) still came through.
    assert "https://example.com/llm-beats-gpt4" not in urls
    assert "https://news.ycombinator.com/item?id=40003" in urls
    # The bad item was retried (initial + 2 retries = 3 GETs for sid 40001) before being skipped.
    bad_gets = [u for u in client.urls if u.endswith("/item/40001.json")]
    assert len(bad_gets) == 3


def test_poll_skips_item_on_transient_transport_error():
    # A read timeout on the item GET (TransportError) is the transient class too: retried, and
    # when it never recovers, that one item is skipped — not fatal to the batch.
    client = _FlakyHnClient(
        _id_list(), _stories(), fail_sid=40003, fail_exc=httpx.ReadTimeout("read timed out")
    )
    adapter = HnAdapterDirect(client=client, retry_backoff=0)
    result = adapter.poll(_source(min_points=100, match=["LLM", "Postgres"]), cursor=None)

    urls = {i.url for i in result.items}
    assert "https://news.ycombinator.com/item?id=40003" not in urls  # skipped
    assert "https://example.com/llm-beats-gpt4" in urls  # the other survivor stayed


class _TransientThenOkHnClient:
    """The listing GET fails transiently ONCE then succeeds; item GETs all succeed. Proves the
    listing GET is retried (a transient blip on the listing must not lose the whole poll)."""

    def __init__(self, id_list, stories):
        self._id_list = id_list
        self._stories = stories
        self._listing_calls = 0
        self.urls: list[str] = []

    def get(self, url, headers=None):
        self.urls.append(url)
        if url.endswith("stories.json"):
            self._listing_calls += 1
            if self._listing_calls == 1:
                raise httpx.ConnectError("connection refused")  # transient, retried
            return _httpx_response(200, json_body=self._id_list)
        sid = url.rsplit("/", 1)[-1].removesuffix(".json")
        return _httpx_response(200, json_body=self._stories.get(sid))


def test_listing_get_retries_a_transient_blip_then_succeeds():
    client = _TransientThenOkHnClient(_id_list(), _stories())
    adapter = HnAdapterDirect(client=client, retry_backoff=0)
    result = adapter.poll(_source(min_points=100, match=["LLM", "Postgres"]), cursor=None)

    urls = {i.url for i in result.items}
    assert urls == {
        "https://example.com/llm-beats-gpt4",
        "https://news.ycombinator.com/item?id=40003",
    }
    # The listing endpoint was hit twice (one transient failure + one success).
    listing_hits = [u for u in client.urls if u.endswith("stories.json")]
    assert len(listing_hits) == 2
