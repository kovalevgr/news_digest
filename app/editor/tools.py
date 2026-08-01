"""On-demand tools for the writer-agent + the provider-response parser (docs/01_technical.md §4).

The writer-agent is the ONE agentic component: a model loop that may call tools on demand. This
module defines those tools — their schemas (what is offered to the model), their dispatch (how a
tool_use is executed), and `_parse_response` (how a provider response is read for text + tool
calls). The agent LOOP itself lives in app/editor/draft.py; this module is its toolbox.

The three tools (all on-demand — offered, never always-on):

  - kb_search(query)  — cosine retrieval over PUBLISHED articles (app.editor.kb.kb_search). The
    voice/continuity seam. Returns [] today (empty KB) and degrades gracefully.
  - fetch_source(url) — full text of a source via app.fetcher.fetch_full_text. Grounding/detail
    on demand: the agent reaches for it when the source bundle's inlined text isn't enough.
  - web_search(query) — OPTIONAL, OFF by default behind env EDITOR_WEB_SEARCH. When off, it is
    NOT offered to the model (it never appears in the tool list), so the agent can't call it; if
    it somehow does, dispatch returns a clear "disabled" result. The seam is clean for a future
    enable: flip the env, and (later) wire a real search backend in `_run_web_search`.

These tools are NOT agents (hard rule 5 — one agent only): each is a single deterministic call
(a DB query, an HTTP fetch). They never loop or call the model.

`_parse_response` is the mockability crux (test requirement): it extracts (text, [tool_calls])
from BOTH a real Anthropic response object (`.content` = list of blocks; a block has `.type` in
{"text","tool_use"}; a tool_use block has `.name`/`.input`/`.id`) AND simple fakes the tests
build (the same shape, or a dict). The default suite scripts the module-level `generate` to emit
a tool_use then a final text, with no real API key — so the parser must work on hand-built
objects, never assuming the SDK is installed.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from app.editor.kb import kb_search as _kb_search
from app.fetcher import fetch_full_text

log = logging.getLogger("editor.tools")

# Tool names — single source of truth, referenced by the schemas, the dispatcher, and tests.
TOOL_KB_SEARCH = "kb_search"
TOOL_FETCH_SOURCE = "fetch_source"
TOOL_WEB_SEARCH = "web_search"

# Cap the fetched text a fetch_source tool_result hands back to the model: a full extraction can
# be huge, and we don't want one tool call to blow the context. The agent gets a generous excerpt
# — enough for grounding/detail — bounded for safety. Env-overridable seam.
DEFAULT_FETCH_TOOL_CHARS = 8000


def fetch_tool_chars() -> int:
    """Max chars a fetch_source result returns to the model (env FETCH_TOOL_CHARS). Falls back on
    absence/garbage/non-positive so the cap is never disabled."""
    raw = os.environ.get("FETCH_TOOL_CHARS")
    if raw is None:
        return DEFAULT_FETCH_TOOL_CHARS
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad FETCH_TOOL_CHARS=%r — falling back to %s", raw, DEFAULT_FETCH_TOOL_CHARS)
        return DEFAULT_FETCH_TOOL_CHARS
    return val if val > 0 else DEFAULT_FETCH_TOOL_CHARS


def web_search_enabled() -> bool:
    """Whether the optional web_search tool is offered (env EDITOR_WEB_SEARCH).

    OFF by default (docs §4: web_search is optional, used sparingly). Truthy values: 1/true/yes/on
    (case-insensitive). Anything else — including unset — is OFF, so the tool is not offered to the
    model. This is the clean enable seam: flip the env to turn it on (a real backend still has to
    be wired in `_run_web_search`)."""
    raw = os.environ.get("EDITOR_WEB_SEARCH")
    if raw is None:
        return False
    return raw.strip().lower() in ("1", "true", "yes", "on")


# --- tool schemas (what is offered to the model) -------------------------------------------


def tool_schemas() -> list:
    """The Anthropic tool schemas offered to the model this turn. kb_search + fetch_source always;
    web_search only when EDITOR_WEB_SEARCH is on (otherwise it is omitted entirely, so the model
    cannot call it). Each schema is the standard {name, description, input_schema} shape."""
    schemas = [
        {
            "name": TOOL_KB_SEARCH,
            "description": (
                "Search the owner's past PUBLISHED articles for voice few-shot and continuity / "
                "non-repetition. Use it to match the owner's established voice and to avoid "
                "repeating a point already made in a past piece. Returns the most relevant past "
                "articles (may be empty if none exist yet)."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to look for in past published articles.",
                    }
                },
                "required": ["query"],
            },
        },
        {
            "name": TOOL_FETCH_SOURCE,
            "description": (
                "Fetch the full text of a source URL (readability extraction) for grounding and "
                "detail. Use it when a source in the bundle has no inlined full text, or when you "
                "need more of a source's content than the bundle excerpt provides. Only fetch URLs "
                "that appear in the source bundle or that a fetched source links to."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The source URL to fetch full text for.",
                    }
                },
                "required": ["url"],
            },
        },
    ]
    if web_search_enabled():
        schemas.append(
            {
                "name": TOOL_WEB_SEARCH,
                "description": (
                    "Search the web for additional context for a long-form piece. Use sparingly; "
                    "anything it returns is outside-the-sources material and must be flagged as "
                    "unverified for the owner to check."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The web search query."}
                    },
                    "required": ["query"],
                },
            }
        )
    return schemas


# --- response parsing (the mockability crux) -----------------------------------------------


@dataclass
class ToolCall:
    """One tool_use the model requested: its id (echoed back in the tool_result), name, input."""
    id: str
    name: str
    input: dict


@dataclass
class ParsedResponse:
    """A provider response read into (text, tool_calls). `text` is the concatenated text blocks;
    `tool_calls` is every tool_use block (empty when the model returned a final answer)."""
    text: str
    tool_calls: list

    @property
    def wants_tools(self) -> bool:
        return bool(self.tool_calls)


def _parse_response(resp) -> ParsedResponse:
    """Extract (text, [ToolCall]) from a provider response. TOLERANT — works on the real Anthropic
    object AND on hand-built fakes (the tests' scripted responses), with NO assumption the SDK is
    installed.

    Accepts, in order:
      - a string (the fake provider's no-tools return, or a model that replied plain text) →
        text=that string, no tool calls.
      - an object/dict with a `content` list of blocks. Each block has a `type`; a "text" block
        has `.text`, a "tool_use" block has `.id`/`.name`/`.input`. Both attribute access (real
        SDK objects, SimpleNamespace fakes) and dict access (plain-dict fakes) are supported via
        `_get`.

    Anything else (None, an unexpected shape) → empty text, no tool calls, so the loop ends
    cleanly rather than crashing on a malformed response."""
    if resp is None:
        return ParsedResponse(text="", tool_calls=[])
    if isinstance(resp, str):
        return ParsedResponse(text=resp, tool_calls=[])

    content = _get(resp, "content", None)
    if content is None:
        # Some shapes might already be a list of blocks.
        if isinstance(resp, (list, tuple)):
            content = resp
        else:
            return ParsedResponse(text="", tool_calls=[])

    text_parts: list[str] = []
    tool_calls: list = []
    for block in content:
        btype = _get(block, "type", None)
        if btype == "text":
            t = _get(block, "text", "")
            if t:
                text_parts.append(t)
        elif btype == "tool_use":
            tool_calls.append(
                ToolCall(
                    id=_get(block, "id", "") or "",
                    name=_get(block, "name", "") or "",
                    input=_get(block, "input", {}) or {},
                )
            )
    return ParsedResponse(text="".join(text_parts), tool_calls=tool_calls)


def _get(obj, key, default):
    """Read `key` from `obj` whether it's a dict (item access) or an object (attribute access).
    The parser must handle both the real SDK blocks (attributes) and plain-dict test fakes."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


# --- tool dispatch -------------------------------------------------------------------------


def dispatch_tool(session, call: ToolCall) -> str:
    """Execute one tool_use and return its result as a STRING (the tool_result content).

    Routes by tool name. Unknown tools and a disabled web_search return a clear, non-raising
    message so the agent loop can hand it back as a tool_result and keep going rather than
    crashing. Each tool is a single deterministic call — never a loop, never a model call (hard
    rule 5). `session` is threaded through for kb_search (the DB-backed tool); fetch_source uses
    the shared fetcher and needs no session."""
    name = call.name
    args = call.input or {}
    if name == TOOL_KB_SEARCH:
        return _run_kb_search(session, str(args.get("query", "")))
    if name == TOOL_FETCH_SOURCE:
        return _run_fetch_source(str(args.get("url", "")))
    if name == TOOL_WEB_SEARCH:
        return _run_web_search(str(args.get("query", "")))
    return f"(unknown tool {name!r} — no such tool is available)"


def _run_kb_search(session, query: str) -> str:
    """kb_search backend: cosine search over published articles, rendered as a string result.

    Returns a clear "no past articles" message when the KB is empty (today's reality) so the agent
    knows to draft from the bundle alone, rather than an empty blob it might misread."""
    hits = _kb_search(session, query)
    if not hits:
        return (
            "kb_search: no past published articles matched (the knowledge base may be empty — "
            "this is normal early on). Draft from the source bundle; do not invent past pieces."
        )
    lines = [f"kb_search: {len(hits)} past published article(s), nearest first:"]
    for h in hits:
        lines.append(
            f"\n[article {h.article_id} · {h.piece_type} · distance {h.distance:.3f}]\n{h.excerpt}"
        )
    return "\n".join(lines)


def _run_fetch_source(url: str) -> str:
    """fetch_source backend: full text of a URL via the shared fetcher, capped for the result.

    A missing url, a fetch that yields nothing (404 / empty extraction / the deferred JS-paywall
    seam), or a transport error all return a clear string (the error is caught here, NOT
    propagated) so the agent gets a usable tool_result and continues rather than the loop dying on
    a flaky fetch. The agent must not invent content for a URL that returned nothing."""
    url = (url or "").strip()
    if not url:
        return "fetch_source: no url provided."
    try:
        text = fetch_full_text(url)
    except Exception as e:  # noqa: BLE001 — a tool failure is a tool_result, not a loop crash.
        log.warning("fetch_source failed for %s: %s", url, e)
        return f"fetch_source: could not fetch {url} ({type(e).__name__}). Do not invent its content."
    if not text:
        return (
            f"fetch_source: {url} returned no extractable text (missing, paywalled, or JS-only). "
            "Do not invent its content."
        )
    cap = fetch_tool_chars()
    body = text[:cap]
    if len(text) > cap:
        body += " […truncated]"
    return f"fetch_source: full text of {url}:\n\n{body}"


def _run_web_search(query: str) -> str:
    """web_search backend — the disabled/seam path.

    web_search is OFF by default (it isn't even offered when EDITOR_WEB_SEARCH is off, so the model
    normally can't call it). If it is somehow invoked while disabled, return a clear "disabled"
    result rather than raising. When the env enables it, a real search backend gets wired in HERE;
    until then, enabled-but-unwired returns an explicit "not yet implemented" so the behaviour is
    never a silent fabrication."""
    if not web_search_enabled():
        return "web_search: disabled (set EDITOR_WEB_SEARCH=1 to enable). No web results."
    # Enabled but no backend wired yet — the clean seam for a future search integration.
    return (
        "web_search: enabled but no search backend is wired yet. No web results available; "
        "do not invent any."
    )


__all__ = [
    "TOOL_KB_SEARCH",
    "TOOL_FETCH_SOURCE",
    "TOOL_WEB_SEARCH",
    "DEFAULT_FETCH_TOOL_CHARS",
    "fetch_tool_chars",
    "web_search_enabled",
    "tool_schemas",
    "ToolCall",
    "ParsedResponse",
    "dispatch_tool",
]

# `_parse_response` is intentionally module-private but exported for the draft loop + tests.
__all__.append("_parse_response")
