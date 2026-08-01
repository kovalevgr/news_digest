#!/usr/bin/env python3
"""Validate config.yaml against the authoritative shape (the file's own header is the spec).

Usage:
  validate_config.py [path]   # validate a config file (default: ./config.yaml)
  validate_config.py --hook   # PostToolUse hook mode: reads the tool-call JSON on stdin
                              # and validates only if the edited file is THIS project's config.yaml

Exit codes: 0 = ok / skipped; 1 = failed (CLI); 2 = failed (hook mode -> blocking error).
"""
import json
import re
import sys
from pathlib import Path

HOOK = "--hook" in sys.argv
PROJECT_ROOT = Path(__file__).resolve().parents[3]  # .claude/skills/config-edit/ -> project root

try:
    import yaml
except ImportError:
    # Never hard-block edits just because the env lacks PyYAML.
    print("validate_config: PyYAML missing (pip install pyyaml) - validation skipped", file=sys.stderr)
    sys.exit(0)

CADENCE = re.compile(r"^(\d+)[hd]$")
DIGEST_WINDOW = re.compile(r"^(\d+)d$")
SCHEDULE = re.compile(r"^(mon|tue|wed|thu|fri|sat|sun) (\d{1,2}):(\d{2})$")
BRIEF_SCHEDULE = re.compile(r"^(\d{1,2}):(\d{2})$")  # daily wall-clock time, no day-of-week
URL_CREDS = re.compile(r"://[^/@\s]+:[^/@\s]+@")  # user:pass@ embedded in a URL
REDDIT_WINDOWS = {"hour", "day", "week", "month", "year"}
SECRET_KEY_HINTS = ("token", "secret", "password", "api_key", "apikey", "bearer")

SOURCE_TYPES = {
    "x_user":     {"required": {"handle"}, "optional": set()},
    "github":     {"required": {"user"}, "optional": set()},
    "rss":        {"required": {"url"}, "optional": set()},
    "reddit_sub": {"required": {"id", "listing"}, "optional": {"window"}},
    "hn":         {"required": {"listing"}, "optional": {"min_points", "match"}},
    "arxiv":      {"required": {"category"}, "optional": set()},
}
LISTINGS = {"reddit_sub": {"top", "hot", "new"}, "hn": {"best", "top", "new"}}
# Required identity fields must be non-empty strings (hn.listing checked via LISTINGS).
STRING_FIELDS = {"handle", "user", "url", "id", "category", "listing"}


def is_pos_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v > 0


def bad_cadence(v):
    m = CADENCE.match(str(v))
    return m is None or int(m.group(1)) < 1


def check_source(src, where, errors, in_people):
    if not isinstance(src, dict):
        errors.append(f"{where}: source must be a mapping")
        return
    for key, val in src.items():
        if any(h in str(key).lower() for h in SECRET_KEY_HINTS):
            errors.append(f"{where}: key {key!r} looks like a secret - secrets never go in config.yaml (env only)")
        if isinstance(val, str) and URL_CREDS.search(val):
            errors.append(f"{where}: {key} embeds credentials in a URL - secrets never go in config.yaml (env only)")
    t = src.get("type")
    if t not in SOURCE_TYPES:
        errors.append(f"{where}: unknown source type {t!r} - allowed: {sorted(SOURCE_TYPES)} (do not invent new types)")
        return
    spec = SOURCE_TYPES[t]
    fields = set(src) - {"type", "cadence"}
    missing = spec["required"] - fields
    extra = fields - spec["required"] - spec["optional"]
    if missing:
        errors.append(f"{where}: {t} missing required field(s): {sorted(missing)}")
    if extra:
        errors.append(f"{where}: {t} has unknown field(s): {sorted(extra)} (do not invent new fields)")
    for fld in spec["required"]:
        if fld in src and fld in STRING_FIELDS and (not isinstance(src[fld], str) or not src[fld].strip()):
            errors.append(f"{where}: {t}.{fld} must be a non-empty string, got {src[fld]!r}")
    if t in LISTINGS and isinstance(src.get("listing"), str) and src["listing"] not in LISTINGS[t]:
        errors.append(f"{where}: {t}.listing must be one of {sorted(LISTINGS[t])}, got {src['listing']!r}")
    if t == "reddit_sub" and "window" in src and str(src["window"]) not in REDDIT_WINDOWS:
        errors.append(f"{where}: reddit_sub.window must be one of {sorted(REDDIT_WINDOWS)}")
    if t == "hn" and "min_points" in src and not is_pos_int(src["min_points"]):
        errors.append(f"{where}: hn.min_points must be a positive int")
    if t == "hn" and "match" in src and not (
        isinstance(src["match"], list) and src["match"] and all(isinstance(m, str) and m for m in src["match"])
    ):
        errors.append(f"{where}: hn.match must be a non-empty list of strings")
    if "cadence" in src and bad_cadence(src["cadence"]):
        errors.append(f"{where}: cadence must look like 6h / 12h / 1d / 2d (positive), got {src['cadence']!r}")
    if t == "x_user" and not in_people:
        errors.append(f"{where}: x_user under topics - X is people-only in v1 (move it under people)")


def check_digest(dg, where, errors):
    if not isinstance(dg, dict):
        errors.append(f"{where} must be a mapping")
        return
    extra = set(dg) - {"schedule", "window", "top_n"}
    if extra:
        errors.append(f"{where}: unknown key(s): {sorted(extra)}")
    missing = {"schedule", "window", "top_n"} - set(dg)
    if missing:
        errors.append(f"{where} missing: {sorted(missing)}")
    if "schedule" in dg:
        m = SCHEDULE.match(str(dg["schedule"]))
        if not m or int(m.group(2)) > 23 or int(m.group(3)) > 59:
            errors.append(f"{where}.schedule must look like 'sun 09:00', got {dg['schedule']!r}")
    if "window" in dg:
        m = DIGEST_WINDOW.match(str(dg["window"]))
        if not m or int(m.group(1)) < 1:
            errors.append(f"{where}.window must look like 7d / 14d, got {dg['window']!r}")
    if "top_n" in dg and not is_pos_int(dg["top_n"]):
        errors.append(f"{where}.top_n must be a positive int")


def check_brief(brief, where, errors):
    """Validate the top-level `brief:` block (the morning roundup). Mirrors check_digest.

    Shape: exactly {schedule, window, top_n}. `schedule` is a daily wall-clock `HH:MM` (no
    day-of-week); `window` is a cadence string (`Nh`/`Nd`, positive — this file has no
    parse_cadence, so we reuse the CADENCE regex); `top_n` is a positive int."""
    if not isinstance(brief, dict):
        errors.append(f"{where} must be a mapping")
        return
    extra = set(brief) - {"schedule", "window", "top_n"}
    if extra:
        errors.append(f"{where}: unknown key(s): {sorted(extra)}")
    missing = {"schedule", "window", "top_n"} - set(brief)
    if missing:
        errors.append(f"{where} missing: {sorted(missing)}")
    if "schedule" in brief:
        m = BRIEF_SCHEDULE.match(str(brief["schedule"]))
        if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
            errors.append(f"{where}.schedule must look like '08:00', got {brief['schedule']!r}")
    if "window" in brief and bad_cadence(brief["window"]):
        errors.append(f"{where}.window must look like 6h / 12h / 1d / 2d (positive), got {brief['window']!r}")
    if "top_n" in brief and not is_pos_int(brief["top_n"]):
        errors.append(f"{where}.top_n must be a positive int")


def validate(path):
    errors = []
    data = yaml.safe_load(Path(path).read_text())
    if not isinstance(data, dict):
        return ["top level must be a mapping with keys: defaults, people, topics"]

    extra_top = set(data) - {"defaults", "people", "topics", "brief"}
    if extra_top:
        errors.append(f"unknown top-level key(s): {sorted(extra_top)}")

    d = data.get("defaults")
    if not isinstance(d, dict) or "cadence" not in d:
        errors.append("defaults.cadence is required")
    else:
        if bad_cadence(d["cadence"]):
            errors.append(f"defaults.cadence must look like 1d / 12h (positive), got {d['cadence']!r}")
        extra = set(d) - {"cadence"}
        if extra:
            errors.append(f"defaults: unknown key(s): {sorted(extra)}")

    people = data.get("people") or []  # absent or bare `people:` == empty
    if not isinstance(people, list):
        errors.append("people must be a list")
    else:
        for i, p in enumerate(people):
            if not isinstance(p, dict):
                errors.append(f"people[{i}]: must be a mapping")
                continue
            label = p.get("name") if isinstance(p.get("name"), str) else f"#{i}"
            where = f"people[{label}]"
            if not isinstance(p.get("name"), str) or not p.get("name", "").strip():
                errors.append(f"{where}: name is required and must be a non-empty string")
            extra = set(p) - {"name", "cadence", "sources"}
            if extra:
                errors.append(f"{where}: unknown key(s): {sorted(extra)}")
            if "cadence" in p and bad_cadence(p["cadence"]):
                errors.append(f"{where}: cadence must look like 1d / 2d (positive), got {p['cadence']!r}")
            srcs = p.get("sources")
            if not isinstance(srcs, list) or not srcs:
                errors.append(f"{where}: sources must be a non-empty list")
            else:
                for j, s in enumerate(srcs):
                    check_source(s, f"{where}.sources[{j}]", errors, in_people=True)

    topics = data.get("topics") or {}  # absent or bare `topics:` == empty
    if not isinstance(topics, dict):
        errors.append("topics must be a mapping of topic-name -> {sources, digest?}")
    else:
        for name, t in topics.items():
            where = f"topics.{name}"
            if not isinstance(name, str) or not name.strip():
                errors.append(f"{where}: topic name must be a non-empty string")
            if not isinstance(t, dict):
                errors.append(f"{where}: must be a mapping")
                continue
            extra = set(t) - {"sources", "digest"}
            if extra:
                errors.append(f"{where}: unknown key(s): {sorted(extra)}")
            srcs = t.get("sources")
            if not isinstance(srcs, list) or not srcs:
                errors.append(f"{where}: sources must be a non-empty list")
            else:
                for j, s in enumerate(srcs):
                    check_source(s, f"{where}.sources[{j}]", errors, in_people=False)
            if t.get("digest") is not None:
                check_digest(t["digest"], f"{where}.digest", errors)

    if data.get("brief") is not None:  # the top-level morning roundup (optional)
        check_brief(data["brief"], "brief", errors)

    return errors


def main():
    if HOOK:
        try:
            payload = json.load(sys.stdin)
        except Exception:
            sys.exit(0)
        file_path = (payload.get("tool_input") or {}).get("file_path", "")
        if not file_path or Path(file_path).name != "config.yaml":
            sys.exit(0)
        try:
            target = Path(file_path).resolve()
        except OSError:
            sys.exit(0)
        if target != (PROJECT_ROOT / "config.yaml").resolve():
            sys.exit(0)  # some other project's config.yaml - not ours to judge
    else:
        flags = [a for a in sys.argv[1:] if a.startswith("-") and a != "--hook"]
        if flags:
            print(f"validate_config: unknown flag(s) {flags}; usage: validate_config.py [path] | --hook", file=sys.stderr)
            sys.exit(1)
        args = [a for a in sys.argv[1:] if not a.startswith("-")]
        target = Path(args[0] if args else "config.yaml")

    try:
        errors = validate(target)
    except FileNotFoundError:
        print(f"validate_config: {target} not found", file=sys.stderr)
        sys.exit(0 if HOOK else 1)
    except yaml.YAMLError as e:
        errors = [f"YAML parse error: {e}"]
    except Exception as e:  # unreadable file, directory, encoding, ...
        errors = [f"cannot read/parse {target}: {e.__class__.__name__}: {e}"]

    if errors:
        print(f"config.yaml validation FAILED ({len(errors)} error(s)):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(2 if HOOK else 1)
    print(f"{target}: OK")


if __name__ == "__main__":
    main()
