"""Context assembly for the writer-agent draft — the quality crux (docs/01_technical.md §2.3,
§4; build plan Phase 3).

The draft's quality is decided here, before the model is ever called. This module builds the
three stable pieces of the draft context:

  (a) the owner's VOICE — content/style_guide.md + content/anti_patterns.md, read from the
      read-only `content/` mount (path via env CONTENT_DIR, default "content"). These are files,
      not DB rows (config-in-file principle), and are loaded into EVERY draft's context.
  (b) the cluster's SOURCE BUNDLE — its items' title + pass-2 full_text + provenance URL. This
      is the grounding set: the agent may use ONLY these facts (plus anything it explicitly
      fetches via a tool). Clusters are first-class — the bundle is assembled from the cluster's
      items, never per-item.
  (c) the PIECE-TYPE template/shape — a short structural brief for hot_news (default) /
      project_post / digest. The per-type templates are an intentionally-OPEN decision
      (docs/03_build_plan.md "Per-piece-type templates"): these are sensible v1 stubs behind a
      clean seam, refined by experiment.

KB retrieval (past published articles) is NOT assembled here — it is an ON-DEMAND tool
(kb_search) the agent calls when it wants voice few-shot / continuity, so the agent decides when
it is worth the retrieval rather than always paying for it. (Today the KB is empty anyway.)

The system prompt also carries the GROUNDING rules (hard rule 2): use only the bundle + tool
facts, carry provenance links, flag unverified claims, never invent facts, and treat opinions as
the owner's (propose, never assert). These are assembled here, in build_system_blocks, so the
one place that builds the context is the one place that enforces grounding.

Prompt-caching seam: the large stable context (voice files + source bundle + grounding +
template) is emitted as system BLOCKS with cache_control on the last block, so the Anthropic
provider can mark it cacheable. Phase-4 iteration resends this same context every turn, so
caching it materially cuts input cost. The blocks degrade to plain text for the fake provider
and the tests (which don't care about cache_control).

Pure where it counts: the prompt assembly (build_source_bundle_text, piece_type_brief,
build_system_blocks) is PURE — string in, string out, no DB, no network — so it is unit-testable
without a database. Only `load_source_bundle` (reads the cluster's items) and `load_voice_files`
(reads the mount) touch I/O, each a thin seam.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

from sqlalchemy import select

from app.db.models import ArticleCluster, Item as ItemModel
from app.editor.article import DEFAULT_PIECE_TYPE

log = logging.getLogger("editor.context")

# The voice files live under the content/ mount (read-only). Path via env so the deploy can
# point at the mounted volume; default "content" matches the repo layout for local runs.
DEFAULT_CONTENT_DIR = "content"
STYLE_GUIDE_FILE = "style_guide.md"
ANTI_PATTERNS_FILE = "anti_patterns.md"

# Cap the per-item full_text we inline into the source bundle. A pass-2 extraction can be very
# long (fetcher caps at 200k chars); inlining several at full length would blow the context.
# The agent can always `fetch_source(url)` for the complete text on demand — this cap is for the
# always-loaded bundle, the fetch tool is the escape hatch for full detail. Env-overridable.
DEFAULT_BUNDLE_ITEM_CHARS = 4000

# Cap how many of a cluster's items go into the bundle. A cluster is one story; a handful of its
# items is plenty of grounding. Oldest-first (stable) so the bundle is reproducible run-to-run.
DEFAULT_BUNDLE_MAX_ITEMS = 12


def content_dir() -> Path:
    """The content/ mount directory (env CONTENT_DIR, default 'content'). Returns a Path; a
    blank override falls back to the default so we never resolve against an empty string."""
    raw = os.environ.get("CONTENT_DIR")
    if raw is None or not raw.strip():
        return Path(DEFAULT_CONTENT_DIR)
    return Path(raw.strip())


def bundle_item_chars() -> int:
    """Max chars of each item's full_text inlined into the bundle (env BUNDLE_ITEM_CHARS).
    Falls back on absence/garbage/non-positive — the inline cap is never disabled."""
    raw = os.environ.get("BUNDLE_ITEM_CHARS")
    if raw is None:
        return DEFAULT_BUNDLE_ITEM_CHARS
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad BUNDLE_ITEM_CHARS=%r — falling back to %s", raw, DEFAULT_BUNDLE_ITEM_CHARS)
        return DEFAULT_BUNDLE_ITEM_CHARS
    return val if val > 0 else DEFAULT_BUNDLE_ITEM_CHARS


def bundle_max_items() -> int:
    """Max items pulled into the bundle (env BUNDLE_MAX_ITEMS). Falls back on absence/garbage/
    non-positive — we always include at least the default number of items."""
    raw = os.environ.get("BUNDLE_MAX_ITEMS")
    if raw is None:
        return DEFAULT_BUNDLE_MAX_ITEMS
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad BUNDLE_MAX_ITEMS=%r — falling back to %s", raw, DEFAULT_BUNDLE_MAX_ITEMS)
        return DEFAULT_BUNDLE_MAX_ITEMS
    return val if val > 0 else DEFAULT_BUNDLE_MAX_ITEMS


# --- voice files (I/O seam over the content/ mount) ----------------------------------------


@dataclass
class VoiceFiles:
    """The owner's voice context, loaded from the content/ mount. Empty strings (not an error)
    when a file is missing — the draft still runs grounded; a missing style guide just means
    weaker voice steering, which the agent loop tolerates."""
    style_guide: str = ""
    anti_patterns: str = ""

    @property
    def present(self) -> bool:
        return bool(self.style_guide.strip() or self.anti_patterns.strip())


def load_voice_files(*, directory: Path | None = None) -> VoiceFiles:
    """Read style_guide.md + anti_patterns.md from the content/ mount. I/O seam.

    A missing or unreadable file degrades to "" (logged) rather than raising — the draft must
    still run if the owner hasn't authored a file yet, or the mount isn't present in a dev run.
    Read-only: this never writes the mount."""
    directory = directory or content_dir()
    return VoiceFiles(
        style_guide=_read_text(directory / STYLE_GUIDE_FILE),
        anti_patterns=_read_text(directory / ANTI_PATTERNS_FILE),
    )


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as e:
        log.warning("voice file %s unreadable (%s); proceeding without it", path, e)
        return ""


# --- source bundle (the grounding set) -----------------------------------------------------


@dataclass
class SourceItem:
    """One item of an article's grounding bundle — primitives only (survives the session closing).

    `kind` distinguishes a third-party source item ("source", a cluster item's fetched text) from
    the owner's own material ("owner", an OwnerSource row — see app.editor.sources). The default
    "source" keeps every existing construction valid; build_source_bundle_text renders an "owner"
    item as [OWNER ARTIFACT] and adds an authoritative-source note (the owner's own numbers are
    facts to cite, not claims to flag)."""
    title: str
    url: str
    full_text: str  # pass-2 extraction / owner content; "" if not fetched (empty/paywalled)
    kind: str = "source"  # "source" (third-party) | "owner" (the owner's own material)


@dataclass
class SourceBundle:
    """The cluster's grounding set: its items + the cluster id they came from."""
    cluster_id: str
    items: list = field(default_factory=list)

    @property
    def has_full_text(self) -> bool:
        """True iff at least one item carries pass-2 full_text. The draft step uses this to refuse
        to draft a cluster with no fetched source text (grounding would have nothing to stand
        on) and surface a clear error to the owner."""
        return any(it.full_text.strip() for it in self.items)

    @property
    def provenance_urls(self) -> list:
        """Every non-empty source URL in the bundle — the provenance links the draft must carry."""
        return [it.url for it in self.items if it.url]


def load_source_bundle(session, cluster_id: str) -> SourceBundle:
    """Assemble a cluster's source bundle from its items (title + pass-2 full_text + url). I/O.

    Selects the cluster's items oldest-first (stable), capped at bundle_max_items(). Reads pass-1
    metadata (title, url) and pass-2 full_text; an item whose full_text is still NULL contributes
    its title + url (the agent can fetch_source(url) for its text on demand). Returns primitives,
    so the bundle survives the request session closing.

    Clusters first-class: the bundle is the cluster's items, never a single item."""
    rows = session.execute(
        select(ItemModel.title, ItemModel.url, ItemModel.full_text)
        .where(ItemModel.cluster_id == cluster_id)
        .order_by(ItemModel.fetched_at.asc(), ItemModel.id.asc())
        .limit(bundle_max_items())
    ).all()
    items = [
        SourceItem(
            title=(r.title or "").strip(),
            url=(r.url or "").strip(),
            full_text=(r.full_text or "").strip(),
        )
        for r in rows
    ]
    return SourceBundle(cluster_id=cluster_id, items=items)


def _linked_cluster_id(session, article_id: str) -> str | None:
    """The cluster id linked to an article (article_clusters), or None. Mirrors the helper in
    draft.py / iterate.py: a hot_news article maps to exactly one cluster (its first link); a
    flagship article has none. Defined here so load_grounding_bundle resolves a cluster without a
    draft↔context import cycle. I/O."""
    return session.execute(
        select(ArticleCluster.cluster_id)
        .where(ArticleCluster.article_id == article_id)
        .order_by(ArticleCluster.cluster_id.asc())
        .limit(1)
    ).scalar_one_or_none()


def load_grounding_bundle(session, article_id: str) -> SourceBundle:
    """Assemble an article's FULL grounding bundle — cluster items + owner material. ALWAYS returns
    a bundle (its items may be empty). I/O.

    The grounding corpus of an article is the union of:
      - the linked cluster's items (the hot_news path) — if the article has a linked cluster;
      - the owner's own attached material (the flagship path) — OwnerSource rows (kind='owner').
    A hot_news article contributes only cluster items; a flagship article contributes only owner
    material; an article could carry both. `cluster_id` on the returned bundle is the linked
    cluster id or None (flagship). `has_full_text` now naturally counts owner content, so the draft
    guard refuses only the truly-empty union (no cluster text AND no owner material).

    Clusters first-class: the cluster portion is still the cluster's items, never per-item."""
    # Lazy import: app.editor.sources imports SourceItem from this module, so importing it at module
    # level would create a cycle. Importing here keeps the seam clean.
    from app.editor.sources import load_owner_sources

    cluster_id = _linked_cluster_id(session, article_id)
    items: list = []
    if cluster_id is not None:
        items.extend(load_source_bundle(session, cluster_id).items)
    items.extend(load_owner_sources(session, article_id))
    return SourceBundle(cluster_id=cluster_id, items=items)


def build_source_bundle_text(bundle: SourceBundle, *, item_chars: int | None = None) -> str:
    """Render the source bundle as the grounding block the model reads. PURE.

    Each item is rendered as a numbered SOURCE with its title, its provenance URL (so the agent
    can carry the link into the draft and cite it), and its pass-2 full_text capped at
    `item_chars`. An item with no fetched text is marked so — the agent knows it can fetch_source
    that URL for detail rather than inventing it. Numbered so the draft and the owner can refer to
    "source 2".

    An item with kind=='owner' (the owner's own material — see app.editor.sources) is labelled
    [OWNER ARTIFACT] instead of [SOURCE], same Title/URL/Text shape. When the bundle contains ANY
    owner item, a single leading note tells the agent the owner's own results are authoritative
    facts to cite — not third-party claims to flag as unverified."""
    cap = item_chars if item_chars is not None else bundle_item_chars()
    if not bundle.items:
        return "(no source items — this cluster has no items; do not invent any.)"
    parts: list[str] = []
    for i, it in enumerate(bundle.items, start=1):
        title = it.title or "(untitled)"
        url = it.url or "(no url)"
        if it.full_text:
            body = it.full_text[:cap]
            if len(it.full_text) > cap:
                body += " […truncated; use fetch_source for the full text]"
        else:
            body = "(no full text fetched — use the fetch_source tool on the URL if you need its content; do NOT invent it)"
        label = "OWNER ARTIFACT" if getattr(it, "kind", "source") == "owner" else "SOURCE"
        parts.append(f"[{label} {i}]\nTitle: {title}\nURL: {url}\nText: {body}")
    rendered = "\n\n".join(parts)
    if any(getattr(it, "kind", "source") == "owner" for it in bundle.items):
        rendered = (
            "OWNER ARTIFACT entries are the owner's own material/results — treat them as "
            "authoritative source facts to cite; do not flag the owner's own numbers as "
            "unverified.\n\n" + rendered
        )
    return rendered


# --- piece-type template (an intentionally-OPEN decision — v1 stubs behind a seam) ---------

# Per-piece-type structural briefs. These are short v1 stubs (docs/03_build_plan.md flags the
# per-piece-type templates as an open decision to refine by experiment). hot_news is the default;
# project_post / digest are deliberately brief stubs — Phase 6 owns the real digest flow.
_PIECE_TYPE_BRIEFS = {
    "hot_news": (
        "PIECE TYPE: hot_news — a timely news-commentary long-read (the canonical, Medium-leaning).\n"
        "- Open with the actual news and why it matters; no throat-clearing.\n"
        "- One clear through-line; subheads only where the piece genuinely shifts.\n"
        "- Concrete over abstract: name the tool, the number, the tradeoff — all sourced.\n"
        "- End on an earned takeaway or open question, not a bolted-on CTA.\n"
        "- The reader can get the bare facts elsewhere; the value is the read and the angle."
    ),
    "project_post": (
        "PIECE TYPE: project_post — a first-person building-in-public piece.\n"
        "- What was built, why, what was hard, what was learned — honest about tradeoffs and dead ends.\n"
        "- Credibility is in the specifics, not the polish."
    ),
    "digest": (
        "PIECE TYPE: digest — a dense rollup of several stories (Phase 6 owns the full digest flow).\n"
        "- Brief, scannable summaries of each story with its provenance link; not a single long-read.\n"
        "- This is a v1 stub; the digest job assembles the real structure."
    ),
    "tech_explainer": (
        "PIECE TYPE: tech_explainer — a teach-down explainer that makes one technical thing click "
        "for a capable-but-non-expert reader (the flagship own-material piece).\n"
        "- Structure: motivation (why it matters) → mechanism (how it works) → a worked example → "
        "when to use it (and when NOT to) → caveats/limitations.\n"
        "- Technical but accessible: define a term the first time, build from the concrete; no hand-"
        "waving and no needless jargon.\n"
        "- Grounded strictly in the owner's material — the owner's own numbers/results are facts to "
        "cite, not claims to soften; never invent detail to fill the structure.\n"
        "- The owner's takes (when X is the right tradeoff, where it falls down) stay PROPOSALS for "
        "the owner to accept or cut, not asserted as settled."
    ),
}


def piece_type_brief(piece_type: str) -> str:
    """The structural brief for a piece type (PURE). Falls back to the hot_news brief for an
    unknown type (the draft step validates the type upstream, so this fallback is defensive)."""
    return _PIECE_TYPE_BRIEFS.get(piece_type, _PIECE_TYPE_BRIEFS[DEFAULT_PIECE_TYPE])


# --- grounding rules (hard rule 2 — one place, enforced in the system prompt) --------------

# The grounding/authenticity contract, verbatim in the system prompt. Hard rule 2 + the style
# guide's "Grounding & authenticity" section. Kept as a constant so the test can pin that the
# system prompt actually carries these instructions (grounding is not optional).
GROUNDING_RULES = (
    "GROUNDING RULES (these are hard rules — follow them exactly):\n"
    "1. Use ONLY facts present in the SOURCE BUNDLE below, plus anything you explicitly fetch via "
    "the fetch_source / kb_search tools. Do NOT introduce outside facts, numbers, names, dates, "
    "or quotes. If you are unsure whether something is in the sources, treat it as not in them.\n"
    "2. Carry PROVENANCE links into the draft: when you state a sourced fact, reference the source "
    "URL it came from so the owner can verify it.\n"
    "3. FLAG any claim that is uncertain or not directly supported by a source — mark it clearly "
    "(e.g. '[unverified — owner to check]') for the owner to verify, rather than asserting it.\n"
    "4. NEVER invent facts to sound authoritative. An unsupported claim is flagged, not stated.\n"
    "5. Opinions and takes are the OWNER'S. You may PROPOSE a position or angle, but present it "
    "clearly as a proposal for the owner to accept, edit, or cut (e.g. '[proposed take: …]'). "
    "Never assert a judgement as the owner's own settled view.\n"
    "6. You are drafting only — you never publish, post, or claim anything has been published."
)


def build_system_blocks(
    *,
    voice: VoiceFiles,
    bundle: SourceBundle,
    piece_type: str = DEFAULT_PIECE_TYPE,
    item_chars: int | None = None,
) -> list:
    """Assemble the system prompt as Anthropic content BLOCKS. PURE (no DB, no network).

    Order: a framing header, the GROUNDING rules (first, so they frame everything), the piece-
    type brief, the VOICE files (style guide + anti-patterns), then the SOURCE BUNDLE. The whole
    thing is the large STABLE context that Phase-4 iteration resends each turn, so the LAST block
    carries `cache_control: ephemeral` — the prompt-caching seam (the Anthropic provider passes
    system blocks straight through; the fake provider/tests ignore cache_control).

    Returns a list of {"type": "text", "text": ...} blocks (the Anthropic `system` shape). Use
    `system_blocks_to_text` to flatten them for a provider/test that wants a single string."""
    header = (
        "You are the writer-agent for a personal AI/IT content engine. You ghostwrite ONE "
        "canonical long-read in the owner's voice, grounded strictly in the provided sources. "
        "The owner reviews and edits everything you produce; you propose, the owner decides."
    )

    voice_block = _voice_block_text(voice)
    bundle_text = build_source_bundle_text(bundle, item_chars=item_chars)
    bundle_block = (
        "SOURCE BUNDLE (the grounding set — your facts come from here and from tools only):\n\n"
        f"{bundle_text}"
    )

    texts = [
        header,
        GROUNDING_RULES,
        piece_type_brief(piece_type),
        voice_block,
        bundle_block,
    ]
    blocks = [{"type": "text", "text": t} for t in texts if t]
    if blocks:
        # Mark the final (largest, stable) block cacheable. The Anthropic provider forwards
        # system blocks verbatim, so this enables prompt caching of the assembled context that
        # Phase-4 iteration resends each turn. Harmless to providers that ignore it.
        blocks[-1] = {**blocks[-1], "cache_control": {"type": "ephemeral"}}
    return blocks


# --- iterate context (Phase 4: edit-in-place on the working draft) -------------------------

# The edit-in-place contract, verbatim in the iterate system prompt (docs §2.3 "Iterate",
# hard rule 5/§4: edit in place, never regenerate; respect manual edits). Kept as a constant so
# the test can pin that the iterate prompt actually carries it. This is what turns the same
# writer-agent from "write a draft" into "apply ONE change to the draft I already have".
EDIT_IN_PLACE_RULES = (
    "ITERATION RULES (these are hard rules — follow them exactly):\n"
    "1. You are EDITING AN EXISTING DRAFT IN PLACE — you are NOT writing a new one. Apply ONLY "
    "the owner's requested change and preserve everything else verbatim: keep the wording, "
    "structure, and especially any of the owner's own hand-edits exactly as they are unless the "
    "instruction is to change them.\n"
    "2. NEVER regenerate or rewrite the whole draft from scratch — that would undo the owner's "
    "refinements. Make the smallest edit that satisfies the instruction.\n"
    "3. Your final message is the COMPLETE revised draft as markdown — the full document, not a "
    "diff, a snippet, or a description of the change. Do NOT add any preamble, sign-off, or "
    "commentary (no 'Here is the updated draft', no notes after it): reply with the draft and "
    "nothing else.\n"
    "4. The GROUNDING RULES still apply to anything NEW you add: only facts from the source "
    "bundle or tools, carry provenance, flag unverified, propose-don't-assert, never publish."
)

# The structural-reformat directive used when the owner switches piece_type mid-stream. A switch
# is NOT a point edit (docs §2.3 "Piece type": switching is a structural reformat) — so we tell
# the agent to restructure the existing draft's content into the new shape rather than tweak it.
PIECE_SWITCH_RULES = (
    "PIECE-TYPE SWITCH: the owner is switching this piece to the piece type described above. "
    "This is a STRUCTURAL REFORMAT, not a point edit — restructure the existing draft's content "
    "into the new shape (reorganise sections, adjust framing/length to fit the new type) while "
    "keeping the same underlying, grounded facts and the owner's substance. Do not invent new "
    "facts to fill the new structure."
)


def build_iterate_system_blocks(
    *,
    voice: VoiceFiles,
    bundle: SourceBundle,
    current_draft: str,
    piece_type: str = DEFAULT_PIECE_TYPE,
    is_piece_switch: bool = False,
    item_chars: int | None = None,
) -> list:
    """Assemble the ITERATE system prompt as content BLOCKS (PURE — no DB, no network).

    The iterate context is the draft context PLUS two things: the EDIT-IN-PLACE rules (so the
    agent edits the existing draft instead of writing a fresh one) and a CURRENT DRAFT block
    carrying the working text the agent must edit. On a piece-type switch we also fold in the
    structural-reformat directive (PIECE_SWITCH_RULES) and use the new type's brief.

    Order: header, GROUNDING rules, the EDIT-IN-PLACE rules (+ the switch directive when
    switching), the piece-type brief, the VOICE files, the SOURCE BUNDLE, then the CURRENT DRAFT.
    The CURRENT DRAFT is last and changes every turn — but the bundle/voice/rules above it are the
    large STABLE prefix that the within-call tool loop resends each turn, so the cache breakpoint
    goes on the SOURCE BUNDLE block (the last *stable* block), not the volatile draft. This keeps
    the prompt-caching seam pointed at what actually repeats (matching build_system_blocks intent).
    """
    header = (
        "You are the writer-agent for a personal AI/IT content engine, now ITERATING on an "
        "existing canonical draft in the owner's voice. The owner gives you one instruction at a "
        "time and you edit the draft in place, grounded strictly in the provided sources. The "
        "owner reviews and edits everything; you propose, the owner decides."
    )

    iterate_rules = EDIT_IN_PLACE_RULES
    if is_piece_switch:
        iterate_rules = f"{EDIT_IN_PLACE_RULES}\n\n{PIECE_SWITCH_RULES}"

    voice_block = _voice_block_text(voice)
    bundle_text = build_source_bundle_text(bundle, item_chars=item_chars)
    bundle_block = (
        "SOURCE BUNDLE (the grounding set — facts for anything NEW come from here and tools only):\n\n"
        f"{bundle_text}"
    )
    draft_block = (
        "CURRENT DRAFT (the working text — edit THIS in place; preserve everything you are not "
        "asked to change):\n\n"
        f"{current_draft or '(the draft is currently empty.)'}"
    )

    stable_texts = [
        header,
        GROUNDING_RULES,
        iterate_rules,
        piece_type_brief(piece_type),
        voice_block,
        bundle_block,
    ]
    stable_blocks = [{"type": "text", "text": t} for t in stable_texts if t]
    if stable_blocks:
        # Cache breakpoint on the last STABLE block (the source bundle) — the draft block below is
        # volatile (it changes every owner turn), so caching it would never hit.
        stable_blocks[-1] = {**stable_blocks[-1], "cache_control": {"type": "ephemeral"}}
    # The volatile current-draft block goes after the cache breakpoint, uncached.
    return [*stable_blocks, {"type": "text", "text": draft_block}]


def build_iterate_message(instruction: str) -> str:
    """The user turn that carries the owner's iterate instruction. PURE.

    The heavy stable context (rules, voice, bundle) and the current draft live in the system
    prompt; this user turn is just the owner's instruction plus a reminder of the edit-in-place
    posture and the tools, so the model returns the full revised draft as its final message."""
    return (
        "Apply this instruction to the CURRENT DRAFT in your system context, editing in place "
        "(preserve everything you are not asked to change). You may call kb_search / fetch_source "
        "if a change needs grounding or detail, but stay within the sources. Reply with the FULL "
        "revised draft as your final message (markdown only, no preamble or commentary).\n\n"
        f"OWNER INSTRUCTION:\n{instruction}"
    )


def _voice_block_text(voice: VoiceFiles) -> str:
    """Render the voice files into one system block. PURE."""
    if not voice.present:
        return (
            "OWNER VOICE: (no style guide or anti-patterns file found — write in a clear, "
            "grounded, non-hype voice and avoid AI clichés.)"
        )
    parts = ["OWNER VOICE — follow these style rules and avoid these anti-patterns:"]
    if voice.style_guide.strip():
        parts.append("=== STYLE GUIDE ===\n" + voice.style_guide.strip())
    if voice.anti_patterns.strip():
        parts.append("=== ANTI-PATTERNS ===\n" + voice.anti_patterns.strip())
    return "\n\n".join(parts)


def system_blocks_to_text(blocks: list) -> str:
    """Flatten system blocks to a single string (PURE) — for a provider/test that wants plain
    text instead of the block list. Joins each block's text with blank lines."""
    return "\n\n".join(b.get("text", "") for b in blocks if b.get("text"))


__all__ = [
    "DEFAULT_CONTENT_DIR",
    "STYLE_GUIDE_FILE",
    "ANTI_PATTERNS_FILE",
    "DEFAULT_BUNDLE_ITEM_CHARS",
    "DEFAULT_BUNDLE_MAX_ITEMS",
    "GROUNDING_RULES",
    "EDIT_IN_PLACE_RULES",
    "PIECE_SWITCH_RULES",
    "content_dir",
    "bundle_item_chars",
    "bundle_max_items",
    "VoiceFiles",
    "load_voice_files",
    "SourceItem",
    "SourceBundle",
    "load_source_bundle",
    "load_grounding_bundle",
    "build_source_bundle_text",
    "piece_type_brief",
    "build_system_blocks",
    "build_iterate_system_blocks",
    "build_iterate_message",
    "system_blocks_to_text",
]
