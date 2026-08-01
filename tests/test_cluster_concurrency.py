"""Concurrency guard for cluster_id assignment (Phase 1 INTEGRATE).

The post-poll pipeline is scheduled as a single-runner job (max_instances=1 + coalesce), so in
normal operation two cluster passes never overlap. But the cluster stage ALSO carries a per-item
correctness guard independent of the scheduler: assignment is a conditional
`UPDATE items SET cluster_id=:c WHERE id=:id AND cluster_id IS NULL`, acted on only when it
changes exactly one row. These tests pin that guard directly against Postgres so it can't
silently regress (RUN_PG_TESTS-gated, like the other DB-backed tests).
"""
from __future__ import annotations

import os
import uuid

import pytest

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"

pytestmark = pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")


def _conn_session():
    from app.db.session import engine, SessionLocal

    conn = engine.connect()
    outer = conn.begin()
    session = SessionLocal(bind=conn)
    return conn, outer, session


def test_claim_item_is_won_once_and_lost_on_second_attempt():
    """_claim_item runs the guarded UPDATE: the FIRST claim of a NULL-cluster_id item wins
    (returns True, persists), a SECOND claim of the now-assigned item loses (returns False) and
    does NOT change the already-set cluster_id. This is the exact mechanism that stops two
    overlapping passes double-assigning the same item."""
    from sqlalchemy import select

    from app.db.models import Cluster, Item as ItemModel
    from app.researcher.cluster import _claim_item

    conn, outer, session = _conn_session()
    run = uuid.uuid4().hex
    try:
        cl_a = f"cl:{run}:a"
        cl_b = f"cl:{run}:b"
        it = f"it:{run}:x"
        session.add_all([Cluster(id=cl_a), Cluster(id=cl_b)])
        session.flush()
        item = ItemModel(id=it, title="x", url=f"https://ex/{run}/x")
        session.add(item)
        session.flush()

        # First claim into cluster A wins.
        assert _claim_item(session, item, cl_a) is True
        assigned = session.execute(
            select(ItemModel.cluster_id).where(ItemModel.id == it)
        ).scalar_one()
        assert assigned == cl_a

        # Second claim (simulating a concurrent pass) into cluster B loses — the WHERE
        # cluster_id IS NULL matches 0 rows now — and the assignment is unchanged.
        assert _claim_item(session, item, cl_b) is False
        still = session.execute(
            select(ItemModel.cluster_id).where(ItemModel.id == it)
        ).scalar_one()
        assert still == cl_a  # never double-assigned / never overwritten
    finally:
        session.close()
        outer.rollback()
        conn.close()


def test_second_cluster_pass_creates_nothing_and_assigns_nothing():
    """Two back-to-back cluster_pending_items passes over the same embedded-but-unclustered
    items: the first clusters them, the second finds nothing pending (idempotent) — it creates
    no clusters and reassigns nothing. Proves the guard + the oldest-first/idempotent contract
    hold together so a periodic re-run is a no-op on unchanged data."""
    from app.db.models import Cluster, Item as ItemModel
    from app.researcher.cluster import cluster_pending_items
    from app.config import Config

    conn, outer, session = _conn_session()
    run = uuid.uuid4().hex
    # An empty Config so source-default topic resolution is a clean no-op (items have no known
    # source here); the cluster stage still runs end to end.
    cfg = Config(default_cadence_s=86400, sources=[])
    try:
        # Two embedded items with identical vectors -> they land in the same cluster.
        vec = [0.0] * 1535 + [1.0]
        for suffix in ("a", "b"):
            session.add(ItemModel(
                id=f"it:{run}:{suffix}", title=suffix,
                url=f"https://ex/{run}/{suffix}", embedding=vec,
            ))
        session.flush()

        first = cluster_pending_items(session, cfg=cfg)
        assert first["clustered"] == 2
        assert first["new_clusters"] == 1  # identical vectors -> one shared cluster

        # A second pass finds nothing still unclustered -> pure no-op.
        second = cluster_pending_items(session, cfg=cfg)
        assert second == {"clustered": 0, "new_clusters": 0}
    finally:
        session.close()
        outer.rollback()
        conn.close()
