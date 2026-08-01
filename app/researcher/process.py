"""The post-poll pipeline: embed_and_cluster -> classify -> rank -> triage, in order
(Phase 1 INTEGRATE, extended in Phase 2 with the triage-summary stage).

The poller polls each source on its own cadence (app.researcher.schedule), writing items +
sightings. These downstream stages turn that raw ingest into ranked, topic-tagged, triage-
summarized clusters — but they are deliberately DECOUPLED from polling (each is its own
re-runnable pass over the DB, coordinating only through Postgres, never called inline from a
poll transaction).

This module is the ONE place that fixes their order and is shared by both runners so they can
never drift:

  1. embed_and_cluster — embed every item lacking an embedding, then group embedded-but-
     unclustered items into clusters by vector similarity (the only model call here is embed()).
  2. classify_pending_topics — fill clusters.topic where it is still NULL via the cheap
     single-shot classifier (role "cheap"; NULL-only, never overwrites a source-default topic).
  3. rank_clusters — recompute clusters.score for every cluster with items (pure deterministic
     blend: native engagement + cross-source frequency + recency; NO model call).
  4. summarize_pending_triage — give the highest-ranked NEW, un-summarized clusters a
     triage_title / triage_summary via ONE single-shot model call each (role from triage_role(),
     default "generation"), so the bot can deliver a Gate-1 card. This is the researcher's last
     step before Gate 1; it never advances status (the bot does that).

Order matters: cluster before classify (a topic is per-cluster, so clusters must exist), rank
before triage (triage SELECTS by score, so scores must be current), and triage last (it reads
the just-computed scores and the cluster's titles). Topic does not feed score, so classify/rank
order is independent, but running classify first keeps a freshly-clustered story tagged, scored,
and summarized in the same pass.

Idempotent end-to-end: each stage only touches its own pending rows (no embedding / no
cluster_id / NULL topic / re-scoreable / NEW+un-summarized), so a second pass over unchanged
data clusters nothing new, tags nothing new, writes the same scores, and summarizes nothing new.
That is exactly what makes it safe to run on a periodic timer alongside the poller and the bot.

`run_process` opens one session and threads it (plus cfg) through all four stages (each commits
its own work), so a periodic invocation is a single DB connection. Pure orchestration — the
determinism / model-call rules live in the stages it calls, not here.
"""
from __future__ import annotations

import logging

from app.config import Config, load_config
from app.db.session import get_session
from app.researcher.classify import classify_pending_topics
from app.researcher.cluster import embed_and_cluster
from app.researcher.rank import rank_clusters
from app.researcher.triage import summarize_pending_triage

log = logging.getLogger("researcher.process")


def run_process(session=None, *, cfg: Config | None = None) -> dict[str, int]:
    """Run embed_and_cluster -> classify -> rank -> triage once over the current DB; return
    combined stats.

    Pass `session`/`cfg` to reuse open ones (tests / a caller that already holds them); otherwise
    a session is opened and closed here and config is loaded once and shared by every stage.
    (The triage stage ignores cfg by design — its knobs are env, its grounding is the DB — but
    run_process threads cfg to it for signature symmetry with the other stages.)

    Combined stats: {embedded, clustered, new_clusters, considered, labeled, scored, triaged}.
    """
    cfg = cfg or load_config()
    own_session = session is None
    session = session or get_session()
    try:
        cluster_stats = embed_and_cluster(session, cfg=cfg)
        classify_stats = classify_pending_topics(session, cfg)
        scored = rank_clusters(session)
        triage_stats = summarize_pending_triage(session, cfg)
    finally:
        if own_session:
            session.close()

    stats = {
        "embedded": cluster_stats["embedded"],
        "clustered": cluster_stats["clustered"],
        "new_clusters": cluster_stats["new_clusters"],
        "considered": classify_stats["considered"],
        "labeled": classify_stats["labeled"],
        "scored": scored,
        "triaged": triage_stats["summarized"],
    }
    log.info(
        "process: embedded=%d clustered=%d new_clusters=%d "
        "considered=%d labeled=%d scored=%d triaged=%d",
        stats["embedded"], stats["clustered"], stats["new_clusters"],
        stats["considered"], stats["labeled"], stats["scored"], stats["triaged"],
    )
    return stats
