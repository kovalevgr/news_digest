"""DB-backed proof of dedup-into-clusters (app.researcher.cluster.cluster_pending_items).

Guarded: skipped unless RUN_PG_TESTS=1 and DATABASE_URL points at a migrated Postgres
(the poller service provides both). Runs inside an outer transaction rolled back at the
end, so it leaves no rows behind and is safe to re-run.

We set the item EMBEDDINGS BY HAND — two near-identical unit vectors and one orthogonal
("far") one — instead of trusting any provider to be semantic. That isolates the grouping
logic: the test asserts what cluster_pending_items does with known cosine distances, namely

  - the two near vectors land in ONE cluster, the far one in a SEPARATE cluster,
  - every clustered item gets a non-null cluster_id,
  - re-running creates no new cluster and reassigns nothing (idempotent),
  - a new cluster seeded by a topic-source item carries that source's topic.
"""
from __future__ import annotations

import math
import os
import uuid

import pytest

from app.adapters.base import item_id

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"
pytestmark = pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")

from app.llm.config import EMBEDDING_DIM


def _unit_vec(seed: float) -> list[float]:
    """A deterministic L2-normalized vector. `seed` perturbs only the first two coords so we
    can dial cosine distance precisely: two close seeds are near-identical; an orthogonal one
    is far. The bulk of the vector is a fixed ramp so norms are well-defined."""
    raw = [float((i % 7) + 1) for i in range(EMBEDDING_DIM)]
    raw[0] += seed
    norm = math.sqrt(sum(x * x for x in raw)) or 1.0
    return [x / norm for x in raw]


def _orthogonal_vec() -> list[float]:
    """A vector pointing in a wholly different direction from `_unit_vec` — cosine distance
    near 1.0 — so it must NOT join the near pair's cluster under any sane threshold."""
    raw = [0.0] * EMBEDDING_DIM
    # Concentrate mass on the tail coords, which `_unit_vec`'s ramp also covers but in a
    # very different distribution; reverse-sign every other coord to push the angle wide.
    for i in range(EMBEDDING_DIM):
        raw[i] = (-1.0 if i % 2 else 1.0) * float(EMBEDDING_DIM - i)
    norm = math.sqrt(sum(x * x for x in raw)) or 1.0
    return [x / norm for x in raw]


@pytest.fixture()
def session():
    from app.db.session import engine, SessionLocal

    conn = engine.connect()
    outer = conn.begin()
    sess = SessionLocal(bind=conn)
    try:
        yield sess
    finally:
        sess.close()
        outer.rollback()
        conn.close()


def _make_item(session, *, url: str, title: str, embedding, source_key: str):
    """Insert one item with a preset embedding + a single sighting under `source_key`.
    Returns the item id. Uses the real store upsert for the item/sighting, then sets the
    embedding directly (the cluster stage's input is an already-embedded item)."""
    from app.adapters.base import Item as AdapterItem
    from app.db.models import Item as ItemModel
    from app.researcher.store import upsert_item_and_sighting

    upsert_item_and_sighting(session, AdapterItem(url=url, title=title), source_key)
    session.flush()
    iid = item_id(url)
    session.get(ItemModel, iid).embedding = embedding
    session.flush()
    return iid


def _fake_cfg(source_key: str, owner: str):
    """A minimal Config whose source_by_key(source_key) returns a Source with `owner`, so
    source_default_topic can resolve a topic from a sighting's source_key."""
    from app.config import Config, Source

    src = Source(type="rss", identity={}, cadence_s=86400, owner=owner, source_key=source_key)
    return Config(default_cadence_s=86400, sources=[src])


def test_near_vectors_cluster_together_far_one_separate(session):
    from app.db.models import Cluster, Item as ItemModel
    from app.researcher.cluster import cluster_pending_items
    from sqlalchemy import func, select

    run = uuid.uuid4().hex
    topic_key = f"rss:topic-{run}"
    cfg = _fake_cfg(topic_key, owner="topic:ai")

    near_a = _unit_vec(0.00)
    near_b = _unit_vec(0.01)   # essentially the same direction -> tiny cosine distance
    far = _orthogonal_vec()    # cosine distance ~1.0 -> its own cluster

    id_a = _make_item(session, url=f"https://ex.com/a-{run}", title="story a",
                      embedding=near_a, source_key=topic_key)
    id_b = _make_item(session, url=f"https://ex.com/b-{run}", title="story b",
                      embedding=near_b, source_key=topic_key)
    id_far = _make_item(session, url=f"https://ex.com/far-{run}", title="unrelated",
                        embedding=far, source_key=topic_key)

    clusters_before = session.execute(select(func.count()).select_from(Cluster)).scalar_one()

    stats = cluster_pending_items(session, cfg=cfg)
    assert stats["clustered"] == 3

    a, b, far_row = (session.get(ItemModel, i) for i in (id_a, id_b, id_far))

    # Every clustered item has a cluster_id.
    assert a.cluster_id and b.cluster_id and far_row.cluster_id

    # The two near vectors share a cluster; the far one is on its own.
    assert a.cluster_id == b.cluster_id
    assert far_row.cluster_id != a.cluster_id

    # Exactly two NEW clusters were created (the near pair's + the far one's).
    clusters_after = session.execute(select(func.count()).select_from(Cluster)).scalar_one()
    assert clusters_after - clusters_before == 2
    assert stats["new_clusters"] == 2

    # The new cluster gets the source-default topic ("topic:ai" owner -> "ai").
    topic = session.execute(
        select(Cluster.topic).where(Cluster.id == a.cluster_id)
    ).scalar_one()
    assert topic == "ai"

    # Score stays NULL this slice; status defaults to 'new'.
    score, status = session.execute(
        select(Cluster.score, Cluster.status).where(Cluster.id == a.cluster_id)
    ).one()
    assert score is None
    assert status == "new"


def test_clustering_is_idempotent(session):
    from app.db.models import Cluster, Item as ItemModel
    from app.researcher.cluster import cluster_pending_items
    from sqlalchemy import func, select

    run = uuid.uuid4().hex
    key = f"rss:topic-{run}"
    cfg = _fake_cfg(key, owner="topic:ai")

    id_a = _make_item(session, url=f"https://ex.com/a-{run}", title="a",
                      embedding=_unit_vec(0.0), source_key=key)
    id_b = _make_item(session, url=f"https://ex.com/b-{run}", title="b",
                      embedding=_unit_vec(0.01), source_key=key)

    first = cluster_pending_items(session, cfg=cfg)
    assert first["clustered"] == 2 and first["new_clusters"] == 1

    cluster_a = session.get(ItemModel, id_a).cluster_id
    cluster_b = session.get(ItemModel, id_b).cluster_id
    count_after_first = session.execute(select(func.count()).select_from(Cluster)).scalar_one()

    # Re-run: nothing is pending (all items already carry a cluster_id) -> no-op.
    second = cluster_pending_items(session, cfg=cfg)
    assert second == {"clustered": 0, "new_clusters": 0}

    # No new clusters, and no reassignment.
    count_after_second = session.execute(select(func.count()).select_from(Cluster)).scalar_one()
    assert count_after_second == count_after_first
    assert session.get(ItemModel, id_a).cluster_id == cluster_a
    assert session.get(ItemModel, id_b).cluster_id == cluster_b


def test_person_only_item_gets_null_topic(session):
    from app.db.models import Cluster, Item as ItemModel
    from app.researcher.cluster import cluster_pending_items
    from sqlalchemy import select

    run = uuid.uuid4().hex
    key = f"rss:person-{run}"
    cfg = _fake_cfg(key, owner="person:Simon Willison")

    iid = _make_item(session, url=f"https://ex.com/p-{run}", title="a personal blog post",
                     embedding=_unit_vec(0.0), source_key=key)
    cluster_pending_items(session, cfg=cfg)

    cluster_id = session.get(ItemModel, iid).cluster_id
    topic = session.execute(
        select(Cluster.topic).where(Cluster.id == cluster_id)
    ).scalar_one()
    # Person-only source -> ambiguous -> topic left NULL for the classifier slice.
    assert topic is None


def test_equidistant_join_is_deterministic(session):
    """Two ALREADY-clustered items in DIFFERENT clusters carry the SAME embedding, so an
    incoming item is EXACTLY equidistant from both. _nearest_clustered must break that tie the
    same way every run (ORDER BY distance, then item id, then cluster id) — otherwise the join
    is arbitrary and order-stability is violated. We pre-seed the two clustered items by hand
    (force them into separate clusters with identical vectors — something the normal pass would
    never do), run cluster_pending_items repeatedly on the SAME incoming item, and assert it
    lands in the SAME cluster — specifically the one whose seed item has the lower item id."""
    from app.db.models import Cluster, Item as ItemModel
    from app.researcher.cluster import (
        cluster_pending_items,
        is_within_threshold,
        new_cluster_id,
    )

    run = uuid.uuid4().hex
    key = f"rss:topic-{run}"
    cfg = _fake_cfg(key, owner="topic:ai")

    # Two seed items with the IDENTICAL embedding, forced into two DISTINCT clusters.
    shared_vec = _unit_vec(0.0)
    cl_x = new_cluster_id()
    cl_y = new_cluster_id()
    session.add_all([Cluster(id=cl_x), Cluster(id=cl_y)])
    session.flush()

    id_x = _make_item(session, url=f"https://ex.com/x-{run}", title="seed x",
                      embedding=shared_vec, source_key=key)
    id_y = _make_item(session, url=f"https://ex.com/y-{run}", title="seed y",
                      embedding=shared_vec, source_key=key)
    session.get(ItemModel, id_x).cluster_id = cl_x
    session.get(ItemModel, id_y).cluster_id = cl_y
    session.flush()

    # The cluster the deterministic tiebreak SHOULD pick: lowest item id among the two
    # equidistant seeds. (Both are within threshold since distance == 0.)
    lower_seed_id = min(id_x, id_y)
    expected_cluster = cl_x if lower_seed_id == id_x else cl_y

    # The incoming item: same vector, so distance to BOTH seeds is exactly 0 -> a true tie.
    id_in = _make_item(session, url=f"https://ex.com/in-{run}", title="incoming",
                       embedding=shared_vec, source_key=key)
    # Sanity: distance 0 is within the join threshold, so it WILL join one of them.
    assert is_within_threshold(0.0)

    chosen = None
    for _ in range(5):
        # Reset the incoming item to unclustered and re-run; the choice must be identical each
        # time. (The two seeds keep their pre-set clusters; only the incoming item is pending.)
        session.get(ItemModel, id_in).cluster_id = None
        session.flush()
        cluster_pending_items(session, cfg=cfg)
        landed = session.get(ItemModel, id_in).cluster_id
        assert landed in (cl_x, cl_y)
        if chosen is None:
            chosen = landed
        assert landed == chosen, "equidistant join was not stable across runs"

    assert chosen == expected_cluster


def test_embed_pending_items_fills_null_embeddings(session):
    """embed_pending_items writes a vector for every titled item that lacks one. Uses the
    fake embedding provider (set EMBEDDING_PROVIDER=fake) so this needs no network."""
    from app.adapters.base import Item as AdapterItem
    from app.db.models import Item as ItemModel
    from app.researcher.cluster import embed_pending_items
    from app.researcher.store import upsert_item_and_sighting

    if os.environ.get("EMBEDDING_PROVIDER", "").lower() != "fake":
        pytest.skip("set EMBEDDING_PROVIDER=fake to exercise the live embed() path")

    run = uuid.uuid4().hex
    url = f"https://ex.com/embed-{run}"
    upsert_item_and_sighting(session, AdapterItem(url=url, title="embed me"), f"rss:{run}")
    session.flush()
    iid = item_id(url)
    assert session.get(ItemModel, iid).embedding is None

    # Drain the whole NULL-embedding backlog: embed_pending_items is batched + oldest-first,
    # so a pre-populated DB (e.g. items from a real poll sharing this database) could push
    # our freshly-inserted item past a single batch. Loop until nothing is pending — that is
    # exactly how the driver/embed_and_cluster is meant to be run repeatedly — then assert our
    # item got a vector. Keep batch_size small so multi-batch draining is actually exercised.
    total = 0
    while True:
        n = embed_pending_items(session, batch_size=10)
        total += n
        if n == 0:
            break
    assert total >= 1
    vec = session.get(ItemModel, iid).embedding
    assert vec is not None and len(list(vec)) == EMBEDDING_DIM
