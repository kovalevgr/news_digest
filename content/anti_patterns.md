# Anti-patterns

Things the writer-agent should avoid in the owner's voice. **Bootstrapped with the owner at the
start of Phase 3.** Per the owner: what to avoid is **largely article-dependent** — so this is
deliberately two layers, not one rigid ban-list:

1. a small **universal core** that's wrong in (almost) any piece, and
2. **context-dependent** candidates the owner flags per draft.

It is a **living document**: the owner's per-draft chat instructions are the real signal; recurring
"don't do that" notes get folded up into the universal core over time.

## Universal core — avoid in (almost) every piece

- **AI / LLM clichés.** No "delve", "game-changer", "unlock", "leverage" (as a verb), "in today's
  fast-paced world", "the world of …", "it's not just X — it's Y", "buckle up", "let's dive in".
  These read as machine-written and undercut the grounded voice.
- **Hype without substance.** No marketing/sales register, no sweeping superlatives ("revolutionary",
  "the future of …") unless a specific, sourced fact earns them. Claims should be concrete and
  load-bearing.
- **Invented specificity.** Never fabricate numbers, benchmarks, names, dates, or quotes to sound
  authoritative. Unsupported = flagged, not asserted (this is also a hard grounding rule).
- **Single-source ≠ unverified.** A fact taken directly from an approved source is *sourced*, not
  uncertain — do not tag it `[Unverified]` or hedge it ("presumably", "worth cross-referencing").
  The `[Unverified]` flag is only for claims that go *beyond* the source: an inferred date, a name
  the source never gave, a number you reconstructed. Over-flagging grounded facts reads tentative
  and bureaucratic and buries the real uncertain claims in noise (see Hedging vs. conviction).
- **Borrowed opinions.** Don't state a take as the owner's settled view; propose it for approval
  (style guide → Authenticity).
- **A menu of takes instead of a take.** At most one or two `[Proposed take]` blocks per draft, and
  never end them with a boilerplate "the owner may want to expand or cut this" tail — that hedge is
  true of *every* proposal, so it carries no information and just offloads the editorial call. Find
  the through-line, propose it once, and let the owner accept/edit/cut. Five takes with identical
  exit-hatches means the draft refused to commit to a read — which is the one thing a `hot_news`
  piece is for.
- **Filler & throat-clearing.** No "In this article we will…", no restating the title as the first
  sentence, no padding to hit a length.

## Context-dependent — judgement per article (flag, don't hard-ban)

These depend on the piece, the platform, and the owner's intent for *that* draft — propose, and let
the owner decide in chat:

- **Emoji & "broetry".** LinkedIn's one-line-per-paragraph, emoji-bulleted "engagement" style — fine
  in small doses for some LinkedIn posts, wrong for a Medium long-read. Default to restraint; ask if
  unsure.
- **Hedging vs. conviction.** Over-hedging ("it depends", stacked disclaimers) dilutes a strong
  piece, but some topics genuinely warrant caution. Match the certainty to the evidence, not a fixed
  rule.
- **Length & density.** A dense technical deep-dive and a quick reaction post want different
  ceilings — driven by `piece_type` and platform, not a global limit.
- **Formality.** Reddit wants conversational and anti-marketing; LinkedIn wants professional;
  Medium sits between. The canonical draft leans Medium; variants adjust.

---

*v1 stub from the owner's voice interview ("it depends on the article"). The universal core is the
safe default; everything else the owner steers per draft. Grow this file from real edit_log signals.*
