"""Editor chat transport seam — the writer-agent iterate plug point (docs/01_technical.md §2.3
"Iterate"; build plan Phase 4).

The editor's realtime chat is the surface for the owner to iterate a draft conversationally. The
TRANSPORT (the socket/round-trip, the per-message streaming) lives in app/web (the routes + the
NiceGUI page). This module is the boundary between that transport and the BRAIN — the writer-agent
iterate phase (app.editor.iterate.iterate_article) — and as of Phase 4 the brain is WIRED:
`handle_editor_message` opens a short-lived DB session and delegates to `iterate_article`.

This stays a THIN seam (cf. ui_pages._draft_existing_article): all the editing logic — edit-in-
place, respect manual edits, append to edit_log, piece-type switch, grounding, never publish —
lives in app.editor.iterate. This module just owns the session lifecycle and the call boundary so
the web layer never imports the agent directly and never holds a session across the page lifetime.

Session lifecycle: `handle_editor_message` opens its OWN session via app.db.session.get_session
(lazily imported so importing this module never constructs the engine / touches the DB), uses it,
and closes it — mirroring ui_pages._db_session. The frontend calls it through `run.io_bound`, so
opening a per-call session off the event loop is correct (one owner, no concurrency).

Streaming: the routes may still stream a reply in chunks via `stream_reply` (kept as-is). The
iterate reply is a short deterministic confirmation — the owner sees the actual change in the live
preview diff — so streaming it is cosmetic, but the seam is preserved for the transport.
"""
from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import contextmanager

from app.editor.iterate import IterateResult, iterate_article

log = logging.getLogger("web.chat")

# Chunk size for the demo streamer. Small enough that a short reply visibly streams in the
# browser, large enough not to spam tiny frames. (The iterate reply is a terse confirmation; the
# owner reviews the diff in the preview, so streaming is cosmetic — but the seam stays.)
_STREAM_CHUNK_CHARS = 24

# The no-op reply for an empty/whitespace instruction (kept in sync with iterate._REPLY_EMPTY so
# the message is identical whether the no-op is caught here or inside the agent).
_EMPTY_REPLY = "received an empty message — nothing to do."


@contextmanager
def _db_session() -> Iterator:
    """Yield a short-lived DB Session, always closed on exit (success AND exception).

    Mirrors ui_pages._db_session: each chat message opens its own session and closes it promptly
    (one owner, no concurrency). `get_session` is imported lazily so importing this module never
    constructs the engine or touches the DB (uvicorn boot / test collection stay side-effect-free)."""
    from app.db.session import get_session

    session = get_session()
    try:
        yield session
    finally:
        session.close()


def handle_editor_message(
    article_id: str,
    instruction: str,
    *,
    base_draft: str | None = None,
    new_piece_type: str | None = None,
) -> IterateResult:
    """Run one owner chat instruction through the writer-agent iterate phase; return the result.

    The thin web seam over `iterate_article` (build plan Phase 4): opens a short-lived session,
    delegates the actual edit-in-place iteration (and the edit_log write, the piece-switch, the
    grounding — all owned by app.editor.iterate), and returns the IterateResult for the chat UI
    (a terse `reply` for the bubble + the revised `draft` for the preview).

    `base_draft` carries the owner's latest working text (unsaved hand-edits) so the agent edits
    THAT, not a stale persisted draft (manual edits are sacred). `new_piece_type` switches the
    piece type mid-stream (a structural reformat). Both are forwarded verbatim to `iterate_article`.

    Runs inside `run.io_bound` on the frontend, so owning its session here is correct. It NEVER
    publishes — `iterate_article` only writes the draft + edit_log."""
    # Empty/whitespace instruction with no piece-switch is a no-op — short-circuit HERE so we don't
    # even open a DB session or touch the agent for whitespace (the agent's iterate_article guards
    # this too, but the seam stays safe and cheap on its own). A piece-switch with no text is NOT a
    # no-op — it still has to reformat — so it falls through to iterate_article.
    if not (instruction or "").strip() and new_piece_type is None:
        return IterateResult(reply=_EMPTY_REPLY, draft="", piece_type="hot_news", changed=False)

    log.info(
        "editor chat: article=%s instruction=%r switch=%s",
        article_id, (instruction or "").strip()[:120], new_piece_type,
    )
    with _db_session() as session:
        return iterate_article(
            session,
            article_id,
            instruction,
            base_draft=base_draft,
            new_piece_type=new_piece_type,
        )


def stream_reply(reply: str, *, chunk_chars: int = _STREAM_CHUNK_CHARS) -> Iterator[str]:
    """Yield a reply in chunks so the socket can stream it to the browser progressively.

    A transport-level seam: it slices a finished string. The iterate reply is short, so this is
    cosmetic, but the route can keep streaming through it unchanged. Always yields at least one
    (possibly empty) chunk so the client gets a well-formed turn even for an empty reply."""
    if not reply:
        yield ""
        return
    step = chunk_chars if chunk_chars > 0 else len(reply)
    for i in range(0, len(reply), step):
        yield reply[i : i + step]


__all__ = [
    "IterateResult",
    "handle_editor_message",
    "stream_reply",
]
