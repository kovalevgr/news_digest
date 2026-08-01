"""The writer-agent (draft + iterate), its on-demand tools, context assembly, and
grounding — the only agentic component (docs/01_technical.md §2.3, §4).

Phase 3 implements the DRAFT phase: turn an approved cluster into a grounded canonical
long-read. Phase 4 adds conversational ITERATE (edit-in-place) + Gate 2 (the chat seam in
app/web/chat.py wires the iterate entrypoint to the web editor).

Public surface:
  Phase 3 (draft):
  - create_article_for_cluster(session, cluster_id, *, piece_type="hot_news") -> article_id
      Mint (or reopen) the article for an approved cluster and link it via article_clusters.
  - draft_article(session, article_id) -> str
      Run the writer-agent tool-use loop and persist articles.current_draft.
  Phase 4 (iterate + Gate 2):
  - iterate_article(session, article_id, instruction, *, base_draft=None, new_piece_type=None)
      -> IterateResult
      Apply one owner instruction to the draft, editing IN PLACE; persist + log to edit_log.
  - approve_article(session, article_id) -> str
      Gate 2: drafting → pre_publish (owner approval of the canonical — NOT publishing).
  Phase 5 (mark-as-published):
  - publish_article(session, article_id) -> str
      pre_publish → published + compute/store the article embedding (KB entry). Bookkeeping of an
      external manual post — NOT publishing.
  Phase 10 (flagship intake — own-material → canonical draft):
  - create_flagship_article(session, *, piece_type="tech_explainer") -> article_id
      Mint a cluster-less article whose grounding is the owner's own attached material.
  - attach_owner_source / attach_owner_url(session, article_id, ...) -> source_id
      Store pasted text / a parsed file / a fetched URL as the article's grounding corpus.
  - parse_uploaded_file(filename, data) -> str
      Extract plain text from an uploaded .md/.txt/.log/.ipynb artefact (PURE).
  - load_owner_sources(session, article_id) -> list[SourceItem]
      The article's owner material as grounding items (kind='owner').
  - find_related_clusters(session, text, *, top_k=5) -> list[RelatedCluster]
      Surface the existing news clusters most related to a piece of the owner's own material
      (deterministic pgvector cosine search over items.embedding — one embed() call, not an agent).

The iterate phase is the SAME one agent as draft (hard rule 5), extended with an iterate
entrypoint — not a second agent.

Submodules: article (creation + Gate 2), context (assembly + grounding, draft & iterate), tools
(kb_search / fetch_source / web_search + the response parser), kb (KB retrieval seam), fusion
(fusion-discovery retrieval over the dedup index), draft (the draft loop), iterate (the iterate
loop).
"""
from app.editor.article import (
    DEFAULT_PIECE_TYPE,
    PIECE_TYPES,
    approve_article,
    create_article_for_cluster,
    new_article_id,
    publish_article,
    restore_article_version,
)
from app.editor.draft import draft_article
from app.editor.fusion import RelatedCluster, find_related_clusters
from app.editor.iterate import IterateResult, iterate_article
from app.editor.sources import (
    attach_owner_source,
    attach_owner_url,
    create_flagship_article,
    load_owner_sources,
    parse_uploaded_file,
)

__all__ = [
    "PIECE_TYPES",
    "DEFAULT_PIECE_TYPE",
    "create_article_for_cluster",
    "new_article_id",
    "draft_article",
    "iterate_article",
    "IterateResult",
    "approve_article",
    "publish_article",
    "restore_article_version",
    "create_flagship_article",
    "attach_owner_source",
    "attach_owner_url",
    "parse_uploaded_file",
    "load_owner_sources",
    "find_related_clusters",
    "RelatedCluster",
]
