"""The shared `get_with_retry` adapter helper — transient-only retry semantics.

No network, no DB. Injects a fake httpx.Client whose `get` is scripted to raise/return per
attempt, and asserts:
  - a transient TransportError (connect/read/timeout) is retried then succeeds,
  - a transient 5xx is retried then succeeds,
  - a 4xx is NOT retried (it raises on the first attempt — client errors aren't transient),
  - the last exception is re-raised once `retries` are exhausted.
`backoff=0` everywhere so the tests never actually sleep.
"""
from __future__ import annotations

import httpx
import pytest

from app.adapters.base import get_with_retry


class _ScriptedClient:
    """A fake httpx.Client whose .get pops the next scripted outcome.

    Each scripted entry is either an Exception (raised) or an httpx.Response (returned, so the
    helper's own raise_for_status decides 4xx/5xx). Records every requested url."""

    def __init__(self, script):
        self._script = list(script)
        self.calls: list[str] = []

    def get(self, url, headers=None):
        self.calls.append(url)
        outcome = self._script.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def _response(status_code: int, *, text: str = "ok") -> httpx.Response:
    # A real httpx.Response with a request attached, so raise_for_status raises a proper
    # HTTPStatusError carrying .response.status_code (which get_with_retry inspects).
    request = httpx.Request("GET", "https://example.test/x")
    return httpx.Response(status_code, text=text, request=request)


def test_transport_error_is_retried_then_succeeds():
    # First attempt: a read timeout (TransportError); second attempt: 200.
    client = _ScriptedClient([
        httpx.ReadTimeout("read timed out"),
        _response(200, text="payload"),
    ])
    resp = get_with_retry(client, "https://example.test/x", retries=2, backoff=0)
    assert resp.status_code == 200
    assert resp.text == "payload"
    assert len(client.calls) == 2  # one retry consumed


def test_5xx_is_retried_then_succeeds():
    # First attempt: 503 (transient server error); second attempt: 200.
    client = _ScriptedClient([
        _response(503),
        _response(200, text="payload"),
    ])
    resp = get_with_retry(client, "https://example.test/x", retries=2, backoff=0)
    assert resp.status_code == 200
    assert len(client.calls) == 2


def test_4xx_is_not_retried():
    # A 404 is a deterministic client error — it must raise on the FIRST attempt, no retry.
    client = _ScriptedClient([
        _response(404),
        _response(200),  # would succeed if (wrongly) retried
    ])
    with pytest.raises(httpx.HTTPStatusError):
        get_with_retry(client, "https://example.test/x", retries=2, backoff=0)
    assert len(client.calls) == 1  # no retry on a client error


def test_retries_exhausted_reraises_last_transient():
    # All attempts transient -> after retries exhausted the last exception is re-raised.
    client = _ScriptedClient([
        httpx.ConnectError("conn refused"),
        _response(502),
        _response(500),
    ])
    with pytest.raises(httpx.HTTPStatusError):  # the last failure was a 5xx
        get_with_retry(client, "https://example.test/x", retries=2, backoff=0)
    assert len(client.calls) == 3  # 1 initial + 2 retries


def test_success_first_attempt_no_retry():
    client = _ScriptedClient([_response(200, text="payload")])
    resp = get_with_retry(client, "https://example.test/x", retries=2, backoff=0)
    assert resp.status_code == 200
    assert len(client.calls) == 1
