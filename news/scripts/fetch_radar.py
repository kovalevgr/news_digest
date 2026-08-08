#!/usr/bin/env python3
"""Deterministic fetcher for the technical radar (news/config/radar.json).

Same contract as fetch_feeds.py: Python STDLIB ONLY, diagnostics to stderr, one JSON
document to stdout:

    {"generated_at": ..., "window_since": ...,
     "sources": {"<id>": {"category": ..., "fresh": [...], "errors": [...]}}}

Every enabled source appears in the output. State (HTTP cursors + seen-sets +
leaderboard snapshots) lives in news/state/radar-cursors.json — script-owned,
never hand-edited.

Source kinds:
  rss       RSS/Atom via conditional GET (shares fetch_feeds.py parsing + guards)
  json      JSON API through a named adapter (algolia, lobsters, hf_papers,
            hf_trending, hf_org_models)
  html      HTML page through a named adapter (anthropic_engineering, baseten,
            lmsys_flight, page_hash)
  git-tags  `git ls-remote --tags <repo>` via the git proxy — release detection
            where the GitHub REST API is unavailable (cloud sessions)

Hardening (each learned from a live failure — see research/connectivity/):
  - control chars stripped before XML parse (answer.ai embeds raw terminal output)
  - 8MB body cap (cameron-wolfe feed is ~5.9MB)
  - per-source max_items caps (NVIDIA/cloudflare bursts, smol.ai archive feed)
  - seen-set dedup for undated sources (github-trending mirror has no pubDates)
  - snapshot-diff for leaderboard APIs (HF trending is a ranking, not a feed)
  - version-agnostic tag diffing (ls-remote order is lexical, not chronological)

Flags:
  --since ISO8601     window start (default: per-source last_run, else 26h ago)
  --source ID         process only this source
  --no-save-state     do not persist state updates
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib import error, request

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_feeds import (  # noqa: E402  (stdlib-only sibling module)
    _clean_summary,
    _parse_date,
    canonicalize_url,
    log,
    looks_like_feed,
    parse_feed_xml,
)

NEWS_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = NEWS_DIR / "config" / "radar.json"
STATE_PATH = NEWS_DIR / "state" / "radar-cursors.json"

USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
TIMEOUT_S = 20
MAX_BYTES = 8 * 1024 * 1024
DEFAULT_WINDOW_HOURS = 26
SEEN_CAP = 400  # per-source seen-set size cap
POLITENESS_DELAY_S = 0.3

_CONTROL_CHARS = re.compile(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]")


# --------------------------------------------------------------------------- http

def http_get(url: str, headers: dict | None, cursor: dict, now_iso: str
             ) -> tuple[bytes | None, dict, str | None]:
    """Conditional GET. Returns (body|None, new_cursor, error|None); body None on 304."""
    new_cursor = dict(cursor)
    req_headers = {"User-Agent": USER_AGENT, "Accept-Encoding": "identity",
                   "Accept": "*/*"}
    req_headers.update(headers or {})
    if cursor.get("etag"):
        req_headers["If-None-Match"] = cursor["etag"]
    if cursor.get("last_modified"):
        req_headers["If-Modified-Since"] = cursor["last_modified"]
    req = request.Request(url, headers=req_headers)
    try:
        with request.urlopen(req, timeout=TIMEOUT_S) as resp:
            body = resp.read(MAX_BYTES)
            if resp.headers.get("ETag"):
                new_cursor["etag"] = resp.headers["ETag"]
            if resp.headers.get("Last-Modified"):
                new_cursor["last_modified"] = resp.headers["Last-Modified"]
            new_cursor["last_run"] = now_iso
            return body, new_cursor, None
    except error.HTTPError as exc:
        if exc.code == 304:
            new_cursor["last_run"] = now_iso
            return None, new_cursor, None
        return None, new_cursor, f"HTTP {exc.code}"
    except error.URLError as exc:
        return None, new_cursor, f"URL error: {exc.reason}"
    except (TimeoutError, OSError) as exc:
        return None, new_cursor, f"transport error: {exc}"


def decode(body: bytes) -> str:
    return body.decode("utf-8", errors="replace")


def make_item(title: str, url: str, published: datetime | None, summary: str = "",
              extra: dict | None = None) -> dict:
    item = {
        "title": title or "(untitled)",
        "url": url,
        "canonical_url": canonicalize_url(url),
        "published": published.isoformat() if published is not None else None,
        "summary": _clean_summary(summary),
    }
    if extra:
        item["extra"] = extra
    return item


# --------------------------------------------------------------------------- json adapters

def adapt_algolia(data: dict, src: dict, since: datetime) -> list[dict]:
    items = []
    for hit in data.get("hits", []):
        url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
        pub = _parse_date(hit.get("created_at"))
        items.append(make_item(
            hit.get("title", ""), url, pub, hit.get("story_text") or "",
            extra={"points": hit.get("points"), "comments": hit.get("num_comments"),
                   "hn_id": hit.get("objectID"),
                   "hn_url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}"}))
    return items


def adapt_lobsters(data: list, src: dict, since: datetime) -> list[dict]:
    drop_tags = set((src.get("filters") or {}).get("drop_tags", []))
    items = []
    for story in data:
        if drop_tags & set(story.get("tags", [])):
            continue
        pub = _parse_date(story.get("created_at"))
        if pub is not None and pub < since:
            continue
        items.append(make_item(
            story.get("title", ""), story.get("url") or story.get("comments_url", ""),
            pub, "", extra={"score": story.get("score"), "tags": story.get("tags"),
                            "comments_url": story.get("comments_url")}))
    return items


def adapt_hf_papers(data: list, src: dict, since: datetime) -> list[dict]:
    """Yesterday-lagged window (upvotes accrue over a day), optional github-repo
    requirement, then top-N by upvotes."""
    f = src.get("filters") or {}
    lag_since = since - timedelta(hours=24)
    rows = []
    for row in data:
        paper = row.get("paper") or {}
        pub = _parse_date(row.get("publishedAt") or paper.get("publishedAt"))
        if pub is not None and pub < lag_since:
            continue
        if f.get("require_github_repo") and not paper.get("githubRepo"):
            continue
        pid = paper.get("id", "")
        rows.append((paper.get("upvotes") or 0, make_item(
            paper.get("title") or row.get("title", ""),
            f"https://huggingface.co/papers/{pid}", pub,
            paper.get("summary", ""),
            extra={"upvotes": paper.get("upvotes"), "arxiv_id": pid,
                   "github_repo": paper.get("githubRepo")})))
    rows.sort(key=lambda r: r[0], reverse=True)
    top_n = f.get("top_n_by_upvotes", 3)
    return [item for _, item in rows[:top_n]]


def adapt_hf_trending(data: list, src: dict, since: datetime) -> list[dict]:
    """Leaderboard snapshot — caller diffs against the stored snapshot."""
    is_spaces = "/spaces" in src["url"]
    items = []
    for row in data:
        rid = row.get("id") or row.get("modelId", "")
        url = f"https://huggingface.co/{'spaces/' if is_spaces else ''}{rid}"
        items.append(make_item(
            rid, url, _parse_date(row.get("createdAt")), "",
            extra={"trending_score": row.get("trendingScore"), "likes": row.get("likes"),
                   "pipeline_tag": row.get("pipeline_tag"), "sdk": row.get("sdk")}))
    return items


def adapt_hf_org_models(data: list, src: dict, since: datetime) -> list[dict]:
    items = []
    for row in data:
        pub = _parse_date(row.get("createdAt"))
        if pub is not None and pub < since:
            continue
        rid = row.get("id") or row.get("modelId", "")
        items.append(make_item(
            f"New model: {rid}", f"https://huggingface.co/{rid}", pub, "",
            extra={"likes": row.get("likes"), "downloads": row.get("downloads"),
                   "tags": (row.get("tags") or [])[:8]}))
    return items


JSON_ADAPTERS = {
    "algolia": adapt_algolia,
    "lobsters": adapt_lobsters,
    "hf_papers": adapt_hf_papers,
    "hf_trending": adapt_hf_trending,
    "hf_org_models": adapt_hf_org_models,
}


# --------------------------------------------------------------------------- html adapters

def adapt_anthropic_engineering(text: str, src: dict) -> list[dict]:
    slugs = []
    for m in re.finditer(r'href="/engineering/([a-z0-9-]+)"', text):
        slug = m.group(1)
        if slug not in slugs:
            slugs.append(slug)
    return [make_item(slug.replace("-", " "),
                      f"https://www.anthropic.com/engineering/{slug}", None)
            for slug in slugs]


def adapt_baseten(text: str, src: dict) -> list[dict]:
    items = []
    seen = set()
    # titles live in <h3>/<h4> inside links to /blog/<slug>
    for m in re.finditer(
            r'href="(/blog/[a-z0-9-]+)"[^>]*>(?:(?!</a>).)*?<h[34][^>]*>(.*?)</h[34]>',
            text, re.S | re.I):
        path, raw_title = m.group(1), m.group(2)
        if path in seen:
            continue
        seen.add(path)
        title = re.sub(r"<[^>]+>", " ", raw_title)
        title = re.sub(r"\s+", " ", title).strip()
        if title:
            items.append(make_item(title, f"https://www.baseten.co{path}", None))
    return items


def adapt_lmsys_flight(text: str, src: dict) -> list[dict]:
    """Posts array is escaped JSON inside Next.js flight data in <script> tags:
    look for \"slug\" / \"title\" / \"date\" triples (order varies; match pairwise)."""
    items = []
    seen = set()
    # the flight payload escapes quotes as \" — normalize both forms
    hay = text.replace('\\"', '"')
    for m in re.finditer(
            r'"slug"\s*:\s*"([a-z0-9-]+)"[^{}]*?"title"\s*:\s*"([^"]+)"(?:[^{}]*?"date"\s*:\s*"([^"]+)")?',
            hay):
        slug, title, date_raw = m.group(1), m.group(2), m.group(3)
        if slug in seen:
            continue
        seen.add(slug)
        items.append(make_item(title, f"https://lmsys.org/blog/{slug}",
                               _parse_date(date_raw)))
    return items


def adapt_page_hash(text: str, src: dict) -> list[dict]:
    """Change detector: emit one item whose 'url-key' is the content hash. The
    seen-set turns this into 'fire once per change'."""
    visible = re.sub(r"<script.*?</script>", " ", text, flags=re.S)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"\s+", " ", visible).strip()
    digest = hashlib.sha256(visible.encode()).hexdigest()[:16]
    return [make_item(f"{src['name']}: page updated", f"{src['url']}#rev-{digest}", None,
                      extra={"content_hash": digest, "real_url": src["url"]})]


HTML_ADAPTERS = {
    "anthropic_engineering": adapt_anthropic_engineering,
    "baseten": adapt_baseten,
    "lmsys_flight": adapt_lmsys_flight,
    "page_hash": adapt_page_hash,
}


# --------------------------------------------------------------------------- git tags

_RC_TAG = re.compile(r"(rc\d*|alpha|beta|dev)\d*$", re.I)


def fetch_git_tags(src: dict, state: dict) -> tuple[list[dict], str | None]:
    """`git ls-remote --tags` via the git proxy; new-vs-seen diff (ls-remote order is
    lexical, so 'new' means 'never seen', not 'last in list')."""
    repo = src["url"]
    try:
        proc = subprocess.run(
            ["git", "ls-remote", "--tags", repo],
            capture_output=True, text=True, timeout=60, check=False)
    except (subprocess.TimeoutExpired, OSError) as exc:
        return [], f"git ls-remote failed: {exc}"
    if proc.returncode != 0:
        return [], f"git ls-remote exit {proc.returncode}: {proc.stderr.strip()[:200]}"
    tags = []
    for line in proc.stdout.splitlines():
        parts = line.split("refs/tags/", 1)
        if len(parts) != 2:
            continue
        tag = parts[1].strip()
        if tag.endswith("^{}"):
            continue
        tags.append(tag)
    if not tags:
        return [], "no tags returned"
    drop_rc = (src.get("filters") or {}).get("drop_rc", False)
    seen = set(state.get("seen", []))
    first_run = not seen
    fresh = []
    for tag in tags:
        if tag in seen:
            continue
        seen.add(tag)
        if first_run:
            continue  # first run seeds the seen-set silently — no fake backlog
        if drop_rc and _RC_TAG.search(tag):
            continue
        repo_name = repo.rstrip("/").rsplit("/", 1)[-1]
        fresh.append(make_item(f"{repo_name} release {tag}",
                               f"{repo}/releases/tag/{tag}", None,
                               extra={"tag": tag}))
    state["seen"] = sorted(seen)[-SEEN_CAP:]
    return fresh, None


# --------------------------------------------------------------------------- core

def apply_common_filters(items: list[dict], src: dict) -> list[dict]:
    f = src.get("filters") or {}
    for pattern in f.get("drop_title_re", []):
        rx = re.compile(pattern)
        items = [i for i in items if not rx.search(i["title"])]
    max_items = f.get("max_items")
    if max_items:
        # newest first when dates exist; undated items keep their source order
        items = sorted(items, key=lambda i: i["published"] or "", reverse=True)[:max_items]
    return items


def seen_dedup(items: list[dict], state: dict) -> list[dict]:
    """First run seeds the seen-set silently — an archive/backlog is not news."""
    seen = state.get("seen", [])
    first_run = not seen
    seen_set = set(seen)
    fresh = [i for i in items if i["canonical_url"] not in seen_set]
    for i in fresh:
        seen.append(i["canonical_url"])
    state["seen"] = seen[-SEEN_CAP:]
    return [] if first_run else fresh


def snapshot_diff(items: list[dict], state: dict) -> list[dict]:
    prev = set(state.get("snapshot", []))
    current = [i["canonical_url"] for i in items]
    fresh = [i for i in items if i["canonical_url"] not in prev] if prev else []
    state["snapshot"] = current
    return fresh


def window_filter(items: list[dict], since: datetime) -> list[dict]:
    out = []
    for i in items:
        pub = _parse_date(i["published"]) if i["published"] else None
        if pub is not None and pub < since:
            continue
        out.append(i)
    return out


def process_source(src: dict, state: dict, since: datetime, now_iso: str
                   ) -> tuple[list[dict], list[str]]:
    kind = src["kind"]
    errors: list[str] = []

    if kind == "git-tags":
        items, err = fetch_git_tags(src, state)
        if err:
            errors.append(err)
        return items, errors

    url = src["url"]
    if "{since_epoch}" in url:
        # 2-day lookback so late-rising HN posts clear the points threshold
        url = url.replace("{since_epoch}", str(int(since.timestamp()) - 86400))

    body, new_http, err = http_get(url, src.get("headers"), state.get("http", {}), now_iso)
    state["http"] = new_http
    if err:
        errors.append(err)
        return [], errors
    if body is None:  # 304
        return [], errors

    if kind == "rss":
        text = decode(_CONTROL_CHARS.sub(b"", body))
        if not looks_like_feed(text):
            errors.append("TRAP/not-a-feed")
            return [], errors
        try:
            entries = parse_feed_xml(text)
        except ET.ParseError as exc:
            errors.append(f"XML parse error: {exc}")
            return [], errors
        items = [make_item(e["title"], e["url"], e["published"], e["summary"])
                 for e in entries]
        items = window_filter(items, since)
    elif kind == "json":
        try:
            data = json.loads(body)
        except json.JSONDecodeError as exc:
            errors.append(f"JSON parse error (HTML trap?): {exc}")
            return [], errors
        adapter = JSON_ADAPTERS.get(src.get("adapter", ""))
        if adapter is None:
            errors.append(f"unknown json adapter: {src.get('adapter')}")
            return [], errors
        items = adapter(data, src, since)
    elif kind == "html":
        adapter = HTML_ADAPTERS.get(src.get("adapter", ""))
        if adapter is None:
            errors.append(f"unknown html adapter: {src.get('adapter')}")
            return [], errors
        items = adapter(decode(body), src)
    else:
        errors.append(f"unknown kind: {kind}")
        return [], errors

    items = apply_common_filters(items, src)

    st = src.get("state") or {}
    if st.get("snapshot_diff"):
        items = snapshot_diff(items, state)
    elif st.get("seen_dedup"):
        items = seen_dedup(items, state)

    return items, errors


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Technical-radar fetcher (stdlib only)")
    ap.add_argument("--since", help="ISO8601 window start")
    ap.add_argument("--source", help="process only this source id")
    ap.add_argument("--no-save-state", action="store_true")
    args = ap.parse_args(argv)

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    args_since = _parse_date(args.since) if args.since else None
    if args.since and args_since is None:
        log(f"error: --since is not valid ISO8601: {args.since!r}")
        return 2

    try:
        with CONFIG_PATH.open(encoding="utf-8") as fh:
            config = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        log(f"error: config unreadable at {CONFIG_PATH}: {exc}")
        return 2

    try:
        with STATE_PATH.open(encoding="utf-8") as fh:
            all_state = json.load(fh)
    except (OSError, json.JSONDecodeError):
        all_state = {}

    sources = [s for s in config.get("sources", []) if s.get("enabled", True)]
    if args.source:
        sources = [s for s in sources if s["id"] == args.source]

    default_since = args_since or (now - timedelta(hours=DEFAULT_WINDOW_HOURS))
    result = {"generated_at": now_iso, "window_since": default_since.isoformat(),
              "sources": {}}

    for src in sources:
        sid = src["id"]
        state = all_state.setdefault(sid, {})
        last_run = _parse_date((state.get("http") or {}).get("last_run") or state.get("last_run"))
        since = args_since or last_run or default_since
        try:
            items, errors = process_source(src, state, since, now_iso)
        except Exception as exc:  # a broken source must never kill the run
            items, errors = [], [f"{type(exc).__name__}: {exc}"]
        state["last_run"] = now_iso
        for e in errors:
            log(f"[{sid}] {e}")
        for i in items:
            i["source_id"] = sid
        result["sources"][sid] = {"category": src["category"], "fresh": items,
                                  "errors": [{"source_url": src["url"], "error": e}
                                             for e in errors]}
        time.sleep(POLITENESS_DELAY_S)

    if not args.no_save_state:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with STATE_PATH.open("w", encoding="utf-8") as fh:
            json.dump(all_state, fh, indent=2, sort_keys=True)
            fh.write("\n")

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
