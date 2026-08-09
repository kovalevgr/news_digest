# Run log

Append-only log of researcher runs. One entry per run, newest at the bottom.
The daily run reads the LAST successful entry's timestamp to set its window
(default 26h when this log has no entries yet).

Entry format:

```
## YYYY-MM-DD HH:MM UTC — daily|weekly — ok|partial|failed
| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
...one row per company...
Totals: N items, M companies fresh, K errors.
```

Column legend:

- **searched** — sources attempted for the company this run (TIER-1 + any fallback).
- **found** — confirmed new items written to the company's topics file.
- **fell-back** — which fallback tier was used (`-`, `fetch`, `jina`, `websearch`).
- **errors** — short error notes (HTTP codes, timeouts, TRAP/not-a-feed), `-` if none.

## 2026-08-01 12:27 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss | 3 | - | - |
| anthropic | fetch | 0 | fetch | - |
| google-deepmind | rss, websearch | 0 | websearch | no in-window post confirmed on deepmind.google |
| google-research | rss, websearch | 0 | websearch | latest post (Science One Framework) predates window |
| microsoft | rss | 2 | - | 2 candidates excluded (partner marketing post, customer-story feature) |
| nvidia | rss, websearch | 0 | websearch | no NVIDIA-domain URL confirmed for in-window items |
| xai | jina | 1 | jina | - |
| mistral | rss, websearch | 0 | websearch | latest news (Microsoft partnership) predates window |
| huggingface | rss, websearch | 0 | websearch | latest post (security incident) predates window |
| cursor | rss, websearch | 0 | websearch | no in-window changelog entry confirmed |
| perplexity | jina→websearch | 0 | websearch | no dated in-window post confirmed (no JINA_API_KEY set) |
| cohere | fetch | 1 | fetch | - |

Totals: 7 items, 4 companies fresh, 0 errors (10 gap-scrapes attempted, 6 came up empty in-window).

Note: Linear already held cards KOV-5..KOV-10 for 6 of these 7 items when this run reached
step 5 — evidence of a prior interrupted attempt at this same run (Linear updated, files/log
not yet written). Only the missing xAI card (KOV-11) was created this run; no duplicates made.

## 2026-08-02 06:05 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss, websearch | 0 | websearch | no in-window post confirmed beyond prior capture |
| anthropic | fetch | 0 | fetch | latest post (cybersecurity evals incidents) Jul 30, predates window |
| google-deepmind | rss, websearch | 0 | websearch | no in-window post with confirmed URL |
| google-research | rss, websearch | 0 | websearch | latest post (Science One Framework) Jul 30, predates window |
| microsoft | rss, websearch | 0 | websearch | no in-window post with confirmed URL |
| nvidia | rss, websearch | 0 | websearch | no NVIDIA-domain in-window item confirmed |
| xai | jina | 0 | jina | latest post Jul 31 (Imagine Video 1.5), already captured, predates window |
| mistral | rss, websearch | 0 | websearch | no in-window post with confirmed URL |
| huggingface | rss, websearch | 0 | websearch | websearch claimed an Aug 3 "Supra2" post (impossible — that's tomorrow); direct blog check found no such post and nothing in-window — rejected as unconfirmed |
| cursor | rss, websearch | 0 | websearch | latest changelog entry Jul 29 (iPad), predates window |
| perplexity | jina | 0 | jina | latest post Jul 30 (Spaces are now Projects), predates window; anonymous Jina worked this run, no 403 |
| cohere | fetch | 0 | fetch | latest post Jul 31 (EU Code of Practice), already captured, predates window |

Totals: 0 items, 0 companies fresh, 0 errors (12 gap-scrapes attempted, all empty in-window;
1 rejected unconfirmed candidate — HF future-dated claim not corroborated by the source).

## 2026-08-03 06:10 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss, websearch | 0 | websearch | no in-window post confirmed beyond prior Aug 1 capture |
| anthropic | fetch | 0 | fetch | latest post Jul 30 (cybersecurity evals incidents), predates window |
| google-deepmind | rss, websearch | 0 | websearch | no confirmed in-window post (websearch returned only a relative-dated, unverifiable result) |
| google-research | rss, websearch | 0 | websearch | latest post (Science One Framework) Jul 30, predates window |
| microsoft | rss, websearch | 0 | websearch | no in-window post with confirmed URL |
| nvidia | rss, websearch | 0 | websearch | latest post Jul 30 (Agent Toolkit expansion), predates window |
| xai | jina | 0 | jina | latest post Jul 31 (Imagine Video 1.5), already captured, predates window |
| mistral | rss, websearch | 0 | websearch | no in-window post with confirmed URL |
| huggingface | rss, websearch | 0 | websearch | no in-window post with confirmed URL |
| cursor | rss, websearch | 0 | websearch | no in-window changelog entry confirmed |
| perplexity | jina | 0 | jina | latest post Jul 30 (Spaces are now Projects), predates window; anonymous Jina worked, no 403 |
| cohere | fetch | 0 | fetch | latest post Jul 31 (EU Code of Practice), already captured, predates window |

Totals: 0 items, 0 companies fresh, 0 errors (12 gap-scrapes attempted, all empty in-window).

## 2026-08-04 06:10 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss | 2 | - | - |
| anthropic | fetch | 0 | fetch | no in-window post confirmed (latest still Jul 30) |
| google-deepmind | rss, websearch | 0 | websearch | no confirmed in-window post with URL |
| google-research | rss, websearch | 0 | websearch | latest post (Science One Framework) Jul 30, predates window |
| microsoft | rss | 0 | - | 2 candidates excluded (Xbox anniversary post, general security threat-intel post — not AI product/company news) |
| nvidia | rss, websearch | 0 | websearch | websearch surfaced unlinked developer.nvidia.com titles for Aug 3, no confirmed URL — rejected as unconfirmed |
| xai | jina | 0 | jina | latest post Jul 31 (Imagine Video 1.5), already captured, predates window |
| mistral | rss, websearch | 0 | websearch | no in-window post with confirmed URL (results were older Mistral 3/Emmi AI/Tesco items) |
| huggingface | rss, websearch | 0 | websearch | no in-window post with confirmed URL |
| cursor | rss, websearch | 0 | websearch | no in-window changelog entry confirmed (latest still Jul 28) |
| perplexity | jina | 0 | jina | latest post Jul 30 (Spaces are now Projects), predates window; anonymous Jina worked, no 403 |
| cohere | fetch | 0 | fetch | no in-window post confirmed |

Totals: 2 items, 1 company fresh, 0 errors (11 gap-scrapes attempted, all empty in-window;
1 rejected unconfirmed candidate — NVIDIA developer-blog titles not corroborated by a source URL).

Note: prior daily-run commits (2026-08-01 through 2026-08-03) existed only on a detached
local HEAD at session start — `origin/main` appeared stale until a fresh `git fetch`
resolved it; no data was lost, `origin/main` already had all commits. Session then moved
off detached HEAD onto `main` before this run's commit.

## 2026-08-05 06:15 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss | 1 | - | - |
| anthropic | fetch | 1 | fetch | - |
| google-deepmind | rss, websearch | 0 | websearch | no confirmed in-window post with URL |
| google-research | rss, websearch | 0 | websearch | latest post (Science One Framework) Jul 30, predates window |
| microsoft | rss | 1 | - | - |
| nvidia | rss | 4 | - | - |
| xai | jina | 0 | jina | latest post Jul 31 (Imagine Video 1.5), already captured, predates window |
| mistral | rss | 1 | - | - |
| huggingface | rss | 1 | - | - |
| cursor | rss, websearch | 0 | websearch | no in-window changelog entry confirmed (closest was Aug 3 Google Workspace Plugins, unconfirmed by URL and predates window anyway) |
| perplexity | jina→websearch | 0 | websearch | no dated in-window post confirmed (no JINA_API_KEY set) |
| cohere | fetch | 0 | fetch | no in-window post confirmed |

Totals: 9 items, 6 companies fresh, 0 errors (7 gap-scrapes attempted, 1 confirmed hit —
anthropic exec-hire announcement — 6 came up empty in-window).

Linear: 9 issues created (KOV-15..KOV-23), all new stories, none duplicate (searched
project "News digest" by URL/title first, no matches found).

## 2026-08-06 06:15 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss, websearch | 0 | websearch | no in-window post with confirmed URL |
| anthropic | fetch | 0 | fetch | latest post still Aug 4 (Tino Cuéllar), already captured, predates window |
| google-deepmind | rss, websearch | 1 | websearch | RSS empty; WebSearch surfaced the Hassabis/Kavukcuoglu/Dean leadership reshuffle, confirmed via the official blog.google post (WebFetch got 403, Jina retry succeeded) |
| google-research | rss, websearch | 0 | websearch | latest post (Science One Framework) Jul 30, predates window |
| microsoft | rss | 1 | - | - |
| nvidia | rss | 1 | - | - |
| xai | jina | 0 | jina | latest post Jul 31 (Imagine Video 1.5), already captured, predates window |
| mistral | rss, websearch | 0 | websearch | latest post (Shieldstral) Aug 4, already captured, predates window |
| huggingface | rss, websearch | 0 | websearch | no in-window post with confirmed URL |
| cursor | rss, websearch | 0 | websearch | no in-window changelog entry confirmed |
| perplexity | jina→websearch | 0 | websearch | no dated in-window post confirmed (no JINA_API_KEY set) |
| cohere | fetch | 0 | fetch | no in-window post confirmed |

Totals: 3 items, 3 companies fresh, 0 errors (10 gap-scrapes attempted, 1 confirmed hit —
Google DeepMind leadership reshuffle — 9 came up empty in-window).

Note: session started on a detached HEAD identical to `origin/main` (3b21c71); checked
out `main` and fast-forwarded before this run's commit — no data lost.

Linear: 3 issues created (KOV-24..KOV-26), all new stories, none duplicate (searched
project "News digest" by URL/title first, no matches found).

## 2026-08-07 06:15 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss | 1 | - | - |
| anthropic | fetch | 1 | fetch | - |
| google-deepmind | rss | 1 | - | - |
| google-research | rss, websearch | 0 | websearch | latest post (Science One Framework) Jul 30, predates window |
| microsoft | rss | 1 | - | - |
| nvidia | rss | 1 | - | 1 candidate excluded (GeForce NOW weekly games list — gaming content, not AI news) |
| xai | jina | 0 | jina | latest post Jul 31 (Imagine Video 1.5), already captured, predates window |
| mistral | rss, websearch | 0 | websearch | 304 not modified on RSS; no in-window post confirmed via websearch |
| huggingface | rss, fetch | 1 | fetch | RSS empty; direct blog fetch confirmed Baseten inference-providers post |
| cursor | rss, websearch | 0 | websearch | latest changelog entry Aug 3 (Google Workspace Plugins), predates window |
| perplexity | jina | 1 | jina | RSS N/A; anonymous Jina worked, confirmed "Computer for Builders" post |
| cohere | fetch | 1 | fetch | - |

Totals: 8 items, 8 companies fresh, 0 errors (8 gap-scrapes attempted, 4 confirmed hits —
anthropic, huggingface, perplexity, cohere — 4 came up empty in-window).

Linear: 8 issues created (KOV-27..KOV-34), all new stories, none duplicate (searched
project "News digest" by URL/title first, no matches found).

Note: session started on a detached HEAD identical to `origin/main` (786ce2d); checked
out `main` and fast-forwarded before this run's commit — no data lost.

## 2026-08-08 06:10 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss | 1 | - | 1 candidate excluded (HSP GRUPPE customer case-study/marketing post) |
| anthropic | fetch | 0 | fetch | latest post Aug 7 (Fable 5 biology safeguards), already captured, predates window |
| google-deepmind | rss, websearch | 0 | websearch | no new in-window post beyond prior Aug 5/6 captures |
| google-research | rss, websearch | 0 | websearch | no in-window post with confirmed URL |
| microsoft | rss | 1 | - | 1 candidate excluded (Indonesia digital-careers human-interest/CSR feature) |
| nvidia | rss, websearch | 0 | websearch | no in-window post with confirmed URL |
| xai | jina | 1 | jina | anonymous Jina worked, no 403; confirmed "Imagine Image 2.0" |
| mistral | rss, websearch | 0 | websearch | RSS 304 not modified; no in-window post with confirmed URL |
| huggingface | rss | 1 | - | - |
| cursor | rss, websearch | 0 | websearch | no in-window changelog entry confirmed |
| perplexity | jina | 0 | jina | latest post Aug 6 (Computer for Builders), already captured, predates window; anonymous Jina worked, no 403 |
| cohere | fetch | 0 | fetch | latest post Aug 6 (Waterloo partnership), already captured, predates window |

Totals: 4 items, 4 companies fresh, 0 errors (9 gap-scrapes attempted, 1 confirmed hit —
xai — 8 came up empty in-window; 2 candidates rejected as non-news: OpenAI customer
case-study, Microsoft human-interest feature).

Note: session started on a detached HEAD identical to `origin/main` (3a2e7bd, 10 commits
behind); stashed the in-progress `cursors.json` update from the TIER-1 fetch, checked out
`main`, fast-forwarded, then reapplied the stash — no data lost.

Linear: 4 issues created (KOV-35..KOV-38), all new stories, none duplicate (searched
project "News digest" by URL/title first, no matches found).

## 2026-08-08 16:27 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss, websearch | 0 | websearch | no in-window post with confirmed URL |
| anthropic | fetch | 0 | fetch | latest post still Aug 7 (Fable 5 biology safeguards), already captured, predates window |
| google-deepmind | rss, websearch | 0 | websearch | no in-window post beyond prior Aug 5/6 captures |
| google-research | rss, websearch | 0 | websearch | latest post (Science One Framework) Jul 30, predates window |
| microsoft | rss, websearch | 0 | websearch | latest post still Aug 7 (India datacenter), already captured, predates window |
| nvidia | rss | 1 | - | - |
| xai | jina | 0 | jina | latest post Aug 7 (Imagine Image 2.0), already captured, predates window; anonymous Jina worked, no 403 |
| mistral | rss, websearch | 0 | websearch | 304 not modified on RSS; websearch surfaced "Robostral Navigate" but direct fetch confirmed it's Jul 8 — rejected as not in-window |
| huggingface | rss, websearch | 0 | websearch | 304 not modified on RSS; no in-window post with confirmed URL |
| cursor | rss, websearch | 0 | websearch | 304 not modified on RSS; no in-window changelog entry confirmed |
| perplexity | jina | 0 | jina | latest post still Aug 6 (Computer for Builders), already captured, predates window; anonymous Jina worked, no 403 |
| cohere | fetch | 0 | fetch | latest post still Aug 6 (Waterloo partnership), already captured, predates window |

Totals: 1 item, 1 company fresh, 0 errors (11 gap-scrapes attempted, all empty in-window;
1 rejected unconfirmed/out-of-window candidate — Mistral "Robostral Navigate" dated Jul 8).

Note: second run today — window is short (~10h, since the 06:10 UTC run this same day), so
most companies had no new content yet; this is expected, not a failure.

Linear: 1 issue created (KOV-39), new story, none duplicate (searched project "News digest"
by URL/title first, no matches found).

## 2026-08-09 05:05 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | lmsys-sglang: 403 Forbidden (tunnel) |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | - |
| technical-newsletters | 0 | 0 | semianalysis: 403 Forbidden (tunnel) |
| practitioner-blogs | 0 | 0 | - |
| youtube | 0 | 0 | - |
| community | 8 | 5 | - |
| mistral-watch | 0 | 0 | - |

Community triage detail: hn-show-mcp (1 raw) dropped — consumer-app marketing (DOCX editor
using MCP as a hook, 13 pts). reddit (6 raw) → 4 confirmed (custom Metal kernel by a local
agent, Kimi K3 quantization 711GB→478GB, Qwen-vs-Gemma tokenizer observation) + 2 dropped
(RTX 5090 Alibaba listing — hardware-market rumor; Intel Optane thread — speculative, no
technique/data). github-trending (6 raw) → 2 confirmed (google/skills — Agent Skills for
Google Cloud, MCP/agent-tooling fit; TauricResearch/TradingAgents v0.3.1 — multi-agent
orchestration release notes) + 4 dropped (ChinaTextbook PDFs, google/guava, Ladybird
browser, denoland/celld — none AI-related).

Totals: 5 items, 0 highlights, 2 source errors (lmsys-sglang, semianalysis — both known
403-Forbidden-in-cloud pattern, no fallback ladder for radar sources per workflow).

Highlight verification: attempted WebFetch on the 3 top-scored (HIGH-fit) candidates —
google/skills, Kimi K3 quantization post, custom-Metal-kernel post. All three failed:
github.com is blocked by the network egress proxy; reddit.com is unreachable via WebFetch
in this environment. Per workflow (§THE RADAR step 3): WebFetch error → item stays a
regular radar item, out of highlight consideration. Net: 0 highlights today — quiet day,
no `radar/daily/2026-08-09.md` written, nothing padded.

Linear: skipped (0 highlights — nothing to card).

## 2026-08-09 06:11 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss, websearch | 0 | websearch | no in-window post on openai.com/news (latest still Aug 7, already captured); 1 candidate rejected unconfirmed — NextSlide acquisition (no openai.com source page exists, only third-party press; techcrunch.com/nextslide.ai both blocked by egress proxy for corroboration) |
| anthropic | fetch | 0 | fetch | latest post still Aug 7 (Fable 5 biology safeguards), already captured, predates window |
| google-deepmind | rss, websearch | 0 | websearch | no in-window post beyond prior Aug 5/6 captures |
| google-research | rss, websearch | 0 | websearch | latest post (Science One Framework) Jul 30, predates window |
| microsoft | rss, websearch | 0 | websearch | latest post (Orchard) Aug 3, predates window |
| nvidia | rss, websearch | 0 | websearch | no in-window post beyond prior Aug 8 capture; SSI/NVIDIA partnership confirmed dated Jul 27, predates window — rejected |
| xai | jina | 0 | jina | latest post still Aug 7 (Imagine Image 2.0), already captured, predates window; anonymous Jina worked, no 403 |
| mistral | rss, websearch | 0 | websearch | 304 not modified on RSS; latest post (Shieldstral) Aug 4, already captured, predates window |
| huggingface | rss, websearch | 0 | websearch | 304 not modified on RSS; latest post (TutorMoments) Aug 7, already captured, predates window |
| cursor | rss, websearch | 0 | websearch | latest changelog entry Aug 3 (Google Workspace Plugins), predates window |
| perplexity | jina | 0 | jina | latest post still Aug 6 (Computer for Builders), already captured, predates window; anonymous Jina worked, no 403 |

Totals: 0 items, 0 companies fresh, 0 errors (10 gap-scrapes attempted, all empty in-window;
1 rejected unconfirmed candidate — OpenAI/NextSlide acquisition, no company-domain source
reachable).

Note: window since last successful daily run (2026-08-08 16:27 UTC) was short (~14h); quiet
run across the board, consistent with the previous same-day run's pattern.

Linear: skipped (0 new stories — nothing to card).
