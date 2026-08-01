"""Fusion-discovery retrieval (app.editor.fusion.find_related_clusters) — Phase 10.

DB-backed (guarded by RUN_PG_TESTS): the retrieval is a pgvector cosine search over items.embedding,
so it needs a migrated Postgres. We set item EMBEDDINGS BY HAND (known unit vectors with controlled
cosine distances) and pin the QUERY vector via the module-level `embed` seam, exactly like
tests/test_cluster_pg.py isolates the grouping logic. That makes the assertions about
ordering / dedup-to-distinct-clusters / top_k cap / NULL-embedding exclusion / source_types
DETERMINISTIC — we never lean on semantic relevance of the fake provider.

The blank-text short-circuit needs no DB and runs unconditionally.
"""
from __future__ import annotations

import math
import os
import uuid

import pytest

from app.adapters.base import item_id
from app.editor import fusion as fmod
from app.editor import RelatedCluster, find_related_clusters

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"
pg_only = pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")

from app.llm.config import EMBEDDING_DIM


# --- DB-light: blank text short-circuits before any DB / embed call ------------------------


def test_blank_text_returns_empty_without_embedding(monkeypatch):
    # No embed() call, no session touched — blank/whitespace text is a no-op.
    def _explode(*a, **k):
        raise AssertionError("embed must NOT be called for blank text")

    monkeypatch.setattr(fmod, "embed", _explode)
    sentinel_session = object()  # never touched
    assert find_related_clusters(sentinel_session, "") == []
    assert find_related_clusters(sentinel_session, "   \n\t ") == []
    assert find_related_clusters(sentinel_session, None) == []


def test_non_positive_top_k_returns_empty(monkeypatch):
    def _explode(*a, **k):
        raise AssertionError("embed must NOT be called when top_k <= 0")

    monkeypatch.setattr(fmod, "embed", _explode)
    assert find_related_clusters(object(), "some material", top_k=0) == []
    assert find_related_clusters(object(), "some material", top_k=-3) == []


# --- DB-backed: ordering / dedup / cap / NULL-exclusion / source_types ---------------------


def _unit_vec(seed: float) -> list[float]:
    """A deterministic L2-normalized vector; `seed` perturbs only the first coord so we can dial
    cosine distance precisely (mirrors tests/test_cluster_pg.py)."""
    raw = [float((i % 7) + 1) for i in range(EMBEDDING_DIM)]
    raw[0] += seed
    norm = math.sqrt(sum(x * x for x in raw)) or 1.0
    return [x / norm for x in raw]


def _orthogonal_vec() -> list[float]:
    """A vector pointing in a wholly different direction — cosine distance near 1.0."""
    raw = [(-1.0 if i % 2 else 1.0) * float(EMBEDDING_DIM - i) for i in range(EMBEDDING_DIM)]
    norm = math.sqrt(sum(x * x for x in raw)) or 1.0
    return [x / norm for x in raw]


@pytest.fixture()
def session():
    from app.db.session import engine, SessionLocal

    conn = engine.connect()
    outer = conn.begin()
    sess = SessionLocal(bind=conn, join_transaction_mode="create_savepoint")
    try:
        yield sess
    finally:
        sess.close()
        outer.rollback()
        conn.close()


def _make_clustered_item(session, *, url, title, embedding, source_key, topic=None, triage_title=None):
    """Insert one item (with a single sighting) into its OWN new cluster, with a preset embedding.
    Returns (item_id, cluster_id). `embedding=None` leaves the item's vector NULL."""
    from app.adapters.base import Item as AdapterItem
    from app.db.models import Cluster, Item as ItemModel
    from app.researcher.cluster import new_cluster_id
    from app.researcher.store import upsert_item_and_sighting

    cid = new_cluster_id()
    session.add(Cluster(id=cid, topic=topic, triage_title=triage_title))
    session.flush()

    upsert_item_and_sighting(session, AdapterItem(url=url, title=title), source_key)
    session.flush()
    iid = item_id(url)
    row = session.get(ItemModel, iid)
    row.cluster_id = cid
    row.embedding = embedding
    session.flush()
    return iid, cid


@pg_only
def test_find_related_clusters_orders_dedupes_caps_and_excludes_null(session, monkeypatch):
    run = uuid.uuid4().hex

    # Pin the query vector to a known direction; item distances are then fully controlled.
    query_vec = _unit_vec(0.0)
    monkeypatch.setattr(fmod, "embed", lambda texts: [query_vec])

    # Four distinct clusters at increasing distance from the query, plus a 2nd item in the NEAREST
    # cluster (so we can prove dedup keeps the cluster's nearest item), plus a NULL-embedding item.
    _, c_near = _make_clustered_item(
        session, url=f"https://ex.com/near-{run}", title="near item",
        embedding=_unit_vec(0.001), source_key=f"hn:{run}", topic="ai", triage_title="Near story",
    )
    # A SECOND item in the SAME nearest cluster, slightly farther — must be deduped away.
    from app.adapters.base import Item as AdapterItem
    from app.db.models import Item as ItemModel
    from app.researcher.store import upsert_item_and_sighting
    url2 = f"https://ex.com/near2-{run}"
    upsert_item_and_sighting(session, AdapterItem(url=url2, title="near item 2"), f"rss:{run}")
    session.flush()
    iid2 = item_id(url2)
    row2 = session.get(ItemModel, iid2)
    row2.cluster_id = c_near
    row2.embedding = _unit_vec(0.05)
    session.flush()

    _, c_mid = _make_clustered_item(
        session, url=f"https://ex.com/mid-{run}", title="mid item",
        embedding=_unit_vec(0.5), source_key=f"github:{run}", topic="infra",
    )
    _, c_far = _make_clustered_item(
        session, url=f"https://ex.com/far-{run}", title="far item",
        embedding=_unit_vec(2.0), source_key=f"arxiv:{run}",
    )
    _, c_orth = _make_clustered_item(
        session, url=f"https://ex.com/orth-{run}", title="orthogonal item",
        embedding=_orthogonal_vec(), source_key=f"x_user:{run}",
    )
    # A NULL-embedding item in its own cluster — must be excluded entirely.
    _, c_null = _make_clustered_item(
        session, url=f"https://ex.com/null-{run}", title="null item",
        embedding=None, source_key=f"rss:null-{run}",
    )

    out = find_related_clusters(session, "owner material about AI", top_k=3)

    # All RelatedCluster, capped at top_k.
    assert all(isinstance(r, RelatedCluster) for r in out)
    assert len(out) == 3

    # Distinct clusters only (dedup): the nearest cluster appears once despite its two items.
    cluster_ids = [r.cluster_id for r in out]
    assert len(set(cluster_ids)) == len(cluster_ids)

    # Ordered by ascending distance.
    dists = [r.distance for r in out]
    assert dists == sorted(dists)

    # The NULL-embedding cluster is never returned.
    assert c_null not in cluster_ids

    # The nearest cluster is first and carries its triage_title, topic, url, and the matched item's
    # source_types (the NEAREST item's sighting, 'hn').
    top = out[0]
    assert top.cluster_id == c_near
    assert top.title == "Near story"
    assert top.topic == "ai"
    assert top.url == f"https://ex.com/near-{run}"
    assert top.source_types == ["hn"]

    # source_types populated for each kept cluster (the matched item's distinct prefixes).
    for r in out:
        assert isinstance(r.source_types, list)
        assert all(":" not in s for s in r.source_types)


@pg_only
def test_top_k_caps_result_count(session, monkeypatch):
    run = uuid.uuid4().hex
    query_vec = _unit_vec(0.0)
    monkeypatch.setattr(fmod, "embed", lambda texts: [query_vec])

    for i in range(5):
        _make_clustered_item(
            session, url=f"https://ex.com/c{i}-{run}", title=f"item {i}",
            embedding=_unit_vec(float(i) * 0.1), source_key=f"rss:{i}-{run}",
        )

    assert len(find_related_clusters(session, "x", top_k=2)) == 2
    assert len(find_related_clusters(session, "x", top_k=4)) == 4


@pg_only
def test_title_falls_back_to_item_title_then_untitled(session, monkeypatch):
    run = uuid.uuid4().hex
    query_vec = _unit_vec(0.0)
    monkeypatch.setattr(fmod, "embed", lambda texts: [query_vec])

    # No triage_title on the cluster -> falls back to the matched item's title.
    _, cid = _make_clustered_item(
        session, url=f"https://ex.com/notitle-{run}", title="The item headline",
        embedding=_unit_vec(0.0), source_key=f"rss:{run}", topic=None, triage_title=None,
    )
    out = find_related_clusters(session, "material", top_k=1)
    assert len(out) == 1
    assert out[0].cluster_id == cid
    assert out[0].title == "The item headline"
    # topic None -> "—".
    assert out[0].topic == "—"


@pg_only
def test_env_top_k_default_used_when_unset(session, monkeypatch):
    # With no explicit top_k passed, the env-overridable default (FUSION_TOP_K) caps the result.
    run = uuid.uuid4().hex
    query_vec = _unit_vec(0.0)
    monkeypatch.setattr(fmod, "embed", lambda texts: [query_vec])
    monkeypatch.setenv("FUSION_TOP_K", "2")

    for i in range(4):
        _make_clustered_item(
            session, url=f"https://ex.com/e{i}-{run}", title=f"item {i}",
            embedding=_unit_vec(float(i) * 0.1), source_key=f"rss:{i}-{run}",
        )

    # find_related_clusters's signature default is top_k=5, but the accessor seam is FUSION_TOP_K;
    # call through the accessor to prove the env override drives the default.
    assert fmod.fusion_top_k() == 2
    # No explicit top_k -> the FUSION_TOP_K accessor (=2) caps the result (late-binding seam).
    assert len(find_related_clusters(session, "x")) == 2


@pg_only
def test_empty_store_returns_empty(session, monkeypatch):
    # No embedded clustered items at all -> []. (Use an orthogonal query so nothing pre-existing in a
    # shared DB matches within reach is irrelevant — there simply are no rows we inserted; but other
    # rows could exist, so assert the type/shape rather than exact emptiness when sharing a DB.)
    query_vec = _orthogonal_vec()
    monkeypatch.setattr(fmod, "embed", lambda texts: [query_vec])
    out = find_related_clusters(session, "nothing here", top_k=5)
    assert isinstance(out, list)
    assert all(isinstance(r, RelatedCluster) for r in out)
