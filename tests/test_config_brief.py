"""The top-level `brief:` config seam (app.config) — Phase 9.

Pure tests (no DB, no network): the Brief dataclass parses from a valid block, rejects malformed
schedule / window / top_n, is accepted at the top level (an unknown top-level key is still
rejected), and is None when absent. Plus parse_brief_schedule's {hour, minute} shape and its
raise-on-garbage guard. Config is loaded from a YAML written to tmp_path so nothing touches the
repo's authoritative config.yaml.
"""
from __future__ import annotations

import textwrap

import pytest

from app.config import ConfigError, load_config, parse_brief_schedule

# A minimal-but-valid config body the brief tests build on. `defaults.cadence` is the only hard
# requirement; people/topics are absent (allowed == empty).
_BASE = "defaults:\n  cadence: 1d\n"


def _write(tmp_path, body: str):
    p = tmp_path / "config.yaml"
    p.write_text(textwrap.dedent(body), encoding="utf-8")
    return p


# --- brief parsing -------------------------------------------------------------------------


def test_brief_valid_parses(tmp_path):
    cfg = load_config(_write(tmp_path, _BASE + "brief:\n  schedule: '08:00'\n  window: 24h\n  top_n: 7\n"))
    assert cfg.brief is not None
    assert cfg.brief.schedule == "08:00"
    assert cfg.brief.window_s == 86400   # 24h -> seconds
    assert cfg.brief.top_n == 7


def test_brief_window_days_unit(tmp_path):
    cfg = load_config(_write(tmp_path, _BASE + "brief:\n  schedule: '06:30'\n  window: 2d\n  top_n: 3\n"))
    assert cfg.brief.window_s == 2 * 86400


def test_brief_absent_is_none(tmp_path):
    cfg = load_config(_write(tmp_path, _BASE))
    assert cfg.brief is None


def test_brief_accepted_at_top_level_but_unknown_key_rejected(tmp_path):
    # A valid brief alongside an UNKNOWN top-level key: the brief is fine, the unknown key fails.
    with pytest.raises(ConfigError) as ei:
        load_config(_write(
            tmp_path,
            _BASE + "brief:\n  schedule: '08:00'\n  window: 24h\n  top_n: 5\nbogus: 1\n",
        ))
    assert "unknown top-level key" in str(ei.value)
    assert "bogus" in str(ei.value)


@pytest.mark.parametrize("sched", ["25:00", "8:0", "sun 09:00", "0800", "ab:cd", "08:60"])
def test_brief_invalid_schedule_rejected(tmp_path, sched):
    with pytest.raises(ConfigError) as ei:
        load_config(_write(tmp_path, _BASE + f"brief:\n  schedule: '{sched}'\n  window: 24h\n  top_n: 5\n"))
    assert "brief.schedule" in str(ei.value)


@pytest.mark.parametrize("window", ["7", "1w", "0h", "abc"])
def test_brief_invalid_window_rejected(tmp_path, window):
    with pytest.raises(ConfigError) as ei:
        load_config(_write(tmp_path, _BASE + f"brief:\n  schedule: '08:00'\n  window: {window}\n  top_n: 5\n"))
    assert "brief.window" in str(ei.value)


@pytest.mark.parametrize("top_n", ["0", "-1", "1.5"])
def test_brief_non_positive_top_n_rejected(tmp_path, top_n):
    with pytest.raises(ConfigError) as ei:
        load_config(_write(tmp_path, _BASE + f"brief:\n  schedule: '08:00'\n  window: 24h\n  top_n: {top_n}\n"))
    assert "brief.top_n" in str(ei.value)


def test_brief_missing_keys_rejected(tmp_path):
    with pytest.raises(ConfigError) as ei:
        load_config(_write(tmp_path, _BASE + "brief:\n  schedule: '08:00'\n"))
    msg = str(ei.value)
    assert "brief missing" in msg


def test_brief_unknown_inner_key_rejected(tmp_path):
    with pytest.raises(ConfigError) as ei:
        load_config(_write(
            tmp_path,
            _BASE + "brief:\n  schedule: '08:00'\n  window: 24h\n  top_n: 5\n  extra: 1\n",
        ))
    assert "brief: unknown key" in str(ei.value)


# --- parse_brief_schedule ------------------------------------------------------------------


def test_parse_brief_schedule_returns_hour_minute():
    assert parse_brief_schedule("08:00") == {"hour": 8, "minute": 0}
    assert parse_brief_schedule("8:05") == {"hour": 8, "minute": 5}
    assert parse_brief_schedule("  23:59 ") == {"hour": 23, "minute": 59}
    # No day_of_week key -> a CronTrigger built from this fires every day.
    assert "day_of_week" not in parse_brief_schedule("08:00")


@pytest.mark.parametrize(
    "bad",
    ["", "0800", "24:00", "08:60", "ab:cd", "sun 09:00"],
)
def test_parse_brief_schedule_raises_on_garbage(bad):
    with pytest.raises(ConfigError):
        parse_brief_schedule(bad)


def test_parse_brief_schedule_non_string_raises():
    with pytest.raises(ConfigError):
        parse_brief_schedule(None)  # type: ignore[arg-type]
