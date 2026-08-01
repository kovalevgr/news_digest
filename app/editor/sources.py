"""Flagship intake — owner-supplied grounding material (docs/01_technical.md §2.3; build plan
Phase 10 "Flagship intake: own-material → canonical draft").

The hot_news flow grounds a draft in an approved cluster's fetched source bundle. The FLAGSHIP
flow grounds a draft in the OWNER'S OWN material instead: pasted text, an uploaded file (notes,
a notebook, a log), or a URL the owner fetches. There is no cluster — the article is minted
cluster-less (`create_flagship_article`) and its grounding corpus is the `article_sources`
(OwnerSource) rows attached to it.

This module is the storage + intake seam for that material. It is deterministic code, NOT an
agent and NOT a model call (hard rule 5): it stores text, parses an uploaded file, or fetches a
URL via the shared app/fetcher extractor. It coordinates only through Postgres (it writes the
article + its OwnerSource rows) and never calls another stage; it never publishes (hard rule 1).

Owner material is AUTHORITATIVE grounding (the owner's own results/numbers/notes), not third-
party reporting — `app.editor.context` renders it as `[OWNER ARTIFACT]` and tells the agent to
treat the owner's own numbers as facts to cite rather than flag as unverified. The honesty
contract still holds for the truly-empty case: `draft_article` refuses an article with NO cluster
AND no owner sources (grounding would have nothing to stand on).

Public surface:
  - create_flagship_article(session, *, piece_type="tech_explainer") -> article_id
  - attach_owner_source(session, article_id, *, kind, content, title=None, url=None) -> source_id
  - attach_owner_url(session, article_id, url, *, client=None) -> source_id
  - parse_uploaded_file(filename, data) -> str   (PURE — no DB, no network)
  - load_owner_sources(session, article_id) -> list[SourceItem]
"""
from __future__ import annotations

import json
import logging

from sqlalchemy import select

from app.db.models import Article, OwnerSource
from app.editor.article import PIECE_TYPES, new_article_id
from app.editor.context import SourceItem
from app.fetcher import DEFAULT_FETCH_MAX_CHARS, fetch_full_text

log = logging.getLogger("editor.sources")

# The owner-source kinds. "text" = pasted prose; "file" = an uploaded artefact's extracted text;
# "url" = the readability-extracted body of a fetched URL. A single source of truth so intake and
# validation can't drift on the literal kind strings.
OWNER_SOURCE_KINDS = ("text", "file", "url")

# Default piece type for a flagship article — the teach-down explainer the flagship flow targets
# (the brief lives in app.editor.context._PIECE_TYPE_BRIEFS). Validated against PIECE_TYPES.
DEFAULT_FLAGSHIP_PIECE_TYPE = "tech_explainer"


def create_flagship_article(session, *, piece_type: str = DEFAULT_FLAGSHIP_PIECE_TYPE) -> str:
    """Mint a cluster-less FLAGSHIP article at status 'drafting'; return the article id.

    Unlike `create_article_for_cluster`, this writes NO `article_clusters` row — a flagship
    article's grounding is its owner sources, not a cluster. It goes straight to 'drafting' (the
    owner is about to attach material and draft). Validates `piece_type` against PIECE_TYPES (an
    unknown type is a programming error — fail loudly rather than mis-template a draft).

    Commits so the article is durable before sources are attached / the draft call runs against
    it. Coordinates only through Postgres; never publishes.
    """
    if piece_type not in PIECE_TYPES:
        raise ValueError(
            f"unknown piece_type {piece_type!r}; expected one of {PIECE_TYPES}"
        )

    article_id = new_article_id()
    session.add(
        Article(id=article_id, piece_type=piece_type, status="drafting", current_draft=None)
    )
    session.commit()
    log.info("created flagship article %s (piece_type=%s, no cluster)", article_id, piece_type)
    return article_id


def attach_owner_source(
    session,
    article_id: str,
    *,
    kind: str,
    content: str,
    title: str | None = None,
    url: str | None = None,
) -> int:
    """Attach one owner-material source to an article; return the new OwnerSource id.

    Validates the article exists (ValueError otherwise), the kind is one of OWNER_SOURCE_KINDS,
    and the content is non-empty after stripping (an empty artefact grounds nothing). Caps the
    stored content at DEFAULT_FETCH_MAX_CHARS — the same bound the fetcher uses on full_text — so a
    pathological paste/file can't balloon the row or the draft context built from it.

    Commits so the source is durable. Coordinates only through Postgres; never publishes.
    """
    if kind not in OWNER_SOURCE_KINDS:
        raise ValueError(
            f"unknown owner-source kind {kind!r}; expected one of {OWNER_SOURCE_KINDS}"
        )
    body = (content or "").strip()
    if not body:
        raise ValueError("owner source content is empty; nothing to ground a draft on")

    article = session.get(Article, article_id)
    if article is None:
        raise ValueError(f"article {article_id!r} not found")

    row = OwnerSource(
        article_id=article_id,
        kind=kind,
        title=(title or None),
        url=(url or None),
        content=body[:DEFAULT_FETCH_MAX_CHARS],
    )
    session.add(row)
    session.commit()
    log.info(
        "attached owner source %s (kind=%s) to article %s: %d chars",
        row.id, kind, article_id, len(row.content),
    )
    return row.id


def attach_owner_url(session, article_id: str, url: str, *, client=None) -> int:
    """Fetch a URL's main text and attach it as a kind='url' owner source; return its id.

    Uses the shared app/fetcher extractor (readability over the server HTML, the same pass-2 path
    the writer-agent's fetch_source tool uses). The httpx.Client is injectable for testing (a
    MockTransport drives it with no network). If the fetch yields no usable text (a >=400 response,
    a paywall preview, or a JS-only page that extracts to nothing) it raises ValueError with a clear
    message so the UI can surface it to the owner rather than silently storing an empty source.

    Commits via attach_owner_source. Coordinates only through Postgres; never publishes.
    """
    text = fetch_full_text(url, client=client)
    if not text:
        raise ValueError(
            f"could not extract any text from {url!r} — the page may be paywalled, "
            "JS-rendered, or unreachable; paste the text instead"
        )
    return attach_owner_source(session, article_id, kind="url", content=text, url=url, title=None)


def parse_uploaded_file(filename: str, data: bytes) -> str:
    """Extract plain text from an uploaded file's bytes. PURE — no DB, no network.

    Dispatch on the extension:
      - .md / .markdown / .txt / .log → utf-8 decode (errors='replace' so a bad byte never raises).
      - .ipynb → parse the notebook JSON and concatenate each code/markdown cell's `source` (which
        is a list-of-lines or a string), cells separated by a blank line — the prose + code the
        owner actually wrote, without the JSON envelope.
      - anything else → best-effort utf-8 decode (a sensible default for an unknown text artefact).

    Capped at DEFAULT_FETCH_MAX_CHARS (the same bound attach_owner_source applies) so a huge file
    can't balloon the draft context. A malformed .ipynb degrades to a best-effort decode rather
    than raising — intake should never hard-fail on a slightly-off file.
    """
    name = (filename or "").lower()

    if name.endswith(".ipynb"):
        text = _parse_notebook(data)
    elif name.endswith((".md", ".markdown", ".txt", ".log")):
        text = data.decode("utf-8", errors="replace")
    else:
        # Unknown extension: best-effort decode (treat it as a text artefact).
        text = data.decode("utf-8", errors="replace")

    return text[:DEFAULT_FETCH_MAX_CHARS]


def _parse_notebook(data: bytes) -> str:
    """Concatenate a Jupyter notebook's code+markdown cell sources. Best-effort: a notebook whose
    JSON won't parse (or isn't the expected shape) falls back to a plain utf-8 decode of the raw
    bytes so intake never hard-fails."""
    try:
        nb = json.loads(data.decode("utf-8", errors="replace"))
        cells = nb.get("cells", [])
    except (ValueError, AttributeError):
        return data.decode("utf-8", errors="replace")

    parts: list[str] = []
    for cell in cells:
        if not isinstance(cell, dict):
            continue
        if cell.get("cell_type") not in ("code", "markdown"):
            continue
        source = cell.get("source", "")
        text = "".join(source) if isinstance(source, list) else str(source)
        if text.strip():
            parts.append(text)
    return "\n\n".join(parts)


def load_owner_sources(session, article_id: str) -> list[SourceItem]:
    """The owner-material sources attached to an article, oldest-first, as SourceItem grounding.

    Reads the article's OwnerSource rows (ORDER BY id ASC — insertion/attach order, the stable
    chronology) and maps each to a SourceItem with kind='owner': title falls back to the url, then
    a constant; url defaults to ""; full_text is the stored content. Returns primitives so the list
    survives the session closing. Returns [] for an article with no owner sources. SELECT-only."""
    rows = session.execute(
        select(OwnerSource.title, OwnerSource.url, OwnerSource.content)
        .where(OwnerSource.article_id == article_id)
        .order_by(OwnerSource.id.asc())
    ).all()
    return [
        SourceItem(
            title=(r.title or r.url or "(owner material)"),
            url=(r.url or ""),
            full_text=(r.content or ""),
            kind="owner",
        )
        for r in rows
    ]


__all__ = [
    "OWNER_SOURCE_KINDS",
    "DEFAULT_FLAGSHIP_PIECE_TYPE",
    "create_flagship_article",
    "attach_owner_source",
    "attach_owner_url",
    "parse_uploaded_file",
    "load_owner_sources",
]
