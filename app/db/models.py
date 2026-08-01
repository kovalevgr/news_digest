"""ORM models for the eight pipeline tables (docs/01_technical.md §3).

The hand-written migration in migrations/versions/0001_initial_schema.py is the
authoritative DDL; these models must mirror it. Embedding dimension is sourced
once from app.llm.config.EMBEDDING_DIM so schema and embedder never drift.
"""
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

from app.db.base import Base
from app.llm.config import EMBEDDING_DIM


class Cluster(Base):
    """A story. Dedup groups items into one cluster; triage/ranking/Gate-1 live here."""
    __tablename__ = "clusters"

    id = Column(String, primary_key=True)
    topic = Column(String)
    score = Column(Float)  # blended cross-source ranking score
    status = Column(String, nullable=False, server_default="new")  # new -> sent -> approved/skipped
    triage_title = Column(Text)     # written by the researcher's triage-summary call
    triage_summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Item(Base):
    """One row per canonical URL (content identity: text + embedding)."""
    __tablename__ = "items"

    id = Column(String, primary_key=True)  # hash of the canonical URL
    cluster_id = Column(String, ForeignKey("clusters.id"), nullable=True)
    title = Column(Text)
    url = Column(Text)
    full_text = Column(Text, nullable=True)  # pass-2 only, for approved stories
    embedding = Column(Vector(EMBEDDING_DIM), nullable=True)  # for dedup
    published_at = Column(DateTime(timezone=True), nullable=True)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())  # first seen


class Sighting(Base):
    """One source's observation of an item. Cross-source frequency counts sightings."""
    __tablename__ = "sightings"

    item_id = Column(String, ForeignKey("items.id"), primary_key=True)
    source_key = Column(String, primary_key=True)  # references a config source (string, not FK)
    engagement = Column(JSONB)  # that platform's signals (points, comments, ...)
    seen_at = Column(DateTime(timezone=True), server_default=func.now())


class Article(Base):
    """The working record through the lifecycle; once published, the knowledge base."""
    __tablename__ = "articles"

    id = Column(String, primary_key=True)
    piece_type = Column(String)  # hot_news / digest / project_post
    status = Column(String, nullable=False, server_default="approved")  # approved->drafting->pre_publish->published
    current_draft = Column(Text)  # the canonical long-read
    embedding = Column(Vector(EMBEDDING_DIM), nullable=True)  # set when published, for KB retrieval
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ArticleCluster(Base):
    """article <-> cluster join. hot_news maps to one cluster; digest aggregates many."""
    __tablename__ = "article_clusters"

    article_id = Column(String, ForeignKey("articles.id"), primary_key=True)
    cluster_id = Column(String, ForeignKey("clusters.id"), primary_key=True)


class OwnerSource(Base):
    """Owner-supplied grounding material for a FLAGSHIP article (Phase 10).

    A flagship article ('own-material' intake) has no cluster — its grounding corpus is the
    owner's own text/file/URL artefacts, stored here, one row per attached source. This is the
    first ON DELETE CASCADE FK in the schema (deliberate: owner material dies with its article)."""
    __tablename__ = "article_sources"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    article_id = Column(String, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    kind = Column(String, nullable=False)  # "text" | "file" | "url"
    title = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    content = Column(Text, nullable=False)  # the grounding text (pasted/file text or fetched URL text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EditLog(Base):
    """Iteration trail and voice signal: every owner instruction during editing."""
    __tablename__ = "edit_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    article_id = Column(String, ForeignKey("articles.id"), nullable=False)
    instruction = Column(Text)
    draft_snapshot = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Variant(Base):
    """Per-platform formatted output derived from the canonical."""
    __tablename__ = "variants"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    article_id = Column(String, ForeignKey("articles.id"), nullable=False)
    platform = Column(String)  # linkedin / medium / reddit
    formatted_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Cursor(Base):
    """Per-source poll state — the only config-adjacent thing that persists."""
    __tablename__ = "cursors"

    source_key = Column(String, primary_key=True)  # derived from the source's identity fields
    cursor = Column(JSONB)  # since_id / last-seen id / etag + last_modified
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
