# Platform playbook: Reddit

Agent-facing reference for writing or reformatting a piece for a technical subreddit. Read by
`/platform-piece` (native write) and `/reddit-variant` (reformat). Owner-editable; fold real
signal into "What worked". Voice lives in `content/style_guide.md` / `content/anti_patterns.md`.

## Who reads here

- The most sceptical audience of the four: practitioners who verify claims, run the code, and
  call out marketing in the first comment.
- They reward reproducible detail (hardware, versions, numbers, what failed) and honest
  first-person reports; they punish self-promotion, link-only posts, and polished "content".
- Each subreddit has its own rules and mods. **The subreddit is chosen first; the post is
  written for that subreddit**, not "for Reddit".

## Choosing the subreddit (default targets for this owner's topics)

| Subreddit | Fits | Conventions to respect |
| --- | --- | --- |
| r/LocalLLaMA | local models, quantization, inference engines, "runs on my hardware" | hardware + versions + tok/s expected; benchmarks with method; no vendor-speak |
| r/LLMDevs | agent harnesses, tooling, MCP, building with LLMs | practical, code-adjacent; "I built X" posts welcome if they show the how |
| r/MachineLearning | research-grade results, papers | title prefix tags `[D]` discussion / `[P]` project / `[R]` research; strict on self-promo |
| r/ClaudeAI, r/cursor, r/ChatGPTCoding | coding-agent workflows, tool-specific | tool-specific; check current rules on promotion |

Always confirm the subreddit's rules at posting time (they change). If a post is about the
owner's own project, the owner must disclose that in the post body — Reddit norms and many
subreddit rules require it.

## Hard format constraints

- **Self-post (text post), not a link post.** Link-only posts to Medium are removed or
  ignored on technical subreddits. Put the substance in the post; link the long-read/repo at
  the bottom as "full write-up".
- **Reddit-flavored Markdown:** headers (`##`), bold, lists, fenced code blocks (render with
  monospace, no highlighting), and pipe tables all work — tables are welcome for benchmarks.
- **Title:** specific, contains the result or the question, no clickbait; add the subreddit's
  tag prefix if it uses one. Titles cannot be edited after posting — get it right.
- **TL;DR** at the top OR the bottom (both are common); for long posts, at the top.
- **Length:** substance decides; technical subreddits read long posts if every paragraph
  carries information. Do not condense a benchmark write-up; do cut narrative padding.
- **Links:** inline, and every claim keeps its source. Repo/gist links for anything
  reproducible.
- **Disclosure:** "I built this" / "this is my project" stated plainly where applicable.

## Structure that works

1. **Title** with the result or the honest question.
2. **TL;DR** (2–4 bullets) for long posts.
3. **Setup:** hardware, versions, model/quant, what was measured and how. Reddit reads this
   before the results — omit it and the first comment asks for it.
4. **Results:** tables and numbers, with units and the run conditions.
5. **What broke / caveats:** the section that earns trust. Include dead ends.
6. **The take**, short, first person, clearly the owner's.
7. **Links:** repo, full write-up, sources.

For `hot_news` on Reddit: the post is a discussion starter — lead with the concrete news,
one sourced detail, and a real question to the community, not a recap of the article.

## Avoid on Reddit

- Marketing register of any kind; superlatives; "excited to share".
- Link-only posts; posts that read as a Medium article pasted in.
- Hiding that it is the owner's own project.
- Numbers without method (hardware, quant, context length, how measured).
- Emoji, hashtags, LinkedIn-style line-per-sentence.
- Not answering comments — the owner should plan to reply in the first hours (this is a note
  for the owner, not a rule for the text).

## Pre-paste checklist

- [ ] Subreddit chosen; its rules and tag prefix checked.
- [ ] Self-post with substance in the body; long-read/repo linked at the end.
- [ ] Setup/method section present for any numbers.
- [ ] Disclosure line present if it is the owner's project.
- [ ] Every claim keeps its link; TL;DR present for long posts.

## What worked (owner fills from published pieces)

_Empty until the first Reddit post ships. Fold in: which subreddit, what got upvoted vs
removed, which questions the comments asked (they reveal what the post should have had)._
