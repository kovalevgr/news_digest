"""The writer-agent ITERATE phase — edit-in-place refinement of a working draft
(docs/01_technical.md §2.3 "Iterate", §4; build plan Phase 4).

This is the SAME one agent as the DRAFT phase (hard rule 5: one agent only) — extended with an
iterate entrypoint, not a new agent. Where `draft_article` turns an approved cluster into the
first canonical long-read, `iterate_article` applies ONE owner instruction to an existing draft,
editing it IN PLACE and never regenerating it from scratch (the core iterate principle: full
regeneration would undo the owner's refinements and hand-edits).

The loop is `draft.py`'s loop, reused verbatim in spirit:

  1. Assemble the iterate context (app.editor.context.build_iterate_system_blocks): the stable
     draft context (header, GROUNDING rules, piece brief, voice, source bundle) PLUS the
     EDIT-IN-PLACE rules and a CURRENT DRAFT block carrying the working text to edit.
  2. Run the AGENT LOOP (the same tool-use loop as draft): generate(role, tools, system) with the
     iterate user turn; dispatch any tool_use (kb_search / fetch_source / web_search); loop until
     the model returns the FULL revised draft or the turn cap is hit.
  3. Persist the revised draft to articles.current_draft, append the instruction to edit_log
     (exactly once — the voice training signal), and commit.

Manual edits are sacred (hard rule, docs §2.3): if the caller passes `base_draft` (the owner's
latest working text, possibly with unsaved hand-edits), it is persisted first and used as the
base the agent edits, so the agent never edits a stale draft and never clobbers a hand-edit.

Piece-type switch mid-stream (docs §2.3 "Piece type"): a `new_piece_type` switches
articles.piece_type and instructs a STRUCTURAL REFORMAT into the new shape (not a point edit).

Coordination is Postgres-only: it reads the article + its cluster's items and writes the draft +
the edit_log row. It uses the shared app/llm (generate) and app/fetcher (via fetch_source) — those
are shared components, not other stages — and never calls the poller/bot/researcher. It NEVER
publishes (hard rule 1): the loop produces text, nothing posts.

MODEL BOUNDARY — mockable for tests: `generate` is imported at MODULE LEVEL so the default suite
monkeypatches `app.editor.iterate.generate` to script the loop, exactly like draft.py. The role is
logical (iterate_role(), default "generation"; env override), never a model id.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from app.db.models import Article, EditLog
from app.editor.article import PIECE_TYPES, _ensure_genesis
from app.editor.context import (
    build_iterate_message,
    build_iterate_system_blocks,
    load_grounding_bundle,
    load_voice_files,
)
from app.editor.tools import _parse_response, dispatch_tool, tool_schemas
from app.llm import generate  # module-level import = the test monkeypatch seam

log = logging.getLogger("editor.iterate")

# The logical role for the iterate call. "generation" by default (the workhorse, docs §4), the
# same default as draft. Env ITERATE_ROLE bumps it to e.g. "generation_high" if iteration quality
# needs it — a logical role only, NEVER a model id (the role→model map lives in app.llm.config).
# A blank override falls back to the default.
DEFAULT_ITERATE_ROLE = "generation"

# Hard cap on agent loop turns (same rationale as draft.MAX_TOOL_TURNS): a misbehaving model that
# keeps requesting tools can't run forever. Each turn is one generate() call. Env-overridable;
# bad/non-positive values fall back so the cap is never accidentally disabled.
DEFAULT_MAX_TOOL_TURNS = 8

# Cap stored draft length — a runaway iteration shouldn't balloon the row. Generous vs a real
# long-read; env-overridable, never disabled. (Shares the DRAFT_MAX_CHARS knob with draft so the
# two phases store under the same bound — they write the same column.)
DEFAULT_DRAFT_MAX_CHARS = 100_000

# max_tokens for the iterate generate() call — a full revised long-read needs room (the model
# returns the WHOLE draft each turn, not a diff). Env-overridable.
DEFAULT_ITERATE_MAX_TOKENS = 8000


def iterate_role() -> str:
    """Logical role for the iterate call (env ITERATE_ROLE, default 'generation'). A blank
    override falls back so we never pass an empty role into the role→model map. NEVER a model id."""
    raw = os.environ.get("ITERATE_ROLE")
    if raw is None or not raw.strip():
        return DEFAULT_ITERATE_ROLE
    return raw.strip()


def max_tool_turns() -> int:
    """Agent-loop turn cap (env MAX_TOOL_TURNS — shared with draft). Falls back on absence/garbage/
    non-positive: a 0/negative cap would stop the model before it can return the revised draft."""
    return _pos_int_env("MAX_TOOL_TURNS", DEFAULT_MAX_TOOL_TURNS)


def draft_max_chars() -> int:
    """Stored-draft length cap (env DRAFT_MAX_CHARS — shared with draft). Falls back on
    absence/garbage/non-positive."""
    return _pos_int_env("DRAFT_MAX_CHARS", DEFAULT_DRAFT_MAX_CHARS)


def iterate_max_tokens() -> int:
    """max_tokens for the iterate generate() call (env ITERATE_MAX_TOKENS). Falls back likewise."""
    return _pos_int_env("ITERATE_MAX_TOKENS", DEFAULT_ITERATE_MAX_TOKENS)


def _pos_int_env(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad %s=%r — falling back to %s", name, raw, default)
        return default
    return val if val > 0 else default


@dataclass
class IterateResult:
    """The outcome of one iterate call, returned to the web seam (and on to the chat UI).

    Fields:
      - reply: a short, deterministic assistant confirmation for the chat bubble (the owner sees
        the actual change in the live preview diff, so the reply stays terse).
      - draft: the FULL revised current_draft, already persisted to the DB.
      - piece_type: the article's piece type NOW (may have changed on a switch).
      - changed: whether the draft text actually changed vs the base it edited (lets the UI avoid a
        needless preview refresh / signals a no-op edit).
    """
    reply: str
    draft: str
    piece_type: str
    changed: bool


# Deterministic chat confirmations (the owner reviews the diff in the preview; the reply is terse).
_REPLY_EDIT = "Applied your edit — review the updated draft on the right."
_REPLY_SWITCH = "Reformatted as {piece_type} — review the updated draft on the right."
_REPLY_EMPTY = "received an empty message — nothing to do."


def iterate_article(
    session,
    article_id: str,
    instruction: str,
    *,
    base_draft: str | None = None,
    new_piece_type: str | None = None,
) -> IterateResult:
    """Apply one owner instruction to an article's draft, editing IN PLACE, and persist the result.

    Loads the article (ValueError if missing) and its FULL grounding bundle — the linked cluster's
    items AND/OR the owner's own attached material (flagship), via load_grounding_bundle — as
    grounding for any NEW facts, plus the voice files. Unlike draft, it does NOT refuse on an empty
    bundle: the draft already exists, and the bundle is grounding for new facts only — most edits
    (tone, cuts, restructuring) need no new facts at all. So iterate works on a hot_news article, a
    flagship article (owner material), AND a zero-source article (editing an existing draft).

    Manual edits (hard rule): if `base_draft is not None` it is the owner's latest working text
    (possibly with unsaved hand-edits) — it is persisted as current_draft first and used as the
    base the agent edits, so the agent never edits a stale draft and never clobbers a hand-edit.
    If `None`, the persisted current_draft is the base.

    Piece-type switch: if `new_piece_type` is set (validated against PIECE_TYPES) the article's
    piece_type is updated and the agent is told to STRUCTURALLY REFORMAT into the new shape rather
    than make a point edit.

    Empty/whitespace `instruction` with NO `new_piece_type` is a no-op: returns immediately
    WITHOUT calling the model or writing edit_log (nothing to edit-in-place from).

    Persists the revised draft (capped at draft_max_chars()), appends the instruction to edit_log
    exactly once (the voice training signal — losing it is a bug), and commits. Never publishes.
    """
    article = session.get(Article, article_id)
    if article is None:
        raise ValueError(f"article {article_id!r} not found")

    instr = (instruction or "").strip()
    is_switch = new_piece_type is not None
    if is_switch and new_piece_type not in PIECE_TYPES:
        raise ValueError(
            f"unknown piece_type {new_piece_type!r}; expected one of {PIECE_TYPES}"
        )

    # Capture the PRE-edit draft text BEFORE any base_draft hand-edit overwrites it — this is the
    # true pre-image the version-trail safety net (below) records as genesis on a first edit.
    pre_edit_draft = article.current_draft

    # If the owner passed their latest working text (hand-edits), it becomes the base the agent
    # edits AND is persisted first so a crash mid-iterate doesn't lose the hand-edit. This must
    # happen before the no-op check so a hand-edit-then-empty-send still saves the hand-edit.
    if base_draft is not None:
        article.current_draft = base_draft[: draft_max_chars()]

    base_text = article.current_draft or ""

    # Empty instruction + no switch → nothing to do. No model call, no edit_log row, no genesis
    # (nothing is being edited). (If a base_draft was supplied we still persist it above, then
    # commit it here, but never log it as an instruction — it isn't one.)
    if not instr and not is_switch:
        if base_draft is not None:
            session.commit()
        return IterateResult(
            reply=_REPLY_EMPTY,
            draft=base_text,
            piece_type=article.piece_type or "hot_news",
            changed=False,
        )

    # Version-trail safety net (Feature A): an actual edit/switch is about to happen. If this is the
    # FIRST edit_log entry for the article (e.g. one that was never anchored by a draft genesis),
    # record the PRE-edit draft as a genesis row BEFORE we apply + log the edit, so the pre-image of
    # the first edit is never lost. It is staged on the session and committed in the SAME commit as
    # this iterate's own edit row below (one transaction). A fresh article's first edit thus ends
    # with TWO rows: genesis (pre-edit) + the edit itself. Idempotent — never adds a 2nd genesis.
    _ensure_genesis(session, article_id, pre_edit_draft)

    # On a pure piece-switch with no instruction text, synthesize one for the edit_log so the
    # voice signal records WHY the draft changed (build_iterate_message still needs a directive).
    effective_instruction = instr or f"[switch piece_type → {new_piece_type}]"
    if is_switch:
        article.piece_type = new_piece_type
    piece_type = article.piece_type or "hot_news"

    # The full grounding bundle: the linked cluster's items AND/OR the owner's own attached
    # material (flagship). May be empty (a zero-source article being edited) — that is fine: the
    # bundle grounds NEW facts only, and most edits add none. Always a bundle, never None.
    bundle = load_grounding_bundle(session, article_id)
    voice = load_voice_files()

    revised = _run_iterate_loop(
        session,
        bundle=bundle,
        voice=voice,
        current_draft=base_text,
        piece_type=piece_type,
        is_piece_switch=is_switch,
        instruction=effective_instruction,
    )

    article.current_draft = revised[: draft_max_chars()]
    changed = (article.current_draft or "") != base_text

    # Append to edit_log exactly once: the owner's instruction + the resulting draft snapshot. This
    # is the voice training signal (docs §2.3) — it is written even when `changed` is False (the
    # owner DID give an instruction; that it was a no-op is itself signal) and even on a pure
    # switch (the synthesized instruction records the switch).
    session.add(
        EditLog(
            article_id=article_id,
            instruction=effective_instruction,
            draft_snapshot=article.current_draft,
        )
    )
    session.commit()

    log.info(
        "iterated article %s (piece_type=%s, switch=%s, changed=%s): %d chars",
        article_id, piece_type, is_switch, changed, len(article.current_draft or ""),
    )

    reply = _REPLY_SWITCH.format(piece_type=piece_type) if is_switch else _REPLY_EDIT
    return IterateResult(
        reply=reply,
        draft=article.current_draft or "",
        piece_type=piece_type,
        changed=changed,
    )


def _run_iterate_loop(
    session,
    *,
    bundle,
    voice,
    current_draft: str,
    piece_type: str,
    is_piece_switch: bool,
    instruction: str,
) -> str:
    """Run the tool-use loop until the model returns the full revised draft or the turn cap.

    The same loop as draft._run_agent_loop, but with the iterate system context (current draft +
    edit-in-place rules) and the iterate user turn (the owner's instruction). Each iteration calls
    generate(role, tools, system); on a tool request it appends the assistant turn + a tool_result
    per call and loops; on a final non-tool answer that text is the revised draft. The turn cap
    bounds the loop; on hitting it we return the best text seen so the owner always gets the
    revised draft back if the model produced one. Falls back to the current draft if the model
    produced nothing at all (so iterate never blanks a draft).

    `bundle` is the article's grounding bundle (load_grounding_bundle), whose items may be empty
    (a zero-source article being edited); build_source_bundle_text renders that as a placeholder so
    the prompt still assembles. A None is also tolerated defensively (→ an empty SourceBundle)."""
    from app.editor.context import SourceBundle

    role = iterate_role()
    cap_turns = max_tool_turns()
    max_tokens = iterate_max_tokens()
    tools = tool_schemas()

    bundle = bundle if bundle is not None else SourceBundle(cluster_id="", items=[])
    system_blocks = build_iterate_system_blocks(
        voice=voice,
        bundle=bundle,
        current_draft=current_draft,
        piece_type=piece_type,
        is_piece_switch=is_piece_switch,
    )

    messages: list = [{"role": "user", "content": build_iterate_message(instruction)}]
    last_text = ""

    for _turn in range(cap_turns):
        resp = generate(
            messages=messages,
            role=role,
            tools=tools,
            system=system_blocks,
            max_tokens=max_tokens,
        )
        parsed = _parse_response(resp)
        if parsed.text:
            last_text = parsed.text

        if not parsed.wants_tools:
            # Final answer — the full revised draft. Fall back to the prior draft if the model
            # somehow returned nothing, so iterate never blanks a working draft.
            return parsed.text or last_text or current_draft

        messages.append(_assistant_turn(resp, parsed))
        tool_results = []
        for call in parsed.tool_calls:
            result_text = dispatch_tool(session, call)
            log.info("iterate tool %s -> %d chars", call.name, len(result_text))
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": call.id,
                    "content": result_text,
                }
            )
        messages.append({"role": "user", "content": tool_results})

    # Turn cap reached without a final non-tool answer — return the best text seen, or the prior
    # draft if none (never blank the draft on a runaway loop).
    log.warning("iterate loop hit the %d-turn cap; persisting best text seen (%d chars)",
                cap_turns, len(last_text))
    return last_text or current_draft


def _assistant_turn(resp, parsed) -> dict:
    """Build the assistant message to append for a tool-requesting turn.

    Identical to draft._assistant_turn: prefer the provider's RAW content blocks (resp.content) so
    the real API sees the exact tool_use blocks it emitted (ids must match the tool_result
    tool_use_id); reconstruct a minimal assistant turn from parsed pieces for bare/minimal fakes."""
    content = getattr(resp, "content", None)
    if content is not None:
        return {"role": "assistant", "content": content}
    blocks: list = []
    if parsed.text:
        blocks.append({"type": "text", "text": parsed.text})
    for call in parsed.tool_calls:
        blocks.append(
            {"type": "tool_use", "id": call.id, "name": call.name, "input": call.input}
        )
    return {"role": "assistant", "content": blocks}


__all__ = [
    "DEFAULT_ITERATE_ROLE",
    "DEFAULT_MAX_TOOL_TURNS",
    "DEFAULT_DRAFT_MAX_CHARS",
    "DEFAULT_ITERATE_MAX_TOKENS",
    "iterate_role",
    "max_tool_turns",
    "draft_max_chars",
    "iterate_max_tokens",
    "IterateResult",
    "iterate_article",
]
