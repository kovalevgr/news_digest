"""initial schema: pgvector extension + the eight pipeline tables

Revision ID: 0001_initial
Revises:
Create Date: Phase 0
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

from app.llm.config import EMBEDDING_DIM

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # clusters first — items references it.
    op.create_table(
        "clusters",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("topic", sa.String()),
        sa.Column("score", sa.Float()),
        sa.Column("status", sa.String(), nullable=False, server_default="new"),
        sa.Column("triage_title", sa.Text()),
        sa.Column("triage_summary", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "items",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("cluster_id", sa.String(), sa.ForeignKey("clusters.id"), nullable=True),
        sa.Column("title", sa.Text()),
        sa.Column("url", sa.Text()),
        sa.Column("full_text", sa.Text(), nullable=True),
        sa.Column("embedding", Vector(EMBEDDING_DIM), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("fetched_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "sightings",
        sa.Column("item_id", sa.String(), sa.ForeignKey("items.id"), primary_key=True),
        sa.Column("source_key", sa.String(), primary_key=True),
        sa.Column("engagement", JSONB()),
        sa.Column("seen_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "articles",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("piece_type", sa.String()),
        sa.Column("status", sa.String(), nullable=False, server_default="approved"),
        sa.Column("current_draft", sa.Text()),
        sa.Column("embedding", Vector(EMBEDDING_DIM), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "article_clusters",
        sa.Column("article_id", sa.String(), sa.ForeignKey("articles.id"), primary_key=True),
        sa.Column("cluster_id", sa.String(), sa.ForeignKey("clusters.id"), primary_key=True),
    )

    op.create_table(
        "edit_log",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("article_id", sa.String(), sa.ForeignKey("articles.id"), nullable=False),
        sa.Column("instruction", sa.Text()),
        sa.Column("draft_snapshot", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "variants",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("article_id", sa.String(), sa.ForeignKey("articles.id"), nullable=False),
        sa.Column("platform", sa.String()),
        sa.Column("formatted_text", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "cursors",
        sa.Column("source_key", sa.String(), primary_key=True),
        sa.Column("cursor", JSONB()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade():
    for table in (
        "cursors",
        "variants",
        "edit_log",
        "article_clusters",
        "articles",
        "sightings",
        "items",
        "clusters",
    ):
        op.drop_table(table)
    op.execute("DROP EXTENSION IF EXISTS vector")
