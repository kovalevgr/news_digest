# Platform playbook: X / Twitter

Agent-facing reference for writing or reformatting a piece for X. Read by `/platform-piece`
(native write) and `/x-variant` (condense). Owner-editable; fold real signal into "What
worked". Voice lives in `content/style_guide.md` / `content/anti_patterns.md`.

## Who reads here

- AI/ML practitioners, researchers, indie builders; the fastest-moving of the four audiences.
- They read the first post only; the thread gets read if the first post earned it.
- They reward a sharp, specific claim with a number or a screenshot; they punish threads that
  restate a blog post and hashtag walls.

## Hard format constraints

- **Plain text only.** No Markdown: no headers, no bold, no code fences, no tables.
- **280 characters per post** for a standard account. Write to 280 even if the owner has a
  longer limit — short posts travel further and paste anywhere. Count characters; URLs count
  as 23 characters regardless of length.
- **Thread:** number posts `1/`, `2/`, … (or `1/N` once N is known). Each post must be
  self-contained — it may be seen alone in a quote or a search result.
- **Thread only when earned:** a single-point piece is ONE post. A thread is for a piece with
  3–7 distinct beats. Never pad to make a thread.
- **Links:** the canonical/source link goes in the LAST post (the link post gets less reach;
  the hook must not depend on it). At most one link in the hook post, and only if the link IS
  the news (a repo, a release).
- **Hashtags:** 0–1, only if it is a real community tag. Default zero.
- **Code:** never as text blocks; a single short command inline is fine. Longer code → say
  "code in the repo" and link in the last post, or note `[screenshot: <what>]` for the owner
  to attach.
- **Images:** note where a chart/screenshot would go as `[image: <what it shows>, source]`;
  the owner attaches. Never describe a chart that does not exist.

## Structure that works

1. **Hook post:** the result, the number, or the claim. Written so it works with zero context.
   Patterns that hold up: a concrete before/after ("47 → 190 tok/s on the same GPU"), a
   contrast ("architecture, not the model, took ARC-AGI-3 from 30% to 100%"), a plain
   first-person result ("I ran X for a week; here's what broke").
2. **Beats 2…N-1:** one idea per post, concrete, each with its own number or fact. Keep the
   owner's angle running through; don't turn it into a neutral summary.
3. **Last post:** the takeaway + the link to the canonical/source.

## Avoid on X

- Hashtag spam, "🧵" as the whole hook, "a thread 👇" with no content in the first post.
- Engagement bait: "like and RT", "follow for more", "bookmark this".
- Restating the long-read paragraph by paragraph.
- Emoji bullets; emoji at all unless one carries meaning.
- Cliffhanger hooks that hide the point ("you won't believe…").
- Posts over 280 characters; posts that only make sense after the previous one.

## Pre-paste checklist

- [ ] Hook post stands alone and contains the concrete point.
- [ ] Every post ≤ 280 characters (URLs = 23).
- [ ] Numbered if a thread; thread only if ≥ 3 real beats.
- [ ] Link in the last post; 0–1 hashtags.
- [ ] No Markdown syntax survives; images noted as `[image: …]` placeholders.

## What worked (owner fills from published pieces)

_Empty until the first X post ships. Fold in: hook patterns that got replies/quotes, thread
vs single post, whether a screenshot helped._
