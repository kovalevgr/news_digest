"""Per-platform single-call formatters (Medium / Reddit / LinkedIn) — Phase 5
(docs/01_technical.md §2.4, §4).

After Gate 2 (the owner approves the canonical → pre_publish), a variant is the canonical
reformatted/condensed for ONE platform, produced on demand by a SINGLE model call per platform —
not an agent (hard rule 5). A variant is TEXT ONLY for the owner to copy and post manually; the
system never publishes (hard rule 1). The model reformats the canonical and adds no facts (hard
rule 2 — grounding).

Public surface (re-exported from app.variants.format):
  - PLATFORMS — the valid target platforms ("medium", "reddit", "linkedin").
  - VariantResult — a detached (primitives-only) produced/loaded variant.
  - generate_variant(session, article_id, platform) -> VariantResult
      Derive + persist (append) a variant from a Gate-2-approved article's canonical.
  - save_variant_edit(session, article_id, platform, text) -> VariantResult
      Persist an owner-edited (hand-tuned) variant — a plain DB write, NO model call.
  - latest_variant(session, article_id, platform) -> VariantResult | None
  - list_latest_variants(session, article_id) -> dict[str, VariantResult]
  - format_variant(platform, canonical, *, piece_type=None) -> str
      The single model-call seam (PURE prompt build + one generate() call).
"""
from app.variants.format import (
    PLATFORMS,
    VariantResult,
    build_variant_prompt,
    build_variant_system_blocks,
    format_variant,
    generate_variant,
    latest_variant,
    list_latest_variants,
    platform_brief,
    save_variant_edit,
    variant_max_chars,
    variant_max_tokens,
    variant_role,
)

__all__ = [
    "PLATFORMS",
    "VariantResult",
    "generate_variant",
    "save_variant_edit",
    "latest_variant",
    "list_latest_variants",
    "format_variant",
    "platform_brief",
    "build_variant_prompt",
    "build_variant_system_blocks",
    "variant_role",
    "variant_max_chars",
    "variant_max_tokens",
]
