"""Runtime loader + validator for config.yaml (the authoritative sources config).

Parses the authoritative shape (source types x_user / github / rss / reddit_sub /
hn / arxiv), applies the cadence cascade (source -> person -> defaults), and derives
the stable per-source `source_key` used for cursors and sightings. Validation mirrors
the authoritative header in config.yaml; on any divergence, config.yaml wins.

Dependency-light on purpose (PyYAML + stdlib) so it is unit-testable without the DB.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

CADENCE_RE = re.compile(r"^(\d+)([hd])$")
DIGEST_WINDOW_RE = re.compile(r"^(\d+)d$")
SCHEDULE_RE = re.compile(r"^(mon|tue|wed|thu|fri|sat|sun) (\d{1,2}):(\d{2})$")
BRIEF_SCHEDULE_RE = re.compile(r"^(\d{1,2}):(\d{2})$")  # daily wall-clock time, no day-of-week
SECRET_KEY_HINTS = ("token", "secret", "password", "api_key", "apikey", "bearer")
URL_CREDS_RE = re.compile(r"://[^/@\s]+:[^/@\s]+@")  # user:pass@ embedded in a URL

SOURCE_TYPES = {
    "x_user": {"required": {"handle"}, "optional": set()},
    "github": {"required": {"user"}, "optional": set()},
    "rss": {"required": {"url"}, "optional": set()},
    "reddit_sub": {"required": {"id", "listing"}, "optional": {"window"}},
    "hn": {"required": {"listing"}, "optional": {"min_points", "match"}},
    "arxiv": {"required": {"category"}, "optional": set()},
}
LISTINGS = {"reddit_sub": {"top", "hot", "new"}, "hn": {"best", "top", "new"}}
REDDIT_WINDOWS = {"hour", "day", "week", "month", "year"}
STRING_FIELDS = {"handle", "user", "url", "id", "category", "listing"}

DEFAULT_CONFIG_PATH = os.environ.get("CONFIG_PATH", "config.yaml")


class ConfigError(ValueError):
    """Raised when config.yaml does not match the authoritative shape."""


def parse_cadence(value) -> int:
    """Cadence string (e.g. '6h', '1d') -> seconds. Raises ConfigError if malformed."""
    m = CADENCE_RE.match(str(value))
    if not m or int(m.group(1)) < 1:
        raise ConfigError(f"bad cadence {value!r} (expected like 6h / 12h / 1d / 2d)")
    n = int(m.group(1))
    return n * 3600 if m.group(2) == "h" else n * 86400


def _is_pos_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and v > 0


def derive_source_key(type_: str, identity: dict) -> str:
    """`<type>:` + stable serialization of identity fields (everything but cadence/type).
    Deterministic across runs; two same-type sources differing only in params get
    distinct keys, and tuning cadence keeps the key."""
    body = json.dumps(identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return f"{type_}:{body}"


@dataclass
class Source:
    type: str
    identity: dict            # fields defining the source (no type, no cadence)
    cadence_s: int
    owner: str                # "person:<name>" or "topic:<name>"
    source_key: str


@dataclass
class Digest:
    schedule: str
    window_days: int
    top_n: int


@dataclass
class Brief:
    schedule: str   # the raw HH:MM wall-clock time the morning brief fires at
    window_s: int   # how far back the roundup looks (window cadence -> seconds)
    top_n: int      # max stories in one morning roundup


@dataclass
class Config:
    default_cadence_s: int
    sources: list = field(default_factory=list)
    digests: dict = field(default_factory=dict)   # topic name -> Digest
    brief: Brief | None = None                    # the morning-brief roundup, or None if absent
    raw: dict = field(default_factory=dict)

    def source_by_key(self, key: str):
        for s in self.sources:
            if s.source_key == key:
                return s
        return None


def _scan_secrets(node, path: str, errors: list[str]) -> None:
    """Recursively reject secret-looking keys and credential-bearing URL strings ANYWHERE in
    the document (rule 3: secrets live in env, never in config.yaml). Walks mappings AND lists,
    so a secret hidden in a list element (e.g. an hn `match` entry) is caught too — not just the
    top-level keys of a source mapping. Run once over the whole loaded YAML before structural
    validation, so the guard is structure-independent."""
    if isinstance(node, dict):
        for k, v in node.items():
            ks = str(k)
            here = f"{path}.{ks}" if path else ks
            if any(h in ks.lower() for h in SECRET_KEY_HINTS):
                errors.append(f"{here}: key {ks!r} looks like a secret — secrets live in env, not config.yaml")
            _scan_secrets(v, here, errors)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _scan_secrets(v, f"{path}[{i}]", errors)
    elif isinstance(node, str):
        if URL_CREDS_RE.search(node):
            errors.append(f"{path or '<root>'}: embeds credentials in a URL — secrets live in env, not config.yaml")


def _check_source(raw_src, where, errors, in_people):
    if not isinstance(raw_src, dict):
        errors.append(f"{where}: source must be a mapping")
        return None
    t = raw_src.get("type")
    if t not in SOURCE_TYPES:
        errors.append(f"{where}: unknown source type {t!r} — allowed: {sorted(SOURCE_TYPES)}")
        return None
    spec = SOURCE_TYPES[t]
    fields_present = set(raw_src) - {"type", "cadence"}
    missing = spec["required"] - fields_present
    extra = fields_present - spec["required"] - spec["optional"]
    if missing:
        errors.append(f"{where}: {t} missing required field(s): {sorted(missing)}")
    if extra:
        errors.append(f"{where}: {t} has unknown field(s): {sorted(extra)}")
    for fld in spec["required"]:
        if fld in raw_src and fld in STRING_FIELDS and (
            not isinstance(raw_src[fld], str) or not raw_src[fld].strip()
        ):
            errors.append(f"{where}: {t}.{fld} must be a non-empty string, got {raw_src[fld]!r}")
    if t in LISTINGS and isinstance(raw_src.get("listing"), str) and raw_src["listing"] not in LISTINGS[t]:
        errors.append(f"{where}: {t}.listing must be one of {sorted(LISTINGS[t])}, got {raw_src['listing']!r}")
    if t == "reddit_sub" and "window" in raw_src and str(raw_src["window"]) not in REDDIT_WINDOWS:
        errors.append(f"{where}: reddit_sub.window must be one of {sorted(REDDIT_WINDOWS)}")
    if t == "hn" and "min_points" in raw_src and not _is_pos_int(raw_src["min_points"]):
        errors.append(f"{where}: hn.min_points must be a positive int")
    if t == "hn" and "match" in raw_src and not (
        isinstance(raw_src["match"], list) and raw_src["match"]
        and all(isinstance(m, str) and m for m in raw_src["match"])
    ):
        errors.append(f"{where}: hn.match must be a non-empty list of strings")
    if "cadence" in raw_src:
        try:
            parse_cadence(raw_src["cadence"])
        except ConfigError as e:
            errors.append(f"{where}: {e}")
    if t == "x_user" and not in_people:
        errors.append(f"{where}: x_user under topics — X is people-only in v1 (move it under people)")
    return t


def _check_digest(raw, where, errors) -> Digest | None:
    if not isinstance(raw, dict):
        errors.append(f"{where} must be a mapping")
        return None
    extra = set(raw) - {"schedule", "window", "top_n"}
    missing = {"schedule", "window", "top_n"} - set(raw)
    if extra:
        errors.append(f"{where}: unknown key(s): {sorted(extra)}")
    if missing:
        errors.append(f"{where} missing: {sorted(missing)}")
    sched = str(raw.get("schedule", ""))
    m = SCHEDULE_RE.match(sched)
    if not m or int(m.group(2)) > 23 or int(m.group(3)) > 59:
        errors.append(f"{where}.schedule must look like 'sun 09:00', got {raw.get('schedule')!r}")
    wm = DIGEST_WINDOW_RE.match(str(raw.get("window", "")))
    if not wm or int(wm.group(1)) < 1:
        errors.append(f"{where}.window must look like 7d / 14d, got {raw.get('window')!r}")
    if not _is_pos_int(raw.get("top_n")):
        errors.append(f"{where}.top_n must be a positive int")
    if missing or extra or not m or not wm or not _is_pos_int(raw.get("top_n")):
        return None
    return Digest(schedule=sched, window_days=int(wm.group(1)), top_n=int(raw["top_n"]))


def _check_brief(raw, where, errors) -> Brief | None:
    """Validate the top-level `brief:` block (the morning roundup). Mirrors _check_digest.

    Shape: exactly {schedule, window, top_n}. `schedule` is a daily wall-clock `HH:MM` (no
    day-of-week — the brief fires every day); `window` is a cadence string (`Nh`/`Nd`, parsed via
    parse_cadence into seconds); `top_n` is a positive int. Returns a Brief only if fully valid,
    else None (errors accumulated)."""
    if not isinstance(raw, dict):
        errors.append(f"{where} must be a mapping")
        return None
    extra = set(raw) - {"schedule", "window", "top_n"}
    missing = {"schedule", "window", "top_n"} - set(raw)
    if extra:
        errors.append(f"{where}: unknown key(s): {sorted(extra)}")
    if missing:
        errors.append(f"{where} missing: {sorted(missing)}")
    sched = str(raw.get("schedule", ""))
    m = BRIEF_SCHEDULE_RE.match(sched)
    if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
        errors.append(f"{where}.schedule must look like '08:00', got {raw.get('schedule')!r}")
    window_s = None
    try:
        window_s = parse_cadence(raw["window"]) if "window" in raw else None
    except ConfigError as e:
        errors.append(f"{where}.window: {e}")
    if not _is_pos_int(raw.get("top_n")):
        errors.append(f"{where}.top_n must be a positive int")
    if missing or extra or not m or window_s is None or not _is_pos_int(raw.get("top_n")):
        return None
    return Brief(schedule=sched, window_s=window_s, top_n=int(raw["top_n"]))


def parse_brief_schedule(schedule: str) -> dict:
    """Parse a `brief.schedule` ("08:00") into APScheduler CronTrigger kwargs.

    PURE — no DB, no network. Returns `{"hour": H, "minute": M}` (ints); NO day_of_week key, so a
    CronTrigger built from it fires every day at that wall-clock time. Tolerant of a single-digit
    hour ("8:05" -> hour 8, minute 5) and surrounding whitespace. config.yaml already validates the
    shape (BRIEF_SCHEDULE_RE + range checks), so this is a defensive guard, not the primary
    validator: it raises ConfigError on a clearly malformed string rather than handing APScheduler
    garbage (mirrors parse_digest_schedule's posture)."""
    if not isinstance(schedule, str):
        raise ConfigError(f"brief schedule must be a string, got {schedule!r}")
    hhmm = schedule.strip()
    if ":" not in hhmm:
        raise ConfigError(f"bad brief schedule {schedule!r}: time must look like '08:00'")
    h_str, m_str = hhmm.split(":", 1)
    try:
        hour, minute = int(h_str), int(m_str)
    except ValueError:
        raise ConfigError(f"bad brief schedule {schedule!r}: non-numeric time")
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ConfigError(f"bad brief schedule {schedule!r}: hour/minute out of range")
    return {"hour": hour, "minute": minute}


def load_config(path: str | os.PathLike | None = None) -> Config:
    """Load, validate, and normalize config.yaml. Raises ConfigError on any problem."""
    path = Path(path or DEFAULT_CONFIG_PATH)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ConfigError("top level must be a mapping with keys: defaults, people, topics")

    errors: list[str] = []
    # Reject secrets anywhere in the document first (rule 3), independent of structure.
    _scan_secrets(data, "", errors)
    extra_top = set(data) - {"defaults", "people", "topics", "brief"}
    if extra_top:
        errors.append(f"unknown top-level key(s): {sorted(extra_top)}")

    # defaults
    defaults = data.get("defaults")
    default_cadence_s = 86400
    if not isinstance(defaults, dict) or "cadence" not in defaults:
        errors.append("defaults.cadence is required")
    else:
        if set(defaults) - {"cadence"}:
            errors.append(f"defaults: unknown key(s): {sorted(set(defaults) - {'cadence'})}")
        try:
            default_cadence_s = parse_cadence(defaults["cadence"])
        except ConfigError as e:
            errors.append(f"defaults.cadence: {e}")

    sources: list[Source] = []

    def _append_source(raw_src, owner, fallback_cadence_s):
        identity = {k: v for k, v in raw_src.items() if k not in ("type", "cadence")}
        if "cadence" in raw_src:
            try:
                cadence_s = parse_cadence(raw_src["cadence"])
            except ConfigError:
                cadence_s = fallback_cadence_s
        else:
            cadence_s = fallback_cadence_s
        sources.append(Source(
            type=raw_src["type"],
            identity=identity,
            cadence_s=cadence_s,
            owner=owner,
            source_key=derive_source_key(raw_src["type"], identity),
        ))

    # people (absent or bare `people:` == empty)
    people = data.get("people") or []
    if not isinstance(people, list):
        errors.append("people must be a list")
        people = []
    for i, p in enumerate(people):
        if not isinstance(p, dict):
            errors.append(f"people[{i}]: must be a mapping")
            continue
        name = p.get("name") if isinstance(p.get("name"), str) else f"#{i}"
        where = f"people[{name}]"
        if not isinstance(p.get("name"), str) or not p.get("name", "").strip():
            errors.append(f"{where}: name is required and must be a non-empty string")
        if set(p) - {"name", "cadence", "sources"}:
            errors.append(f"{where}: unknown key(s): {sorted(set(p) - {'name', 'cadence', 'sources'})}")
        person_cadence_s = default_cadence_s
        if "cadence" in p:
            try:
                person_cadence_s = parse_cadence(p["cadence"])
            except ConfigError as e:
                errors.append(f"{where}: {e}")
        srcs = p.get("sources")
        if not isinstance(srcs, list) or not srcs:
            errors.append(f"{where}: sources must be a non-empty list")
            continue
        for j, s in enumerate(srcs):
            t = _check_source(s, f"{where}.sources[{j}]", errors, in_people=True)
            if t and not errors_for(errors, f"{where}.sources[{j}]"):
                _append_source(s, owner=f"person:{p.get('name', name)}", fallback_cadence_s=person_cadence_s)

    # topics (absent or bare `topics:` == empty)
    topics = data.get("topics") or {}
    digests: dict[str, Digest] = {}
    if not isinstance(topics, dict):
        errors.append("topics must be a mapping of topic-name -> {sources, digest?}")
        topics = {}
    for name, t in topics.items():
        where = f"topics.{name}"
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{where}: topic name must be a non-empty string")
        if not isinstance(t, dict):
            errors.append(f"{where}: must be a mapping")
            continue
        if set(t) - {"sources", "digest"}:
            errors.append(f"{where}: unknown key(s): {sorted(set(t) - {'sources', 'digest'})}")
        srcs = t.get("sources")
        if not isinstance(srcs, list) or not srcs:
            errors.append(f"{where}: sources must be a non-empty list")
        else:
            for j, s in enumerate(srcs):
                st = _check_source(s, f"{where}.sources[{j}]", errors, in_people=False)
                if st and not errors_for(errors, f"{where}.sources[{j}]"):
                    _append_source(s, owner=f"topic:{name}", fallback_cadence_s=default_cadence_s)
        if t.get("digest") is not None:
            dg = _check_digest(t["digest"], f"{where}.digest", errors)
            if dg:
                digests[name] = dg

    # brief (top-level, optional): the batched morning roundup. Absent -> Config.brief is None.
    brief: Brief | None = None
    if data.get("brief") is not None:
        brief = _check_brief(data["brief"], "brief", errors)

    if errors:
        raise ConfigError("config.yaml is invalid:\n  - " + "\n  - ".join(errors))

    return Config(
        default_cadence_s=default_cadence_s,
        sources=sources,
        digests=digests,
        brief=brief,
        raw=data,
    )


def errors_for(errors: list[str], prefix: str) -> bool:
    """True if any accumulated error concerns `prefix` (so we skip materializing a
    Source that failed validation)."""
    return any(e.startswith(prefix) for e in errors)
