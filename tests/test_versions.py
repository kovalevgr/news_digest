"""Article version history + restore (Feature A) and source links (Feature B).

Feature A — the version trail is the edit_log: every article's first draft is anchored by a
GENESIS_INSTRUCTION row (writer-agent draft, or the digest rollup), iterate drops one as a safety
net if the first edit would otherwise lose the pre-edit text, `load_article_versions` reads the
trail oldest-first (with a synthetic-genesis fallback for a zero-edit_log article), and
`restore_article_version` rolls the working draft back to a recorded snapshot (append-only — the
restore is itself logged; refuses on a published canonical). Restore/version are BOOKKEEPING only
(hard rule 1 — nothing publishes/posts), coordinated through Postgres.

Feature B — `load_article_sources` walks article_clusters → clusters → items and surfaces each
source URL with the distinct platform-type prefixes (the bit before ':' in its sightings'
source_keys), deduped by url, for the editor's sources panel.

DB-LIGHT by default (the restore transitions run on a tiny stub session, mirroring
tests/test_publish.py). The reads (`load_article_versions` ordering / fallback,
`load_article_sources` dedupe / multi-cluster) and the genesis-on-draft / genesis-on-digest /
iterate-safety-net behaviour are exercised against real Postgres behind RUN_PG_TESTS.

This is a NEW test file (kept separate from test_editor.py / test_web.py so it doesn't clash with
the parallel frontend slice editing the UI files).
"""
from __future__ import annotations

import os
import uuid

import pytest

from app.editor.article import GENESIS_INSTRUCTION, restore_article_version

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"
pg_only = pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")


# --- DB-light: restore_article_version on a stub session ------------------------------------


class _StubEditLog:
    """A captured edit_log row (mirrors the ORM fields restore reads/writes)."""
    def __init__(self, *, id, article_id, instruction, draft_snapshot):
        self.id = id
        self.article_id = article_id
        self.instruction = instruction
        self.draft_snapshot = draft_snapshot


class _StubArticle:
    def __init__(self, *, status="drafting", current_draft="# Draft\n\ncurrent body"):
        self.id = "a:stub"
        self.status = status
        self.current_draft = current_draft


class _RestoreSession:
    """A stub sufficient for restore_article_version: session.get(Article|EditLog, id) resolves
    from a small registry; session.add captures the new (restore) row; commit() records."""
    def __init__(self, *, article, rows=None):
        from app.db.models import Article, EditLog
        self._Article = Article
        self._EditLog = EditLog
        self._article = article
        self._rows = {r.id: r for r in (rows or [])}
        self.added = []
        self.committed = False

    def get(self, model, ident):
        if model is self._Article:
            return self._article if self._article is not None and ident == self._article.id else (
                self._article if self._article is not None else None
            )
        if model is self._EditLog:
            return self._rows.get(ident)
        return None

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.committed = True


def _added_edit_log(session):
    from app.db.models import EditLog
    return [o for o in session.added if isinstance(o, EditLog)]


def test_restore_sets_current_draft_and_appends_row():
    art = _StubArticle(status="drafting", current_draft="LATEST body")
    row = _StubEditLog(id=7, article_id="a:stub", instruction="[genesis draft]",
                       draft_snapshot="THE ORIGINAL first draft")
    sess = _RestoreSession(article=art, rows=[row])

    restored = restore_article_version(sess, "a:stub", 7)

    # The working draft rolled back to the snapshot, and the function returned it.
    assert restored == "THE ORIGINAL first draft"
    assert art.current_draft == "THE ORIGINAL first draft"
    assert sess.committed
    # Restore is append-only: a NEW edit_log row records the restore (referencing the id).
    appended = _added_edit_log(sess)
    assert len(appended) == 1
    assert appended[0].article_id == "a:stub"
    assert "restored version #7" in appended[0].instruction
    assert appended[0].draft_snapshot == "THE ORIGINAL first draft"


def test_restore_null_snapshot_restores_empty_string():
    art = _StubArticle(current_draft="body")
    row = _StubEditLog(id=3, article_id="a:stub", instruction="[genesis draft]",
                       draft_snapshot=None)
    sess = _RestoreSession(article=art, rows=[row])
    restored = restore_article_version(sess, "a:stub", 3)
    assert restored == ""
    assert art.current_draft == ""


def test_restore_refuses_on_published():
    art = _StubArticle(status="published", current_draft="published canonical")
    row = _StubEditLog(id=1, article_id="a:stub", instruction="[genesis draft]",
                       draft_snapshot="older text")
    sess = _RestoreSession(article=art, rows=[row])
    with pytest.raises(ValueError, match="published"):
        restore_article_version(sess, "a:stub", 1)
    assert art.current_draft == "published canonical"  # unchanged
    assert not sess.committed
    assert _added_edit_log(sess) == []


def test_restore_missing_article_raises():
    sess = _RestoreSession(article=None)
    with pytest.raises(ValueError, match="not found"):
        restore_article_version(sess, "a:nope", 1)


def test_restore_missing_edit_log_row_raises():
    art = _StubArticle()
    sess = _RestoreSession(article=art, rows=[])  # no rows
    with pytest.raises(ValueError, match="not found"):
        restore_article_version(sess, "a:stub", 99)
    assert not sess.committed


def test_restore_cross_article_row_refused():
    """A version id that belongs to ANOTHER article must be refused (no cross-pollination)."""
    art = _StubArticle()
    row = _StubEditLog(id=5, article_id="a:OTHER", instruction="[genesis draft]",
                       draft_snapshot="someone else's text")
    sess = _RestoreSession(article=art, rows=[row])
    with pytest.raises(ValueError, match="belongs to article"):
        restore_article_version(sess, "a:stub", 5)
    assert art.current_draft == "# Draft\n\ncurrent body"  # untouched
    assert not sess.committed


# --- DB-backed (guarded): the loaders + genesis-on-draft / digest / iterate safety net -------


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


def _make_article(session, *, status="drafting", piece_type="hot_news", draft="# A\n\nbody"):
    from app.db.models import Article
    from app.editor.article import new_article_id

    aid = new_article_id()
    session.add(Article(id=aid, piece_type=piece_type, status=status, current_draft=draft))
    session.flush()
    return aid


def _add_edit(session, article_id, instruction, snapshot):
    from app.db.models import EditLog

    row = EditLog(article_id=article_id, instruction=instruction, draft_snapshot=snapshot)
    session.add(row)
    session.flush()
    return row.id


# load_article_versions -----------------------------------------------------------------------


@pg_only
def test_load_versions_orders_oldest_first_and_marks_genesis(session):
    from app.web.queries import load_article_versions

    aid = _make_article(session, draft="latest")
    _add_edit(session, aid, GENESIS_INSTRUCTION, "v1 genesis snapshot")
    _add_edit(session, aid, "sharpen intro", "v2 snapshot")
    _add_edit(session, aid, "cut the close", "v3 snapshot")

    versions = load_article_versions(session, aid)
    assert [v.seq for v in versions] == [1, 2, 3]
    assert [v.instruction for v in versions] == [
        GENESIS_INSTRUCTION, "sharpen intro", "cut the close"
    ]
    assert [v.draft for v in versions] == ["v1 genesis snapshot", "v2 snapshot", "v3 snapshot"]
    # Only the first row is the genesis.
    assert [v.is_genesis for v in versions] == [True, False, False]
    # Real edit_log ids carried (restorable handles), created_at populated.
    assert all(v.edit_log_id is not None for v in versions)
    assert all(v.created_at is not None for v in versions)


@pg_only
def test_load_versions_synthetic_genesis_for_zero_edit_log(session):
    """An article with NO edit_log rows still shows ONE (synthetic) version from current_draft."""
    from app.web.queries import load_article_versions

    aid = _make_article(session, draft="# Only\n\nthe current draft, never edited")
    versions = load_article_versions(session, aid)
    assert len(versions) == 1
    (v,) = versions
    assert v.edit_log_id is None  # synthetic — there is no row to restore
    assert v.seq == 1
    assert v.is_genesis is True
    assert v.instruction == GENESIS_INSTRUCTION
    assert v.draft == "# Only\n\nthe current draft, never edited"
    assert v.created_at is not None


@pg_only
def test_load_versions_empty_for_missing_article(session):
    from app.web.queries import load_article_versions

    assert load_article_versions(session, "a:does-not-exist") == []


@pg_only
def test_load_versions_first_genesis_only_when_multiple_genesis_strings(session):
    """If a later instruction happens to equal the genesis marker, only the FIRST row is flagged."""
    from app.web.queries import load_article_versions

    aid = _make_article(session)
    _add_edit(session, aid, GENESIS_INSTRUCTION, "first")
    _add_edit(session, aid, GENESIS_INSTRUCTION, "second (not the root)")
    versions = load_article_versions(session, aid)
    assert [v.is_genesis for v in versions] == [True, False]


# genesis capture on draft / digest / iterate (DB-backed) -------------------------------------


def _scripted_text_response(text):
    from types import SimpleNamespace
    return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)])


def _approved_cluster_with_item(session, *, full_text="A grounded source fact."):
    from app.adapters.base import Item as AdapterItem, item_id
    from app.db.models import Cluster, Item as ItemModel
    from app.researcher.cluster import new_cluster_id
    from app.researcher.store import upsert_item_and_sighting

    cid = new_cluster_id()
    session.add(Cluster(id=cid, status="approved", topic="ai", score=0.5,
                        triage_title="Approved", triage_summary="s"))
    session.flush()
    url = f"https://example.com/src/{uuid.uuid4().hex}"
    upsert_item_and_sighting(session, AdapterItem(url=url, title="Source headline"), "rss:a")
    session.flush()
    item = session.get(ItemModel, item_id(url))
    item.cluster_id = cid
    item.full_text = full_text
    session.flush()
    session.commit()
    return cid


@pg_only
def test_draft_records_genesis_version(session, monkeypatch):
    """draft_article anchors the version trail with exactly one genesis row carrying the first draft."""
    from app.editor import create_article_for_cluster
    from app.editor import draft as draft_mod
    from app.web.queries import load_article_versions

    cid = _approved_cluster_with_item(session)
    aid = create_article_for_cluster(session, cid)
    monkeypatch.setattr(
        draft_mod, "generate",
        lambda **kw: _scripted_text_response("# First Draft\n\nGrounded body."),
    )
    draft_mod.draft_article(session, aid)

    session.expire_all()
    versions = load_article_versions(session, aid)
    assert len(versions) == 1
    assert versions[0].is_genesis is True
    assert versions[0].instruction == GENESIS_INSTRUCTION
    assert "First Draft" in versions[0].draft
    assert versions[0].edit_log_id is not None  # a real, restorable row (not synthetic)


@pg_only
def test_draft_genesis_is_idempotent_across_redraft(session, monkeypatch):
    """Re-drafting never adds a SECOND genesis (idempotent _ensure_genesis)."""
    from app.editor import create_article_for_cluster
    from app.editor import draft as draft_mod
    from app.db.models import EditLog

    cid = _approved_cluster_with_item(session)
    aid = create_article_for_cluster(session, cid)
    monkeypatch.setattr(draft_mod, "generate",
                        lambda **kw: _scripted_text_response("# Draft one\n\nbody"))
    draft_mod.draft_article(session, aid)
    monkeypatch.setattr(draft_mod, "generate",
                        lambda **kw: _scripted_text_response("# Draft two\n\nbody"))
    draft_mod.draft_article(session, aid)

    session.expire_all()
    genesis_rows = session.execute(
        EditLog.__table__.select()
        .where(EditLog.article_id == aid)
        .where(EditLog.instruction == GENESIS_INSTRUCTION)
    ).all()
    assert len(genesis_rows) == 1


@pg_only
def test_iterate_safety_net_genesis_then_edit_on_fresh_article(session, monkeypatch):
    """A fresh article (no draft genesis) edited for the FIRST time ends with TWO rows: the
    pre-edit genesis (the safety net) then the edit — the pre-image is never lost."""
    from app.editor import iterate as it_mod
    from app.editor import context as ctx
    from app.web.queries import load_article_versions

    aid = _make_article(session, draft="# Pre-edit\n\noriginal body")
    # The article has no linked cluster and no owner material → load_grounding_bundle returns an
    # empty bundle from the real DB; iterate edits the existing draft regardless.
    monkeypatch.setattr(it_mod, "load_voice_files", lambda: ctx.VoiceFiles())
    monkeypatch.setattr(it_mod, "generate",
                        lambda **kw: _scripted_text_response("# Pre-edit\n\nrevised body"))

    result = it_mod.iterate_article(session, aid, "tighten it")
    assert "revised body" in result.draft

    session.expire_all()
    versions = load_article_versions(session, aid)
    assert len(versions) == 2
    # Genesis carries the PRE-edit text; the edit carries the instruction + revised snapshot.
    assert versions[0].is_genesis is True
    assert versions[0].instruction == GENESIS_INSTRUCTION
    assert versions[0].draft == "# Pre-edit\n\noriginal body"
    assert versions[1].instruction == "tighten it"
    assert "revised body" in versions[1].draft


@pg_only
def test_digest_records_genesis_version(session, monkeypatch):
    """run_digest anchors its digest article's version trail with one genesis row = the rollup."""
    import app.digest.run as run_mod
    from app.web.queries import load_article_versions
    from types import SimpleNamespace

    def _digest_cfg(**kw):
        return SimpleNamespace(window_days=30, top_n=10, schedule="sun 09:00", **kw)

    def _make_cluster(topic):
        from app.db.models import Cluster
        from app.researcher.cluster import new_cluster_id
        cid = new_cluster_id()
        session.add(Cluster(id=cid, status="new", topic=topic, score=0.9,
                            triage_title="A story", triage_summary="what it is"))
        session.flush()
        return cid

    topic = f"vtopic-{uuid.uuid4().hex[:8]}"
    _make_cluster(topic)
    monkeypatch.setattr(run_mod, "generate",
                        lambda messages, role: "## Weekly digest\n\n- a story")

    result = run_mod.run_digest(session, topic, _digest_cfg())
    assert result is not None

    session.expire_all()
    versions = load_article_versions(session, result.article_id)
    assert len(versions) == 1
    assert versions[0].is_genesis is True
    assert versions[0].draft == "## Weekly digest\n\n- a story"
    assert versions[0].edit_log_id is not None


# restore against real Postgres ---------------------------------------------------------------


@pg_only
def test_restore_end_to_end_in_postgres(session):
    from app.db.models import Article
    from app.web.queries import load_article_versions

    aid = _make_article(session, draft="latest body")
    genesis_id = _add_edit(session, aid, GENESIS_INSTRUCTION, "the original draft")
    _add_edit(session, aid, "edit one", "edited body")
    session.commit()

    restored = restore_article_version(session, aid, genesis_id)
    assert restored == "the original draft"

    session.expire_all()
    assert session.get(Article, aid).current_draft == "the original draft"
    # The restore appended a third version (append-only trail).
    versions = load_article_versions(session, aid)
    assert len(versions) == 3
    assert versions[-1].draft == "the original draft"
    assert f"restored version #{genesis_id}" in versions[-1].instruction


@pg_only
def test_restore_refuses_published_in_postgres(session):
    aid = _make_article(session, status="published", draft="published canonical")
    rid = _add_edit(session, aid, GENESIS_INSTRUCTION, "older")
    session.commit()
    with pytest.raises(ValueError, match="published"):
        restore_article_version(session, aid, rid)


# --- Feature B: load_article_sources (DB-backed) --------------------------------------------


def _item_in_cluster(session, cluster_id, *, url, title, source_keys):
    """Create one item in a cluster with the given sighting source_keys."""
    from app.adapters.base import Item as AdapterItem, item_id
    from app.db.models import Item as ItemModel
    from app.researcher.store import upsert_item_and_sighting

    for sk in source_keys:
        upsert_item_and_sighting(session, AdapterItem(url=url, title=title), sk)
    session.flush()
    item = session.get(ItemModel, item_id(url))
    item.cluster_id = cluster_id
    session.flush()
    return item.id


def _bare_cluster(session, *, topic="ai"):
    from app.db.models import Cluster
    from app.researcher.cluster import new_cluster_id
    cid = new_cluster_id()
    session.add(Cluster(id=cid, status="approved", topic=topic, score=0.5))
    session.flush()
    return cid


def _link(session, article_id, cluster_id):
    from app.db.models import ArticleCluster
    session.add(ArticleCluster(article_id=article_id, cluster_id=cluster_id))
    session.flush()


@pg_only
def test_load_sources_returns_items_with_source_types(session):
    from app.web.queries import load_article_sources

    aid = _make_article(session)
    cid = _bare_cluster(session)
    _link(session, aid, cid)
    url = f"https://ex.com/a/{uuid.uuid4().hex}"
    # Same URL seen by two sources → two sightings, one item, two source_types.
    _item_in_cluster(session, cid, url=url, title="The story",
                     source_keys=['rss:{"url":"x"}', 'x_user:{"handle":"y"}'])
    session.commit()

    sources = load_article_sources(session, aid)
    assert len(sources) == 1
    s = sources[0]
    assert s.title == "The story"
    assert s.url == url
    assert s.cluster_id == cid
    # distinct prefix-before-':' of the source_keys, sorted.
    assert s.source_types == ["rss", "x_user"]


@pg_only
def test_load_sources_multi_cluster_lists_all_clusters_sources(session):
    """A digest article spanning many clusters lists EVERY cluster's sources, in stable order."""
    from app.web.queries import load_article_sources

    aid = _make_article(session, piece_type="digest")
    c1 = _bare_cluster(session)
    c2 = _bare_cluster(session)
    _link(session, aid, c1)
    _link(session, aid, c2)
    url_a = f"https://ex.com/a/{uuid.uuid4().hex}"
    url_b = f"https://ex.com/b/{uuid.uuid4().hex}"
    _item_in_cluster(session, c1, url=url_a, title="Story A", source_keys=["rss:a"])
    _item_in_cluster(session, c2, url=url_b, title="Story B", source_keys=["hn:b"])
    session.commit()

    sources = load_article_sources(session, aid)
    assert {s.url for s in sources} == {url_a, url_b}
    # Multi-cluster (digest): both clusters' sources are listed.
    assert {s.cluster_id for s in sources} == {c1, c2}
    # Stable order: by cluster_id, then title.
    assert [s.cluster_id for s in sources] == sorted(s.cluster_id for s in sources)


@pg_only
def test_load_sources_dedupes_by_url(session):
    """A URL appearing more than once across the article's items is surfaced ONCE (deduped by url).

    Item identity IS the URL hash, so the same item lands in at most one cluster — to produce the
    same URL twice in the walk we put one item in cluster c1 and a SECOND item carrying the SAME url
    string (forced) under c2, then assert the loader collapses them to a single ArticleSource."""
    from app.db.models import Item as ItemModel
    from app.web.queries import load_article_sources

    aid = _make_article(session, piece_type="digest")
    c1 = _bare_cluster(session)
    c2 = _bare_cluster(session)
    _link(session, aid, c1)
    _link(session, aid, c2)
    dup_url = f"https://ex.com/dup/{uuid.uuid4().hex}"
    _item_in_cluster(session, c1, url=dup_url, title="Story A", source_keys=["rss:a"])
    # A second, distinct item row carrying the same url string but a different id, placed in c2.
    session.add(ItemModel(id=f"i:{uuid.uuid4().hex}", cluster_id=c2, title="Story B", url=dup_url))
    session.commit()

    sources = load_article_sources(session, aid)
    # Deduped by url → exactly one entry for the duplicated url (first in stable order kept).
    assert len([s for s in sources if s.url == dup_url]) == 1


@pg_only
def test_load_sources_untitled_and_empty_cases(session):
    from app.web.queries import load_article_sources

    # Missing article → [].
    assert load_article_sources(session, "a:none") == []

    # Article with a linked cluster but no items → [].
    aid = _make_article(session)
    cid = _bare_cluster(session)
    _link(session, aid, cid)
    session.commit()
    assert load_article_sources(session, aid) == []

    # An item with no title → "(untitled)".
    url = f"https://ex.com/nt/{uuid.uuid4().hex}"
    _item_in_cluster(session, cid, url=url, title=None, source_keys=["github:z"])
    session.commit()
    sources = load_article_sources(session, aid)
    assert len(sources) == 1
    assert sources[0].title == "(untitled)"
    assert sources[0].source_types == ["github"]


# --- Phase 10: load_article_sources surfaces owner material ---------------------------------


@pg_only
def test_load_sources_includes_owner_material(session):
    """A flagship article's owner material surfaces as source_types=['owner'], cluster_id None,
    after any cluster rows, oldest-first."""
    from app.editor.sources import attach_owner_source, create_flagship_article
    from app.web.queries import load_article_sources

    aid = create_flagship_article(session)
    attach_owner_source(session, aid, kind="text", content="pasted notes", title="My notes")
    url = f"https://ex.com/owner/{uuid.uuid4().hex}"
    attach_owner_source(session, aid, kind="url", content="fetched body", url=url)
    session.commit()

    sources = load_article_sources(session, aid)
    assert len(sources) == 2
    assert all(s.source_types == ["owner"] for s in sources)
    assert all(s.cluster_id is None for s in sources)
    # oldest-first: the text note, then the url.
    assert sources[0].title == "My notes"
    assert sources[0].url == ""
    assert sources[1].title == url  # title falls back to url
    assert sources[1].url == url


@pg_only
def test_load_sources_mixes_cluster_items_then_owner_rows(session):
    """An article with BOTH a cluster item and owner material lists the cluster item FIRST, then the
    owner row."""
    from app.editor.sources import attach_owner_source
    from app.web.queries import load_article_sources

    aid = _make_article(session)
    cid = _bare_cluster(session)
    _link(session, aid, cid)
    item_url = f"https://ex.com/cl/{uuid.uuid4().hex}"
    _item_in_cluster(session, cid, url=item_url, title="Cluster story", source_keys=["rss:a"])
    attach_owner_source(session, aid, kind="text", content="owner body", title="Owner note")
    session.commit()

    sources = load_article_sources(session, aid)
    assert len(sources) == 2
    # cluster row first
    assert sources[0].url == item_url
    assert sources[0].source_types == ["rss"]
    assert sources[0].cluster_id == cid
    # owner row second
    assert sources[1].title == "Owner note"
    assert sources[1].source_types == ["owner"]
    assert sources[1].cluster_id is None
