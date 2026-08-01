"""The writer-agent DRAFT phase — the codebase's first real tool-use agent loop
(docs/01_technical.md §2.3 "Draft", §4; build plan Phase 3).

This is THE agent (hard rule 5: one agent only — everything else is single-shot or
deterministic). `draft_article` turns an approved cluster's article into a grounded canonical
long-read in `articles.current_draft`:

  1. Assemble the context (app.editor.context): the owner's voice files + the cluster's source
     bundle + the piece-type brief + the grounding rules → system blocks (cacheable).
  2. Run the AGENT LOOP: call generate(role, tools=tool_schemas(), system=...) with the kickoff
     user turn; read the response for tool_use blocks (_parse_response); dispatch each tool
     (kb_search / fetch_source / web_search), append a tool_result, and loop — until the model
     returns a final text draft or the iteration cap (MAX_TOOL_TURNS) is hit.
  3. Persist the final text to articles.current_draft.

Coordination is Postgres-only: it reads the article + its cluster's items and writes the draft.
It uses the shared app/llm (generate) and app/fetcher (via the fetch_source tool) — those are
shared components, not other stages — and it never calls the poller/bot/researcher. It NEVER
publishes (hard rule 1): the loop produces text, nothing posts.

Grounding (hard rule 2) is enforced via the system prompt (context.GROUNDING_RULES + the voice
files' authenticity section): only bundle + tool facts, carry provenance, flag unverified, never
invent, opinions are the owner's (propose, don't assert). The loop itself can't fabricate — its
only inputs are the bundle and the deterministic tools.

MODEL BOUNDARY — mockable for tests: `generate` is imported at MODULE LEVEL so the default suite
monkeypatches `app.editor.draft.generate` to script the loop (turn 1 → a tool_use; turn 2 → a
final text draft) with NO ANTHROPIC_API_KEY. The fake provider returns a string and cannot emit
tool_use, so it can't exercise the real tool loop — hence the scripted-generate seam. The role is
logical (draft_role(), default "generation"; "generation_high" via env), never a model id.
"""
from __future__ import annotations

import logging
import os

from app.db.models import Article
from app.editor.article import _ensure_genesis
from app.editor.context import (
    build_system_blocks,
    load_grounding_bundle,
    load_voice_files,
)
from app.editor.tools import _parse_response, dispatch_tool, tool_schemas
from app.llm import generate  # module-level import = the test monkeypatch seam

log = logging.getLogger("editor.draft")

# The logical role for the draft call. "generation" by default (the workhorse, docs §4). The
# owner can bump the draft to the higher-quality tier with env DRAFT_ROLE=generation_high if
# Sonnet's writing isn't good enough — a logical role only, NEVER a model id (the role→model map
# lives in app.llm.config). A blank override falls back to the default.
DEFAULT_DRAFT_ROLE = "generation"

# Hard cap on agent loop turns so a misbehaving model that keeps requesting tools can't run
# forever (cost + latency safety). Each turn is one generate() call; a real draft needs only a
# few tool calls at most, so 8 is generous. Env-overridable; bad/non-positive values fall back so
# the cap is never accidentally disabled (a 0 cap would never let the model produce a draft).
DEFAULT_MAX_TOOL_TURNS = 8

# Cap stored draft length — a runaway generation shouldn't balloon the row. Generous vs a real
# long-read; bounds the worst case. Env-overridable, never disabled.
DEFAULT_DRAFT_MAX_CHARS = 100_000

# max_tokens for the draft generate() call — a long-read needs room. Env-overridable.
DEFAULT_DRAFT_MAX_TOKENS = 8000


def draft_role() -> str:
    """Logical role for the draft call (env DRAFT_ROLE, default 'generation'). A blank override
    falls back so we never pass an empty role into the role→model map. NEVER a model id."""
    raw = os.environ.get("DRAFT_ROLE")
    if raw is None or not raw.strip():
        return DEFAULT_DRAFT_ROLE
    return raw.strip()


def max_tool_turns() -> int:
    """Agent-loop turn cap (env MAX_TOOL_TURNS). Falls back on absence/garbage/non-positive — a
    0/negative cap would stop the model before it can produce a draft."""
    return _pos_int_env("MAX_TOOL_TURNS", DEFAULT_MAX_TOOL_TURNS)


def draft_max_chars() -> int:
    """Stored-draft length cap (env DRAFT_MAX_CHARS). Falls back on absence/garbage/non-positive."""
    return _pos_int_env("DRAFT_MAX_CHARS", DEFAULT_DRAFT_MAX_CHARS)


def draft_max_tokens() -> int:
    """max_tokens for the draft generate() call (env DRAFT_MAX_TOKENS). Falls back likewise."""
    return _pos_int_env("DRAFT_MAX_TOKENS", DEFAULT_DRAFT_MAX_TOKENS)


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


# --- kickoff prompt (pure) -----------------------------------------------------------------


def build_kickoff_message(piece_type: str) -> str:
    """The first user turn that kicks off the draft. PURE.

    The system prompt carries voice + grounding + the source bundle; this user turn just asks for
    the draft and reminds the model of the tools and the grounding posture. Kept short — the
    heavy, stable context is the system prompt (which is what gets cached)."""
    return (
        f"Write the canonical {piece_type} long-read now, grounded strictly in the SOURCE BUNDLE "
        "in your system context. Carry provenance links for sourced facts, flag anything "
        "unverified for the owner, and present any take as a clearly-marked proposal. You may call "
        "kb_search (past published articles, for voice/continuity) and fetch_source (a source "
        "URL's full text) on demand if they help — but draft from the sources you have if they "
        "don't. Reply with the finished draft as your final message (markdown)."
    )


# --- the agent loop ------------------------------------------------------------------------


def draft_article(session, article_id: str) -> str:
    """Draft (and persist) the canonical long-read for an article. Returns the draft text.

    Loads the article + its FULL grounding bundle (the linked cluster's items AND/OR the owner's
    own attached material — app.editor.context.load_grounding_bundle), assembles the grounded
    context, runs the tool-use agent loop, and writes the final text to articles.current_draft.

    Two grounding paths feed the same loop: a hot_news article grounds in its approved cluster's
    fetched source bundle; a FLAGSHIP article (no cluster) grounds in the owner's own material
    (text/file/url, attached via app.editor.sources). The bundle is the union — an article could
    carry both.

    Refuses (ValueError) when:
      - the article doesn't exist,
      - the grounding bundle has NO usable text at all (no cluster full_text AND no owner material).
        This is the truly-empty union — grounding would have nothing to stand on (hard rule 2) — and
        covers both "approved story whose pass-2 text hasn't landed" and "flagship article with no
        material attached yet". The web trigger surfaces it to the owner as a clear error rather
        than producing an ungrounded draft.

    The loop caps at max_tool_turns(); if the cap is hit before the model returns a final draft,
    the best text seen so far is persisted (never an empty draft when the model produced prose).
    Commits the draft. Never publishes.
    """
    article = session.get(Article, article_id)
    if article is None:
        raise ValueError(f"article {article_id!r} not found")

    piece_type = article.piece_type or "hot_news"

    bundle = load_grounding_bundle(session, article_id)
    if not bundle.has_full_text:
        # The grounding union is empty: no cluster full_text and no owner material. Refuse rather
        # than draft ungrounded (hard rule 2) — the owner must attach material, or approve a story
        # whose full text has been fetched, before drafting.
        raise ValueError(
            f"article {article_id!r} has no grounding corpus — attach source material, or approve "
            "a story whose full text has been fetched, before drafting"
        )

    voice = load_voice_files()
    system_blocks = build_system_blocks(voice=voice, bundle=bundle, piece_type=piece_type)

    draft_text = _run_agent_loop(session, system_blocks, piece_type)

    article.current_draft = draft_text[: draft_max_chars()]
    session.commit()
    log.info(
        "drafted article %s (cluster %s, piece_type=%s): %d chars",
        article_id, bundle.cluster_id, piece_type, len(article.current_draft or ""),
    )

    # Anchor the version trail (Feature A): record this first draft as the genesis edit_log row
    # IFF the article has none yet. Idempotent — a re-draft never adds a second genesis. Committed
    # separately (after the draft is durable) so a crash between the two leaves a valid draft.
    if _ensure_genesis(session, article_id, article.current_draft):
        session.commit()
        log.info("recorded genesis version for article %s", article_id)

    return article.current_draft


def _run_agent_loop(session, system_blocks: list, piece_type: str) -> str:
    """Run the tool-use loop until a final text draft or the turn cap. Returns the draft text.

    Each iteration: call generate(role, tools=tool_schemas(), system=system_blocks) with the
    running message history; parse the response (_parse_response). If the model requested tools,
    append its assistant turn + a tool_result for each call and loop. If it returned final text
    (no tool calls), that text is the draft. The turn cap bounds the loop; on hitting it we return
    the best text we've seen so the owner always gets something to edit if the model produced prose.

    The assistant turn we append carries the model's RAW content blocks when available (so the API
    sees a well-formed tool_use/tool_result pair); for fakes without `.content`, we reconstruct a
    minimal assistant turn from the parsed text + tool calls. This keeps the loop working against
    both the real SDK response and the tests' scripted fakes.
    """
    role = draft_role()
    cap_turns = max_tool_turns()
    max_tokens = draft_max_tokens()
    tools = tool_schemas()

    messages: list = [{"role": "user", "content": build_kickoff_message(piece_type)}]
    last_text = ""

    for turn in range(cap_turns):
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
            # Final answer — the draft.
            return parsed.text or last_text

        # Model wants tools: append its assistant turn, then a tool_result per call, and loop.
        messages.append(_assistant_turn(resp, parsed))
        tool_results = []
        for call in parsed.tool_calls:
            result_text = dispatch_tool(session, call)
            log.info("draft tool %s -> %d chars", call.name, len(result_text))
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": call.id,
                    "content": result_text,
                }
            )
        messages.append({"role": "user", "content": tool_results})

    # Turn cap reached without a final non-tool answer — return the best text we saw (may be "").
    log.warning("draft loop hit the %d-turn cap; persisting best text seen (%d chars)",
                cap_turns, len(last_text))
    return last_text


def _assistant_turn(resp, parsed) -> dict:
    """Build the assistant message to append for a tool-requesting turn.

    Prefer the provider's RAW content blocks (resp.content) so the real API sees the exact
    tool_use blocks it emitted (their ids must match the tool_result tool_use_id). When the
    response has no `.content` (a bare-string or minimal fake), reconstruct a minimal assistant
    turn from the parsed text + tool calls so the loop still round-trips in tests."""
    content = getattr(resp, "content", None)
    if content is not None:
        return {"role": "assistant", "content": content}
    # Reconstruct from parsed pieces (test fakes / unusual shapes).
    blocks: list = []
    if parsed.text:
        blocks.append({"type": "text", "text": parsed.text})
    for call in parsed.tool_calls:
        blocks.append(
            {"type": "tool_use", "id": call.id, "name": call.name, "input": call.input}
        )
    return {"role": "assistant", "content": blocks}


__all__ = [
    "DEFAULT_DRAFT_ROLE",
    "DEFAULT_MAX_TOOL_TURNS",
    "DEFAULT_DRAFT_MAX_CHARS",
    "DEFAULT_DRAFT_MAX_TOKENS",
    "draft_role",
    "max_tool_turns",
    "draft_max_chars",
    "draft_max_tokens",
    "build_kickoff_message",
    "draft_article",
]
