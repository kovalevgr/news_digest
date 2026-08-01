"""Source adapters — one module per source type, each returning normalized Items.

`get_adapter(type)` is the single lookup the poll runner uses. The no-credential adapters
are wired in: `rss`, `hn`, `github`, `arxiv`. arXiv and GitHub Atom are thin URL-builders
over app.adapters.rss.parse_feed (same Atom parsing, different feed URL); HN uses the
official Firebase JSON API. `x_user` uses the X API v2 read endpoints (Bearer token from env,
read at call time) and is wired in too. The remaining deferred seam raises NotImplementedError:

  - `reddit_sub` — owner-credential-gated (Reddit OAuth JSON API).

The Item/PollResult/Adapter seam lives in app.adapters.base.
"""
from __future__ import annotations

from app.adapters.arxiv import ArxivAdapter
from app.adapters.base import Adapter, Item, PollResult, canonical_url, item_id
from app.adapters.github import GithubAdapter
from app.adapters.hn import HnAdapter
from app.adapters.rss import RssAdapter, parse_feed
from app.adapters.x import XAdapter

# Source types that have a working adapter.
_IMPLEMENTED: dict[str, type[Adapter]] = {
    "rss": RssAdapter,
    "hn": HnAdapter,
    "github": GithubAdapter,
    "arxiv": ArxivAdapter,
    "x_user": XAdapter,
}

# Recognized-but-not-yet-built types, with the reason they are deferred. Listed so the
# poll runner can log a clear skip note instead of crashing on a configured source.
_DEFERRED: dict[str, str] = {
    "reddit_sub": "Reddit OAuth JSON API adapter (owner-credential-gated) — later slice",
}


def get_adapter(type_: str) -> Adapter:
    """Return an adapter instance for a configured source type.

    Raises NotImplementedError for recognized-but-deferred types and ValueError for
    anything the config validator would never have allowed through.
    """
    cls = _IMPLEMENTED.get(type_)
    if cls is not None:
        return cls()
    if type_ in _DEFERRED:
        raise NotImplementedError(f"source type {type_!r} not built yet: {_DEFERRED[type_]}")
    raise ValueError(f"unknown source type {type_!r}; known: {available_types()}")


def is_implemented(type_: str) -> bool:
    return type_ in _IMPLEMENTED


def available_types() -> list[str]:
    """Source types with a working adapter, sorted (currently arxiv, github, hn, rss, x_user)."""
    return sorted(_IMPLEMENTED)


__all__ = [
    "Adapter",
    "Item",
    "PollResult",
    "canonical_url",
    "item_id",
    "parse_feed",
    "RssAdapter",
    "HnAdapter",
    "GithubAdapter",
    "ArxivAdapter",
    "XAdapter",
    "get_adapter",
    "is_implemented",
    "available_types",
]
