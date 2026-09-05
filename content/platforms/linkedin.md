# Platform playbook: LinkedIn

Agent-facing reference for writing or reformatting a piece for LinkedIn. Read by
`/platform-piece` (native write) and `/linkedin-variant` (condense). Owner-editable; fold real
signal into "What worked". Voice lives in `content/style_guide.md` / `content/anti_patterns.md`.

## Who reads here

- Engineers, engineering managers, founders, recruiters scrolling a feed on a phone.
- They see the first 2–3 lines, then a "…see more" fold. The hook decides everything.
- They reward a specific, useful point from a real person; they punish marketing register
  and obvious engagement-bait.

## Hard format constraints

- **Plain text only.** No Markdown: no `#`, no `**bold**`, no code fences, no pipe tables.
  Line breaks and blank lines are the only formatting. (Unicode bold/italic exists but reads
  as a gimmick — do not use it.)
- **Length:** post limit is 3,000 characters. Working range 900–1,600 characters; a
  project_post or a strong hot_news can go to ~2,200. Never fill to the limit.
- **The fold:** the first ~200 characters (2–3 short lines) show before "…see more". The hook
  must earn the click without clickbait: a concrete number, a surprising result, a sharp
  contrast, or the owner's clear claim.
- **Paragraphs:** 1–3 sentences each, blank line between. Mobile reading, not a wall of text.
- **Links:** LinkedIn deprioritises posts with external links in the body (widely reported
  platform behaviour; treat as a practical rule, not a law). Default: put the ONE deep link
  (repo, source, or the Medium long-read) as a final line labelled for the owner to move into
  the first comment if they prefer:
  `[link → first comment or keep here, owner's call]: <url>`
  Provenance for facts still has to be recoverable — if several sources matter, the canonical
  carries them; the LinkedIn post points at the canonical.
- **Hashtags:** 0–3, at the very end, specific (`#LLM #LocalAI`), never inline.
- **Mentions:** `@` people/companies only when they are actually part of the story.
- **Code:** never as fences. A one-line command is fine inline in backticks-less plain text;
  anything longer → screenshot or link.

## Structure that works

1. **Hook (line 1–2):** the result or the claim. Not the topic, not "I've been thinking about".
2. **One concrete detail** that proves the hook: a number with its unit, a named tool, a
   before/after.
3. **Why it matters** for the reader (one paragraph).
4. **The owner's take**, in one or two sentences, in the first person.
5. **Close:** a question that a practitioner would actually want to answer, or a plain
   takeaway. No "agree?", no "thoughts?", no "repost if useful".
6. Link line + hashtags.

Shapes: for `project_post` a short first-person "what I built / what I measured / what broke"
works; for `hot_news` lead with the news and the angle, not a recap.

## Avoid on LinkedIn

- Broetry (one word per line, emoji bullets) unless the owner asks for it explicitly.
- Engagement bait: "agree?", "thoughts?", "like if…", "follow for more".
- Inspirational framing, "humbled to announce", "game-changer".
- Recapping the whole long-read; keep ONE point and send readers to the canonical for the rest.
- Emoji as bullets; at most one or two emoji if they carry meaning, usually zero.
- Hashtag spam and inline hashtags.

## Pre-paste checklist

- [ ] First 2–3 lines stand alone and contain a concrete hook.
- [ ] No Markdown syntax survives (`#`, `**`, backticks, tables).
- [ ] 900–1,600 characters (≤ 2,200 for a strong piece).
- [ ] One deep link, positioned per the link rule; 0–3 hashtags at the end.
- [ ] No engagement bait in the close.

## What worked (owner fills from published pieces)

_Empty until the first LinkedIn post ships. Fold in: which hooks got expands, whether the
link-in-comment rule mattered, best length._
