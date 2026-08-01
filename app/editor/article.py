"""Article creation for an approved cluster (docs/01_technical.md §2.3; build plan Phase 3).

This is the seam between Gate 1 (the bot's cluster approval, Phase 2) and the writer-agent
draft (Phase 3). The bot's job ends at `clusters.status = 'approved'` + the pass-2 full-text
fetch; it deliberately does NOT create an article. The article row is minted HERE, when the
owner INITIATES drafting from the web dashboard's "ready to draft" list.

Why create-on-draft, not create-on-approve (a design decision, documented):

  - It keeps the bot strictly Phase-2 (status + pass-2 fetch). Article-lifecycle writes belong
    to the web/editor stage, not the triage stage — stages coordinate only through Postgres, so
    moving the write here keeps each stage's responsibility clean.
  - It avoids orphan `articles` rows for stories the owner approved but never drafted. Approving
    a story at Gate 1 means "worth a closer look", not "definitely a post"; only a story that
    actually got a piece should have an article.
  - `article_clusters` is the digest "covered" marker (docs §2.5): a cluster is excluded from a
    future digest ONLY once it is linked to an article. If approval created the article+link,
    every approved-but-undrafted story would be silently dropped from the digest. Creating the
    link on draft means "covered" == "actually got a piece", which is the intended semantics.

The function is the Postgres-only coordination point: it reads the approved cluster and writes
the article + the join row. It never calls the bot/poller/researcher and it NEVER publishes.

Idempotent-ish: a cluster can map to at most one hot_news article in this flow, so if the
cluster is already linked to an article we return that article's id instead of duplicating.
(A re-click of "draft this" therefore reopens the existing draft rather than minting a second
article.)
"""
from __future__ import annotations

import hashlib
import logging
import uuid

from sqlalchemy import func, select

from app.db.models import Article, ArticleCluster, Cluster, EditLog
from app.llm import embed  # module-level import = the mark-published embed monkeypatch seam

log = logging.getLogger("editor.article")

# Piece types the draft step understands (docs §2.3 "Piece type"). hot_news is the default
# (a single approved story → one canonical long-read); digest/project_post are valid shapes the
# template module stubs. Kept as a constant so the web trigger and the draft step share one
# source of truth and an unknown type is rejected loudly rather than silently mis-templated.
PIECE_TYPES = ("hot_news", "digest", "project_post", "tech_explainer")
DEFAULT_PIECE_TYPE = "hot_news"

# The edit_log instruction that marks an article's FIRST recorded draft — the root of its version
# trail (Feature A: version history + restore). Every article that gets drafted (writer-agent
# draft, or the digest rollup) is anchored by exactly one of these so the full trail exists from
# the very first state; iterate also drops one as a safety net if the first edit would otherwise
# lose the pre-edit text. A single source of truth so draft/iterate/digest can't drift on the
# literal string the version loader keys `is_genesis` on.
GENESIS_INSTRUCTION = "[genesis draft]"


def _ensure_genesis(session, article_id: str, draft_text: str | None) -> bool:
    """Insert the genesis edit_log row for an article IFF it has NO edit_log rows yet.

    The genesis row (instruction=GENESIS_INSTRUCTION, draft_snapshot=the given draft text) records
    an article's first draft so the version history starts at a real state rather than mid-stream.
    Idempotent by construction: it checks for zero existing edit_log rows first, so calling it more
    than once (draft, then a first iterate, then digest re-run) never adds a second genesis.

    Does NOT commit — the caller owns the transaction boundary (draft/iterate/digest each commit
    their own unit of work, and the genesis row must land in the SAME commit as the draft it
    snapshots). Returns True iff a genesis row was added, for the caller's logging.
    """
    has_rows = session.execute(
        select(func.count()).select_from(EditLog).where(EditLog.article_id == article_id)
    ).scalar_one()
    if has_rows:
        return False
    session.add(
        EditLog(
            article_id=article_id,
            instruction=GENESIS_INSTRUCTION,
            draft_snapshot=draft_text,
        )
    )
    return True


def new_article_id() -> str:
    """Mint a fresh, opaque article id: `a:` + sha256(uuid4) hex.

    Same opaque-hex shape as cluster ids (app.researcher.cluster.new_cluster_id mints
    `cl:` + sha256(uuid4)); an article, like a cluster, has no natural key (it is created on
    owner action, not derived from a URL), so we hash a random uuid4. The `a:` prefix makes
    article ids self-describing in logs and joins and distinguishes them from `cl:`/item ids."""
    return "a:" + hashlib.sha256(uuid.uuid4().bytes).hexdigest()


def existing_article_for_cluster(session, cluster_id: str) -> str | None:
    """The id of the cluster's OWN draft article, or None.

    Reads `article_clusters` (the join that also serves as the digest "covered" marker) but
    EXCLUDES digest articles. A digest links MANY clusters via the covered-marker, so a cluster
    that is merely covered by a digest is NOT "already drafted" — it has no own piece. We only
    return a NON-digest article (the hot_news/project_post draft a cluster maps to 1:1). Returns
    None when the cluster has no own draft (including a cluster that is only covered by a digest),
    so the Write flow mints a FRESH hot_news article instead of reopening — and redrafting — the
    digest (which would clobber the digest's rollup)."""
    return session.execute(
        select(ArticleCluster.article_id)
        .join(Article, Article.id == ArticleCluster.article_id)
        .where(ArticleCluster.cluster_id == cluster_id)
        .where(Article.piece_type != "digest")
        .order_by(ArticleCluster.article_id.asc())
        .limit(1)
    ).scalar_one_or_none()


def create_article_for_cluster(
    session, cluster_id: str, *, piece_type: str = DEFAULT_PIECE_TYPE
) -> str:
    """Create (or return the existing) article for an approved cluster; return the article id.

    Steps:
      1. Validate `piece_type` against PIECE_TYPES (an unknown type is a programming error — the
         web trigger passes a fixed value — so we fail loudly rather than mis-template a draft).
      2. If the cluster is already linked to an article (article_clusters), return THAT article's
         id — idempotent-ish: a re-click of "draft this" reopens the existing draft, it never
         mints a second article for the same story.
      3. Verify the cluster exists and is `approved`. Drafting a `new`/`sent`/`skipped` cluster
         is a no-op the owner shouldn't reach (the dashboard lists only approved clusters), so we
         reject it with a clear error rather than creating an article for an un-green-lit story.
      4. Insert an `articles` row at status `'drafting'` (the draft step is about to run; the row
         goes straight from creation into drafting, never sitting at `approved`), and link the
         cluster via `article_clusters`. The link is the digest "covered" marker (docs §2.5).

    Commits so the article is durable before the (possibly long) draft call runs against it, and
    so a crash mid-draft leaves a re-openable `drafting` row rather than losing the article.

    Coordinates only through Postgres: reads the cluster, writes the article + join. Never calls
    another stage; never publishes.
    """
    if piece_type not in PIECE_TYPES:
        raise ValueError(
            f"unknown piece_type {piece_type!r}; expected one of {PIECE_TYPES}"
        )

    # Idempotent-ish: a cluster already drafted reopens its existing article.
    existing = existing_article_for_cluster(session, cluster_id)
    if existing is not None:
        log.info("article for cluster %s already exists: %s", cluster_id, existing)
        return existing

    cluster = session.get(Cluster, cluster_id)
    if cluster is None:
        raise ValueError(f"cluster {cluster_id!r} not found")
    if cluster.status != "approved":
        # The owner reaches this only via the "ready to draft" list, which lists approved
        # clusters; a non-approved cluster here means a stale link or a forged request.
        raise ValueError(
            f"cluster {cluster_id!r} is {cluster.status!r}, not 'approved'; "
            "only an approved (Gate-1) story can be drafted"
        )

    article_id = new_article_id()
    session.add(
        Article(id=article_id, piece_type=piece_type, status="drafting", current_draft=None)
    )
    session.add(ArticleCluster(article_id=article_id, cluster_id=cluster_id))
    session.commit()
    log.info(
        "created article %s (piece_type=%s) for cluster %s", article_id, piece_type, cluster_id
    )
    return article_id


def approve_article(session, article_id: str) -> str:
    """Gate 2: approve the canonical draft — move articles.status `drafting` → `pre_publish`.

    This is the owner approving the canonical long-read (docs §2.3 "Gate 2", build plan Phase 4),
    NOT publishing it (hard rule 1): `pre_publish` means "the owner is happy with the canonical;
    variants can now be derived from it" — nothing is posted anywhere. The actual mark-as-published
    bookkeeping (and the article embedding) is Phase 5.

    Transitions:
      - `drafting` → `pre_publish` (commit, return "pre_publish").
      - `pre_publish` → idempotent no-op (return "pre_publish") so a re-click of Approve is safe.
      - `published` → ValueError: Gate 2 can't pull a published piece backward (publishing is a
        later, owner-driven act; reversing it isn't a thing this function does).
      - missing article → ValueError.

    Coordinates only through Postgres: it reads + updates the one article row, calls no other
    stage, and never publishes.
    """
    article = session.get(Article, article_id)
    if article is None:
        raise ValueError(f"article {article_id!r} not found")

    status = article.status
    if status == "pre_publish":
        # Already approved — idempotent so a double-click of Approve doesn't error.
        log.info("article %s already at pre_publish (Gate 2 idempotent)", article_id)
        return "pre_publish"
    if status == "published":
        # Can't un-publish via Gate 2; this is a programming/UI error reaching us, not a flow.
        raise ValueError(
            f"article {article_id!r} is already 'published'; Gate 2 cannot move it backward"
        )
    # Any pre-approval status (the expected 'drafting', or a stray 'approved') advances to Gate 2.
    article.status = "pre_publish"
    session.commit()
    log.info("approved article %s at Gate 2: %s -> pre_publish", article_id, status)
    return "pre_publish"


def publish_article(session, article_id: str) -> str:
    """Mark-as-published — articles.status `pre_publish` → `published` + compute the embedding
    (docs/01_technical.md §2 step 7, §3 decision 3; build plan Phase 5).

    THIS IS NOT PUBLISHING (hard rule 1). Nothing is posted anywhere and there is no posting API.
    This is BOOKKEEPING of an EXTERNAL MANUAL ACT: the owner has already copied a variant and
    posted it by hand, and now clicks "mark as published" so the system records that the canonical
    is live. The pipeline never publishes — it only records that the owner did.

    The point of the embedding: computing and storing `articles.embedding` (role `embedding`, via
    the swappable embed() seam) is what adds this article to the knowledge base that
    app.editor.kb.kb_search retrieves from for voice few-shot / continuity when drafting the next
    piece (docs §3 decision 3 — a published article + its embedding *is* the KB; there is no
    separate finals table). Marking published is the click that closes that loop.

    Transitions:
      - `pre_publish` → embed the canonical, set status `published`, commit, return "published".
      - `published` → idempotent: normally a no-op, BUT defensively, if the embedding is missing
        (NULL), recompute and store it (an article must be KB-retrievable once published — a missing
        embedding would silently keep it out of the KB), commit, return "published".
      - any other status (e.g. `drafting`, a stray `approved`) → ValueError: the article must clear
        Gate 2 first; we don't publish an un-approved canonical.
      - empty current_draft → ValueError: there is nothing to embed for the KB (an empty article
        can't ground future voice/continuity retrieval), so refuse rather than store a degenerate
        embedding.
      - missing article → ValueError.

    Coordinates only through Postgres: it reads + updates the one article row and calls the shared
    app.llm.embed (a shared component, not another stage). It calls no other stage and publishes
    nothing.
    """
    article = session.get(Article, article_id)
    if article is None:
        raise ValueError(f"article {article_id!r} not found")

    if article.status == "published":
        # Idempotent. Defensive backfill: if a prior publish left the embedding NULL (e.g. an embed
        # failure, or a row published before this stage existed), recompute it now so the article is
        # actually KB-retrievable — the whole point of marking published.
        if article.embedding is None:
            canonical = (article.current_draft or "").strip()
            if not canonical:
                raise ValueError(
                    f"article {article_id!r} is published but has an empty draft — there is "
                    "nothing to embed for the knowledge base"
                )
            article.embedding = embed(canonical)[0]
            session.commit()
            log.info("backfilled embedding for already-published article %s", article_id)
        return "published"

    if article.status != "pre_publish":
        # Must clear Gate 2 first. A drafting/approved article has no owner-approved canonical to
        # mark live; this is a UI/programming error reaching us, not a flow.
        raise ValueError(
            f"article {article_id!r} is {article.status!r}; approve it at Gate 2 (→ pre_publish) "
            "before marking published"
        )

    canonical = (article.current_draft or "").strip()
    if not canonical:
        raise ValueError(
            f"article {article_id!r}: cannot publish an empty article — there is nothing to embed "
            "for the knowledge base"
        )

    # Compute + store the embedding (role 'embedding', via the swappable embed() seam — never a
    # model id) BEFORE flipping status, so a published row always carries the embedding that makes
    # it KB-retrievable. embed() validates the vector dimension at its boundary.
    article.embedding = embed(canonical)[0]
    article.status = "published"
    session.commit()
    log.info(
        "marked article %s published (bookkeeping of a manual post; embedding stored for the KB)",
        article_id,
    )
    return "published"


def restore_article_version(session, article_id: str, edit_log_id: int) -> str:
    """Restore an article's draft to a recorded edit_log snapshot; return the restored draft text.

    Version-history restore (Feature A): the owner picks a past version (an edit_log row) in the UI
    and rolls the working draft back to it. This is BOOKKEEPING only (it mutates the working draft
    + appends an audit row); it never publishes/posts anything (hard rule 1) and coordinates only
    through Postgres — it reads + writes the one article + its edit_log, calling no other stage.

    Restore is itself recorded as a new edit_log row (instruction "[restored version #N]"), so the
    trail stays append-only: rolling back is a forward step you can in turn roll back from, and the
    voice/edit signal isn't rewritten. The restored snapshot becomes the new current_draft and the
    new row's draft_snapshot, so the version list shows the restore as the latest state.

    Refuses (ValueError) when:
      - the article doesn't exist,
      - the edit_log row doesn't exist, or belongs to a DIFFERENT article (a stale/forged id must
        not let one article's text leak into another),
      - the article is 'published': a published canonical is the KB entry (its embedding is live);
        we don't mutate it out from under the KB. Restore is a drafting/pre_publish-stage action.

    Commits. Returns the restored draft string (which the UI re-renders in the preview)."""
    article = session.get(Article, article_id)
    if article is None:
        raise ValueError(f"article {article_id!r} not found")
    if article.status == "published":
        raise ValueError(
            f"article {article_id!r} is 'published'; cannot restore a version of a published "
            "canonical (it is the live KB entry)"
        )

    row = session.get(EditLog, edit_log_id)
    if row is None:
        raise ValueError(f"edit_log row {edit_log_id!r} not found")
    if row.article_id != article_id:
        # A version id must belong to the article being restored — a mismatch is a stale link or a
        # forged request; never cross-pollinate one article's text into another.
        raise ValueError(
            f"edit_log row {edit_log_id!r} belongs to article {row.article_id!r}, "
            f"not {article_id!r}"
        )

    restored = row.draft_snapshot or ""
    article.current_draft = restored
    # Record the restore as a new (append-only) edit_log row so the trail isn't rewritten and the
    # restore is itself a version you can roll back from. Reference the restored row by its id (the
    # seq the UI shows is derived from ordering, but the id is the stable handle).
    session.add(
        EditLog(
            article_id=article_id,
            instruction=f"[restored version #{edit_log_id}]",
            draft_snapshot=restored,
        )
    )
    session.commit()
    log.info(
        "restored article %s to edit_log row %s (%d chars)",
        article_id, edit_log_id, len(restored),
    )
    return restored


__all__ = [
    "PIECE_TYPES",
    "DEFAULT_PIECE_TYPE",
    "GENESIS_INSTRUCTION",
    "new_article_id",
    "existing_article_for_cluster",
    "create_article_for_cluster",
    "approve_article",
    "publish_article",
    "restore_article_version",
]
