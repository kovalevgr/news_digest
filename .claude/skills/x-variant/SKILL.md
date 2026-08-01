---
name: x-variant
description: Produce the X/Twitter variant (standalone hook post, optionally a numbered thread) of an approved canonical piece for manual copy-paste. Use when the owner asks for an X version, tweet, Twitter thread, or X variant of a piece.
---

# X / Twitter variant

Reformat an approved canonical into an X hook post (plus a thread only when warranted). This is
a single reformatting pass — not a re-draft, not an agent loop. The result is TEXT ONLY for the
owner to copy and post manually: **you NEVER post anywhere — the owner posts by hand.**

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
5. Write it to `pieces/<slug>/variants/x.md` (`mkdir -p pieces/<slug>/variants`). The file
   contains the formatted variant ONLY — no preamble, no notes, no commentary before or after
   it.
6. **Commit:** `git add pieces/<slug>/variants && git commit -m "variant(<slug>): x"`.
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

## Platform brief (ported verbatim from app/variants/format.py _PLATFORM_BRIEFS["x"])

```text
TARGET PLATFORM: X / Twitter (a hook post, optionally followed by a thread).
CONDENSE the canonical into a strong, standalone HOOK POST first, then a numbered THREAD ('1/', '2/', …) ONLY when the piece warrants more than the hook — a short, single-point canonical may be just the hook with no thread. Format rules: PLAIN TEXT only — NO Markdown headings, no '#' headers, no code fences; each tweet must be SELF-CONTAINED and roughly AT OR UNDER 280 characters. Hook-first: the opening tweet must stand on its own and earn the read without relying on the rest. Carry the owner's angle through the thread and keep the single most important sourced point. Put the canonical/source link in the FINAL tweet so readers can go deeper. Stay strictly grounded in the canonical — condensing only, never adding. NO hashtag spam, NO clickbait, NO engagement-bait ('like and retweet', 'follow for more', etc.).
```

## Shared conventions (all writing skills)

- Never invent facts; a variant adds NOTHING the canonical does not already say.
- Carry provenance links through the variant.
- Proposed takes stay marked as proposals unless the owner approved them — in an approved
  canonical the takes are already the owner's settled positions; carry them through as-is.
- All output text is for MANUAL copy-paste — the system never posts anywhere, integrates no
  posting API, and never claims something has been published.
