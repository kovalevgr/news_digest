---
name: publish-piece
description: Mark a piece as published — bookkeeping ONLY, never posts anything. Records which platforms the owner posted to (with dates), sets status published, and freezes the canonical into published/ (the voice KB). Use when the owner says they posted or published a piece.
---

# Mark a piece as published

Bookkeeping for a canonical the owner has ALREADY posted manually. This skill posts NOTHING —
it records what the owner did and freezes the canonical into `published/`, which is the voice
knowledge base the /draft-piece skill mines for voice few-shot and continuity on every future
draft. A published article IS the knowledge base — there is no separate store.

## File layout (all writing skills operate on this)

- `pieces/<slug>/draft.md` — the working canonical draft
- `pieces/<slug>/meta.yaml` — `piece_type` (hot_news|tech_explainer|project_post|digest),
  `status` (drafting|pre_publish|published), `created`, `posted: {linkedin:, medium:, reddit:, x:}`
- `pieces/<slug>/sources/` — grounding files (frontmatter `kind: source|owner`; `url:` carries
  each source's provenance link)
- `pieces/<slug>/variants/<platform>.md` — per-platform variants
- `published/<date>-<slug>.md` — frozen published canonicals: THE VOICE KB (this skill writes it)
- `content/style_guide.md`, `content/anti_patterns.md` — voice files (read-only; never modify)

## Procedure

1. Identify the `<slug>`; read `pieces/<slug>/meta.yaml`.
2. **PRECONDITION:** `status` must be `pre_publish` — refuse otherwise:
   - `drafting` → tell the owner to /approve-piece first (Gate 2 comes before publishing).
   - `published` → already recorded. To record an ADDITIONAL platform posting, just fill the
     new `posted.<platform>` date in `meta.yaml` and commit — do not re-freeze the canonical.
     <!-- Simplest option for late extra-platform postings; not specified upstream. -->
3. Ask (or take from the conversation) WHICH platforms the owner posted to and the dates.
   Fill `posted.<platform>: <YYYY-MM-DD>` for each platform the owner names (linkedin, medium,
   reddit, x) — leave un-posted platforms empty. Default date: today.
4. Set `status: published` in `meta.yaml`.
5. **Freeze the canonical:** copy `pieces/<slug>/draft.md` to `published/<YYYY-MM-DD>-<slug>.md`
   (`mkdir -p published`; date = the publish date, today unless the owner gave an earlier
   posted date), prepending frontmatter:

   ```yaml
   ---
   title: <the draft's H1 title>
   date: <YYYY-MM-DD>
   piece_type: <from meta.yaml>
   sources:
     - <url from each sources/ file's frontmatter, in order>
   ---
   ```

   <!-- Frontmatter shape (title/date/piece_type/sources) is the simplest option; date in the
        filename = publish date. Not specified further upstream. -->
   The body below the frontmatter is the draft VERBATIM — the frozen file is the canonical as
   approved and posted, never a rewrite.
6. **Commit:** `git add pieces/<slug>/meta.yaml published/ && git commit -m "publish(<slug>)"`.
   <!-- If the directory is not a git repository yet, skip the commit, tell the owner, and do
        not run `git init` unasked. -->
7. Confirm to the owner what was recorded (platforms + dates) and that the canonical is now in
   the voice KB.

## Shared conventions (all writing skills)

- Never invent facts; this skill records only what the owner actually reports having posted —
  never assume or backfill a platform the owner did not name.
- Carry provenance links: the frozen file's frontmatter preserves the piece's source links.
- Proposed takes stay marked as proposals unless the owner approved them (an approved,
  published canonical's takes are the owner's settled positions).
- All output text is for MANUAL copy-paste — the system never posts anywhere, integrates no
  posting API, and never claims something has been published beyond what the owner reported.
