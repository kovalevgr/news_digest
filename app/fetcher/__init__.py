"""Pass-2 full-text extraction (docs/01_technical.md §2.2; build plan Phase 2).

This is the pipeline's SECOND fetch pass: pass 1 (the adapters) records cheap metadata
for everything; pass 2 fetches full article text — but ONLY for clusters the owner has
approved at Gate 1. It is a shared COMPONENT, not a pipeline stage and not a source
adapter: the bot calls `fetch_cluster_full_text` off the back of an approval, and Phase 3's
writer-agent reuses the same extractor for its `fetch_source` tool. It coordinates with the
rest of the system purely through `items.full_text` in Postgres; it never calls another
stage.

Three layers, each tested at the right altitude (see tests/test_fetcher.py):

  - extract_main_text(html, url=None) — PURE. Readability main-content extraction down to
    plain text, with a tag-strip fallback so it NEVER raises on a malformed/minimal page.
    No network, no DB; unit-tested against a realistic article fixture.
  - fetch_full_text(url, *, client=None) — the single-URL I/O seam: a real-UA, redirect-
    following GET, then extract. None on a >=400 response or an empty extraction; transport
    errors (httpx.ConnectError etc.) PROPAGATE so the cluster loop can count and isolate them.
    The httpx.Client is injectable (tests drive it with a MockTransport — no network).
  - fetch_cluster_full_text(session, cluster_id, *, client=None) — the DB-backed driver:
    fetch + persist full_text for a cluster's still-empty items, isolating per-item failures,
    idempotent, committing per item so a long cluster makes incremental, crash-safe progress.

Determinism / grounding contract:
  - NO model call lives here. Extraction is deterministic parsing; this component never
    generates or summarizes (that is the writer-agent's job, Phase 3).
  - full_text is written ONCE per item (the predicate selects full_text IS NULL), so a
    re-run never re-fetches an already-extracted item and never overwrites it.

Intentionally-OPEN / DEFERRED seam — paywalled & JS-rendered pages (docs/03_build_plan.md):
  readability sees only the server-returned HTML. A member-only Medium post truncates to its
  preview; a fully client-rendered page yields little or no body text. The design's fallback
  is a headless browser, but that pulls in a heavy browser dependency, so it is deliberately
  NOT added in Phase 2. The seam is clean: when `extract_main_text` returns "" (or a stub
  too short to be useful) on a 200, that is the signal a future headless renderer would take
  over for that URL. Today such a page simply yields an empty extraction -> the item is
  counted "empty" and left with full_text NULL (no browser dependency, no silent bad text).
"""
from __future__ import annotations

import logging
import os

import httpx
from sqlalchemy import select

from app.db.models import Item as ItemModel

log = logging.getLogger("fetcher")

# A real UA — some article hosts 403 the default httpx/python agent (mirrors the adapters).
_USER_AGENT = "news-digest/0.1 (+https://github.com/) personal-article-reader"
_TIMEOUT = httpx.Timeout(20.0, connect=10.0)

# Cap on stored full_text. A pathological page (or a misbehaving site that streams megabytes)
# should not balloon a row or the embedding/draft context built from it. 200k chars is far
# more than any real article yet bounds the worst case. Env-overridable seam; bad/non-positive
# values fall back to the default so the cap is never accidentally disabled.
DEFAULT_FETCH_MAX_CHARS = 200_000


def fetch_max_chars() -> int:
    """Max characters of extracted text persisted per item (env FETCH_MAX_CHARS).
    Falls back to the default on absence/garbage/non-positive — the cap is never disabled."""
    raw = os.environ.get("FETCH_MAX_CHARS")
    if raw is None:
        return DEFAULT_FETCH_MAX_CHARS
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad FETCH_MAX_CHARS=%r — falling back to %s", raw, DEFAULT_FETCH_MAX_CHARS)
        return DEFAULT_FETCH_MAX_CHARS
    return val if val > 0 else DEFAULT_FETCH_MAX_CHARS


# --- pure extraction -----------------------------------------------------------------------


def _strip_to_text(html: str) -> str:
    """Last-resort fallback: parse the whole document, drop noise tags, return its text.

    Used when readability is unavailable or bails on a page too minimal to have a clear
    "article" container (the fixture's one-paragraph case). lxml is lazy-imported so a caller
    that never reaches extraction doesn't pay for it; if even lxml is unavailable or the parse
    fails, we degrade to a crude regex tag-strip rather than raise — this function must never
    throw (its whole reason for existing is to be the safety net)."""
    try:
        import lxml.html

        doc = lxml.html.fromstring(html)
        # Drop tags whose payload is markup/noise, not prose — otherwise their text content
        # (JS source, CSS rules, tracking pixels) leaks into the "article" text.
        for el in doc.xpath("//script | //style | //noscript"):
            el.drop_tree()
        return _collapse_whitespace(doc.text_content())
    except Exception:  # noqa: BLE001 — the fallback must never raise; degrade further below.
        import re

        no_tags = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
        no_tags = re.sub(r"(?s)<[^>]+>", " ", no_tags)
        return _collapse_whitespace(no_tags)


def _collapse_whitespace(text: str) -> str:
    """Collapse any run of whitespace (incl. newlines) to single spaces and trim the ends.
    Plain extracted text is for embedding/draft context, not display, so a single normalized
    space stream is what we want — no attempt to preserve paragraph structure here."""
    return " ".join(text.split())


def extract_main_text(html: str, url: str | None = None) -> str:
    """Extract an article's main body from raw HTML as plain text. PURE — no network, no DB.

    Strategy: try readability-lxml (`Document.summary()`), which isolates the main content
    container and drops nav/sidebar/footer chrome; render that subtree to text via lxml,
    dropping <script>/<style>/<noscript> so their payloads (JS, CSS, tracking) never leak
    into the text; collapse whitespace. If readability is unavailable, yields nothing, or
    raises (it can bail on a page with no clear article container — e.g. a single bare
    paragraph), fall back to `_strip_to_text` over the WHOLE document so we still salvage the
    prose.

    Never raises: every failure path degrades to the tag-strip fallback or "". Empty/
    whitespace-only input returns "" without touching the parser. `url` is accepted for the
    readability base-URL hint and future per-site handling; it is not required for extraction.
    """
    if not html or not html.strip():
        return ""

    try:
        from readability import Document

        # `summary()` returns an HTML fragment of just the main content; re-parse it to pull
        # clean text and to guarantee script/style payloads in that fragment are dropped too.
        summary_html = Document(html, url=url).summary(html_partial=True)
        text = _strip_to_text(summary_html) if summary_html else ""
        if text:
            return text
    except Exception:  # noqa: BLE001 — readability bailed; fall through to the whole-doc strip.
        log.debug("readability extraction failed for %s; falling back to tag strip", url)

    # Fallback: salvage text from the whole document (minimal pages, readability misses, or a
    # readability summary that came back empty).
    return _strip_to_text(html)


# --- single-URL fetch (I/O seam, injectable client) ---------------------------------------


def fetch_full_text(url: str, *, client: httpx.Client | None = None) -> str | None:
    """GET `url`, extract its main text, return it — or None when there is nothing usable.

    I/O seam for one URL. A real User-Agent and follow_redirects mirror the adapters (some
    hosts 403 a bare client or 301 to a canonical path). The httpx.Client is injectable for
    testability (a MockTransport drives the fetch tests with no network); when omitted, one is
    created and closed within this call so the caller need not manage it.

    Returns:
      - None for a >=400 response (missing/forbidden/paywalled-as-error) — nothing to store.
      - None when extraction yields "" (e.g. a JS-only page: the DEFERRED headless seam) —
        we never store an empty body.
      - the extracted text otherwise.

    Transport errors (httpx.ConnectError, timeouts, ...) are NOT swallowed: they PROPAGATE so
    `fetch_cluster_full_text` can isolate and COUNT a per-item failure distinctly from an
    empty extraction. The caller owns that policy; a bare single-URL fetch surfaces the error.
    """
    own_client = client is None
    client = client or httpx.Client(timeout=_TIMEOUT, follow_redirects=True)
    try:
        resp = client.get(url, headers={"User-Agent": _USER_AGENT})
    finally:
        if own_client:
            client.close()

    if resp.status_code >= 400:
        log.info("fetch %s -> HTTP %d; no full text", url, resp.status_code)
        return None

    text = extract_main_text(resp.text, url=url)
    if not text:
        # 200 but nothing extractable (paywall preview stripped to nothing, JS-rendered body):
        # the DEFERRED headless-render seam. Today: no text stored.
        log.info("fetch %s -> empty extraction (JS/paywall?); no full text", url)
        return None
    return text


# --- DB-backed driver: fetch a cluster's full text ----------------------------------------


def fetch_cluster_full_text(
    session, cluster_id: str, *, client: httpx.Client | None = None
) -> dict:
    """Fetch + persist `full_text` for every item of a cluster that still lacks it. Pass 2.

    Selects the cluster's items WHERE full_text IS NULL AND url IS NOT NULL, oldest-first, and
    for each: fetch the URL, write `items.full_text` (capped at FETCH_MAX_CHARS), and COMMIT
    that item. Committing per item means a long cluster makes incremental, crash-safe progress
    and a later item's failure never costs the earlier items their stored text.

    Per-item failure isolation (the design's correctness point): a raised fetch (transport
    error) is caught, COUNTED under "failed", and skipped. Such a failure made NO database
    change for that item, so we do NOT roll back — that would discard the prior items' already
    committed text. The failed item simply keeps full_text NULL and is reconsidered on the
    next run.

    Idempotent: the NULL predicate means an already-fetched item is never reconsidered, so a
    re-run only retries the still-empty/failed items. One httpx.Client is reused across all of
    the cluster's items (created+closed here when not injected) to amortize connection setup.

    Returns {"considered", "fetched", "empty", "failed"} (considered = items that were NULL at
    selection; fetched + empty + failed sum to it).
    """
    item_ids = session.execute(
        select(ItemModel.id)
        .where(ItemModel.cluster_id == cluster_id)
        .where(ItemModel.full_text.is_(None))
        .where(ItemModel.url.is_not(None))
        .order_by(ItemModel.fetched_at.asc(), ItemModel.id.asc())
    ).scalars().all()

    stats = {"considered": len(item_ids), "fetched": 0, "empty": 0, "failed": 0}
    if not item_ids:
        return stats

    cap = fetch_max_chars()
    own_client = client is None
    client = client or httpx.Client(timeout=_TIMEOUT, follow_redirects=True)
    try:
        for item_id_ in item_ids:
            item = session.get(ItemModel, item_id_)
            if item is None or item.url is None or item.full_text is not None:
                # Re-confirm against the live row: another pass may have filled it between the
                # id select and now. Never overwrite an already-fetched item.
                continue
            try:
                text = fetch_full_text(item.url, client=client)
            except Exception:  # noqa: BLE001 — isolate ONE bad fetch; the rest of the cluster proceeds.
                # No DB write happened for this item, so there is nothing to roll back; rolling
                # back here would discard prior items' committed full_text.
                log.warning("fetch failed for item %s (%s); skipping", item_id_, item.url, exc_info=True)
                stats["failed"] += 1
                continue

            if not text:
                stats["empty"] += 1
                continue

            item.full_text = text[:cap]
            session.commit()  # commit per item: incremental, crash-safe progress
            stats["fetched"] += 1
    finally:
        if own_client:
            client.close()

    log.info(
        "fetch cluster %s: considered=%d fetched=%d empty=%d failed=%d",
        cluster_id, stats["considered"], stats["fetched"], stats["empty"], stats["failed"],
    )
    return stats


__all__ = [
    "DEFAULT_FETCH_MAX_CHARS",
    "fetch_max_chars",
    "extract_main_text",
    "fetch_full_text",
    "fetch_cluster_full_text",
]
