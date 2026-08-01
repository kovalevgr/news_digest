---
name: reddit-variant
description: Produce the Reddit variant (Reddit-flavored Markdown with a light conversational tone shift, full substance kept) of an approved canonical piece for manual copy-paste. Use when the owner asks for a Reddit version, Reddit post, or Reddit variant of a piece.
---

# Reddit variant

Reformat an approved canonical for a technical subreddit. This is a single reformatting pass —
not a re-draft, not an agent loop. The result is TEXT ONLY for the owner to copy and post
manually: **you NEVER post anywhere — the owner posts by hand.**

Role framing (ported verbatim from app/variants/format.py build_variant_system_blocks):

```text
You are a formatter for a personal AI/IT content engine. The owner has already written and approved a canonical long-read; your only job is to REFORMAT it for one target platform. You add no facts and no opinions — you reshape what is already there.
```

## File layout (all writing skills operate on this)

- `pieces/<slug>/draft.md` — the canonical (THE ONLY input to this skill)
- `pieces/<slug>/meta.yaml` — `piece_type`, `status` (drafting|pre_publish|published), `created`,
  `posted: {linkedin:, medium:, reddit:, x:}`
- `pieces/<slug>/sources/` — grounding files (NOT read here — a variant reformats, never re-reports)
- `pieces/<slug>/variants/<platform>.md` — the output of this skill
- `published/<date>-<slug>.md` — frozen published canonicals (the voice KB)
- `content/style_guide.md`, `content/anti_patterns.md` — voice files (read-only; never modify)

## Procedure

1. Identify the `<slug>`; read `pieces/<slug>/meta.yaml`.
2. **PRECONDITION:** `status` must be `pre_publish` or `published`. If it is `drafting`,
   **STOP** and tell the owner to run /approve-piece first — variants come only after Gate 2.
3. Read `pieces/<slug>/draft.md`. It is the ONLY input — do not read `sources/`, do not fetch
   anything, do not consult other files for facts.
4. Produce the variant per the GROUNDING block and the platform brief below. May note the
   canonical's `piece_type` as light context for tone (a hot_news vs project_post canonical
   reads differently) without changing the brief.
5. Write it to `pieces/<slug>/variants/reddit.md` (`mkdir -p pieces/<slug>/variants`). The file
   contains the formatted variant ONLY — no preamble, no notes, no commentary before or after
   it.
6. **Commit:** `git add pieces/<slug>/variants && git commit -m "variant(<slug>): reddit"`.
   <!-- If the directory is not a git repository yet, skip the commit, tell the owner, and do
        not run `git init` unasked. -->
7. **Show the full variant text in chat** so the owner can copy-paste it. Remind them: the
   system never posts — they post it manually.

## GROUNDING (ported verbatim from app/variants/format.py _VARIANT_GROUNDING)

```text
GROUNDING (hard rules — follow exactly):
- You are REFORMATTING the owner's already-approved canonical below — you are NOT writing a new piece and NOT re-reporting. Use ONLY what is in the canonical.
- Do NOT introduce any new facts, numbers, names, dates, quotes, or claims that are not already in the canonical. Add nothing it does not already say.
- PRESERVE the provenance links the canonical carries (keep the source URLs/citations) so the owner can still verify and attribute.
- The opinions and takes are the OWNER'S and are already settled in the canonical — carry them through as-is; do not soften, strengthen, or invent positions.
- You output TEXT ONLY for the owner to copy and post manually. You never publish or post.
```

## Platform brief (ported verbatim from app/variants/format.py _PLATFORM_BRIEFS["reddit"])

```text
TARGET PLATFORM: Reddit (a technical subreddit).
Format the canonical as Reddit-flavored Markdown, with a LIGHT tone adjustment for a technical subreddit: slightly more conversational and direct, a touch less formal — without changing the substance. PRESERVE the substance and length (do NOT condense significantly) and keep every provenance link. You are reformatting and lightly adjusting tone, not rewriting or shortening the piece.
```

## Shared conventions (all writing skills)

- Never invent facts; a variant adds NOTHING the canonical does not already say.
- Carry provenance links through the variant.
- Proposed takes stay marked as proposals unless the owner approved them — in an approved
  canonical the takes are already the owner's settled positions; carry them through as-is.
- All output text is for MANUAL copy-paste — the system never posts anywhere, integrates no
  posting API, and never claims something has been published.
