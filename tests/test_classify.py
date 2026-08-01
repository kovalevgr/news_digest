"""Unit tests for the cheap topic classifier (app.researcher.classify) — no DB, no network.

Two layers:
  - PURE: configured_topics reads config; build_prompt embeds the labels + titles + escape;
    parse_label maps clean/messy replies and rejects unknown/ambiguous/"other" -> None.
  - DB PATH with a FAKE session + monkeypatched `generate`: assert classify_pending_topics
    only fills topic for NULL clusters, never overwrites a source-default topic, and leaves
    topic NULL on an "other"/garbage verdict. We monkeypatch the module's `generate` reference
    (the fake provider just echoes, so we substitute a chosen reply instead).
"""
from __future__ import annotations

import types

import app.researcher.classify as cl
from app.researcher.classify import (
    OTHER_LABEL,
    build_prompt,
    classify_pending_topics,
    configured_topics,
    parse_label,
)


LABELS = ["ai", "dotnet"]


# --- configured_topics: label set comes from config, not hardcoded -------------------

def _cfg(topics: dict) -> object:
    """Minimal stand-in for app.config.Config carrying just .raw (what the classifier reads)."""
    return types.SimpleNamespace(raw={"topics": topics})


def test_configured_topics_are_the_topic_keys_in_order():
    cfg = _cfg({"ai": {}, "dotnet": {}})
    assert configured_topics(cfg) == ["ai", "dotnet"]


def test_configured_topics_excludes_reserved_other_and_blanks():
    cfg = _cfg({"ai": {}, OTHER_LABEL: {}, "  ": {}})
    assert configured_topics(cfg) == ["ai"]


def test_configured_topics_empty_when_no_topics():
    assert configured_topics(_cfg({})) == []
    assert configured_topics(types.SimpleNamespace(raw={})) == []


# --- build_prompt: contains labels, escape, and titles -------------------------------

def test_build_prompt_includes_labels_escape_and_titles():
    p = build_prompt(["GPT-5 released", "New LLM benchmark"], LABELS)
    for label in LABELS:
        assert label in p
    assert OTHER_LABEL in p           # the decline escape is offered
    assert "GPT-5 released" in p
    assert "New LLM benchmark" in p


def test_build_prompt_handles_no_titles_gracefully():
    p = build_prompt([], LABELS)
    assert "ai" in p and OTHER_LABEL in p
    assert "no title" in p.lower()    # placeholder rather than an empty block


# --- parse_label: tolerant mapping to a configured label or None ---------------------

def test_parse_label_clean_single_label():
    assert parse_label("ai", LABELS) == "ai"
    assert parse_label("dotnet", LABELS) == "dotnet"


def test_parse_label_is_case_insensitive_and_strips():
    assert parse_label("  AI  ", LABELS) == "ai"
    assert parse_label("DotNet", LABELS) == "dotnet"


def test_parse_label_tolerates_surrounding_chatter():
    assert parse_label("Topic: ai", LABELS) == "ai"
    assert parse_label("I'd say dotnet.", LABELS) == "dotnet"
    assert parse_label("The best label is: ai", LABELS) == "ai"


def test_parse_label_other_maps_to_none():
    assert parse_label(OTHER_LABEL, LABELS) is None
    assert parse_label("other", LABELS) is None


def test_parse_label_unknown_or_hallucinated_topic_is_none():
    # A topic the model invented that is NOT configured -> never accepted.
    assert parse_label("crypto", LABELS) is None
    assert parse_label("Topic: blockchain", LABELS) is None


def test_parse_label_empty_or_none_is_none():
    assert parse_label("", LABELS) is None
    assert parse_label(None, LABELS) is None
    assert parse_label("   ", LABELS) is None


def test_parse_label_whole_word_not_substring():
    # 'ai' must not fire inside 'maintain'/'available'; no configured label as a bounded token.
    assert parse_label("this is hard to maintain", LABELS) is None
    assert parse_label("the model is widely available", LABELS) is None


def test_parse_label_ambiguous_multiple_labels_is_none():
    # Naming two distinct configured topics is not a clean verdict -> decline.
    assert parse_label("could be ai or dotnet", LABELS) is None


def test_parse_label_repeated_same_label_still_resolves():
    assert parse_label("ai, definitely ai", LABELS) == "ai"


# --- classify_pending_topics: NULL-only fill / no-overwrite / other->NULL ------------

class _FakeCluster:
    def __init__(self, id_, topic):
        self.id = id_
        self.topic = topic
        self.created_at = id_  # ordering key; sortable stand-in


class _FakeSession:
    """In-memory stand-in for a SQLAlchemy Session covering only the calls classify makes:
    a select of NULL-topic cluster ids, _cluster_titles' title select, session.get, commit.

    `titles_by_cluster` maps cluster id -> list of titles. The select() calls are routed by
    inspecting the compiled statement's text for the table involved — crude but enough to keep
    this test DB-free and dependency-light."""

    def __init__(self, clusters, titles_by_cluster):
        self._clusters = {c.id: c for c in clusters}
        self._titles = titles_by_cluster
        self.commits = 0

    def execute(self, stmt):
        text = str(stmt).lower()
        if "from clusters" in text:
            # NULL-topic cluster ids, ordered by created_at then id (mirror the real query).
            ids = [c.id for c in self._clusters.values() if c.topic is None]
            ids.sort()
            return _ScalarResult(ids)
        if "from items" in text:
            # _cluster_titles binds the cluster id as a parameter; pull it from the compiled
            # statement's params so we return that cluster's titles.
            params = stmt.compile().params
            cluster_id = next(
                (v for k, v in params.items() if "cluster_id" in k), None
            )
            return _ScalarResult(list(self._titles.get(cluster_id, [])))
        raise AssertionError(f"unexpected statement: {text}")

    def get(self, model, pk):
        return self._clusters.get(pk)

    def commit(self):
        self.commits += 1


class _ScalarResult:
    def __init__(self, values):
        self._values = values

    def scalars(self):
        return self

    def all(self):
        return list(self._values)


def _patch_generate(monkeypatch, replies):
    """Monkeypatch the classifier's `generate` to return canned replies keyed by the first
    title in the prompt's headline list. The fake provider only echoes, so we substitute the
    reply we want and assert the DB effect."""
    def fake_generate(messages, role="generation", tools=None, **kwargs):
        assert role == "cheap"  # the classifier must always use the cheap role
        prompt = messages[-1]["content"]
        for needle, reply in replies.items():
            if needle in prompt:
                return reply
        return OTHER_LABEL
    monkeypatch.setattr(cl, "generate", fake_generate)


def test_classify_fills_only_null_clusters_and_never_overwrites(monkeypatch):
    cfg = _cfg({"ai": {}, "dotnet": {}})
    clusters = [
        _FakeCluster("cl:a", topic=None),       # NULL -> classifier should set 'ai'
        _FakeCluster("cl:b", topic="dotnet"),   # source-default -> must be left untouched
        _FakeCluster("cl:c", topic=None),       # NULL but model declines -> stays NULL
    ]
    titles = {
        "cl:a": ["New LLM benchmark tops the charts"],
        "cl:c": ["Some unrelated gardening news"],
    }
    session = _FakeSession(clusters, titles)
    _patch_generate(monkeypatch, {
        "New LLM benchmark": "ai",
        "Some unrelated gardening news": OTHER_LABEL,  # decline
    })

    stats = classify_pending_topics(session, cfg)

    by_id = {c.id: c for c in clusters}
    assert by_id["cl:a"].topic == "ai"        # NULL cluster filled
    assert by_id["cl:b"].topic == "dotnet"    # non-null never reconsidered/overwritten
    assert by_id["cl:c"].topic is None        # "other" verdict leaves it NULL
    assert stats == {"considered": 2, "labeled": 1}  # cl:b not even considered (predicate)
    assert session.commits == 2               # one commit per considered cluster


def test_classify_garbage_reply_leaves_topic_null(monkeypatch):
    cfg = _cfg({"ai": {}, "dotnet": {}})
    clusters = [_FakeCluster("cl:x", topic=None)]
    titles = {"cl:x": ["Quarterly earnings call recap"]}
    session = _FakeSession(clusters, titles)
    _patch_generate(monkeypatch, {"Quarterly earnings call recap": "i think maybe blockchain??"})

    stats = classify_pending_topics(session, cfg)

    assert clusters[0].topic is None          # unparseable/hallucinated -> never invent
    assert stats == {"considered": 1, "labeled": 0}


def test_classify_no_configured_topics_is_a_noop_without_model_call(monkeypatch):
    # Empty label set -> we must not call the model at all.
    def boom(*a, **k):
        raise AssertionError("generate must not be called when no topics are configured")
    monkeypatch.setattr(cl, "generate", boom)

    session = _FakeSession([_FakeCluster("cl:z", topic=None)], {"cl:z": ["anything"]})
    stats = classify_pending_topics(session, _cfg({}))
    assert stats == {"considered": 0, "labeled": 0}
    assert session.commits == 0


def test_module_exports_public_seam():
    for name in (
        "configured_topics",
        "build_prompt",
        "parse_label",
        "classify_titles_for_cluster",
        "classify_pending_topics",
        "OTHER_LABEL",
    ):
        assert hasattr(cl, name)
