"""Pure unit tests for the clustering stage (app.researcher.cluster) — no DB, no network.

These pin the two decisions that don't need Postgres: the threshold cutoff rule and the
source-default-topic resolution (topic owner -> that topic; person-only / ambiguous -> None).
The DB-backed grouping/idempotence proof lives in test_cluster_pg.py (RUN_PG_TESTS-gated).
"""
from __future__ import annotations

import app.researcher.cluster as cl
from app.researcher.cluster import (
    DEFAULT_DEDUP_COSINE_MAX,
    dedup_cosine_max,
    is_within_threshold,
    new_cluster_id,
    source_default_topic,
)


# --- threshold decision helper -------------------------------------------------------

def test_within_threshold_joins_when_at_or_below_cutoff():
    # Distance exactly at and just under the cutoff -> join.
    assert is_within_threshold(0.10, cutoff=0.17) is True
    assert is_within_threshold(0.17, cutoff=0.17) is True  # boundary is inclusive


def test_outside_threshold_does_not_join():
    assert is_within_threshold(0.18, cutoff=0.17) is False
    assert is_within_threshold(0.99, cutoff=0.17) is False


def test_no_neighbour_never_joins():
    # No clustered item exists yet -> distance is None -> always a new cluster.
    assert is_within_threshold(None, cutoff=0.17) is False


def test_threshold_uses_env_override(monkeypatch):
    monkeypatch.delenv("DEDUP_COSINE_MAX", raising=False)
    assert dedup_cosine_max() == DEFAULT_DEDUP_COSINE_MAX

    monkeypatch.setenv("DEDUP_COSINE_MAX", "0.30")
    assert dedup_cosine_max() == 0.30
    # A distance the default would reject is accepted under the looser override.
    assert is_within_threshold(0.25) is True

    # Garbage override falls back to the default rather than crashing.
    monkeypatch.setenv("DEDUP_COSINE_MAX", "not-a-float")
    assert dedup_cosine_max() == DEFAULT_DEDUP_COSINE_MAX


# --- source-default topic resolution -------------------------------------------------

def test_single_topic_owner_resolves_to_that_topic():
    assert source_default_topic(["topic:ai"]) == "ai"


def test_person_only_owner_is_ambiguous_and_left_null():
    # Person sources carry no inherent topic -> None (the cheap classifier's job, next slice).
    assert source_default_topic(["person:Andrej Karpathy"]) is None
    assert source_default_topic(["person:Simon Willison", "person:Andrej Karpathy"]) is None


def test_topic_plus_person_owner_resolves_to_the_topic():
    # An item seen by both a topic source and a person source is unambiguously that topic.
    assert source_default_topic(["person:Simon Willison", "topic:dotnet"]) == "dotnet"


def test_multiple_distinct_topics_stay_null():
    # Genuinely ambiguous across topics -> None (no deterministic pick; classifier territory).
    assert source_default_topic(["topic:ai", "topic:dotnet"]) is None


def test_repeated_same_topic_still_resolves():
    # Two sightings from two sources of the SAME topic is still one topic.
    assert source_default_topic(["topic:ai", "topic:ai"]) == "ai"


def test_no_owners_stay_null():
    assert source_default_topic([]) is None


# --- new cluster id scheme -----------------------------------------------------------

def test_new_cluster_id_is_prefixed_and_unique():
    a, b = new_cluster_id(), new_cluster_id()
    assert a.startswith("cl:") and b.startswith("cl:")
    assert a != b  # random uuid4 source -> collision-free
    # cl: + 64 hex chars (sha256), mirroring the opaque-hex shape of item ids.
    assert len(a) == len("cl:") + 64
    assert all(c in "0123456789abcdef" for c in a[len("cl:"):])


def test_module_exports_the_public_seam():
    for name in (
        "embed_pending_items",
        "cluster_pending_items",
        "embed_and_cluster",
        "is_within_threshold",
        "source_default_topic",
        "new_cluster_id",
        "dedup_cosine_max",
    ):
        assert hasattr(cl, name)
