# Platform playbook: Medium

Agent-facing reference for writing or reformatting a piece for Medium. Read by
`/platform-piece` (native write) and `/medium-variant` (reformat). Owner-editable; the
"What worked" section at the bottom is where real signal from published pieces gets folded in.
The voice itself lives in `content/style_guide.md` / `content/anti_patterns.md` — this file is
only about the platform.

## Who reads here

- Practitioners who clicked a title from a feed, a Google result, or a LinkedIn/X link.
- They decide in the first paragraph whether the piece is worth 6–10 minutes.
- They expect depth: a Medium reader who wanted a summary would have stayed on LinkedIn.

## Hard format constraints

- **Title:** one line, specific, no clickbait; aim ≤ 60 characters so it does not truncate in
  cards. The title says what the reader gets, not what the topic is
  ("Four V100s match a 5090 on Qwen3.8 decode" beats "Thoughts on old GPUs").
- **Subtitle:** one sentence, the promise of the piece (Medium shows it under the title).
- **Headers:** `##` for sections, `###` sparingly. No `#` H1 (the title field is the H1).
- **Length:** 1,200–2,500 words is the working range for a technical piece; longer only when
  the substance needs it. Medium shows read time; 6–10 min is the sweet spot.
- **Code:** fenced code blocks render but without syntax highlighting; keep snippets short
  (≤ 15 lines) and only when they explain the mechanism. Long code → link to a gist/repo.
- **Tables:** Medium has NO native tables. Render tabular data as a short list, a code block
  (monospace), or say "see table in the repo" with a link. Never leave Markdown pipe tables in
  a Medium variant — they paste as broken text.
- **Images:** one image per major section at most; every image gets a caption with the source.
  Charts and screenshots are worth more than stock art. Never fabricate a chart.
- **Links:** inline Markdown links; every sourced claim keeps its provenance link. External
  links are fine on Medium (no reach penalty).
- **Tags:** up to 5 at the end (`Tags: AI, LLM, Software Engineering, …`) — write them as a
  final line for the owner to paste into the tag field.

## Structure that works

1. **Lede (first 2–3 sentences):** the actual news/result and why it matters. This paragraph
   is the preview text in feeds — it must stand alone.
2. **Context in one paragraph:** what the reader needs to follow, no more.
3. **The body:** one through-line; each `##` marks a real shift. Concrete first, then
   interpretation. Numbers in prose only when there are one or two; more → list.
4. **The take:** the owner's angle, clearly marked as such. One, not five.
5. **Close:** an earned takeaway or open question. No "follow me", no CTA paragraph.
6. Optional **TL;DR** block right under the subtitle for dense technical pieces (3 bullets max).

## Avoid on Medium

- Listicle titles ("7 things…") unless the piece really is a list.
- A paragraph of throat-clearing before the point.
- Bare URLs in the text; always anchor text.
- Emoji in headers; bold-every-other-sentence.
- Markdown tables (see constraints).
- Ending with a sales-style CTA or "let me know in the comments".

## Pre-paste checklist

- [ ] Title ≤ 60 chars, subtitle present.
- [ ] First paragraph works as a standalone preview.
- [ ] No `#` H1, no pipe tables, code blocks ≤ 15 lines.
- [ ] Every fact keeps its link; every image has a caption + source.
- [ ] Tags line at the end (≤ 5).

## What worked (owner fills from published pieces)

_Empty until the first Medium piece is published. Fold in: which titles got read, what length,
which structure._
