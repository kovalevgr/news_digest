"""article_sources: owner-supplied grounding material for flagship articles

Revision ID: 0002_article_sources
Revises: 0001_initial
Create Date: Phase 10

The flagship intake flow ('own-material' → canonical draft) grounds a draft in the owner's own
text/file/URL artefacts instead of a cluster. Those artefacts live here, one row per attached
source, joined to the article by article_id. This is the schema's FIRST ON DELETE CASCADE FK
(deliberate — owner material dies with its article).
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0002_article_sources"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "article_sources",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "article_id",
            sa.String(),
            sa.ForeignKey("articles.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(), nullable=False),  # "text" | "file" | "url"
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("article_sources")
