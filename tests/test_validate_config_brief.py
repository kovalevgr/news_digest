"""The config-edit validator mirror (validate_config.py) must stay in lockstep with app.config
for the `brief:` block — Phase 9.

The validator runs as a BLOCKING PostToolUse hook, so a malformed brief MUST be reported (so the
hook would block). These load the standalone script module by path (it lives under
.claude/skills/config-edit/, outside the importable package tree) and drive its `validate()` on
YAML written to tmp_path.
"""
from __future__ import annotations

import importlib.util
import textwrap
from pathlib import Path

import pytest

_VALIDATOR = (
    Path(__file__).resolve().parents[1]
    / ".claude" / "skills" / "config-edit" / "validate_config.py"
)


def _load_validator():
    spec = importlib.util.spec_from_file_location("_validate_config_brief", _VALIDATOR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


validate_config = _load_validator()

_BASE = "defaults:\n  cadence: 1d\n"


def _write(tmp_path, body: str):
    p = tmp_path / "config.yaml"
    p.write_text(textwrap.dedent(body), encoding="utf-8")
    return p


def test_validator_accepts_valid_brief(tmp_path):
    errors = validate_config.validate(
        _write(tmp_path, _BASE + "brief:\n  schedule: '08:00'\n  window: 24h\n  top_n: 5\n")
    )
    assert errors == []


def test_validator_accepts_absent_brief(tmp_path):
    assert validate_config.validate(_write(tmp_path, _BASE)) == []


@pytest.mark.parametrize("sched", ["25:00", "8:0", "sun 09:00", "0800"])
def test_validator_rejects_malformed_schedule(tmp_path, sched):
    errors = validate_config.validate(
        _write(tmp_path, _BASE + f"brief:\n  schedule: '{sched}'\n  window: 24h\n  top_n: 5\n")
    )
    assert any("brief.schedule" in e for e in errors)


def test_validator_rejects_malformed_window(tmp_path):
    errors = validate_config.validate(
        _write(tmp_path, _BASE + "brief:\n  schedule: '08:00'\n  window: 1w\n  top_n: 5\n")
    )
    assert any("brief.window" in e for e in errors)


def test_validator_rejects_non_positive_top_n(tmp_path):
    errors = validate_config.validate(
        _write(tmp_path, _BASE + "brief:\n  schedule: '08:00'\n  window: 24h\n  top_n: 0\n")
    )
    assert any("brief.top_n" in e for e in errors)


def test_validator_rejects_unknown_brief_key(tmp_path):
    errors = validate_config.validate(
        _write(tmp_path, _BASE + "brief:\n  schedule: '08:00'\n  window: 24h\n  top_n: 5\n  extra: 1\n")
    )
    assert any("brief: unknown key" in e for e in errors)


def test_validator_rejects_missing_brief_keys(tmp_path):
    errors = validate_config.validate(
        _write(tmp_path, _BASE + "brief:\n  schedule: '08:00'\n")
    )
    assert any("brief missing" in e for e in errors)
