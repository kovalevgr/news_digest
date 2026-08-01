"""Flagship intake — owner-material storage + intake (app.editor.sources) — build plan Phase 10.

The flagship flow grounds a draft in the OWNER'S OWN material (pasted text / an uploaded file / a
fetched URL) instead of an approved cluster. This slice is deterministic storage + parsing code
(NOT an agent, NOT a model call): mint a cluster-less article, attach owner sources, parse an
uploaded file, load the material back as grounding items.

DB-LIGHT by default (build plan testing note: the default suite needs no live Postgres). The
validations, the pure file parser, and attach_owner_url's fetch seam run on a tiny stub session /
without a DB; the DB-backed pieces (create_flagship_article writes a real row, the ON DELETE
CASCADE) are guarded behind RUN_PG_TESTS like the other PG tests.
"""
from __future__ import annotations

import json
import os

import pytest

from app.editor import sources as sources_mod
from app.editor.sources import (
    attach_owner_source,
    attach_owner_url,
    create_flagship_article,
    load_owner_sources,
    parse_uploaded_file,
)
from app.fetcher import DEFAULT_FETCH_MAX_CHARS

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"
pg_only = pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")


# --- DB-light stubs --------------------------------------------------------------------------


class _StubArticle:
    def __init__(self, article_id="a:flagship"):
        self.id = article_id


class _StubSession:
    """Tiny stub: session.get(Article, id) → the article (or None); session.add assigns an
    autoincrement id to an OwnerSource and captures it; commit records. Enough for
    attach_owner_source's validate → add → commit → return row.id path without Postgres."""
    def __init__(self, article):
        self._article = article
        self.added = []
        self.committed = False
        self._next_id = 1

    def get(self, model, ident):
        return self._article

    def add(self, obj):
        if getattr(obj, "id", None) is None:
            obj.id = self._next_id
            self._next_id += 1
        self.added.append(obj)

    def commit(self):
        self.committed = True


# --- parse_uploaded_file (PURE) --------------------------------------------------------------


def test_parse_uploaded_file_md_and_txt_passthrough():
    assert parse_uploaded_file("notes.md", b"# Title\n\nbody text") == "# Title\n\nbody text"
    assert parse_uploaded_file("run.log", b"line1\nline2") == "line1\nline2"
    assert parse_uploaded_file("doc.markdown", b"## H\n\np") == "## H\n\np"
    assert parse_uploaded_file("a.txt", b"plain") == "plain"


def test_parse_uploaded_file_bad_bytes_do_not_raise():
    # An invalid utf-8 byte must degrade (errors='replace'), never raise.
    out = parse_uploaded_file("x.txt", b"ok\xffbad")
    assert "ok" in out and "bad" in out


def test_parse_uploaded_file_ipynb_concats_code_and_markdown_cells():
    nb = {
        "cells": [
            {"cell_type": "markdown", "source": ["# Intro\n", "some prose"]},
            {"cell_type": "code", "source": "x = 1\nprint(x)"},
            {"cell_type": "raw", "source": "RAW_SHOULD_BE_SKIPPED"},
            {"cell_type": "markdown", "source": []},  # empty cell skipped
        ],
        "metadata": {},
    }
    out = parse_uploaded_file("analysis.ipynb", json.dumps(nb).encode("utf-8"))
    assert "# Intro\nsome prose" in out
    assert "x = 1\nprint(x)" in out
    assert "RAW_SHOULD_BE_SKIPPED" not in out  # only code + markdown cells
    # Cells separated by a blank line.
    assert "\n\n" in out


def test_parse_uploaded_file_ipynb_malformed_degrades():
    # Not valid JSON → best-effort plain decode, no raise.
    out = parse_uploaded_file("broken.ipynb", b"not json at all")
    assert "not json at all" in out


def test_parse_uploaded_file_unknown_extension_decodes():
    assert parse_uploaded_file("weird.xyz", b"still text") == "still text"


def test_parse_uploaded_file_caps_length():
    out = parse_uploaded_file("big.txt", b"a" * (DEFAULT_FETCH_MAX_CHARS + 500))
    assert len(out) == DEFAULT_FETCH_MAX_CHARS


# --- attach_owner_source: validations --------------------------------------------------------


def test_attach_owner_source_rejects_bad_kind():
    session = _StubSession(_StubArticle())
    with pytest.raises(ValueError, match="kind"):
        attach_owner_source(session, "a:flagship", kind="bogus", content="hello")


def test_attach_owner_source_rejects_empty_content():
    session = _StubSession(_StubArticle())
    with pytest.raises(ValueError, match="empty"):
        attach_owner_source(session, "a:flagship", kind="text", content="   ")


def test_attach_owner_source_rejects_missing_article():
    session = _StubSession(None)  # session.get → None
    with pytest.raises(ValueError, match="not found"):
        attach_owner_source(session, "a:nope", kind="text", content="hello")


def test_attach_owner_source_persists_and_caps_and_returns_id():
    from app.db.models import OwnerSource

    session = _StubSession(_StubArticle())
    sid = attach_owner_source(
        session, "a:flagship", kind="text", content="  grounded text  ", title="My note"
    )
    assert isinstance(sid, int)
    assert session.committed
    (row,) = [o for o in session.added if isinstance(o, OwnerSource)]
    assert row.kind == "text"
    assert row.content == "grounded text"  # stripped
    assert row.title == "My note"
    assert row.url is None


def test_attach_owner_source_caps_content_length():
    from app.db.models import OwnerSource

    session = _StubSession(_StubArticle())
    attach_owner_source(
        session, "a:flagship", kind="file", content="b" * (DEFAULT_FETCH_MAX_CHARS + 100)
    )
    (row,) = [o for o in session.added if isinstance(o, OwnerSource)]
    assert len(row.content) == DEFAULT_FETCH_MAX_CHARS


# --- attach_owner_url: fetch seam ------------------------------------------------------------


def test_attach_owner_url_fetches_and_attaches(monkeypatch):
    from app.db.models import OwnerSource

    session = _StubSession(_StubArticle())
    monkeypatch.setattr(
        sources_mod, "fetch_full_text", lambda url, client=None: "extracted body text"
    )
    sid = attach_owner_url(session, "a:flagship", "https://ex.com/post")
    assert isinstance(sid, int)
    (row,) = [o for o in session.added if isinstance(o, OwnerSource)]
    assert row.kind == "url"
    assert row.url == "https://ex.com/post"
    assert row.content == "extracted body text"


def test_attach_owner_url_raises_on_empty_extraction(monkeypatch):
    session = _StubSession(_StubArticle())
    monkeypatch.setattr(sources_mod, "fetch_full_text", lambda url, client=None: None)
    with pytest.raises(ValueError, match="could not extract"):
        attach_owner_url(session, "a:flagship", "https://ex.com/paywalled")


# --- DB-backed (guarded): create_flagship_article, load_owner_sources, CASCADE ----------------


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


@pg_only
def test_create_flagship_article_no_cluster_link(session):
    from app.db.models import Article, ArticleCluster

    aid = create_flagship_article(session)

    art = session.get(Article, aid)
    assert art is not None
    assert art.status == "drafting"
    assert art.piece_type == "tech_explainer"
    assert art.current_draft is None
    # NO ArticleCluster row (a flagship article has no cluster).
    links = session.execute(
        ArticleCluster.__table__.select().where(ArticleCluster.article_id == aid)
    ).all()
    assert links == []


@pg_only
def test_create_flagship_article_rejects_unknown_piece_type(session):
    with pytest.raises(ValueError, match="unknown piece_type"):
        create_flagship_article(session, piece_type="bogus")


@pg_only
def test_load_owner_sources_maps_to_owner_items(session):
    aid = create_flagship_article(session)
    attach_owner_source(session, aid, kind="text", content="first note", title="Note A")
    attach_owner_source(session, aid, kind="url", content="fetched body", url="https://ex.com/x")

    items = load_owner_sources(session, aid)
    assert len(items) == 2
    # oldest-first; all owner kind.
    assert all(it.kind == "owner" for it in items)
    assert items[0].title == "Note A"
    assert items[0].full_text == "first note"
    assert items[0].url == ""
    # title falls back to url when no title.
    assert items[1].title == "https://ex.com/x"
    assert items[1].url == "https://ex.com/x"
    assert items[1].full_text == "fetched body"


@pg_only
def test_load_owner_sources_title_fallback_constant(session):
    aid = create_flagship_article(session)
    # No title, no url → "(owner material)".
    attach_owner_source(session, aid, kind="text", content="bare paste")
    items = load_owner_sources(session, aid)
    assert items[0].title == "(owner material)"


@pg_only
def test_delete_article_cascades_owner_sources(session):
    """The ON DELETE CASCADE FK: deleting an Article drops its article_sources rows."""
    from sqlalchemy import func, select

    from app.db.models import Article, OwnerSource

    aid = create_flagship_article(session)
    attach_owner_source(session, aid, kind="text", content="material one")
    attach_owner_source(session, aid, kind="text", content="material two")
    assert session.execute(
        select(func.count()).select_from(OwnerSource).where(OwnerSource.article_id == aid)
    ).scalar_one() == 2

    session.delete(session.get(Article, aid))
    session.commit()

    assert session.execute(
        select(func.count()).select_from(OwnerSource).where(OwnerSource.article_id == aid)
    ).scalar_one() == 0
