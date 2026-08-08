#!/usr/bin/env python3
"""Connectivity test for radar candidate sources (stdlib-only).

Fetches every source in news/config/radar-candidates.json and validates that the
response is genuinely what the pipeline expects (parseable feed XML / JSON with
items / HTML containing the expected marker) — not a 200-with-HTML trap.

Usage:
    python3 news/scripts/test_sources.py --label local
    python3 news/scripts/test_sources.py --label cloud --only reddit-multireddit,netflix

Writes news/research/connectivity/<date>-<label>.json and .md. Always exits 0 —
the report is the artifact; failures belong in it, not in the exit code.
"""

import argparse
import datetime
import gzip
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # news/
CONFIG = ROOT / "config" / "radar-candidates.json"
OUT_DIR = ROOT / "research" / "connectivity"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
TIMEOUT = 20
MAX_BYTES = 8 * 1024 * 1024
DELAY = 0.5  # politeness between requests


def fetch(url, headers):
    req_headers = {"User-Agent": UA, "Accept-Encoding": "identity"}
    req_headers.update(headers or {})
    # GitHub blocks anonymous datacenter IPs; a token lifts that (and raises API limits)
    host = urllib.parse.urlsplit(url).hostname or ""
    token = os.environ.get("GITHUB_TOKEN")
    if token and host in ("github.com", "api.github.com"):
        req_headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=req_headers)
    start = time.time()
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        body = resp.read(MAX_BYTES)
        elapsed = time.time() - start
        if body[:2] == b"\x1f\x8b":  # server ignored Accept-Encoding
            body = gzip.GzipFile(fileobj=io.BytesIO(body)).read(MAX_BYTES)
        return resp.status, resp.headers.get("Content-Type", ""), body, elapsed


def validate_rss(body):
    # stdlib-only sandbox forbids defusedxml; ET won't expand external entities,
    # and refusing ENTITY declarations outright blocks billion-laughs inputs.
    if b"<!ENTITY" in body:
        raise ValueError("XML contains ENTITY declarations — refusing to parse")
    # some feeds embed raw terminal output with control chars, illegal in XML 1.0
    # (seen live: answer.ai's pip-spinner output) — strip before parsing
    body = bytes(b for b in body if b >= 0x20 or b in (0x09, 0x0A, 0x0D))
    root = ET.fromstring(body)
    items = [e for e in root.iter() if e.tag.split("}")[-1] in ("item", "entry")]
    title = ""
    for it in items[:1]:
        for child in it:
            if child.tag.split("}")[-1] == "title":
                title = (child.text or "").strip()[:100]
                break
    return len(items), title


def validate_api(body):
    data = json.loads(body)
    if isinstance(data, list):
        return len(data), ""
    if isinstance(data, dict):
        for key in ("hits", "items", "papers"):
            if isinstance(data.get(key), list):
                return len(data[key]), ""
        return len(data), ""
    return 0, ""


def test_source(src):
    result = {"id": src["id"], "category": src["category"], "url": src["url"],
              "method": src["method"], "ok": False, "status": None, "items": None,
              "size": None, "ms": None, "error": None, "detail": ""}
    try:
        status, ctype, body, elapsed = fetch(src["url"], src.get("headers"))
        result.update(status=status, size=len(body), ms=int(elapsed * 1000))
        if src["method"] in ("rss",):
            try:
                count, title = validate_rss(body)
            except ET.ParseError:
                if len(body) < MAX_BYTES:
                    raise
                # feed bigger than the cap, truncated mid-entity — count raw tags
                count = body.count(b"<item") + body.count(b"<entry")
                title = f"truncated at {MAX_BYTES} cap; raw tag count"
            result["items"] = count
            result["detail"] = title
            result["ok"] = count > 0
            if count == 0:
                result["error"] = "parsed as XML but zero item/entry elements"
        elif src["method"] == "api":
            count, _ = validate_api(body)
            result["items"] = count
            result["ok"] = count > 0
            if count == 0:
                result["error"] = "valid JSON but zero items"
        else:  # fetch
            text = body.decode("utf-8", errors="replace")
            marker = src.get("expect", "")
            if marker and marker in text:
                result["ok"] = True
                result["detail"] = f"marker '{marker}' present"
            else:
                result["error"] = f"HTTP {status} but marker '{marker}' NOT in body (trap?)"
    except urllib.error.HTTPError as e:
        result["status"] = e.code
        try:
            snippet = " ".join(e.read(500).decode("utf-8", errors="replace").split())[:200]
        except Exception:
            snippet = ""
        rl = e.headers.get("x-ratelimit-limit") if e.headers else None
        rr = e.headers.get("x-ratelimit-remaining") if e.headers else None
        extra = f" [ratelimit {rr}/{rl}]" if rl else ""
        result["error"] = f"HTTP {e.code} {e.reason}{extra} :: {snippet}"
    except urllib.error.URLError as e:
        # DNS failure / connection refused usually means the env allowlist blocks the domain
        result["error"] = f"connection failed (allowlist?): {e.reason}"
    except TimeoutError:
        result["error"] = "timeout"
    except ET.ParseError as e:
        result["error"] = f"not parseable XML (HTML trap?): {e}"
        result["ok"] = False
    except json.JSONDecodeError as e:
        result["error"] = f"not parseable JSON (HTML trap?): {e}"
    except Exception as e:  # keep going — the report must cover every source
        result["error"] = f"{type(e).__name__}: {e}"
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="local", help="environment label for the report filename")
    ap.add_argument("--only", default="", help="comma-separated source ids to test (default: all)")
    args = ap.parse_args()

    sources = json.loads(CONFIG.read_text())["sources"]
    if args.only:
        wanted = set(args.only.split(","))
        sources = [s for s in sources if s["id"] in wanted]

    results = []
    for src in sources:
        r = test_source(src)
        results.append(r)
        mark = "OK " if r["ok"] else "FAIL"
        print(f"[{mark}] {r['id']:26s} status={r['status']} items={r['items']} "
              f"{r['error'] or r['detail']}", flush=True)
        time.sleep(DELAY)

    date = datetime.date.today().isoformat()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = {"date": date, "label": args.label, "total": len(results),
              "passed": sum(1 for r in results if r["ok"]), "results": results}
    (OUT_DIR / f"{date}-{args.label}.json").write_text(json.dumps(report, indent=2))

    lines = [f"# Source connectivity report — {date} ({args.label})", "",
             f"{report['passed']}/{report['total']} sources OK.", "",
             "| id | ok | status | items | ms | error |",
             "| --- | --- | --- | --- | --- | --- |"]
    for r in results:
        lines.append(f"| {r['id']} | {'✅' if r['ok'] else '❌'} | {r['status']} "
                     f"| {r['items'] if r['items'] is not None else ''} | {r['ms'] or ''} "
                     f"| {r['error'] or ''} |")
    fails = [r for r in results if not r["ok"]]
    if fails:
        lines += ["", "## Failures", ""]
        for r in fails:
            lines.append(f"- **{r['id']}** ({r['url']}): {r['error']}")
    (OUT_DIR / f"{date}-{args.label}.md").write_text("\n".join(lines) + "\n")
    print(f"\n{report['passed']}/{report['total']} OK → {OUT_DIR / f'{date}-{args.label}.md'}")


if __name__ == "__main__":
    main()
