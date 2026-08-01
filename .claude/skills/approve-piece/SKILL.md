---
name: approve-piece
description: Gate 2 approval — mark a drafted piece's canonical as approved (status drafting → pre_publish in pieces/<slug>/meta.yaml). Use when the owner says a draft is done, approved, ready, final, or "ship it", before any platform variants are generated.
---

# Approve a piece (Gate 2)

Gate 2 of the pipeline: the owner approves the canonical long-read. This is pure bookkeeping on
`meta.yaml` — it changes no draft text and (as always) posts nothing anywhere.

## File layout (all writing skills operate on this)

- `pieces/<slug>/draft.md` — the working canonical draft (edited in place by /draft-piece)
- `pieces/<slug>/meta.yaml` — `piece_type` (hot_news|tech_explainer|project_post|digest),
  `status` (drafting|pre_publish|published), `created`, `posted: {linkedin:, medium:, reddit:, x:}`
- `pieces/<slug>/sources/` — grounding files (frontmatter `kind: source|owner`)
- `pieces/<slug>/variants/<platform>.md` — per-platform variants (made after this gate)
- `published/<date>-<slug>.md` — frozen published canonicals (the voice KB)
- `content/style_guide.md`, `content/anti_patterns.md` — voice files (read-only; never modify)

## Procedure

1. Identify the `<slug>` (from the conversation, or ask; `ls pieces/` to list candidates).
2. **Verify preconditions:**
   - `pieces/<slug>/draft.md` exists and is non-empty — refuse otherwise (nothing to approve).
   - `meta.yaml` has `status: drafting`.
     - If `status: published` — **REFUSE**: the piece is already published; approval cannot be
       re-applied.
     - If `status: pre_publish` — it is already approved; tell the owner and stop (no-op, no
       commit). <!-- Simplest option: re-approving an approved piece is a no-op, not an error. -->
3. Set `status: pre_publish` in `pieces/<slug>/meta.yaml` (change nothing else in the file).
4. **Commit:** `git add pieces/<slug>/meta.yaml && git commit -m "approve(<slug>)"`.
   <!-- If the directory is not a git repository yet, skip the commit, tell the owner, and do
        not run `git init` unasked. -->
5. Tell the owner the piece is approved and the variant skills (/linkedin-variant, /x-variant,
   /medium-variant, /reddit-variant) are now available for it.

## Shared conventions (all writing skills)

- Never invent facts; every factual claim traces to a `sources/` file or an explicit fetch.
- Carry provenance links in everything written.
- Proposed takes stay marked as proposals (`[proposed take: …]`) unless the owner approved them —
  approval at this gate means the owner has settled the canonical, including its takes.
- All output text is for MANUAL copy-paste — the system never posts anywhere, integrates no
  posting API, and never claims something has been published.
