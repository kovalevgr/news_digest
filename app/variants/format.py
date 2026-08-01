"""Per-platform variant formatting — single calls, on demand (docs/01_technical.md §2.4, §4;
build plan Phase 5).

After Gate 2 the owner has an approved canonical long-read. A *variant* is that canonical
reformatted/condensed for ONE target platform, produced on demand for the platform being posted
to. Each variant is a SINGLE model call — NOT an agent (hard rule 5: the one agent is the writer;
triage/variant formatting are single-shot). This module is the same shape as the canonical
single-shot pattern (app.researcher.triage): a PURE prompt build + a module-level `generate`
monkeypatch seam + a thin DB path + env knobs with fallback-on-garbage.

Grounding contract (HARD RULE — docs hard rule 2): a variant REFORMATS the already-approved
canonical; it does NOT re-report. The prompt forbids introducing ANY new facts, numbers, names,
dates, or quotes beyond the canonical, requires preserving the provenance links the canonical
carries, and keeps opinions as the owner's (they are already settled in the canonical). The model
reformats; it never invents. The canonical is the model's only input.

NEVER publish (hard rule 1): a variant is TEXT ONLY for the owner to copy and post by hand. This
module posts nothing and integrates no posting API.

Two layers, split so the model boundary is unit-testable without a DB or network:

  - build_variant_prompt / format_variant — PURE prompt assembly + the ONE generate() call. The
    canonical goes in a cacheable system block (cache_control ephemeral on the last block, matching
    context.build_system_blocks); the user turn carries the platform brief. Tested directly with a
    monkeypatched module-level `generate`.
  - generate_variant / latest_variant / list_latest_variants — the DB path: derive a variant for a
    Gate-2-approved (pre_publish/published) article, APPEND a variants row (regenerating appends,
    never overwrites — there is no unique constraint on (article_id, platform)), and read back the
    latest per platform.

MODEL SWAPPABLE: the one generate() call uses a logical ROLE via variant_role() (default
"generation" — docs §4 maps variant formatting to the `generation` workhorse). NEVER a model id.

The platform set is a CODE constant (PLATFORMS) matching docs §3's variants enum (linkedin /
medium / reddit) — it is not config (config.yaml is for sources/people/topics/cadences).
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from sqlalchemy import select

from app.db.models import Article, Variant
from app.llm import generate  # module-level import = the test monkeypatch seam

log = logging.getLogger("variants.format")

# The platforms a variant can target. A CODE constant (not config): the variants table's platform
# enum (docs §3 "linkedin / medium / reddit") is part of the schema/code surface, not owner-tunable
# config. Ordered medium → reddit → linkedin → x (lightest reformat → heaviest condense, with the
# X/Twitter thread last) for stable, readable iteration; membership is what callers validate
# against.
PLATFORMS = ("medium", "reddit", "linkedin", "x")

# Article statuses from which a variant may be derived. Variants come AFTER Gate 2 (docs §2.4
# "After Gate 2, variants are derived from it"): pre_publish (approved canonical, not yet posted)
# or published (already posted — re-deriving a variant is still fine). A drafting article has no
# approved canonical to reformat, so it is refused.
_VARIANT_FROM_STATUSES = ("pre_publish", "published")

# Output caps so a runaway reply can't bloat a row. Generous vs a real variant; bounds the worst
# case, not the normal case (LinkedIn condenses, Medium ~passes through a long-read).
DEFAULT_VARIANT_MAX_CHARS = 100_000

# max_tokens for the variant generate() call. A Medium/Reddit variant is ~the length of the
# canonical (roughly passthrough), so it needs the same room as a draft; LinkedIn is far shorter.
DEFAULT_VARIANT_MAX_TOKENS = 8000

# The logical role for the variant call. "generation" — docs §4 maps variant formatting to the
# `generation` workhorse (same tier as drafting). A logical role only — NEVER a model id (the
# role→model map lives in app.llm.config).
DEFAULT_VARIANT_ROLE = "generation"


def variant_role() -> str:
    """Logical role for the variant call (env VARIANT_ROLE, default 'generation'). A blank
    override falls back to the default so we never pass an empty role into the role→model map.
    NEVER a model id."""
    raw = os.environ.get("VARIANT_ROLE")
    if raw is None or not raw.strip():
        return DEFAULT_VARIANT_ROLE
    return raw.strip()


def variant_max_chars() -> int:
    """Stored-variant length cap (env VARIANT_MAX_CHARS). Falls back on absence/garbage/
    non-positive — the cap is never accidentally disabled."""
    return _pos_int_env("VARIANT_MAX_CHARS", DEFAULT_VARIANT_MAX_CHARS)


def variant_max_tokens() -> int:
    """max_tokens for the variant generate() call (env VARIANT_MAX_TOKENS). Falls back on
    absence/garbage/non-positive."""
    return _pos_int_env("VARIANT_MAX_TOKENS", DEFAULT_VARIANT_MAX_TOKENS)


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


# --- result type ---------------------------------------------------------------------------


@dataclass
class VariantResult:
    """One produced/loaded variant — primitives only (detached from the ORM), so it survives the
    request session closing and renders into the web UI without touching a live Variant row."""
    article_id: str
    platform: str
    formatted_text: str
    variant_id: int


# --- per-platform briefs (the single-call instruction) -------------------------------------

# The grounding constraint every brief carries, verbatim. A variant REFORMATS the canonical — it
# never re-reports — so the model must add no new facts, must keep the canonical's provenance
# links, and must treat the takes as the owner's (already settled in the canonical). Kept as a
# constant so the test can pin that every platform's prompt enforces it.
_VARIANT_GROUNDING = (
    "GROUNDING (hard rules — follow exactly):\n"
    "- You are REFORMATTING the owner's already-approved canonical below — you are NOT writing a "
    "new piece and NOT re-reporting. Use ONLY what is in the canonical.\n"
    "- Do NOT introduce any new facts, numbers, names, dates, quotes, or claims that are not "
    "already in the canonical. Add nothing it does not already say.\n"
    "- PRESERVE the provenance links the canonical carries (keep the source URLs/citations) so "
    "the owner can still verify and attribute.\n"
    "- The opinions and takes are the OWNER'S and are already settled in the canonical — carry "
    "them through as-is; do not soften, strengthen, or invent positions.\n"
    "- You output TEXT ONLY for the owner to copy and post manually. You never publish or post."
)

# Per-platform formatting briefs. These shape the single call's output. Kept as a dict constant
# (mirroring context._PIECE_TYPE_BRIEFS) so the platform-specific instruction is one source of
# truth and the test can pin each platform's markers.
_PLATFORM_BRIEFS = {
    "medium": (
        "TARGET PLATFORM: Medium.\n"
        "Format the canonical as a clean, well-structured Markdown article: use headers, "
        "subheaders, bold/emphasis, code blocks where code appears, and proper Markdown links. "
        "This is roughly a PASSTHROUGH — PRESERVE the full length and substance of the canonical; "
        "do NOT condense, summarize, or cut. You are formatting, not rewriting: keep the wording "
        "and the argument intact and only impose Markdown structure on it. Keep every provenance "
        "link."
    ),
    "reddit": (
        "TARGET PLATFORM: Reddit (a technical subreddit).\n"
        "Format the canonical as Reddit-flavored Markdown, with a LIGHT tone adjustment for a "
        "technical subreddit: slightly more conversational and direct, a touch less formal — "
        "without changing the substance. PRESERVE the substance and length (do NOT condense "
        "significantly) and keep every provenance link. You are reformatting and lightly "
        "adjusting tone, not rewriting or shortening the piece."
    ),
    "linkedin": (
        "TARGET PLATFORM: LinkedIn (a short feed post).\n"
        "CONDENSE the canonical into a short, hook-first, PLAIN-TEXT feed post — NO Markdown "
        "headers, no '#' headings, no code fences. The long-read does not fit the feed, so decide "
        "what to KEEP and what to CUT: lead with a strong hook in the first line, keep only the "
        "core point and the single most compelling detail, and keep it tight (a few short "
        "paragraphs). Stay strictly grounded in the canonical — condensing only, never adding. "
        "Keep the key provenance link(s) so readers can go deeper."
    ),
    "x": (
        "TARGET PLATFORM: X / Twitter (a hook post, optionally followed by a thread).\n"
        "CONDENSE the canonical into a strong, standalone HOOK POST first, then a numbered THREAD "
        "('1/', '2/', …) ONLY when the piece warrants more than the hook — a short, single-point "
        "canonical may be just the hook with no thread. Format rules: PLAIN TEXT only — NO Markdown "
        "headings, no '#' headers, no code fences; each tweet must be SELF-CONTAINED and roughly "
        "AT OR UNDER 280 characters. Hook-first: the opening tweet must stand on its own and earn "
        "the read without relying on the rest. Carry the owner's angle through the thread and keep "
        "the single most important sourced point. Put the canonical/source link in the FINAL tweet "
        "so readers can go deeper. Stay strictly grounded in the canonical — condensing only, never "
        "adding. NO hashtag spam, NO clickbait, NO engagement-bait ('like and retweet', 'follow "
        "for more', etc.)."
    ),
}


def platform_brief(platform: str) -> str:
    """The formatting brief for a platform (PURE). Raises ValueError on an unknown platform — the
    caller validates against PLATFORMS upstream, so this guards the pure path independently."""
    if platform not in _PLATFORM_BRIEFS:
        raise ValueError(
            f"unknown platform {platform!r}; expected one of {PLATFORMS}"
        )
    return _PLATFORM_BRIEFS[platform]


# --- pure: prompt assembly -----------------------------------------------------------------


def build_variant_system_blocks(canonical: str) -> list:
    """Assemble the variant system prompt as content BLOCKS (PURE — no DB, no network).

    Order: a framing header + the GROUNDING constraint, then the CANONICAL itself. The canonical
    is the large stable context, so the LAST block carries `cache_control: ephemeral` — the
    prompt-caching seam (matching context.build_system_blocks). The Anthropic provider forwards
    system blocks verbatim; the fake provider/tests ignore cache_control."""
    header = (
        "You are a formatter for a personal AI/IT content engine. The owner has already written "
        "and approved a canonical long-read; your only job is to REFORMAT it for one target "
        "platform. You add no facts and no opinions — you reshape what is already there."
    )
    canonical_block = (
        "CANONICAL (the owner's approved long-read — reformat THIS; add nothing it does not say):\n\n"
        f"{canonical}"
    )
    texts = [header, _VARIANT_GROUNDING, canonical_block]
    blocks = [{"type": "text", "text": t} for t in texts if t]
    if blocks:
        # Mark the final (largest, stable) block cacheable — the prompt-caching seam.
        blocks[-1] = {**blocks[-1], "cache_control": {"type": "ephemeral"}}
    return blocks


def build_variant_prompt(platform: str, *, piece_type: str | None = None) -> str:
    """The user turn that asks for the variant. PURE.

    The heavy stable context (header, grounding, the canonical) lives in the system blocks; this
    user turn carries the platform brief and a final reminder of the reformat-don't-re-report
    posture, so the model returns ONLY the formatted variant. `piece_type` is folded in as light
    context (a hot_news vs project_post canonical reads differently) without changing the brief."""
    brief = platform_brief(platform)
    piece_note = (
        f"\n\n(The canonical's piece type is '{piece_type}'.)" if piece_type else ""
    )
    return (
        f"{brief}{piece_note}\n\n"
        "Reformat the CANONICAL in your system context for this platform, following the GROUNDING "
        "rules exactly (no new facts, preserve provenance, keep the owner's takes). Reply with the "
        "formatted variant ONLY — no preamble, no notes, no commentary before or after it."
    )


# --- the single model call -----------------------------------------------------------------


def format_variant(platform: str, canonical: str, *, piece_type: str | None = None) -> str:
    """The ONE model call: build the prompt + system blocks, call generate(role=variant_role()),
    return the model's variant text (capped).

    Factored out (platform + canonical in, variant text out) so the model boundary is a single
    seam the DB path shares and tests can monkeypatch via the module-level `generate`. NO tools are
    passed — this is a single-shot call, not an agent loop (hard rule 5) — so the provider returns
    plain text. The role is logical (variant_role()), never a model id. Validates the platform so a
    bad platform is rejected before the call."""
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform {platform!r}; expected one of {PLATFORMS}")

    system_blocks = build_variant_system_blocks(canonical)
    user_message = build_variant_prompt(platform, piece_type=piece_type)
    text = generate(
        messages=[{"role": "user", "content": user_message}],
        role=variant_role(),
        system=system_blocks,
        max_tokens=variant_max_tokens(),
    )
    return (text or "")[: variant_max_chars()]


# --- DB path -------------------------------------------------------------------------------


def generate_variant(session, article_id: str, platform: str) -> VariantResult:
    """Derive (and persist) a platform variant from an article's approved canonical.

    Steps:
      1. Validate `platform` against PLATFORMS (a bad platform is a programming/UI error).
      2. Load the article (ValueError if missing).
      3. Require the article be past Gate 2 (status in pre_publish/published) — variants are
         derived from the APPROVED canonical (docs §2.4 "After Gate 2, variants are derived"). A
         drafting article has no approved canonical, so we refuse with a clear message.
      4. Require a non-empty current_draft (there is nothing to reformat otherwise).
      5. Run the single model call (format_variant) → the variant text.
      6. APPEND a new variants row — regenerating a platform appends a fresh row rather than
         overwriting (there is no unique constraint on (article_id, platform), so the variant
         history is preserved and latest_variant just reads the newest).

    Commits and returns a detached VariantResult. Coordinates only through Postgres (reads the
    article, writes the variant); calls no other stage; NEVER publishes — it produces text only.
    """
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform {platform!r}; expected one of {PLATFORMS}")

    article = session.get(Article, article_id)
    if article is None:
        raise ValueError(f"article {article_id!r} not found")
    if article.status not in _VARIANT_FROM_STATUSES:
        raise ValueError(
            f"article {article_id!r} is {article.status!r}; approve the canonical at Gate 2 "
            "(→ pre_publish) before generating variants"
        )

    canonical = (article.current_draft or "").strip()
    if not canonical:
        raise ValueError(
            f"article {article_id!r}: the canonical draft is empty — nothing to format"
        )

    text = format_variant(platform, canonical, piece_type=article.piece_type)

    variant = Variant(article_id=article_id, platform=platform, formatted_text=text)
    session.add(variant)
    session.commit()
    log.info(
        "generated %s variant %s for article %s (%d chars)",
        platform, variant.id, article_id, len(text),
    )
    return VariantResult(
        article_id=article_id,
        platform=platform,
        formatted_text=text,
        variant_id=variant.id,
    )


def save_variant_edit(session, article_id: str, platform: str, text: str) -> VariantResult:
    """Persist an OWNER-EDITED variant: a hand-tuned variant text the owner typed/adjusted in an
    editable UI field, saved back to the store.

    This is the MANUAL hand-tune persistence path — NOT generate_variant/format_variant. It makes
    NO model call: it is a plain DB write of the owner's own text. (generate_variant runs the single
    model call; this one just stores what the owner already wrote.)

    Steps:
      1. Validate `platform` against PLATFORMS (a bad platform is a programming/UI error).
      2. Load the article (ValueError if missing). Unlike generate_variant we do NOT gate on
         status here: this saves text the owner has already authored by hand, so the canonical's
         lifecycle stage is irrelevant — the only requirement is that the article exists.
      3. Strip the text; refuse empty/whitespace-only (there is nothing to save otherwise).
      4. Cap at variant_max_chars() (same bound generate_variant applies, so a hand-paste cannot
         bloat a row past the stored cap).
      5. No-op guard: if the latest variant for (article, platform) already holds exactly this
         (capped) text, return it unchanged rather than appending a duplicate row — re-saving an
         unedited field is a no-op, so the history stays meaningful.
      6. Otherwise APPEND a new variants row (the same append-history pattern as generate_variant —
         there is no unique constraint on (article_id, platform), so saving preserves prior
         versions and latest_variant just reads the newest).

    Commits and returns a detached VariantResult. Coordinates only through Postgres (reads the
    article, writes the variant); calls no other stage; NEVER publishes — it stores text only.
    """
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform {platform!r}; expected one of {PLATFORMS}")

    article = session.get(Article, article_id)
    if article is None:
        raise ValueError(f"article {article_id!r} not found")

    text = (text or "").strip()
    if not text:
        raise ValueError("nothing to save — the variant text is empty")
    text = text[: variant_max_chars()]

    existing = latest_variant(session, article_id, platform)
    if existing is not None and existing.formatted_text == text:
        log.info(
            "save_variant_edit no-op for %s article %s (text unchanged)",
            platform, article_id,
        )
        return existing

    variant = Variant(article_id=article_id, platform=platform, formatted_text=text)
    session.add(variant)
    session.commit()
    log.info(
        "saved owner-edited %s variant %s for article %s (%d chars)",
        platform, variant.id, article_id, len(text),
    )
    return VariantResult(
        article_id=article_id,
        platform=platform,
        formatted_text=text,
        variant_id=variant.id,
    )


def latest_variant(session, article_id: str, platform: str) -> VariantResult | None:
    """The most-recently-generated variant for (article, platform), or None.

    Reads the newest variants row by id DESC (the id is a BigInteger autoincrement, so it is
    monotonic — the highest id is the latest generation). Returns a detached VariantResult or None
    when this platform has never been generated for the article."""
    row = session.execute(
        select(Variant)
        .where(Variant.article_id == article_id)
        .where(Variant.platform == platform)
        .order_by(Variant.id.desc())
        .limit(1)
    ).scalar_one_or_none()
    if row is None:
        return None
    return VariantResult(
        article_id=article_id,
        platform=row.platform,
        formatted_text=row.formatted_text or "",
        variant_id=row.id,
    )


def list_latest_variants(session, article_id: str) -> dict:
    """The latest variant per platform for an article: {platform: VariantResult}.

    Only platforms that ACTUALLY have a row appear (a never-generated platform is absent, not a
    None entry). Reads all of the article's variants newest-first and keeps the first (newest) seen
    per platform — one query, deterministic. Returns detached VariantResults."""
    rows = session.execute(
        select(Variant)
        .where(Variant.article_id == article_id)
        .order_by(Variant.id.desc())
    ).scalars().all()
    latest: dict = {}
    for row in rows:
        if row.platform in latest:
            continue  # newer row already kept (we scan id DESC)
        latest[row.platform] = VariantResult(
            article_id=article_id,
            platform=row.platform,
            formatted_text=row.formatted_text or "",
            variant_id=row.id,
        )
    return latest


__all__ = [
    "PLATFORMS",
    "DEFAULT_VARIANT_MAX_CHARS",
    "DEFAULT_VARIANT_MAX_TOKENS",
    "DEFAULT_VARIANT_ROLE",
    "variant_role",
    "variant_max_chars",
    "variant_max_tokens",
    "VariantResult",
    "platform_brief",
    "build_variant_system_blocks",
    "build_variant_prompt",
    "format_variant",
    "generate_variant",
    "save_variant_edit",
    "latest_variant",
    "list_latest_variants",
]
