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

## 2026-08-10 05:22 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | - |
| technical-newsletters | 1 | 1 | - |
| practitioner-blogs | 1 | 1 | - |
| youtube | 4 | 4 | - |
| community | 45 | 9 | - |
| mistral-watch | 0 | 0 | - |

Totals: 15 items, 3 highlights, 0 source errors.

Technical-newsletters/practitioner-blogs/youtube: all raw candidates confirmed as-is — SemiAnalysis
TileRT InferenceX article (inference-infra technique, HIGH fit), Interconnects "Lessons from the
hacks" (alignment/safety essay, MEDIUM fit), 4 AI Engineer conference-talk uploads (agentic
engineering / production agents, HIGH/MEDIUM fit).

Community triage detail (45 raw → 9 confirmed):
- HN Show HN (11 raw across inference/rag/mcp/agents queries, 6 unique after cross-query dedup) →
  0 confirmed. Dropped: DOCX editor w/ MCP server (revise.io, consumer-app marketing — same item
  rejected 2026-08-09, resurfaced by the Algolia time-window query outside the actual 26h window;
  not re-added); voice-driven murder-mystery app and Alphabet Soup word game (consumer
  apps/non-AI); "replayable A2A jury" trace tool and "Tura" agent framework (marketing-shell Show
  HNs, no benchmark/repro shown); open-source agent red-team playground (landing-page pitch, no
  visible technical depth).
- Reddit (25 raw) → 8 confirmed: KLQ training-free rotation quantization, Ling-3.0-flash DGX Spark
  tuning (20.8→38.7 tok/s), AMD llama.cpp MTP buffer fix (64K→149K context), Colibrì→Lumabri MoE
  swarm engine, OneRingAI v1 TS agent runtime, 300b-on-32gb MoE-streaming findings, independent
  DeepSeek V4 Flash Terminal-Bench 2.1 verification (Ante harness), Lophius LM-research workbench.
  Dropped 17: meta/community complaint thread; ByteDance distillation statement + KPMG AI-agent-cost
  Forbes repost (business/policy, not engineering); 3 support/Q&A threads (DeepSeek OpenCode
  stall report, "best local setup" and "best embedding model" questions); SupraElegans-500K
  (unverifiable novel-architecture claim from an unknown lab, no recoverable repo link) and
  BigBang-v1 finetune (post is skeptical of its own benchmark claims, not a technique); MiniMax H3
  video-gen report and Tencent WorldClaw 3D-gen (real content but video/3D-gen is explicit LOW fit
  per interests.md, dropped for volume budget); Google WeatherNext 2 (company-track overlap —
  already in topics/google-deepmind.md); Gemma Aug-20 event teaser (speculative, no technical
  content); omlab/VLX-Seek-1.5-10B embodied-vision model (off stated interest categories); updated
  SlopCodeBench benchmark post (redundant with the confirmed independent Terminal-Bench item, same
  underlying model).
- HF trending models (1 raw) → 0 confirmed: Kijai/MiniMax-H3-experimental is the same MiniMax H3
  release as the dropped Reddit report above (LOW-fit video-gen), not double-counted.
- HF trending spaces (2 raw) → 0 confirmed: Wan 2.2 LoRA demo space (low-substance personal demo);
  LiquidAI/LFM2.5-2.6B-WebGPU is the same model already covered in topics/huggingface.md
  (2026-08-04 deploy guide) — company-track overlap, not re-added per dedup rule.
- GitHub trending (6 raw) → 1 confirmed (vitali87/code-graph-rag — Tree-sitter + Memgraph
  code-knowledge-graph RAG, mature project). Dropped 5: agency-agents (marketing-flavored agent
  personas template, no real substance); witr (general devops tool, not AI-related); WeatherNext
  repo (company-track overlap, same as above); daily_stock_analysis (finance-flavored LLM app);
  ComfyUI (long-established tool resurfacing on trending, not fresh/notable).

Highlight verification: attempted on the 5 highest-scored HIGH-fit candidates — Colibrì/Lumabri
(verified via `git clone` of github.com/JustVugg/colibri: real, mature MoE-on-consumer-hardware
inference engine with measured findings), Lophius (verified via `git clone` of
github.com/p-e-w/lophius: real notebook-based LM research workbench), code-graph-rag (verified via
`git clone`: CI/PyPI/active-release project, substantive README beyond badges), SemiAnalysis
TileRT article (verified via WebFetch: concrete B200 throughput numbers vs Cerebras/Groq/
SambaNova), and the DeepSeek Terminal-Bench/Ante claim (verified via the feed entry's own
substantive body — trial counts, accuracy, author disclosure; already reads as a full write-up,
not a marketing shell). All 5 passed. Reddit direct-fetch (curl w/ browser UA) hit a JS-challenge
page (403, not the usual 429) on every attempt today — KLQ, AMD llama.cpp MTP fix and OneRingAI
were confirmed on their own substantive feed-body text but were not spent on the 5-candidate
verification budget, so they stayed regular items, out of highlight consideration.

3 top picks marked `highlight`: TileRT InferenceX (SemiAnalysis), code-graph-rag, Colibrì/Lumabri —
spread across inference-infra, RAG/agent-tooling, and local-hardware MoE.

Linear: 15 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to
Review" — KOV-46 through KOV-60. Priorities set by fit (HIGH→High, MEDIUM→Medium). Source labels
applied per item (newsletter/blog/youtube/github/reddit); `highlight` label on KOV-46, KOV-52,
KOV-56.

## 2026-08-10 06:12 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss, websearch | 0 | websearch | 2 WebSearch candidates (OpenAI $122B raise, ChatGPT Futures Class of 2026) could not be confirmed — both openai.com/index/* pages Cloudflare-challenge-blocked via WebFetch (403) and Jina retry; RSS (tier-1, applies the Company-category filter) reported zero fresh, giving no corroboration either is a new in-window Product/Engineering/Research item |
| anthropic | fetch | 0 | fetch | latest post still Aug 7 (Fable 5 biology safeguards), already captured, predates window |
| google-deepmind | rss, websearch | 0 | websearch | 2 candidates checked via WebFetch and rejected as out-of-window — Gemma Scope 2 (Dec 2025), multi-agent safety funding call (Jun 2026) |
| google-research | rss, websearch | 0 | websearch | latest post (Science One Framework) Jul 30, predates window |
| microsoft | rss, websearch | 0 | websearch | no in-window Research-blog post confirmed (Aug 4 ChainDrop post is Security blog, off-scope) |
| nvidia | rss, websearch | 0 | websearch | RSS 304 not modified; no in-window post beyond prior Aug 8 capture confirmed |
| xai | jina | 0 | jina | r.jina.ai returned a Cloudflare JS-challenge page (not the usual clean fetch); x.ai itself is egress-blocked for WebFetch — could not verify WebSearch candidate "Grok Voice Think Fast 2.0"'s date, transport error only, no fallback beyond the one jina attempt per workflow |
| mistral | rss, websearch | 0 | websearch | RSS 304 not modified; no in-window post with confirmed URL |
| huggingface | rss, websearch | 0 | websearch | RSS 304 not modified; no in-window post with confirmed URL |
| cursor | rss, websearch | 0 | websearch | no in-window changelog entry confirmed |
| perplexity | jina, websearch | 0 | jina→websearch | anonymous Jina hit the same Cloudflare JS-challenge page (no JINA_API_KEY set); websearch fallback found no in-window post either |

Totals: 0 items, 0 companies fresh, 2 errors (11 gap-scrapes attempted, all empty in-window;
xai's and perplexity's Jina calls both hit a Cloudflare JS-challenge page today instead of the
usual clean anonymous fetch — a transport error, not a content finding; 2 rejected out-of-window
candidates on Google DeepMind; 2 unconfirmed OpenAI candidates whose source pages could not be
reached through either verification transport).

Note: fully quiet day across all 11 companies — consistent with the pattern seen on 2026-08-02/03.
Window per fetch_feeds.py: since 2026-08-09T04:12 UTC (default ~26h, script-computed).

Linear: skipped (0 new stories — nothing to card).

## 2026-08-10 — deep-dive — ok (no approved cards)

Project "Radar" checked: 0 cards with `hot` label (15 in Ready to Review, 5 legacy [Idea] cards
in Todo — none approved). Review queue is fresh (created today 05:22 UTC), owner has not triaged
yet. No research, no files written, no card moves. Exiting quietly per workflow.

## 2026-08-11 05:14 UTC — radar — ok

Window: since 2026-08-10T03:06 UTC (fetch_radar.py, ~26h default). `fetch_radar.py` ran clean
(exit 0); all 7 `yt-*` sources (ai-engineer, gpu-mode, karpathy, latent-space, mlst, sentdex,
umar-jamil) returned HTTP 404 on their `youtube.com/feeds/videos.xml` URLs today — confirmed via
direct curl (not a per-channel issue, looks like a platform-side change to that endpoint). No
gap-scrape ladder for radar sources per workflow — logged, moved on, zero youtube items today.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | — |
| inference-infra | 0 | 0 | — |
| oss-ml-systems | 3 | 3 | — |
| bigtech-eng | 2 | 0 | — |
| research-institutes | 0 | 0 | — |
| technical-newsletters | 1 | 1 | — |
| practitioner-blogs | 1 | 0 | — |
| youtube | 0 | 0 | 7 sources HTTP 404 |
| community | 58 | 10 | — |
| mistral-watch | 0 | 0 | — |
| **Total** | **65** | **14** | **7 source errors** |

**Triage detail.** The day was dominated by one story: Meta released **Muse Glimmer**, a 30B
dense open-weight (Apache 2.0) multimodal model built for local agentic workflows — it drove
SGLang day-0 support, PyTorch/ExecuTorch on-device support, a vLLM release cycle, an official-style
Reddit announcement, and most of today's 25 raw r/LocalLLaMA candidates. Kept 3 ecosystem-support
angles (SGLang, ExecuTorch, the anchor announcement post) plus 2 hands-on hardware-fit reports
(RTX 3090 fit, 1M-context-in-24GB); dropped ~16 other Muse-Glimmer reddit threads as thin
appreciation/hype/question posts (no real technical content beyond "I tried it and here's my
vibe") or as duplicates of an already-kept item (e.g. the Unsloth GGUF Reddit repost duplicates
the `hf-trending-models` entry for the same resource).

Dropped explicitly per workflow rules: `github-ai`'s "GitHub Copilot SDK for Java" post
(tutorial-grade Copilot education); `cloudflare-ai`'s "Agents Week" recap (verified via WebFetch —
20+ initiatives, one sentence each, no architecture/benchmarks — marketing recap, not engineering
content); `interconnects`' "5 useful things from my post-training textbook" (verified via WebFetch
— confirmed primarily a book-promo post, chapter summaries only, "reserves technical explanation
for the book"); `smolai`'s "not much happened today" (explicit skip rule). Off-topic HN Show-HN
noise (climbing-gym photogrammetry, a word game, a murder-mystery voice app) dropped as
non-AI/consumer-app. `hf-trending-spaces` (4 items: two AI-humanizer/detector spaces, two thin
demo spaces) dropped — no summary content, can't confirm real substance. `github-trending` kept
only `paperclipai/paperclip` (agent-orchestration platform); dropped MediaCrawler (general
scraper, not AI-specific), RuView (RF/hardware sensing, not LLM/agent), LifeOS (personal-productivity
app, weaker fit than paperclip), and firecrawl (established tool resurfacing on trending, same
"not fresh" call as ComfyUI on 2026-08-10).

**Highlight verification** (budget: up to 5). `cactuscompute.com/needle` (Needle2) — both WebFetch
(EGRESS_BLOCKED) and curl retry (CONNECT tunnel 403) failed; kept as a regular item on its
substantive HN feed-body text (14MB/45M-param/2-bit specifics), out of highlight consideration
per workflow. `AntigmaLabs/ante` — verified via `git clone`: real alpha-stage Rust coding-agent
harness, binary-only by design, publishes its own Terminal-Bench numbers — passed. Reddit's
"$200 1B LLM from scratch" and "GGUF quant comparison" — direct curl hit the same Cloudflare
JS-challenge 403 seen on 2026-08-09/08-10 (systemic, not per-post); both confirmed instead on
their own detailed feed-body methodology text, consistent with the 2026-08-09 precedent for
curl-blocked Reddit items. `huggingface.co/papers/2608.09096` (Evo-Bench) — verified via WebFetch:
real benchmark methodology (fixed policy model + evolver LLM, budgeted iterations), github repo
in the source metadata (RUCAIBox/Evo-Bench) though not visible on the fetched page itself.
`blog.cloudflare.com` Agents Week — verified and dropped (see above), so not spent as a highlight.

3 top picks marked `highlight`: Ante (coding-agent harness — directly in the "agent harnesses"
HIGH-fit lane, and adjacent to this project's own harness), Evo-Bench (agent-harness-evolution
research, same lane), "$200 1B LLM from scratch" (fully reproducible train-from-scratch recipe
with a real cost number — strong `project_post` seed). Spread: oss-ml-systems untouched by
highlights today (solid but institutional/expected content), community carries all 3.

Linear: 14 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to
Review" — KOV-61 through KOV-74. Priorities by fit (HIGH→High, MEDIUM→Medium; no LOW-fit survivors
today). Source labels applied per item (blog/github/newsletter/hn/reddit/hf); `highlight` on
KOV-66 (Ante), KOV-69 ($200 LLM), KOV-73 (Evo-Bench). Searched the project by title first — no
collisions with the 15 existing Ready-to-Review cards or the 5 legacy [Idea] cards.

## 2026-08-11 06:12 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss, websearch | 0 | websearch | no in-window Product/Engineering/Research/Publication/Release item confirmed — WebSearch surfaced Astra (Aug 1), GPT-5.6 (Aug 4), ChatGPT Work/Codex (Aug 6), all predate window |
| anthropic | fetch | 0 | fetch | WebFetch of anthropic.com/news confirms latest post still Aug 7 (Fable 5 biology safeguards), predates window |
| google-deepmind | rss, websearch | 0 | websearch | RSS 304 not modified; WebSearch's only lead (Pichai/Hassabis/Dean leadership post, "The next chapter of our AI momentum") is dated Aug 5 on blog.google — predates window and is off the configured deepmind.google/blog source anyway |
| google-research | rss, websearch | 0 | websearch | RSS 304 not modified; latest post (Science One Framework) Jul 30, predates window |
| microsoft | rss, websearch | 0 | websearch | RSS 304 not modified; no Research-blog post newer than Aug 3 confirmed |
| nvidia | rss, websearch | 0 | websearch | RSS 304 not modified; developer.nvidia.com posts found (Alpamayo 2 Super, Kubernetes-on-shared-GPU, World Action Models, Vera Storage) all Aug 3–4, predate window |
| xai | jina | 0 | jina | curl r.jina.ai clean 200 this time (no Cloudflare challenge); full news list confirms latest post "Imagine Image 2.0" Aug 7, predates window |
| mistral | rss, websearch | 0 | websearch | RSS 304 not modified; only dated lead (Shieldstral) is Aug 4, predates window |
| huggingface | rss, websearch | 0 | websearch | RSS 304 not modified (deterministic signal trusted over WebFetch); WebFetch surfaced 3 Aug-10 posts but one is the Meta Muse Glimmer story already owned by today's radar run, the other two (NVIDIA Magpie TTS, Multiverse Computing distillation) are guest posts with no clear company-channel ownership — not carried as company items given the RSS 304 |
| cursor | rss, websearch | 0 | websearch | RSS 304 not modified; WebFetch of the changelog confirms latest entry Aug 3 (Google Workspace Plugins), predates window |
| perplexity | jina, websearch | 0 | jina→websearch | anonymous Jina hit AbuseAlleviationError 403 again (same as 2026-08-10); WebSearch's only Aug lead (Aug 6 update) predates window |

Totals: 0 items, 0 companies fresh, 1 error (11 gap-scrapes attempted, all empty in-window;
Perplexity's Jina call hit the same anonymous-abuse 403 as yesterday — a transport error, not a
content finding).

Note: second fully quiet day in a row across all 11 companies (following 2026-08-10) — the
window (since 2026-08-10T04:12 UTC, script-computed) sits between two clusters of activity:
several companies' most recent posts land Aug 3–7 (just before the window opens), and today's
big AI story (Meta's Muse Glimmer release) belongs to a company outside this list and was
already captured by the daily radar run.

Linear: skipped (0 new stories — nothing to card).

## 2026-08-12 05:05 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | 0 |
| inference-infra | 0 | 0 | 0 |
| oss-ml-systems | 3 | 3 | 0 |
| bigtech-eng | 0 | 0 | 0 |
| research-institutes | 0 | 0 | 0 |
| technical-newsletters | 0 | 0 | 0 |
| practitioner-blogs | 1 | 0 | 0 |
| youtube | 0 | 0 | 7 (all 7 sources HTTP 404/500) |
| community | 57 | 12 | 0 |
| mistral-watch | 0 | 0 | 0 |

Totals: 61 raw candidates, 15 confirmed, 7 source errors (youtube only).

**youtube**: all 7 configured channel feeds (yt-ai-engineer, yt-gpu-mode, yt-karpathy,
yt-latent-space, yt-mlst, yt-umar-jamil → HTTP 404; yt-sentdex → HTTP 500) failed today —
systemic, not per-channel; no fallback ladder for radar per workflow, logged and moved on.

**oss-ml-systems** (3/3 confirmed): SGLang's day-0 Nemotron 3.5 Lightning support and vLLM
v0.27.1 are routine-release items (MEDIUM fit). Unified Radix Cache — verified via WebFetch:
substantial systems writeup (component-based radix tree unifying full/SWA/Mamba prefix reuse,
multi-tier GPU/host/L3 caching, concrete DeepSeek-V4-Flash and SWE-bench numbers) — HIGH fit,
marked `highlight`.

**practitioner-blogs** (0/1 confirmed): Latent.Space's Chai Discovery BioAI interview cleared
pass 1 (real content) but dropped in pass 2 — biotech/protein-design angle sits outside
`config/interests.md`'s HIGH/MEDIUM lanes, and today's community volume already filled the
≤15/day budget with stronger owner-fit items.

**community** (12/57 confirmed) — heaviest-volume category today (Reddit r/LocalLLaMA alone
had 25 fresh items, a big Local-LLaMA news day). Triage dropped, in order: two items already
covered in this week's radar (`cactuscompute.com/needle` Needle2 and `AntigmaLabs/ante`, both
2026-08-10 — re-surfaced today via different HN "Show HN" queries, same URLs, skipped as
duplicates); off-topic HN "Show HN" false positives from broad query terms (TermDOM — a
terminal-DOM library, not AI; a climbing-gym photogrammetry tour) — not real AI content, dropped;
novelty/gimmick posts (AI Pulse LED-strip macOS dock indicator; thin protocol pitch `ojcp.dev`,
11 pts) — dropped for weak signal; policy/business content (EU AI-content-transparency signing)
— company-news territory, not radar; marketplace/anecdote/rumor/meme Reddit threads (hardware
for-sale, "fgn manifesto" hype, VRAM-poor discussion, 8B-12B-dropped discussion, Rubin Ultra
memory rumor, Qwen-3.8 "coming this week" rumor, thin "all tests passed" Muse Glimmer repost,
duplicate HF-model-page repost of the already-covered Nemotron model) — dropped, no concrete
technique/release; a `stolen-thoughts.com`/Reddit reasoning-trace-extraction pair judged same
story — kept the higher-signal HN item (558 pts), dropped the Reddit repost as duplicate angle;
a second Muse-Glimmer-vs-Qwen coding-specific benchmark thread judged same story as the broader
3-way local benchmark — kept the broader one, dropped the narrower repost; thin HF-trending
model/space entries (video-gen model, LoRA demo space, one NSFW image space) — LOW fit
(robotics/3D/video per interests.md), dropped; GitHub-trending mirror items (non-AI false
positives `nvm-sh/nvm`, `3b1b/manim`, `cathrynlavery/diagram-design`; `anthropics/skills` judged
company-core territory not radar signal; `HKUDS/DeepTutor` — no reliable freshness signal from
this no-pubDate mirror source) — dropped for the day given stronger candidates elsewhere.

VERIFY SUBSTANCE (5 highest-scored candidates): `trycua/cua` GPU-passthrough post — verified via
`git clone`: detailed, reproducible Metal-capability-shim writeup with raw benchmark logs
(11–16× llama.cpp speedup on M1 Ultra) — passed, `highlight`. `activeing123/mcptoon` — verified
via `git clone`: real, working MCP-token-compaction CLI with concrete before/after token counts
— passed, `highlight`. `lmsys.org` Unified Radix Cache — verified via WebFetch (see
oss-ml-systems above) — passed, `highlight`. Reddit "Revision Prompting" — curl hit the same
Cloudflare JS-challenge as prior days; confirmed instead on the feed's own detailed body text
(explains the diff-based patch mechanism, external write-up link) — passed verification, not
selected for one of the 3 highlight slots. `stolen-thoughts.com` "Stealing Reasoning Traces" —
WebFetch EGRESS_BLOCKED, curl 403 tunnel fail, and news.ycombinator.com itself also
EGRESS_BLOCKED — no transport worked and the HN API metadata carries no body text; kept as a
regular (title-only, explicitly flagged unverified) radar item per workflow, out of highlight
consideration.

3 top picks marked `highlight`: Cua's macOS-VM Metal-capability shim (directly actionable on the
owner's own Mac, reproducible with published scripts/logs — strongest `project_post` seed today),
mcptoon (MCP-ecosystem tool, trivial to try in the owner's own agent setup), Unified Radix Cache
(deepest systems-engineering content of the day, `tech_explainer` seed). Spread: mistral-watch,
lab-engineering, inference-infra, bigtech-eng, research-institutes and technical-newsletters were
silent today (0 raw candidates each).

Linear: 15 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to
Review" — KOV-75 through KOV-89. Priorities by fit (HIGH→High, MEDIUM→Medium; no LOW-fit
survivors today). Source labels applied per item (hn/blog/github/reddit/hf/lobsters); `highlight`
on KOV-76 (Cua), KOV-77 (mcptoon), KOV-78 (Unified Radix Cache). Searched the project by title
first — no collisions with the 24 existing Ready-to-Review cards or the 5 legacy [Idea] cards.

## 2026-08-12 06:12 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss | 1 | - | - |
| anthropic | fetch | 0 | fetch | latest post still Aug 7 (Fable 5 biology safeguards), predates window |
| google-deepmind | rss, fetch | 0 | fetch | RSS empty; direct fetch of deepmind.google/blog confirms latest post still WeatherNext (Aug 6, already captured), predates window |
| google-research | rss | 1 | - | - |
| microsoft | rss | 1 | - | - |
| nvidia | rss | 3 | - | - |
| xai | jina | 1 | jina | anonymous Jina clean 200, no 403 — confirmed "Introducing Grok Bot" |
| mistral | rss | 1 | - | - |
| huggingface | rss | 1 | - | - |
| cursor | rss (timeout), fetch | 0 | fetch | RSS: `_ssl.c:999` handshake timeout on cursor.com/changelog/rss.xml; direct fetch of cursor.com/changelog confirms latest entry still Aug 3 (Google Workspace Plugins), predates window |
| perplexity | jina | 0 | jina | anonymous Jina hit AbuseAlleviationError 403 again (no JINA_API_KEY set); WebSearch corroborates latest post still Aug 6 (Computer for Builders), already captured, predates window |

Totals: 9 items, 7 companies fresh, 0 errors (5 gap-scrapes attempted, 1 confirmed hit — xai
Grok Bot — 4 came up empty in-window; cursor's RSS transport error was resolved via one direct
fetch of the changelog page, confirming no in-window entry rather than leaving it unconfirmed).

NVIDIA's developer.nvidia.com/blog fed 3 distinct genuine posts today (Nemotron 3.5 Lightning
model release, NeMo Switchyard routing SDK, JetPack 7.2.1) — all kept per the "genuine
announcements/major posts" trap-note bar, none were tutorial filler.

Window: since last successful daily run (2026-08-11 06:12 UTC).

Note: session started on a detached HEAD identical to `origin/main` (df39235); stashed the
in-progress `cursors.json` update from the TIER-1 fetch, checked out `main` (fast-forwarded 13
commits — yesterday's radar run + workflow.md rewrite), then reapplied the stash — no data lost.

Linear: 9 issues created (KOV-90..KOV-98), all new stories, none duplicate (searched project
"News digest" by URL/title first, no matches found). Priorities: High — Mistral sovereign-AI
initiative, NVIDIA Nemotron 3.5 Lightning, xAI Grok Bot; Medium — OpenAI Daybreak/AWS, Google
Research AMIE video, Microsoft CARE-X, NVIDIA NeMo Switchyard, Hugging Face ALTK-Evolve; Low —
NVIDIA JetPack 7.2.1. Type labels: business, research (x3), infra (x2), model-release, product
(x2).

## 2026-08-13 05:06 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | 0 |
| inference-infra | 0 | 0 | 0 |
| oss-ml-systems | 1 | 1 | 0 |
| bigtech-eng | 1 | 0 | 0 |
| research-institutes | 0 | 0 | 0 |
| technical-newsletters | 0 | 0 | 0 |
| practitioner-blogs | 1 | 1 | 1 (hamel XML parse error) |
| youtube | 0 | 0 | 7 (all 7 sources HTTP 404/500) |
| community | 47 | 10 | 0 |
| mistral-watch | 0 | 0 | 0 |

Totals: 50 raw candidates, 12 confirmed, 8 source errors (hamel XML parse + 7 youtube).

**youtube**: same systemic failure as prior days (yt-ai-engineer, yt-gpu-mode, yt-latent-space,
yt-mlst, yt-umar-jamil → HTTP 404; yt-karpathy, yt-sentdex → HTTP 500) — no fallback ladder for
radar sources, logged and moved on.

**bigtech-eng** (0/1 confirmed): GitHub blog's "Write your first prompt with the GitHub Copilot
app" is tutorial-grade Copilot education — explicit pass-1 drop per workflow.

**practitioner-blogs** (1/1 confirmed, 1 error): `hamel.dev`'s feed hit an XML parse error
("junk after document element") — logged, no fallback ladder for radar, moved on. Interconnects'
"I wrote an AI textbook" essay cleared pass 1 but is general capability-trajectory reflection
rather than one of `config/interests.md`'s HIGH/MEDIUM lanes — kept as a LOW-fit item (still
radar-file-worthy, not review-queue highlight).

**oss-ml-systems** (1/1 confirmed): SGLang+Miles day-0 support for Qwen3.8-2.4T-A95B — verified
via WebFetch: substantial systems writeup (hybrid-state handling for KV cache/GDN/conv windows,
ReplaySSM for speculative-decode recovery, prefill-decode disaggregation) with concrete GB300
numbers (5,126 tok/s/GPU peak, 334 tok/s low-latency, 346 tok/s w/ MTP) — HIGH fit, `highlight`.

**community** (10/47 confirmed) — Reddit r/LocalLLaMA again heaviest (25 fresh; the whole sub is
mid Qwen3.8-2.4T-A95B release-day hype). Triage dropped, in order: pure hype/rumor/poll threads
about the Qwen3.8 release date and sizes (6 threads: "release date took down?", "MTP or DFlash?",
"which size do you want most", "exact release date and time", "final countdown", "How do you plan
to run it locally?") — no technique, discussion-only, dropped; the bare "Qwen3.8-2.4T-A95B
Released" repost and the matching HF-trending-models leaderboard entry — same story as the
SGLang/Miles day-0 post above (which carries far more technical detail), dropped as duplicate
angle; NVIDIA Nemotron-3.5-Lightning-NVFP4 HF-trending entry — same story already covered in
`topics/nvidia.md` (2026-08-11) and `radar/oss-ml-systems.md`'s day-0 SGLang post, dropped per
"already covered in a company topics file"; `inclusionAI/Ling-3.0-tiny` and
`endless-frontier/BigBang-v1` HF-trending entries — no model-card text available from the
adapter, too thin to write an honest card, dropped; two "reasoning trace stealing" repost/meme
threads ("All your reasoning are belong to us", "Hidden Reasoning from Claude and GPT are
Decoded") — same story as `stolen-thoughts.com` already in this week's radar, dropped as
duplicate; `DeepSeek V4 Flash 0731 uncensored (jailbreak pt2)` — jailbreak content, off-focus for
`config/interests.md`, dropped; `LFM2.5-VL-3B recognizes Steve from Minecraft` and the matching
bare `LiquidAI/LFM2.5-VL-3B` HF-page repost — cute demo, no real technique/numbers beyond timing,
dropped as gimmick; `CohereLabs/North-Micro-Vision-Instruct` — thin HF-model-card repost, no
independent commentary, dropped (same pattern as prior days); two NVIDIA RTX PRO 6000 price-hike
posts (duplicates of each other) and the AMD/Arm/Microsoft CPU:GPU-ratio conference-punditry
post — hardware-market/business analysis, explicit LOW bucket in `config/interests.md`, no
benchmark/release/technique, dropped; `RAG for regular users?` (help-request thread) and `FYI:
Muse Glimmer Chat Template Got Updated` (too thin, no real change described) — dropped; `Today is
Models Day` — meme, dropped. HN Show-HN false positives from broad query terms: `Woxi`
(Mathematica/Wolfram reimplementation — not AI, matched on "inference" query) appeared twice
(hn-show-inference, hn-show-rag), dropped both; `Tokyo Trains` (a Claude-built 3D map demo, no
AI-technique content) and `OJCP` (thin agent-data protocol pitch, 11 pts — dropped again, same as
2026-08-12) — dropped. `Ballet` (workflow-automation HN post, 26 pts, no body text to verify
against) — too thin to confirm, dropped. Lobsters' `blog.comma.ai/chestnut` ("Introducing
chestnut", score 1) — both WebFetch and curl hit EGRESS_BLOCKED/403 on blog.comma.ai, and the
feed carried no summary text at all (unlike prior title-only keeps such as `stolen-thoughts.com`
or `ngrok.com`, which had a legible AI-relevant title) — dropped rather than write an
unsubstantiated card, per "never invent facts."

VERIFY SUBSTANCE (5 highest-scored candidates): `lmsys.org` SGLang/Miles Qwen3.8 day-0 post —
verified via WebFetch (see oss-ml-systems above) — passed, `highlight`. Reddit "Meta's Muse
Glimmer 30B now runs up to ~3.3x faster on Mac with mlx-dspark" — reddit `.json` curl hit HTTP
403 (Cloudflare); confirmed instead on the feed's own detailed body text (concrete before/after
tok/s, per-domain speedup multipliers, byte-identical-output claim) — passed, `highlight`.
`Spark-to-Paper` (hf-daily-papers, 33 upvotes) — verified via `git clone` of
`spark-to-paper-skills`: real, substantial 14-skill Claude Code pipeline (LaTeX build, citation
verification, figure engine, deterministic gates), MIT-licensed, 7 showcased generated papers —
passed, not selected for a highlight slot. `stablyai/orca` — verified via `git clone`: real,
actively developed desktop agent-orchestrator app (parallel git-worktree agents, mobile
companion, Design Mode) — passed, not selected for a highlight slot. `Tura-AI/tura` (Show HN, 11
pts) — verified via `git clone`: real MIT-licensed agent-runtime harness with published DeepSWE
v1.1 benchmark artifacts (77.5% fewer tokens vs Codex CLI at comparable success rate, or +16.7pp
success rate at 31.1% fewer tokens) — passed, `highlight`.

3 top picks marked `highlight`: SGLang/Miles day-0 Qwen3.8 support (deepest systems-engineering
content of the day, directly tied to the release the whole community is reacting to —
`tech_explainer` seed), Tura-AI/tura (concrete, reproducible token-reduction benchmark, trivial to
try in the owner's own agent setup via npm — strongest `project_post` seed today), Muse Glimmer
mlx-dspark speedup (author's own OSS project, directly reproducible on the owner's own Mac
hardware). Spread: lab-engineering, inference-infra, research-institutes, technical-newsletters
and mistral-watch were silent today (0 raw candidates each).

Linear: 12 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to
Review" — KOV-99 through KOV-110. Priorities by fit (HIGH→High ×6, MEDIUM→Medium ×5, LOW→Low
×1). Source labels applied per item (blog/hn/reddit/hf/github); `highlight` on KOV-99
(SGLang/Miles Qwen3.8), KOV-101 (Tura), KOV-102 (Muse Glimmer mlx-dspark). Searched the project by
title first — no collisions with the 41 existing cards across all states.

## 2026-08-13 06:20 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss | 0 | - | - |
| anthropic | fetch | 0 | fetch | latest post still Aug 7 (Fable 5 biology safeguards), predates window |
| google-deepmind | rss | 1 | - | - |
| google-research | rss | 1 | - | - |
| microsoft | rss | 1 | - | - |
| nvidia | rss | 1 | - | - |
| xai | jina, websearch | 0 | jina (401 invalid key), websearch | JINA_API_KEY present but rejected (401 AuthenticationFailedError, not the usual anonymous 403) — worth rotating the key; WebSearch turned up only stale/speculative third-party aggregator content (Grok 4.6, Voice Think Fast 2.0) with no dated primary x.ai URL in-window, so no item added |
| mistral | rss | 0 | - | - |
| huggingface | rss | 2 | - | - |
| cursor | rss | 0 | fetch | direct fetch of cursor.com/changelog confirms latest entry still Aug 3 (Google Workspace Plugins), predates window |
| perplexity | jina, websearch | 0 | jina (401 invalid key), websearch | same JINA_API_KEY 401 as xai; WebSearch turned up only undated/speculative aggregator content (Personal Computer, Comet Enterprise), no primary hub.perplexity.ai post confirmed in-window — no item added |

Totals: 6 items, 5 companies fresh, 0 errors (5 gap-scrapes attempted — anthropic/cursor via
direct fetch (both predate window, confirmed), xai/perplexity via Jina-then-WebSearch (Jina hard
401'd on both — API key present but invalid, distinct from the usual anonymous AbuseAlleviation
403 — flagging for the owner to check/rotate JINA_API_KEY; WebSearch found no dated primary-source
announcement for either company in-window), mistral needed no gap-scrape (rss ran clean, 0 in
window, Aug 11 sovereign-AI post already captured yesterday)).

NVIDIA developer blog surfaced 2 posts; kept the Qwen3.8-2.4T-A95B GB300 serving write-up
(genuine technical content tied to Alibaba's day-0 open-weight release) and dropped "How to
Choose Full-Stack Observability for NVIDIA AI Factories" as a generic best-practices guide, not
an announcement — per the NVIDIA trap note ("keep only genuine announcements/major posts, not
every tutorial").

Window: since last successful daily run (2026-08-12 06:12 UTC).

Linear: 6 issues created (KOV-111..KOV-116), all new stories, none duplicate (searched project
"News digest" by title/URL first, no matches found). All Medium priority (regular technical
announcements, none rising to a major model/product launch or major org news). Type labels:
product ×2 (Google DeepMind SL2T, HF OlmoEarth embeddings), research ×2 (Google Research
parametric-factuality, Microsoft MindTopo), infra ×1 (NVIDIA Qwen3.8 GB300 serving),
model-release ×1 (HF LFM2.5-VL-3B).

## 2026-08-13 07:02 UTC — deep-dive — ok (no approved cards)

Searched project "Radar" for cards with label `hot` in status "Ready to Review", then the
Todo fallback, then all states as a sanity check — zero hot cards anywhere in the project.
No cards processed, no files written, no leftovers. Exiting quietly per workflow.

## 2026-08-14 05:24 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 1 | 1 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | - |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 0 | 0 | - |
| youtube | 2 (1 fresh source + 3 source errors) | 1 | yt-ai-engineer HTTP 404, yt-gpu-mode HTTP 500, yt-latent-space HTTP 500, yt-umar-jamil HTTP 404 |
| community | 56 | 12 | see triage below |
| mistral-watch | 0 | 0 | - |

Totals: 58 raw candidates across all sources, 14 confirmed, 4 youtube source errors (no
fallback ladder for radar sources per workflow — logged, moved on).

TRIAGE (pass 1 technical bar): heavy community day, driven by yesterday's Qwen3.8 release and
today's DeepSeek-V4-Pro / DeepSeek Harness launches. Dropped as hype/meme/no-content: 5 separate
"Qwen3.8-27B countdown" posts (r/LocalLLaMA — no technical content, pure hype), "Is waiting for
Qwen 3.8 27B like waiting for Star Wars Episode 1?", "OpenAI vs. Anthropic" (rant, no content).
Dropped as off-topic for a technical radar: "The White House is going to expand its AI policy"
(policy, not engineering — belongs in company/policy coverage if anywhere, not here). Dropped as
thin/unsubstantiated (repeat offenders from prior days, same verdict): `OJCP` (agent job-data
protocol, dropped again — same as 2026-08-12/13), `Ballet` (workflow automation, dropped again —
too thin, same as 2026-08-13). Dropped as off-topic (not AI/ML): `Woxi` (Wolfram Language
reimplementation), `Stackdome` (Railway alternative on K8s), `A Rosetta Stone for UI component
libraries`, `megadose/holehe` and `smicallef/spiderfoot` (OSINT tools, no AI angle),
`altic-dev/FluidVoice` (macOS dictation app — consumer product, not engineering technique).
Dropped as low-signal/no-body-text: "Show HN: Posts grew 6x since ChatGPT..." (11 pts, no
summary). Dropped as secondary aggregation (not a standalone technique/announcement): "Open
Models - July 2026" monthly roundup. Dropped for LOW owner-fit under volume budget (robotics/3D/
video/audio-gen — technically clean but off the owner's core interests, and budget was tight
today): `DreamX-Phi 1.0` (robotic-manipulation world model, 55 upvotes), `PlayWorld` (world-model
benchmark, 19 upvotes), `MiniMax-Music3` (audio-gen release — 3 duplicate mentions across
reddit/hf-trending-models/hf-trending-spaces collapsed to one drop), `dots-studio/dots3-note-prev`
(280B MoE, HF page came back 401/gated — dropped on weak sourcing rather than guess a canonical
URL). Dropped `MCP-stama` (Rust MCP server, 71 pts but zero comments and empty summary — too thin
to confirm without spending a verify slot). Dropped as company-topics duplicates (already covered
there, not re-added to radar per workflow): `cactus-compute/needle` (GitHub-trending repo — same
project as the Needle2 Show HN post already on the radar 2026-08-10), `unslothai/unsloth`
(GitHub-trending — same Unsloth Desktop app already on the radar 2026-08-11),
`NVIDIA-NeMo/Switchyard` (GitHub-trending — already in `topics/nvidia.md` 2026-08-11, linked
instead of re-added).

VERIFY SUBSTANCE (5 highest-scored candidates): `deepseek-ai/deepseek-harness` — verified via
`git clone`: real, substantial monorepo (apps/packages/docs/examples), MIT-licensed, Cordis
plugin architecture, matches the reddit summaries — passed, `highlight`. `DeepSeek-V4-Pro-0813` —
verified via WebFetch of the HF model page: real 1.7T MoE release, MIT license, concrete
benchmark numbers (Terminal-Bench 2.1 87.9, Cybergym 83.3, DeepSWE 62.7) — passed, `highlight`.
Gemma 4 12B Q3 tensor-quant post, "Doom running on an LLM", and the 1.5B shell-command model —
all three reddit `.json` curls hit HTTP 403 (Cloudflare, consistent with recent days); confirmed
on each feed entry's own detailed body text per workflow fallback — all three passed on that
basis, none selected for a highlight slot (Doom-on-LLM was, see below). `fellowgeek/mcp-memory`
(not one of the 5, but checked anyway given thin auto-fetched summary) — verified via `git
clone`: real, substantial MCP server (OKF v0.2 + SQLite FTS5), matches the HN title exactly —
passed.

2 highlight-tier candidates transport-blocked, kept without highlight per workflow: `/show-me`
agent skill (humanlayer.com — WebFetch egress-blocked, curl hit a 403 tunnel failure) — kept on
HN submission text only. `yt-mlst` Wyart interview (YouTube page fetch hit a Google bot-check
redirect) — kept on title/channel only.

3 top picks marked `highlight`: DeepSeek Harness (KOV-125 — first public release of the agent
harness DeepSeek only referenced obliquely before, directly on the owner's #1 HIGH-interest line;
`tech_explainer` seed), Doom running on an LLM (KOV-122 — most distinctive "weights as program"
trick of the day, fully reproducible via the published HF checkpoint; `tech_explainer`/
`project_post` seed), DeepSeek-V4-Pro-0813 (KOV-124 — today's biggest model release, MIT-licensed,
Unsloth GGUF quants already up day-0). Spread: lab-engineering, inference-infra, bigtech-eng,
research-institutes, technical-newsletters, practitioner-blogs and mistral-watch were silent
today (0 raw candidates each) — an unusually community/agent-heavy day.

Linear: 14 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to
Review" — KOV-117 through KOV-130. Priorities by fit (HIGH→High ×9, MEDIUM→Medium ×2, LOW→Low
×2 — top-heavy today given the DeepSeek/agent-harness/quantization news mix matches
`config/interests.md`'s HIGH bullets closely). Source labels applied per item (hn ×2, reddit ×6,
hf ×3, github ×1, blog ×1, youtube ×1); `highlight` on KOV-122, KOV-124, KOV-125. Searched the
project by title first — no collisions with the 113 existing cards across all states.
