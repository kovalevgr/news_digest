"""Knowledge-base retrieval over PUBLISHED articles (docs/01_technical.md §3 decision 3, §4).

There is no separate "finals" table: a published article plus its embedding *is* the knowledge
base the writer-agent retrieves from for voice few-shot and continuity / non-repetition. This
module is that retrieval — the backend of the editor's `kb_search` tool.

The retrieval is pgvector cosine search, exactly the operator the dedup stage already uses
(app.researcher.cluster._nearest_clustered): embed the query via app.llm.embed, then ORDER BY
`articles.embedding <=> query` over the published, embedded rows.

Cold-start contract (Phase 3 reality): the embedding is computed at mark-as-published, which is
Phase 5. So TODAY there are zero published, embedded articles and `kb_search` returns []. The
SEAM must exist and degrade gracefully — the agent loop calls the tool, gets [], and drafts from
the source bundle alone — so that when Phase 5 lands and articles carry embeddings, retrieval
starts working with no change to the agent loop. This module is built and tested for both the
empty case (today) and the non-empty case (a hand-seeded embedded article, the PG test).

Determinism / coordination: the ONLY model call here is embed() (role "embedding", via the
swappable role→provider seam — no model id). It reads `articles` and nothing else; it never
writes, never calls another stage, never publishes.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from sqlalchemy import select

from app.db.models import Article
from app.llm import embed

log = logging.getLogger("editor.kb")

# How many past published articles a single kb_search returns by default. Voice few-shot +
# continuity want a SMALL set (a couple of the most relevant prior pieces), not the whole
# corpus — too many would bloat the agent's context and dilute the signal. Env-overridable seam;
# bad/non-positive values fall back so the cap is never accidentally disabled.
DEFAULT_KB_TOP_K = 3

# Cap on how much of each retrieved article's text we hand back to the agent. A published
# long-read can be thousands of words; the agent needs a representative excerpt for voice/
# continuity, not the entire piece re-injected verbatim. Bounds the worst-case context size.
DEFAULT_KB_EXCERPT_CHARS = 2000


def kb_top_k() -> int:
    """Default number of KB hits per search (env KB_TOP_K). Falls back on absence/garbage/
    non-positive — a 0/negative k would make every search return nothing."""
    raw = os.environ.get("KB_TOP_K")
    if raw is None:
        return DEFAULT_KB_TOP_K
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad KB_TOP_K=%r — falling back to %s", raw, DEFAULT_KB_TOP_K)
        return DEFAULT_KB_TOP_K
    return val if val > 0 else DEFAULT_KB_TOP_K


def kb_excerpt_chars() -> int:
    """Max chars of each KB hit's draft returned (env KB_EXCERPT_CHARS). Falls back on
    absence/garbage/non-positive so the excerpt cap is never disabled."""
    raw = os.environ.get("KB_EXCERPT_CHARS")
    if raw is None:
        return DEFAULT_KB_EXCERPT_CHARS
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad KB_EXCERPT_CHARS=%r — falling back to %s", raw, DEFAULT_KB_EXCERPT_CHARS)
        return DEFAULT_KB_EXCERPT_CHARS
    return val if val > 0 else DEFAULT_KB_EXCERPT_CHARS


@dataclass
class KBHit:
    """One retrieved past published article — primitives only, so it survives the session
    closing and renders into the agent's tool_result without touching the ORM."""
    article_id: str
    piece_type: str
    excerpt: str
    distance: float


def kb_search(session, query: str, *, top_k: int | None = None) -> list[KBHit]:
    """Cosine search over PUBLISHED, embedded articles for the `top_k` nearest to `query`.

    Embeds the query (role "embedding"), then ORDER BY `articles.embedding <=> query_vec` over
    rows WHERE status=='published' AND embedding IS NOT NULL. Returns a small list of KBHit
    (id, piece_type, capped excerpt, cosine distance), nearest first.

    Returns [] — never raises — when there is nothing to search: an empty/whitespace query, or
    (the Phase-3 reality) no published+embedded articles yet. This is the graceful cold-start
    degradation: the agent gets [] and drafts from the source bundle. A deterministic tiebreak
    (article id) after the distance keeps results stable when two articles are equidistant.
    """
    query = (query or "").strip()
    if not query:
        return []

    k = top_k if top_k is not None else kb_top_k()
    if k <= 0:
        return []

    query_vec = embed(query)[0]
    distance = Article.embedding.cosine_distance(query_vec)
    rows = session.execute(
        select(
            Article.id,
            Article.piece_type,
            Article.current_draft,
            distance.label("distance"),
        )
        .where(Article.status == "published")
        .where(Article.embedding.is_not(None))
        .order_by(distance.asc(), Article.id.asc())
        .limit(k)
    ).all()

    cap = kb_excerpt_chars()
    return [
        KBHit(
            article_id=r.id,
            piece_type=r.piece_type or "—",
            excerpt=(r.current_draft or "")[:cap],
            distance=float(r.distance),
        )
        for r in rows
    ]


__all__ = [
    "DEFAULT_KB_TOP_K",
    "DEFAULT_KB_EXCERPT_CHARS",
    "kb_top_k",
    "kb_excerpt_chars",
    "KBHit",
    "kb_search",
]
