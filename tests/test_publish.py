"""Mark-as-published (app.editor.article.publish_article) — Phase 5
(docs/01_technical.md §2 step 7, §3 decision 3; build plan Phase 5).

publish_article is BOOKKEEPING of an external manual act (the owner posted by hand) — NOT
publishing (hard rule 1): it flips status pre_publish → published and computes/stores the article
embedding (role 'embedding'). That embedding is what makes the article retrievable by
app.editor.kb.kb_search when drafting the next piece (docs §3 decision 3 — the published article +
its embedding *is* the KB).

DB-LIGHT by default: the status transitions / embedding behaviour run on a tiny stub session with
a monkeypatched module-level `embed`. The end-to-end "published article becomes KB-retrievable"
check (the build-plan Phase-5 Done criterion) is guarded behind RUN_PG_TESTS and uses the real
embed() with EMBEDDING_PROVIDER=fake.

This is a NEW test file (kept separate from test_editor.py to avoid clashing with the parallel
frontend slice that may be editing that file).
"""
from __future__ import annotations

import os
import uuid

import pytest

from app.editor import article as article_mod
from app.editor.article import publish_article

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"
pg_only = pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")


# --- DB-light: stub session + monkeypatched embed ------------------------------------------


class _StubArticle:
    def __init__(self, *, status="pre_publish", current_draft="A grounded canonical long-read.",
                 embedding=None):
        self.id = "a:stub"
        self.status = status
        self.current_draft = current_draft
        self.embedding = embedding


class _StubSession:
    """Tiny stub: session.get(Article, id) → the article; commit() records."""
    def __init__(self, article):
        self._article = article
        self.committed = False

    def get(self, model, ident):
        return self._article

    def commit(self):
        self.committed = True


def _fake_embed(monkeypatch, vec=None):
    """Monkeypatch the module-level embed so no provider is needed. Returns the list of inputs
    embed() was called with so a test can assert it embedded the canonical."""
    calls = []
    vector = vec if vec is not None else [0.1, 0.2, 0.3]

    def fake_embed(texts):
        calls.append(texts)
        return [vector]

    monkeypatch.setattr(article_mod, "embed", fake_embed)
    return calls


def test_publish_pre_publish_to_published_sets_embedding(monkeypatch):
    calls = _fake_embed(monkeypatch, vec=[0.5, 0.6])
    art = _StubArticle(status="pre_publish", current_draft="Canonical body here.")
    sess = _StubSession(art)

    result = publish_article(sess, "a:stub")
    assert result == "published"
    assert art.status == "published"
    assert art.embedding == [0.5, 0.6]
    assert sess.committed
    # Embedded the canonical text (role 'embedding' is inside embed()).
    assert calls == [["Canonical body here."]] or calls == ["Canonical body here."]


def test_publish_missing_article_raises():
    class _Empty:
        def get(self, model, ident):
            return None
    with pytest.raises(ValueError, match="not found"):
        publish_article(_Empty(), "a:missing")


def test_publish_refuses_drafting(monkeypatch):
    embedded = _fake_embed(monkeypatch)
    sess = _StubSession(_StubArticle(status="drafting"))
    with pytest.raises(ValueError, match="pre_publish"):
        publish_article(sess, "a:stub")
    assert not sess.committed
    assert embedded == []  # never embedded an un-approved article


def test_publish_refuses_approved(monkeypatch):
    embedded = _fake_embed(monkeypatch)
    sess = _StubSession(_StubArticle(status="approved"))
    with pytest.raises(ValueError, match="pre_publish"):
        publish_article(sess, "a:stub")
    assert embedded == []


def test_publish_refuses_empty_draft(monkeypatch):
    embedded = _fake_embed(monkeypatch)
    sess = _StubSession(_StubArticle(status="pre_publish", current_draft="   "))
    with pytest.raises(ValueError, match="empty"):
        publish_article(sess, "a:stub")
    assert not sess.committed
    assert embedded == []  # nothing to embed → never called


def test_publish_idempotent_on_published_with_embedding(monkeypatch):
    # Already published WITH an embedding → no-op, no re-embed.
    embedded = _fake_embed(monkeypatch)
    art = _StubArticle(status="published", embedding=[0.9, 0.9])
    sess = _StubSession(art)
    result = publish_article(sess, "a:stub")
    assert result == "published"
    assert art.embedding == [0.9, 0.9]  # untouched
    assert embedded == []  # no re-embed
    assert not sess.committed  # pure no-op


def test_publish_backfills_missing_embedding_on_published(monkeypatch):
    # Defensive: published but embedding NULL → recompute + store (must be KB-retrievable).
    _fake_embed(monkeypatch, vec=[0.7, 0.8])
    art = _StubArticle(status="published", embedding=None, current_draft="Body to embed.")
    sess = _StubSession(art)
    result = publish_article(sess, "a:stub")
    assert result == "published"
    assert art.embedding == [0.7, 0.8]
    assert sess.committed


def test_publish_published_empty_draft_missing_embedding_raises(monkeypatch):
    # Defensive backfill path can't embed an empty draft either.
    embedded = _fake_embed(monkeypatch)
    art = _StubArticle(status="published", embedding=None, current_draft="")
    sess = _StubSession(art)
    with pytest.raises(ValueError, match="nothing to embed"):
        publish_article(sess, "a:stub")
    assert embedded == []


# --- DB-backed (guarded): real publish → KB-retrievable ------------------------------------


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


def _pre_publish_article(session, *, draft):
    from app.db.models import Article
    from app.editor.article import new_article_id

    aid = new_article_id()
    session.add(Article(id=aid, piece_type="hot_news", status="pre_publish",
                        current_draft=draft, embedding=None))
    session.commit()
    return aid


@pg_only
def test_publish_real_then_kb_retrievable(session):
    """The build-plan Phase-5 Done criterion: after marking published, the article is retrievable
    via kb_search (with the real embed(), EMBEDDING_PROVIDER=fake). Closes the loop to app.editor.kb."""
    from app.db.models import Article
    from app.editor.kb import kb_search

    draft = (
        "A published long-read about retrieval augmented generation and vector search, "
        f"with a unique marker {uuid.uuid4().hex}."
    )
    aid = _pre_publish_article(session, draft=draft)

    # Before publish: not in the KB (no embedding yet).
    pre = {h.article_id for h in kb_search(session, "retrieval augmented generation", top_k=50)}
    assert aid not in pre

    result = publish_article(session, aid)
    assert result == "published"

    session.expire_all()
    art = session.get(Article, aid)
    assert art.status == "published"
    assert art.embedding is not None

    # After publish: retrievable via kb_search (this is the Phase-5 Done criterion).
    hits = kb_search(session, "retrieval augmented generation and vector search", top_k=50)
    assert aid in {h.article_id for h in hits}


@pg_only
def test_publish_real_idempotent(session):
    from app.db.models import Article

    aid = _pre_publish_article(session, draft="Some grounded canonical content for the KB.")
    publish_article(session, aid)
    session.expire_all()
    first_embedding = list(session.get(Article, aid).embedding)

    # Second call is a no-op; status stays published, embedding unchanged.
    assert publish_article(session, aid) == "published"
    session.expire_all()
    art = session.get(Article, aid)
    assert art.status == "published"
    assert list(art.embedding) == first_embedding
