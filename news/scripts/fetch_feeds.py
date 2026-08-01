#!/usr/bin/env python3
"""Deterministic TIER-1 feed fetcher for the file-based news module (news/).

Reads news/config/sources.json, fetches every ``kind == "rss"`` source with a
conditional GET (ETag / Last-Modified persisted in news/state/cursors.json), parses
both RSS 2.0 and Atom, canonicalizes URLs, filters to the run window, and prints one
JSON document to stdout:

    {"generated_at": ..., "window_since": ...,
     "companies": {"<slug>": {"fresh": [...], "source_errors": [...]}}}

EVERY company from the config appears in the output — an empty "fresh" list is the
gap-scrape signal for the agent. Diagnostics go to stderr; stdout is pure JSON.

Python STDLIB ONLY — no pip dependencies; must run in a bare cloud sandbox.
(Uses ``re`` in addition to the core listed modules — stdlib, for HTML-tag stripping.)

Exit codes: 0 on success (including per-source errors, which are reported in-band);
non-zero (2) only when the config itself is unreadable.

Flags:
  --since ISO8601        window start (default: per-source last_run cursor, else 26h ago UTC)
  --company SLUG         process only this company
  --parse-file PATH SLUG parse a local XML file through the same pipeline (offline self-test)
  --no-save-cursors      do not persist cursor updates
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib import error, request
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

NEWS_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = NEWS_DIR / "config" / "sources.json"
CURSORS_PATH = NEWS_DIR / "state" / "cursors.json"

USER_AGENT = "news-digest-fetch-feeds/1.0 (+personal news module)"
TIMEOUT_S = 20
DEFAULT_WINDOW_HOURS = 26
SUMMARY_MAX_CHARS = 500
GUARD_BYTES = 512

# Tracking params that never identify content — ported from app/adapters/base.py.
_TRACKING_PREFIXES = ("utm_",)
_TRACKING_KEYS = {"ref", "ref_src", "fbclid", "gclid", "mc_cid", "mc_eid", "source"}


def log(msg: str) -> None:
    """Diagnostics to stderr so stdout stays pure JSON."""
    print(msg, file=sys.stderr)


def canonicalize_url(url: str) -> str:
    """Normalize a URL to a stable identity key (ported from app/adapters/base.py):
    lowercase scheme+host, drop default ports, strip tracking params (utm_*, fbclid,
    gclid, ref, ...), strip the fragment, strip a trailing slash. Conservative on
    purpose — over-normalizing would merge distinct articles."""
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


def load_config(path: Path = CONFIG_PATH) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_cursors(path: Path = CURSORS_PATH) -> dict:
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}


def save_cursors(cursors: dict, path: Path = CURSORS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(cursors, fh, indent=2, sort_keys=True)
        fh.write("\n")


def _parse_date(raw: str | None) -> datetime | None:
    """Parse an RFC 2822 (RSS pubDate) or ISO 8601 (Atom) date; None if unparseable.
    Naive results are assumed UTC."""
    if not raw:
        return None
    raw = raw.strip()
    dt: datetime | None = None
    try:
        dt = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        try:
            iso = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
            dt = datetime.fromisoformat(iso)
        except ValueError:
            return None
    if dt is not None and dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _clean_summary(raw: str | None) -> str:
    """Strip tags, collapse whitespace, truncate. (HTML entities are left as-is —
    acceptable for a raw excerpt; the agent rewrites the one-liner anyway.)"""
    if not raw:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:SUMMARY_MAX_CHARS]


def _local(tag: str) -> str:
    """Element tag without its XML namespace."""
    return tag.rsplit("}", 1)[-1]


def looks_like_feed(body: str) -> bool:
    """GUARD against HTML-trap URLs that return 200 with a web page: the body must
    contain '<rss' or '<feed' within its first GUARD_BYTES characters."""
    head = body[:GUARD_BYTES]
    return "<rss" in head or "<feed" in head


def parse_feed_xml(body: str) -> list[dict]:
    """Parse RSS 2.0 (<item>) or Atom (<entry>) into a list of
    {title, url, published (datetime|None), summary} dicts. Namespace-agnostic.

    Security note: stdlib-only is a hard constraint here (no defusedxml), so instead
    we refuse any body carrying a DTD/entity declaration — real feeds never have one,
    and this blocks XXE / billion-laughs payloads before they reach the parser."""
    if "<!DOCTYPE" in body or "<!ENTITY" in body:
        raise ET.ParseError("DTD/entity declaration refused (not a plain feed)")
    root = ET.fromstring(body)
    entries = []
    for el in root.iter():
        if _local(el.tag) in ("item", "entry"):
            entries.append(el)
    parsed = []
    for el in entries:
        title = None
        link = None
        atom_link_fallback = None
        published_raw = None
        updated_raw = None
        summary_raw = None
        for child in el:
            name = _local(child.tag)
            text = (child.text or "").strip()
            if name == "title":
                title = text or title
            elif name == "link":
                if text:  # RSS: <link>url</link>
                    link = link or text
                else:  # Atom: <link href="..." rel="..."/>
                    href = child.get("href")
                    rel = child.get("rel", "alternate")
                    if href and rel == "alternate":
                        link = link or href
                    elif href:
                        atom_link_fallback = atom_link_fallback or href
            elif name in ("pubDate", "published"):
                published_raw = published_raw or text
            elif name == "updated":
                updated_raw = updated_raw or text
            elif name in ("description", "summary", "content"):
                summary_raw = summary_raw or text
        url = link or atom_link_fallback
        if not url:
            continue  # an item without a link is unusable — every item must carry its URL
        parsed.append({
            "title": title or "(untitled)",
            "url": url,
            "published": _parse_date(published_raw or updated_raw),
            "summary": _clean_summary(summary_raw),
        })
    return parsed


def fetch_one(url: str, cursor: dict, now_iso: str) -> tuple[str | None, dict, str | None]:
    """Conditional GET of one feed URL. Returns (body_text|None, new_cursor, error|None).
    body_text is None on 304 (not modified) or on error. new_cursor is ALWAYS seeded
    from the old cursor so a 200 without ETag/Last-Modified headers never wipes the
    existing breadcrumb."""
    new_cursor = dict(cursor)  # seed from the old one — never wipe breadcrumbs
    headers = {"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*"}
    if cursor.get("etag"):
        headers["If-None-Match"] = cursor["etag"]
    if cursor.get("last_modified"):
        headers["If-Modified-Since"] = cursor["last_modified"]
    req = request.Request(url, headers=headers)
    try:
        with request.urlopen(req, timeout=TIMEOUT_S) as resp:
            raw = resp.read()
            etag = resp.headers.get("ETag")
            last_modified = resp.headers.get("Last-Modified")
            if etag:
                new_cursor["etag"] = etag
            if last_modified:
                new_cursor["last_modified"] = last_modified
            new_cursor["last_run"] = now_iso
            charset = resp.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace"), new_cursor, None
    except error.HTTPError as exc:
        if exc.code == 304:
            new_cursor["last_run"] = now_iso
            return None, new_cursor, None  # not modified — a clean skip, not an error
        return None, new_cursor, f"HTTP {exc.code}"
    except error.URLError as exc:
        return None, new_cursor, f"URL error: {exc.reason}"
    except (TimeoutError, OSError) as exc:
        return None, new_cursor, f"transport error: {exc}"


def _window_start(args_since: datetime | None, cursor: dict, now: datetime) -> datetime:
    """Per-source window start: explicit --since wins, then the source's last_run
    cursor, then the 26h default."""
    if args_since is not None:
        return args_since
    last_run = _parse_date(cursor.get("last_run"))
    if last_run is not None:
        return last_run
    return now - timedelta(hours=DEFAULT_WINDOW_HOURS)


def _to_output_items(entries: list[dict], since: datetime, source_url: str) -> list[dict]:
    """Window-filter parsed entries and shape them for output. Items with an
    unparseable date are INCLUDED (dedup downstream handles re-yields) — simplest
    safe choice, noted here as a decision."""
    out = []
    for e in entries:
        pub = e["published"]
        if pub is not None and pub < since:
            continue
        out.append({
            "title": e["title"],
            "url": e["url"],
            "canonical_url": canonicalize_url(e["url"]),
            "published": pub.isoformat() if pub is not None else None,
            "summary": e["summary"],
            "source_url": source_url,
        })
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TIER-1 RSS/Atom fetcher for news/ (stdlib only)")
    ap.add_argument("--since", help="ISO8601 window start (default: per-source cursor last_run, else 26h ago UTC)")
    ap.add_argument("--company", help="process only this company slug")
    ap.add_argument("--parse-file", nargs=2, metavar=("PATH", "COMPANY"),
                    help="offline: parse a local XML file through the same pipeline")
    ap.add_argument("--no-save-cursors", action="store_true", help="do not persist cursor updates")
    args = ap.parse_args(argv)

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    args_since = _parse_date(args.since) if args.since else None
    if args.since and args_since is None:
        log(f"error: --since is not valid ISO8601: {args.since!r}")
        return 2

    try:
        config = load_config()
    except (OSError, json.JSONDecodeError) as exc:
        log(f"error: config unreadable at {CONFIG_PATH}: {exc}")
        return 2

    companies = config.get("companies", [])
    if args.company:
        companies = [c for c in companies if c["slug"] == args.company]

    default_since = args_since or (now - timedelta(hours=DEFAULT_WINDOW_HOURS))
    result = {
        "generated_at": now_iso,
        # The global default window; a per-source last_run cursor may narrow it further.
        "window_since": default_since.isoformat(),
        "companies": {},
    }

    # --- offline self-test seam: parse a local file as one company's single source ---
    if args.parse_file:
        path_str, slug = args.parse_file
        body = Path(path_str).read_text(encoding="utf-8")
        entry = {"fresh": [], "source_errors": []}
        if not looks_like_feed(body):
            entry["source_errors"].append({"source_url": path_str, "error": "TRAP/not-a-feed"})
        else:
            try:
                entry["fresh"] = _to_output_items(parse_feed_xml(body), default_since, path_str)
            except ET.ParseError as exc:
                entry["source_errors"].append({"source_url": path_str, "error": f"XML parse error: {exc}"})
        result["companies"][slug] = entry
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    cursors = load_cursors()

    for company in companies:
        slug = company["slug"]
        entry = {"fresh": [], "source_errors": []}
        result["companies"][slug] = entry  # every company appears, even with no rss source
        for source in company.get("sources", []):
            if source.get("kind") != "rss":
                continue
            url = source["url"]
            cursor = cursors.get(url, {})
            since = _window_start(args_since, cursor, now)
            body, new_cursor, err = fetch_one(url, cursor, now_iso)
            if err is not None:
                log(f"[{slug}] {url}: {err}")
                entry["source_errors"].append({"source_url": url, "error": err})
                continue
            cursors[url] = new_cursor
            if body is None:
                log(f"[{slug}] {url}: 304 not modified — skip")
                continue
            if not looks_like_feed(body):
                log(f"[{slug}] {url}: TRAP/not-a-feed — skip")
                entry["source_errors"].append({"source_url": url, "error": "TRAP/not-a-feed"})
                continue
            try:
                parsed = parse_feed_xml(body)
            except ET.ParseError as exc:
                log(f"[{slug}] {url}: XML parse error: {exc}")
                entry["source_errors"].append({"source_url": url, "error": f"XML parse error: {exc}"})
                continue
            entry["fresh"].extend(_to_output_items(parsed, since, url))

    if not args.no_save_cursors:
        save_cursors(cursors)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
