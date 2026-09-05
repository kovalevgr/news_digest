---
name: platform-piece
description: Write a piece NATIVELY for one platform (linkedin, x, medium, reddit) straight from grounding sources, when the story does not need a canonical long-read first — a LinkedIn post about a release, an X thread on a benchmark, a Reddit write-up of an experiment. Use when the owner asks to write/draft a post, thread, or article FOR a named platform (not a variant of an existing piece), or says "напиши пост для LinkedIn/X/Reddit/Medium про …".
---

# Write a piece natively for one platform

The canonical flow (`/draft-piece` → `/approve-piece` → `/<platform>-variant`) is for stories
that deserve a long-read first. This skill is the short path: the owner names a platform and
a story, and you write the post FOR that platform from the grounding sources, in the owner's
voice, following that platform's playbook. Same grounding rules as `/draft-piece`, same
edit-in-place contract, same gates afterwards. The result is TEXT for manual copy-paste —
**you NEVER post anywhere; the owner posts by hand.**

## File layout (all writing skills operate on this)

- `pieces/<slug>/draft.md` — the platform-native draft (THE file you edit in place)
- `pieces/<slug>/meta.yaml` — `piece_type` (hot_news|tech_explainer|project_post|digest),
  **`platform`** (linkedin|x|medium|reddit — set by this skill; absent on canonical pieces),
  `status` (drafting|pre_publish|published), `created`, `posted: {linkedin:, medium:, reddit:, x:}`
- `pieces/<slug>/sources/` — grounding files (`kind: source` third-party, `kind: owner` own material)
- `pieces/<slug>/variants/<platform>.md` — variants for OTHER platforms, made after approval
- `published/<date>-<slug>.md` — frozen published pieces (the voice KB)
- `content/style_guide.md`, `content/anti_patterns.md` — voice files (read-only; never modify)
- **`content/platforms/<platform>.md`** — the platform playbook (read-only for the skill; the
  owner edits it and folds real signal into its "What worked" section)

## Procedure

1. **Platform + piece_type + slug.** The platform must be one of `linkedin | x | medium |
   reddit`; if the owner did not name one, ask — do not guess. `piece_type` defaults to
   `hot_news` for a news story, `project_post` when the owner is writing about their own
   experiment/build, `tech_explainer` for own-material teach-downs. Slug: short kebab-case from
   the working title, suffixed with the platform when a canonical piece with the same slug
   exists or is planned (e.g. `spec-driven-agents-linkedin`).
2. **Create the piece dir:** `mkdir -p pieces/<slug>/sources`.
3. **Gather grounding into `sources/`.** COPY (never move) the relevant `news/artifacts/*.md`,
   the matching lines from `news/topics/*.md` / `news/radar/*.md`, the relevant
   `news/research/*.md` section, or the owner's own material (notes, benchmark tables, repo
   README). Each file gets frontmatter:

   ```yaml
   ---
   kind: source   # or `kind: owner` for the owner's own material
   title: <title>
   url: <provenance url, if any>
   ---
   ```

   **REFUSE to draft when `sources/` is empty.** Tell the owner what material you need.
   If a primary source has only a one-line summary on disk and the post needs more, WebFetch
   it and save the fetched text into `sources/` as a new `kind: source` file (grounding stays
   on disk).
4. **Load context, in this order:**
   1. `content/style_guide.md` and `content/anti_patterns.md` (every draft, no exceptions);
   2. `content/platforms/<platform>.md` — the playbook: constraints, structure, avoid-list,
      checklist. Constraints in the playbook are hard; "structure that works" is the default
      shape unless the owner asks for another;
   3. the 2–3 most related `published/*.md` (by topic) for voice few-shot and continuity;
      prefer published pieces for the SAME platform when any exist. Skip if none.
5. **Write `pieces/<slug>/draft.md`** — the platform-native post, following the GROUNDING
   RULES, the piece-type brief, and the playbook. The file holds the post exactly as it will
   be pasted (plain text for LinkedIn/X, Markdown for Medium/Reddit) plus, ABOVE it, a short
   fenced `yaml` header block the owner does not paste:

   ````markdown
   ```yaml
   platform: linkedin
   chars: 1340          # or `words:` for medium/reddit; `posts: 5` for an X thread
   playbook_checklist: pass   # or list the items that need the owner's call
   ```
   <the post>
   ````

   For X, separate posts with a blank line and a `---` line; number them per the playbook.
   For Reddit, the first line is `Title: …` followed by the target subreddit on the second
   line (`Subreddit: r/…`), then the body. For Medium, the first two lines are `Title:` and
   `Subtitle:`.
6. **Run the playbook checklist** against the draft (character/word counts, no Markdown on
   plain-text platforms, link placement, hashtags, disclosure on Reddit). Fix what fails;
   record anything that needs the owner's decision in `playbook_checklist`.
7. **Create `pieces/<slug>/meta.yaml`:**

   ```yaml
   piece_type: hot_news        # hot_news | tech_explainer | project_post | digest
   platform: linkedin          # linkedin | x | medium | reddit
   status: drafting
   created: <YYYY-MM-DD>
   posted:
     linkedin:
     medium:
     reddit:
     x:
   ```

8. **Commit:** `git add pieces/<slug> && git commit -m "draft(<slug>): genesis [<platform>]"`.
9. **Show the post in chat** in full so the owner can react. Remind them that nothing is posted
   by the system.

Afterwards the normal gates apply: `/approve-piece` sets `pre_publish`; the OTHER platforms'
variants can then be produced with `/<platform>-variant` from this draft (they treat it as the
canonical); `/publish-piece` freezes it into `published/`.

## GROUNDING RULES (identical to /draft-piece — hard rules)

```text
GROUNDING RULES (these are hard rules — follow them exactly):
1. Use ONLY facts present in the SOURCE BUNDLE (pieces/<slug>/sources/), plus anything you explicitly fetch and save there. Do NOT introduce outside facts, numbers, names, dates, or quotes. If you are unsure whether something is in the sources, treat it as not in them.
2. Carry PROVENANCE links into the draft: when you state a sourced fact, reference the source URL it came from so the owner can verify it. On platforms where links in the body are limited (LinkedIn, X), keep the ONE deep link the playbook allows and make sure every other fact is traceable through it or through the sources/ files.
3. FLAG any claim that is uncertain or not directly supported by a source — mark it clearly (e.g. '[unverified — owner to check]') for the owner to verify, rather than asserting it. A fact taken directly from a source is sourced, not uncertain — do not over-flag.
4. NEVER invent facts to sound authoritative. An unsupported claim is flagged, not stated.
5. Opinions and takes are the OWNER'S. You may PROPOSE a position or angle, but present it clearly as a proposal for the owner to accept, edit, or cut (e.g. '[proposed take: …]'). At most one or two proposals per draft. Never assert a judgement as the owner's own settled view.
6. You are drafting only — you never publish, post, or claim anything has been published.
```

OWNER ARTIFACT note: a `sources/` file with `kind: owner` is the owner's own material — cite
its numbers as facts; do not flag them as unverified.

## Piece-type briefs (same as /draft-piece, applied through the platform's shape)

```text
hot_news — lead with the actual news and why it matters; one through-line; concrete over abstract (the tool, the number, the tradeoff — all sourced); end on an earned takeaway or open question, not a CTA. The reader can get the bare facts elsewhere; the value is the angle.
project_post — first-person building-in-public: what was built, why, what was hard, what was learned; honest about tradeoffs and dead ends; credibility is in the specifics.
tech_explainer — motivation → mechanism → worked example → when to use it (and when not) → caveats; define a term the first time; grounded in the owner's material; takes stay proposals.
digest — brief, scannable summaries of several stories with provenance links (rare on a single platform post; usually a Medium/Reddit shape).
```

The playbook decides how the brief is expressed: on LinkedIn a hot_news is a hook + one detail
+ the angle; on Reddit a project_post is setup → results table → what broke; on X it is the
hook post + numbered beats; on Medium it is the full structured long-read.

## Iterating (the edit-in-place contract — identical to /draft-piece)

- Every subsequent owner instruction in the same session is an **edit-in-place on `draft.md`**
  via the Edit tool — the smallest change that satisfies the instruction. NEVER regenerate the
  post from scratch.
- **Owner hand-edits are sacred.** Re-Read `draft.md` before every edit.
- **One instruction = one commit:** `edit(<slug>): <the owner's instruction>`; a no-op
  instruction gets `git commit --allow-empty` with the same message. The commit history is the
  voice-training signal.
- After each edit, re-run the playbook checklist and update the `yaml` header (counts,
  checklist status).
- Switching platform mid-stream is a STRUCTURAL REFORMAT, not a point edit: update
  `meta.yaml`, reshape the same grounded substance into the new playbook's shape, commit as
  `edit(<slug>): switch platform to <platform>`.

## Shared conventions (all writing skills)

- Never invent facts; every factual claim traces to a `sources/` file or an explicit fetch.
- Carry provenance links in everything you write.
- Proposed takes stay marked as proposals (`[proposed take: …]`) unless the owner approved them.
- All output text is for MANUAL copy-paste — the system never posts anywhere, integrates no
  posting API, and never claims something has been published.
- Never modify `content/style_guide.md`, `content/anti_patterns.md`, or
  `content/platforms/*.md` — those are the owner's files.
