"""Read-only DB query helpers for the editor web app (docs/01_technical.md §2.6;
build plan Phase 3 — "the web app skeleton").

The web app is the one always-on HTTP surface. For the Phase-3 skeleton it READS the
pipeline state (the status dashboard) and READS one article (the editor view); it writes
nothing yet — article creation, the edit log, and Gate-2 are later backend slices that the
routes here leave seams for. Like every other stage, the web app coordinates ONLY through
Postgres (it never calls the poller/bot/researcher) and it NEVER publishes anything — this is
a preview/editing surface, not a posting one (hard rule).

Why a dedicated query module:
  - The routes stay thin: a route resolves a `Session` from the FastAPI dependency, calls one
    function here, and renders. The SQL lives in one place, away from the HTTP/templating glue.
  - These functions take a `session` and return plain dataclasses / dicts of primitives — no
    ORM objects leak into the templates and no detached-instance surprises after the request's
    session closes. That also makes them trivially testable against a stub session (the default
    suite overrides the session dependency, see tests/test_web.py) and against a real Postgres
    behind RUN_PG_TESTS.

Everything here is SELECT-only by construction; there is no write path in this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import select

from app.db.models import (
    Article,
    ArticleCluster,
    Cluster,
    EditLog,
    Item,
    OwnerSource,
    Sighting,
)
from app.editor.article import GENESIS_INSTRUCTION

# --- Unified "Stories" list (Phase 8) -------------------------------------------------------
#
# The dashboard is a single filterable Stories list. A "Story" is the owner-facing unit of work
# and is computed entirely in the read layer (no table change): every cluster that has NOT yet
# grown its own article shows as a raw story, every drafted (non-digest) article shows as the
# story it came from, and every digest shows as its own span-many-clusters story. The blended
# `score` lives in the model but is intentionally NOT surfaced here.

# The full status spectrum a Story row can hold, in lifecycle order: the cluster Gate-1 states
# (new -> sent -> approved/skipped) then the article lifecycle (drafting -> pre_publish ->
# published). `unified_status_counts` zero-fills across exactly these so the UI filter shows a
# stable, ordered set of buckets.
STATUS_SPECTRUM = (
    "new", "sent", "approved", "skipped", "drafting", "pre_publish", "published",
)


@dataclass
class StoryRow:
    """One row in the unified Stories list — detached primitives, so it survives the request
    session closing and renders without touching the ORM.

    A Story is one of three kinds:
      - "cluster":  an UNDRAFTED cluster (no own non-digest article); status is the cluster's.
      - "article":  a NON-digest article; status is the article's. Either backed by a single linked
                    cluster (the hot_news path, source_types from its sightings) OR a FLAGSHIP
                    article with NO cluster (the own-material path, source_types=["owner"],
                    cluster_id=None — Phase 10).
      - "digest":   a piece_type='digest' article spanning many clusters; status is the article's.

    `key` is a stable row id (article_id for article/digest rows, else cluster_id) so the UI can
    address a row across kinds. `in_digest` flags an undrafted cluster that a digest article
    covers (it still appears as its own cluster row, NOT relabelled to the digest). There is no
    score field by design."""
    key: str
    kind: str                 # "cluster" | "article" | "digest"
    effective_status: str     # one of STATUS_SPECTRUM
    title: str
    topic: str                # "—" if none
    source_types: list[str]   # distinct sighting source-type prefixes; [] for digest
    original_url: str | None  # a representative item URL to open; None for digest / no url
    in_digest: bool           # True iff an undrafted cluster is covered by a digest article
    cluster_id: str | None    # for Gate-1 actions (Approve/Skip/Draft); None for digest rows
    article_id: str | None    # for Open->editor; set for article & digest rows


def _first_heading(draft: str | None) -> str | None:
    """The first markdown `# ` heading line of a draft, stripped, or None.

    Used to title drafted/digest rows from the working draft. Only a top-level ATX `# ` heading
    counts (not `## `); leading blank lines are skipped. Returns None when there is no such
    heading (the caller then falls back to a cluster title / a constant)."""
    if not draft:
        return None
    for line in draft.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            text = stripped[2:].strip()
            if text:
                return text
        # A non-blank, non-H1 line before any heading means there is no leading title; keep
        # scanning anyway (a `# ` heading later in the body still counts as the title).
    return None


def _source_types_and_url_by_cluster(
    session, cluster_ids: set[str]
) -> tuple[dict[str, list[str]], dict[str, str | None], dict[str, str | None]]:
    """For each cluster id, its distinct sighting source-type prefixes (sorted) and a deterministic
    representative item URL. Two batched reads (no N+1), mirroring load_article_sources' join shape.

    source_types: the prefix-before-first-':' of each item's sightings' source_key (e.g.
    'hn:...'->'hn', 'x_user:...'->'x_user'), deduped and sorted, per cluster.
    original_url: a representative non-null item.url per cluster, chosen deterministically (the
    item with the lowest id), or None if the cluster has no sourced item."""
    if not cluster_ids:
        return {}, {}, {}

    # One read: every (cluster, item-id, url) for the clusters in play, ordered so the FIRST row
    # per cluster is the lowest item id with a non-null url (the deterministic representative).
    item_rows = session.execute(
        select(Item.cluster_id, Item.id, Item.url, Item.title)
        .where(Item.cluster_id.in_(cluster_ids))
        .order_by(Item.cluster_id.asc(), Item.id.asc())
    ).all()

    url_by_cluster: dict[str, str | None] = {cid: None for cid in cluster_ids}
    # A representative item title per cluster (first non-empty by item id asc) — the fallback the
    # Stories list uses when a cluster has no triage_title, so untriaged stories show a real
    # headline instead of "(untitled)".
    title_by_cluster: dict[str, str | None] = {cid: None for cid in cluster_ids}
    items_by_cluster: dict[str, list[str]] = {}
    all_item_ids: set[str] = set()
    for cid, item_id_, url, item_title in item_rows:
        all_item_ids.add(item_id_)
        items_by_cluster.setdefault(cid, []).append(item_id_)
        if url and url_by_cluster.get(cid) is None:
            url_by_cluster[cid] = url
        if item_title and item_title.strip() and title_by_cluster.get(cid) is None:
            title_by_cluster[cid] = item_title.strip()

    # One read: the source-type prefixes for every item in play, folded back to its cluster.
    types_by_cluster: dict[str, set[str]] = {cid: set() for cid in cluster_ids}
    if all_item_ids:
        cluster_of_item = {
            item_id_: cid
            for cid, ids in items_by_cluster.items()
            for item_id_ in ids
        }
        sighting_rows = session.execute(
            select(Sighting.item_id, Sighting.source_key).where(
                Sighting.item_id.in_(all_item_ids)
            )
        ).all()
        for item_id_, source_key in sighting_rows:
            prefix = (source_key or "").split(":", 1)[0]
            if prefix:
                cid = cluster_of_item.get(item_id_)
                if cid is not None:
                    types_by_cluster[cid].add(prefix)

    return (
        {cid: sorted(types) for cid, types in types_by_cluster.items()},
        url_by_cluster,
        title_by_cluster,
    )


def _story_rows(session) -> list[StoryRow]:
    """Assemble the full unified Stories list (unfiltered, unsorted-by-time). One small set of
    batched reads, then merge/sort in Python — fine at single-user scale (~hundreds of rows) and
    clearer than one giant SQL. SELECT-only.

    The story set = (clusters with no own non-digest article, as "cluster")
                  ∪ (non-digest articles, as "article")
                  ∪ (digest articles, as "digest").
    A cluster that grew its own hot_news/project_post draft appears ONCE as the article (not also
    as a cluster). A cluster merely COVERED by a digest still appears as a cluster row with
    in_digest=True (it is NOT relabelled to the digest's status, and NOT hidden)."""
    # All articles (id, piece_type, status, draft, updated_at).
    article_rows = session.execute(
        select(
            Article.id,
            Article.piece_type,
            Article.status,
            Article.current_draft,
            Article.updated_at,
        )
    ).all()

    # All article<->cluster links, so we can map articles to their clusters and find which
    # clusters are "owned" by a non-digest article vs merely covered by a digest.
    link_rows = session.execute(
        select(ArticleCluster.article_id, ArticleCluster.cluster_id)
    ).all()
    clusters_by_article: dict[str, list[str]] = {}
    for aid, cid in link_rows:
        clusters_by_article.setdefault(aid, []).append(cid)

    # Partition articles and resolve cluster ownership.
    nondigest_articles = []  # (id, status, draft, updated_at, linked_cluster_id|None)
    digest_articles = []     # (id, status, draft, updated_at)
    owned_cluster_ids: set[str] = set()       # clusters with a non-digest article
    digest_covered_cluster_ids: set[str] = set()  # clusters linked to a digest article
    for r in article_rows:
        linked = clusters_by_article.get(r.id, [])
        if r.piece_type == "digest":
            digest_articles.append((r.id, r.status, r.current_draft, r.updated_at))
            digest_covered_cluster_ids.update(linked)
        else:
            # A non-digest article maps to one cluster (its first/only link); pick deterministically.
            linked_cid = min(linked) if linked else None
            nondigest_articles.append(
                (r.id, r.status, r.current_draft, r.updated_at, linked_cid)
            )
            if linked_cid is not None:
                owned_cluster_ids.add(linked_cid)

    # All clusters (id, status, topic, triage_title, updated_at).
    cluster_rows = session.execute(
        select(
            Cluster.id,
            Cluster.status,
            Cluster.topic,
            Cluster.triage_title,
            Cluster.updated_at,
        )
    ).all()
    cluster_by_id = {r.id: r for r in cluster_rows}

    # The clusters that show as their own "cluster" story: every cluster NOT owned by a non-digest
    # article. (A digest-covered-but-undrafted cluster IS in here — with in_digest=True.)
    undrafted_cluster_ids = {r.id for r in cluster_rows if r.id not in owned_cluster_ids}

    # Clusters whose source_types/url we need: the undrafted ones (for "cluster" rows) and the
    # ones linked to a non-digest article (for "article" rows). Batch both in one lookup.
    needed_cluster_ids = set(undrafted_cluster_ids)
    for _aid, _status, _draft, _upd, linked_cid in nondigest_articles:
        if linked_cid is not None:
            needed_cluster_ids.add(linked_cid)
    types_by_cluster, url_by_cluster, title_by_cluster = _source_types_and_url_by_cluster(
        session, needed_cluster_ids
    )

    # Phase 10: FLAGSHIP articles — non-digest articles with NO linked cluster — are grounded in the
    # owner's own material, not a cluster. They still surface as "article" rows, but with
    # source_types=["owner"] and a representative owner-source url. Batch the per-flagship owner-url
    # in one read (the first owner-source url for the article, oldest-first), no N+1.
    flagship_article_ids = {
        aid for aid, _s, _d, _u, linked_cid in nondigest_articles if linked_cid is None
    }
    owner_url_by_article: dict[str, str | None] = {aid: None for aid in flagship_article_ids}
    if flagship_article_ids:
        owner_rows = session.execute(
            select(OwnerSource.article_id, OwnerSource.url)
            .where(OwnerSource.article_id.in_(flagship_article_ids))
            .order_by(OwnerSource.article_id.asc(), OwnerSource.id.asc())
        ).all()
        for a_id, url in owner_rows:
            if url and owner_url_by_article.get(a_id) is None:
                owner_url_by_article[a_id] = url

    rows: list[tuple[StoryRow, object]] = []  # (row, updated_at) for the time sort

    # (A) undrafted clusters.
    for cid in undrafted_cluster_ids:
        c = cluster_by_id[cid]
        title = (c.triage_title or "").strip() or title_by_cluster.get(cid) or "(untitled)"
        rows.append((
            StoryRow(
                key=cid,
                kind="cluster",
                effective_status=c.status or "new",
                title=title,
                topic=(c.topic or "—"),
                source_types=types_by_cluster.get(cid, []),
                original_url=url_by_cluster.get(cid),
                in_digest=cid in digest_covered_cluster_ids,
                cluster_id=cid,
                article_id=None,
            ),
            c.updated_at,
        ))

    # (B) non-digest articles (the drafted stories).
    for aid, status, draft, updated_at, linked_cid in nondigest_articles:
        title = _first_heading(draft)
        if not title and linked_cid is not None:
            c = cluster_by_id.get(linked_cid)
            if c is not None:
                title = (c.triage_title or "").strip() or None
            title = title or title_by_cluster.get(linked_cid)
        title = title or "(untitled)"
        topic = "—"
        source_types: list[str] = []
        original_url: str | None = None
        if linked_cid is not None:
            c = cluster_by_id.get(linked_cid)
            if c is not None:
                topic = c.topic or "—"
            source_types = types_by_cluster.get(linked_cid, [])
            original_url = url_by_cluster.get(linked_cid)
        else:
            # FLAGSHIP article (no cluster): grounded in the owner's own material. The frontend
            # distinguishes it from a cluster-backed article by source_types=["owner"].
            source_types = ["owner"]
            original_url = owner_url_by_article.get(aid)
        rows.append((
            StoryRow(
                key=aid,
                kind="article",
                effective_status=status or "approved",
                title=title,
                topic=topic,
                source_types=source_types,
                original_url=original_url,
                in_digest=False,
                cluster_id=linked_cid,
                article_id=aid,
            ),
            updated_at,
        ))

    # (C) digest articles (span many clusters — no single source list).
    for aid, status, draft, updated_at in digest_articles:
        title = _first_heading(draft) or "Weekly digest"
        rows.append((
            StoryRow(
                key=aid,
                kind="digest",
                effective_status=status or "approved",
                title=title,
                topic="—",
                source_types=[],
                original_url=None,
                in_digest=False,
                cluster_id=None,
                article_id=aid,
            ),
            updated_at,
        ))

    # Order by the row's own updated_at DESC, with a deterministic key tiebreak (key ASC). A row's
    # updated_at can be None on a freshly-inserted row (the server_default isn't refreshed until a
    # commit/expire); those sort LAST. We sort to epoch seconds so the timestamp can be negated for
    # a single ASC sort that puts newest first while keeping key ASC within ties (a two-pass
    # reverse=True sort would flip the key tiebreak too).
    _MIN = datetime.min.replace(tzinfo=timezone.utc)

    def _epoch(updated_at) -> float:
        if updated_at is None:
            return float("-inf")  # None -> oldest, so it lands last after negation
        ts = updated_at if updated_at.tzinfo is not None else updated_at.replace(tzinfo=timezone.utc)
        return (ts - _MIN).total_seconds()

    rows.sort(key=lambda p: (-_epoch(p[1]), p[0].key))
    return [row for row, _ts in rows]


def load_stories(
    session, *, status: str | None = None, source: str | None = None
) -> list[StoryRow]:
    """The unified Stories list, newest-activity first, optionally filtered by status and/or source.

    `status=None` returns every status; `status=X` keeps only rows whose effective_status == X.
    `source=None` returns every source; `source=S` keeps only rows whose source_types contains S —
    where S is a source-type prefix as surfaced on StoryRow ("rss", "hn", "arxiv", "x_user",
    "github", …). A digest (source_types=[]) matches NO source filter (it only shows under "All").
    The two filters AND together (both None = everything). Order: the row's own updated_at DESC
    (article.updated_at for article/digest rows, cluster.updated_at for cluster rows) with a
    deterministic key tiebreak. SELECT-only; assembles in Python after a few batched reads
    (single-user scale). Coordinates only through Postgres — no model/agent call, no score
    surfaced."""
    rows = _story_rows(session)
    if status is not None:
        rows = [r for r in rows if r.effective_status == status]
    if source is not None:
        rows = [r for r in rows if source in r.source_types]
    return rows


def unified_status_counts(session, *, source: str | None = None) -> dict[str, int]:
    """{status: count} over the SAME story definition as `load_stories`, zero-filled across the
    full STATUS_SPECTRUM (in lifecycle order) so the UI filter shows a stable, ordered set of
    buckets. SELECT-only.

    `source` cross-filters the counts: `source=None` counts over every story (current behavior);
    `source=S` counts only over stories whose source_types contains S — so the status counts reflect
    the source filter the UI currently has selected (a digest, source_types=[], is excluded by any
    source filter). This pairs with `source_counts(status=…)` to make both filters dynamic.

    Any out-of-band effective_status (shouldn't happen — statuses are a closed set) is appended
    after the known ones rather than dropped, so an unexpected value is visible, not lost."""
    counts = {status: 0 for status in STATUS_SPECTRUM}
    for row in _story_rows(session):
        if source is not None and source not in row.source_types:
            continue
        counts[row.effective_status] = counts.get(row.effective_status, 0) + 1
    return counts


def source_counts(session, *, status: str | None = None) -> dict[str, int]:
    """{source_type: count} over the unified story set — how many stories carry each source-type
    prefix ("rss", "hn", "arxiv", "x_user", "github", …). SELECT-only.

    `status` cross-filters: `status=None` counts over every story; `status=X` counts only over
    stories whose effective_status == X — so the source counts reflect the status filter the UI
    currently has selected. This pairs with `unified_status_counts(source=…)` to make both filters
    dynamic.

    A story counts toward EACH of its source_types (the value is multi-valued), so the per-source
    counts need NOT sum to the story total. Keys are exactly the source types PRESENT in the
    (status-filtered) story set — no fixed universe and no zero-fill (a digest contributes nothing,
    having source_types=[])."""
    counts: dict[str, int] = {}
    for row in _story_rows(session):
        if status is not None and row.effective_status != status:
            continue
        for source_type in row.source_types:
            counts[source_type] = counts.get(source_type, 0) + 1
    return counts


@dataclass
class ArticleView:
    """The editor view's payload — the article's identity + its current working draft.

    `current_draft` is whatever the draft holds RIGHT NOW (it may be empty for a freshly-created
    article — the writer-agent draft step is a later slice). The editor renders it as the live
    preview; the chat panel will mutate it once the agent is wired in."""
    id: str
    piece_type: str
    status: str
    current_draft: str


def load_article(session, article_id: str) -> ArticleView | None:
    """Fetch one article for the editor view, or None if it doesn't exist (the route turns None
    into a 404). SELECT-only; returns a detached dataclass so the template never touches a
    possibly-expired ORM instance after the request session closes."""
    row = session.execute(
        select(
            Article.id,
            Article.piece_type,
            Article.status,
            Article.current_draft,
        ).where(Article.id == article_id)
    ).first()
    if row is None:
        return None
    return ArticleView(
        id=row.id,
        piece_type=row.piece_type or "—",
        status=row.status or "—",
        current_draft=row.current_draft or "",
    )


def article_exists(session, article_id: str) -> bool:
    """True iff an article row exists. Used by the WebSocket handler to reject a chat connection
    for an unknown article before the (stubbed) writer-agent is even consulted. A bare existence
    SELECT — cheaper than loading the draft, which the socket doesn't need to open."""
    return session.execute(
        select(Article.id).where(Article.id == article_id).limit(1)
    ).first() is not None


# --- Feature A: version history (read-only loader; the restore mutation lives in app/editor) ---


@dataclass
class ArticleVersion:
    """One point in an article's version trail — an edit_log row, oldest-first (docs §2.3 edit_log).

    Primitives only, detached from the ORM (mirrors ArticleView) so it survives the request session
    closing and renders without touching a possibly-expired instance. `edit_log_id` is the stable
    handle the restore mutation takes; it is None ONLY for the synthetic genesis a zero-edit_log
    article falls back to (an existing un-edited article still shows one version). `seq` is the
    1-based display position (oldest first). `is_genesis` flags the article's FIRST recorded draft."""
    edit_log_id: int | None  # None only for the synthetic genesis-from-current fallback
    seq: int                 # 1-based, oldest first
    instruction: str
    draft: str               # the draft_snapshot at that point ("" if NULL)
    created_at: datetime | None
    is_genesis: bool


def load_article_versions(session, article_id: str) -> list[ArticleVersion]:
    """The article's version trail, oldest first, for the history/restore UI (Feature A). SELECT-only.

    Reads the article's edit_log rows ORDER BY id ASC (id is the insertion order — the true
    chronology) into ArticleVersion list with seq=1,2,…. `is_genesis` is set on the FIRST row whose
    instruction is the genesis marker (only the first such row — a later stray genesis-looking
    instruction is not the root).

    Fallback for an article that has NO edit_log rows yet (e.g. one created before Feature A, or a
    bare row that was never drafted/iterated): return a SINGLE synthetic version carrying the
    article's current_draft, so the history UI always shows at least one (restorable-to-current)
    version. That synthetic row has edit_log_id=None (there is no row to restore — it IS the
    current state). Returns [] if the article doesn't exist."""
    rows = session.execute(
        select(
            EditLog.id,
            EditLog.instruction,
            EditLog.draft_snapshot,
            EditLog.created_at,
        )
        .where(EditLog.article_id == article_id)
        .order_by(EditLog.id.asc())
    ).all()

    if not rows:
        # No edit_log trail: fall back to a single synthetic genesis from the current draft, but
        # only if the article actually exists (else []).
        art = session.execute(
            select(Article.current_draft, Article.created_at).where(Article.id == article_id)
        ).first()
        if art is None:
            return []
        return [
            ArticleVersion(
                edit_log_id=None,
                seq=1,
                instruction=GENESIS_INSTRUCTION,
                draft=art.current_draft or "",
                created_at=art.created_at,
                is_genesis=True,
            )
        ]

    versions: list[ArticleVersion] = []
    genesis_marked = False
    for seq, r in enumerate(rows, start=1):
        is_genesis = (not genesis_marked) and (r.instruction == GENESIS_INSTRUCTION)
        if is_genesis:
            genesis_marked = True
        versions.append(
            ArticleVersion(
                edit_log_id=r.id,
                seq=seq,
                instruction=r.instruction or "",
                draft=r.draft_snapshot or "",
                created_at=r.created_at,
                is_genesis=is_genesis,
            )
        )
    return versions


# --- Feature B: source links (read-only loader) ---------------------------------------------


@dataclass
class ArticleSource:
    """One source behind an article — a cluster item (Feature B) OR an owner-material row (Phase 10).

    Primitives only, detached from the ORM. `source_types` is the distinct set of platform-type
    prefixes (the bit before ':' in each sighting's source_key, e.g. 'rss', 'x_user') that observed
    the item — cross-source provenance at a glance; an owner-material row uses ["owner"]. `cluster_id`
    is the linked cluster the source came in through (a digest article spans many); it is None for an
    owner-material row (a flagship article has no cluster)."""
    title: str
    url: str
    source_types: list[str]  # distinct sighting source-type prefixes; ["owner"] for owner material
    cluster_id: str | None


def load_article_sources(session, article_id: str) -> list[ArticleSource]:
    """The source links behind an article, for the editor's "sources" panel (Feature B). SELECT-only.

    Walks article_clusters(article_id) → clusters → items (URL not null) and, per item, the distinct
    source-type prefixes of its sightings' source_keys (the bit before the first ':' — e.g.
    'rss:{"url":...}' → 'rss'). Each row is title (item.title or "(untitled)"), url, those
    source_types (sorted), and the cluster_id it came in through.

    Deduped by url (keep the first occurrence — a URL can appear under multiple clusters; we surface
    it once, under the first cluster in the stable order). Stable order: cluster items first (by
    cluster_id, then title), THEN the article's owner-material rows oldest-first (Phase 10). Each
    owner row is ArticleSource(title=title-or-url-or-"(owner material)", url=url-or-"",
    source_types=["owner"], cluster_id=None); owner rows with no url are each kept (not url-deduped
    away). Returns [] if the article has no linked clusters / no sourced items AND no owner material
    (or doesn't exist)."""
    rows = session.execute(
        select(
            Item.title,
            Item.url,
            Item.id,
            ArticleCluster.cluster_id,
        )
        .join(Cluster, Cluster.id == ArticleCluster.cluster_id)
        .join(Item, Item.cluster_id == Cluster.id)
        .where(ArticleCluster.article_id == article_id)
        .where(Item.url.isnot(None))
        .order_by(ArticleCluster.cluster_id.asc(), Item.title.asc(), Item.id.asc())
    ).all()

    # Gather the distinct source-type prefixes per item id in one pass (one extra query, not N).
    types_by_item: dict[str, set[str]] = {}
    if rows:
        item_ids = {r.id for r in rows}
        sighting_rows = session.execute(
            select(Sighting.item_id, Sighting.source_key).where(Sighting.item_id.in_(item_ids))
        ).all()
        for item_id, source_key in sighting_rows:
            prefix = (source_key or "").split(":", 1)[0]
            if prefix:
                types_by_item.setdefault(item_id, set()).add(prefix)

    out: list[ArticleSource] = []
    seen_urls: set[str] = set()
    for r in rows:
        if r.url in seen_urls:
            continue  # dedupe by url, keep the first (stable-order) occurrence
        seen_urls.add(r.url)
        out.append(
            ArticleSource(
                title=(r.title or "").strip() or "(untitled)",
                url=r.url,
                source_types=sorted(types_by_item.get(r.id, set())),
                cluster_id=r.cluster_id,
            )
        )

    # Phase 10: append the article's OWN owner-material rows (a flagship article's grounding),
    # oldest-first, after the cluster rows. A URL-bearing owner row is url-deduped against what's
    # already shown; a text/file owner row (no url) is always kept.
    owner_rows = session.execute(
        select(OwnerSource.title, OwnerSource.url, OwnerSource.content)
        .where(OwnerSource.article_id == article_id)
        .order_by(OwnerSource.id.asc())
    ).all()
    for r in owner_rows:
        url = r.url or ""
        if url and url in seen_urls:
            continue
        if url:
            seen_urls.add(url)
        out.append(
            ArticleSource(
                title=(r.title or r.url or "(owner material)"),
                url=url,
                source_types=["owner"],
                cluster_id=None,
            )
        )

    return out


__all__ = [
    "STATUS_SPECTRUM",
    "StoryRow",
    "load_stories",
    "unified_status_counts",
    "source_counts",
    "ArticleView",
    "ArticleVersion",
    "ArticleSource",
    "load_article",
    "article_exists",
    "load_article_versions",
    "load_article_sources",
]
