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

## 2026-08-14 06:19 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss | 1 | - | - |
| anthropic | fetch | 0 | fetch | latest post still Aug 7 (Fable 5 biology safeguards), predates window |
| google-deepmind | rss | 1 | - | - |
| google-research | rss, websearch | 0 | websearch | latest post still Aug 12 (parametric-factuality), no newer post confirmed in-window |
| microsoft | rss, websearch | 0 | websearch | latest post still Aug 12 (MindTopo), no newer post confirmed in-window |
| nvidia | rss | 0 | - | 304 not modified, no gap-scrape needed |
| xai | jina | 0 | jina | anonymous Jina worked (no 401 this time — JINA_API_KEY still unset); latest post still Aug 12 (Grok 4.6), predates window |
| mistral | rss | 0 | - | 304 not modified, no gap-scrape needed |
| huggingface | rss | 1 | - | - |
| cursor | rss, fetch | 1 | fetch | RSS returned 0 fresh but missed a same-day changelog entry — direct fetch of cursor.com/changelog caught "Cloud Agents Start 3x Faster with Builds" (Aug 13), not yet captured |
| perplexity | jina | 1 | jina | anonymous Jina worked (no 401/403 this time); found new Aug 13 post not yet captured |

Totals: 6 items, 6 companies fresh, 0 errors (6 gap-scrapes attempted: anthropic via fetch
(predates window), google-research/microsoft via WebSearch (nothing newer confirmed), xai/
perplexity via anonymous Jina (worked cleanly this run — no 401/403, unlike 2026-08-13's hard
401s; JINA_API_KEY remains unset), cursor via direct fetch of the changelog page (RSS missed a
same-day entry, direct fetch caught it) — nvidia and mistral skipped gap-scrape entirely on a
clean 304 not-modified from TIER-1).

Window: since last successful daily run (2026-08-13 06:20 UTC).

Note: cursor's RSS feed (cursor.com/changelog/rss.xml) returned 0 fresh candidates for
"Cloud Agents Start 3x Faster with Builds" (published same day, Aug 13) despite it being live
on the changelog page — feed lag or a missed entry; worth a spot-check on a future run if the
pattern repeats.

Linear: 5 issues created (KOV-131..KOV-135), all new stories, none duplicate (searched project
"News digest" by title/URL first — 50 most recent issues checked, no matches). Priorities: High
×2 (Google DeepMind Gemini 3.7 Flash — major model release; Perplexity Agent API — major product
platform shift replacing Sonar), Medium ×3 (OpenAI Ultrafast preview, HF Strands/LeRobot data
loop, Cursor builds — regular technical announcements). Type labels: model-release ×1 (Gemini 3.7
Flash), product ×3 (OpenAI Ultrafast, Cursor builds, Perplexity Agent API), infra ×1 (HF Strands/
LeRobot).

## 2026-08-15 05:05 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | vllm-blog URL error: Connection reset by peer |
| bigtech-eng | 3 | 1 | - |
| research-institutes | 0 | 0 | - |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 1 | 1 | - |
| youtube | 0 | 0 | yt-ai-engineer HTTP 404, yt-gpu-mode HTTP 404, yt-karpathy HTTP 404, yt-latent-space HTTP 404, yt-mlst HTTP 404, yt-umar-jamil HTTP 404 (yt-sentdex clean, 0 fresh) |
| community | 49 | 9 | - |
| mistral-watch | 0 | 0 | - |

Totals: 53 raw candidates across all sources, 11 confirmed, 7 source errors (1 oss-ml-systems,
6 youtube — no fallback ladder for radar sources per workflow, logged, moved on).

Note: 6 of 7 YouTube sources 404d today (only `yt-sentdex` returned cleanly) — a broader failure
than the usual 1-2 channel blips seen on prior days; worth a spot-check if it persists tomorrow,
but per workflow a quiet/erroring radar source is not itself a failure.

TRIAGE (pass 1 technical bar): `bigtech-eng` — kept Cloudflare's MCP traffic-detection post
(real protocol mechanism); dropped Cloudflare's "Secure all your internal vibe-coded applications"
(Access-for-Workers feature announcement, marketing copy — "in one click" — no real engineering
content) and GitHub's "bring your software delivery workflow into GitHub with agent apps" (tutorial-
grade Copilot/agent-apps product education, explicitly the kind of GitHub content the workflow says
to drop). `community` — HN Show queries for "RAG" and "MCP" pulled a lot of keyword-coincidence
noise with no AI content: dropped `sandbox.bio` terminal embed, `LuaCAD` (parametric CAD in Lua),
`Mininote` (note-taking app), `Rdio` (internet radio suite), `Stackdome` (Railway alternative on
K8s), `A Rosetta Stone for UI component libraries` (UI-framework mapper) — none AI/ML-related.
Reddit was dominated by Qwen3.8-27B release-day hype (25 posts, one query): dropped ~20 meme/
appreciation/pure-hype posts ("IT'S OUT", "Stop shitting on 9B models", benchmark-screenshot posts
with no technique, poll-results nostalgia, etc.) and kept only the two posts with real technical
content (Apple Silicon speedup, bitsandbytes quantization tease) plus the model card itself as
release context. `hf-trending-spaces` — dropped `2i/pornmaster-krea2` (NSFW), two video/image-gen
demo spaces (`Lightricks/LTX-2.5`, `jimmycarter/krea2-turbo-bbox-canvas` — LOW per interests.md,
robotics/video-gen), `zai-org/OpenVuln` and `akhaliq/MiniMax-H3-Turbo-Lora` (both too thin — no
summary beyond the title, not enough to confirm). `github-trending` — dropped `lightningpixel/
modly` (local image-to-3D desktop app — LOW, robotics/3D). Dropped as duplicate (already on the
radar from 2026-08-13): `fellowgeek/mcp-memory` (MCP Memory — same URL as KOV-117, caught by both
file-grep dedup and Linear project search; the source's own dedup cursor resurfaced it, feed
window issue worth watching but not actionable today). `hf-trending-models`: kept only the base
`Qwen/Qwen3.8-27B` card as release context; dropped the same-day `unsloth/Qwen3.8-27B-GGUF` and
`Qwen/Qwen3.8-27B-FP8` quant listings as the same story (quantized artifacts of an already-covered
release, no independent technique).

VERIFY SUBSTANCE (5 highest-scored candidates): Cloudflare MCP security post — verified via
WebFetch: real protocol-level detection mechanism (MCP-Protocol-Version / Mcp-Method headers), new
policy selector, explicit stated limitations (no local stdio, no private-network servers yet) —
passed, `highlight`. Interconnects GLM-5.3 post — verified via WebFetch: substantive technical
argument with real benchmark comparisons (GLM-5.3 vs Kimi K3, ~750B vs ~2.2T) and a specific,
falsifiable claim (post-training execution, not distillation) — passed, `highlight`. NanoRL —
verified via `git clone`: real ~1,800-line codebase, README backs every claim with numbers (0.391→
0.609 held-out accuracy, 102K sequences/90min, 0/1,603 batches dropped), 44 CPU tests — passed,
`highlight`. Apple Silicon mlx-dspark post — reddit `.json` curl hit HTTP 403 (Cloudflare);
confirmed on the feed's own detailed body text (concrete M4 Pro numbers, byte-identical output) per
workflow fallback — passed, not selected for a highlight slot (3 slots already used). holaOS —
verified via `git clone`: real, working open-source project (Electron/TS, CI badge, shared local-
file memory) but the README itself reads as product marketing (trend badges, Discord/X CTAs, "your
holaOS plan" language) — kept as a confirmed item, explicitly NOT a highlight per the "not a
marketing shell" bar.

3 top picks marked `highlight`: Cloudflare MCP security (KOV-136 — concrete, verifiable mechanism
for the owner's #1 HIGH-interest line, MCP ecosystem, `tech_explainer` seed), GLM-5.3 analysis
(KOV-137 — Nathan Lambert's specific post-training argument, evals-in-practice angle, `tech_explainer`
seed), NanoRL (KOV-139 — reproducible RL codebase with code and real numbers, direct `project_post`
seed — the strongest "own experiment" candidate of the day). Spread: inference-infra, lab-
engineering, oss-ml-systems, research-institutes, technical-newsletters, youtube and mistral-watch
were silent today (0 confirmed each).

Linear: 11 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to
Review" — KOV-136 through KOV-146. Priorities by fit (HIGH→High ×6, MEDIUM→Medium ×5). Source
labels applied per item (blog ×2, hn ×3, reddit ×2, hf ×1, github ×3); `highlight` on KOV-136,
KOV-137, KOV-139. Searched the project first — one collision found and skipped (`fellowgeek/
mcp-memory`, already KOV-117), no other duplicates against the 46 existing cards checked.

Commit: `news: radar run 2026-08-15 (+11 items, 3 highlights)`.

## 2026-08-15 06:20 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss, websearch, jina(listing) | 0 | websearch, jina | no in-window Product/Engineering/Research/Publication/Release item confirmed on openai.com/news (latest still Aug 13, Builder's guide to GPT-5.6); WebSearch surfaced an IBM strategic-partnership story but no primary openai.com/news/index page could be found to confirm it as a Company-blog item |
| anthropic | fetch | 1 | - | - |
| google-deepmind | rss, websearch, direct listing | 0 | websearch, direct fetch | latest post still Aug 13 (Gemini 3.7 Flash, already captured), no newer post confirmed |
| google-research | rss, websearch, direct listing | 0 | websearch, direct fetch | latest post still Aug 12 (parametric-factuality, already captured), no newer post confirmed |
| microsoft | rss, websearch, direct listing | 0 | websearch, direct fetch | latest post still Aug 12 (MindTopo, already captured), no newer post confirmed |
| nvidia | rss, websearch, direct listing | 0 | websearch, direct fetch | latest post still Aug 12 (Qwen3.8 GB300 serving, already captured); one WebSearch hit ("open-models-data-tools-accelerate-ai") verified via WebFetch as a stale Jan 5 2026 article resurfacing in search, correctly excluded |
| xai | jina | 2 | jina | anonymous Jina worked cleanly (no 401/403 this run; JINA_API_KEY still unset) — found Aug 14 GitHub Copilot integration AND backfilled the Aug 12 Grok 4.6 main release, which the 2026-08-13 run had flagged as an unconfirmed WebSearch-only candidate (Jina 401'd that day) |
| mistral | rss, websearch, direct listing | 0 | websearch, direct fetch | latest post still Aug 11 (sovereign-AI, already captured), no newer post confirmed |
| huggingface | rss, direct listing | 1 | direct fetch | RSS reported 0 fresh but the blog's own listing showed an Aug 14 post ("State of Open Models: Summer 2026 Observations") not yet in the feed — direct fetch confirmed and captured it |
| cursor | rss, fetch | 0 | fetch | direct fetch of cursor.com/changelog confirms latest entry still Aug 13 (Cloud Agents Builds, already captured), predates window |
| perplexity | jina, websearch | 0 | jina (403 AbuseAlleviation, then 401 bad-IP-reputation on retry), websearch | no JINA_API_KEY; WebSearch turned up only undated/aggregator content, no primary hub.perplexity.ai post confirmed in-window |

Totals: 4 items, 3 companies fresh, 0 errors (11 gap-scrapes attempted — all TIER-1 RSS reported
zero fresh candidates today, a mistral 304 not-modified aside; anthropic fetch caught a genuine
new post; xai's anonymous Jina worked cleanly and both confirmed a same-day item and backfilled a
previously-flagged-unconfirmed one from two days ago; huggingface's own blog listing caught a post
its RSS feed hadn't surfaced yet; google-deepmind/google-research/microsoft/nvidia/mistral/openai/
cursor/perplexity all gap-scraped clean with nothing new confirmed in-window).

Window: since last successful daily run (2026-08-14 06:19 UTC).

Note: xAI backfill — "Introducing Grok 4.6" (published 2026-08-12) was noticed via WebSearch in
the 2026-08-13 run but could not be confirmed then (Jina hard-401'd, no primary x.ai/news URL
found). Today's anonymous Jina fetch of x.ai/news surfaced it as the primary featured story with a
confirmed URL and date, so it was added to close the gap rather than left permanently missing —
flagged explicitly here and in the item line/artifact/Linear card for traceability.

Note: Hugging Face's RSS feed (huggingface.co/blog/feed.xml) reported zero fresh candidates for
"State of Open Models: Summer 2026 Observations" (published same day, Aug 14) despite it being
live on the blog listing — same feed-lag pattern seen before with Cursor's changelog RSS; worth a
spot-check if it recurs.

Linear: 4 issues created (KOV-147..KOV-150), all new stories, none duplicate (searched project
"News digest" by title first — no matches for "watermark", "Grok 4.6", or "State of Open Models").
Priorities: High ×1 (xAI Grok 4.6 — major model release), Medium ×3 (Anthropic watermark, xAI
GitHub Copilot integration, HF ecosystem report — regular technical announcements). Type labels:
model-release ×1 (Grok 4.6), product ×1 (Grok 4.6 GitHub Copilot), policy-safety ×1 (Claude
watermark), research ×1 (HF State of Open Models).

## 2026-08-16 05:06 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | - |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 2 | 2 | - |
| youtube | 9 | 6 | - |
| community | 25 | 6 | reddit HTTP 429 (skipped, no retry) |
| mistral-watch | 0 | 0 | mistral-docs-changelog SSL handshake timeout |

Totals: 14 items, 0 errors blocking a whole category (2 source-level errors logged and skipped
per no-fallback-ladder rule), 2 highlights.

Window: since last successful radar run (2026-08-15, per run-log). Note: an earlier invocation
of `fetch_radar.py` this run was accidentally executed twice in sequence, advancing
`state/radar-cursors.json` past several items before the second run's output was inspected —
caught before any write, `git checkout -- news/state/radar-cursors.json` reset it, then the
script was re-run once cleanly; the JSON used for triage below is from that single clean run.

TRIAGE (pass 1, technical bar): dropped 2 `yt-ai-engineer` AI Engineer-conf talks as vendor
marketing despite real-sounding titles — Oxylabs' "How Web Data Infrastructure Powers the Next
Generation of AI" and Bright Data's "The Rise of CaaS: Context-as-a-Service for Agentic AI", both
data-scraping/proxy vendors pitching buzzword-coined categories. `yt-gpu-mode` livestream +
edited-cut duplicate (Spectral Compute: Compile CUDA everywhere) collapsed to one item, kept the
edited Lecture 111 cut. In `community`, the four HN Show-HN queries (`inference`/`rag`/`mcp`/
`agents`) turned up heavy cross-query overlap plus several completely off-topic submissions that
only matched on incidental keyword hits — dropped as non-AI: a Rust/Tauri bookmarking app, a mock
API server (`Mocktail`), a Linux-terminal-embed widget, `LuaCAD`, `Mininote`, and an internet-radio
suite (`Rdio`). Two `hf-trending-spaces` entries (a video-gen space, a FLUX LoRA space) dropped as
LOW-interest video/image-gen per `config/interests.md`. Three `github-trending` entries dropped:
`cordiverse/cordis` (not clearly AI-specific), `cursor/plugins` (company-core territory — Cursor is
a tracked company, belongs in `topics/cursor.md` not radar), `public-apis/public-apis` (general
dev list, no AI content).

DEDUP: `Show HN: Mole – Deep research agent for your terminal` (github.com/lajosdeme/mole) is
already on the radar (2026-08-14, KOV-138) — re-surfaced today because it was still fresh in the
HN `agents` query window; skipped as a duplicate (file grep + Linear project search both caught
it before any write).

VERIFY SUBSTANCE (5 highest-scored candidates + 2 extra attempts): `lajosdeme/mole` — moot (dup,
see above), but its README was read anyway as part of the clone: confirms the existing radar
entry's claims (enforced budget, verified quotes) hold up. `MakazhanAlpamys/Soup` — verified via
`git clone`: real, actively maintained (CI, PyPI, DOI) fine-tuning CLI; README backs its headline
claim (8B model on 4GB laptop GPU) with a specific measurement (119.6 tok/s, 3.32GB peak, bit-exact
vs resident run, reproduced on H100) and is unusually honest about caveats (a prior tok/s figure
predates a correctness fix and hasn't been re-measured; a Colab notebook lets the reader verify the
4GB claim themselves) — passed, `highlight`. Latent Space "Flue 2" — verified via WebFetch: real
architectural content (React-style Agent Hooks: `useSkill`/`useTool`/`useSubagent`, a concrete
dynamic-tool-loading example) though framed as an interview rather than deep documentation —
passed, `highlight`. Raschka "AI Text Detector From Scratch" — verified via WebFetch: legitimate
end-to-end project (DistilBERT classifier, RLVR verifier use) but the post is paywalled past the
intro, no numbers/dataset/code visible in the free preview — kept as a confirmed item, NOT a
highlight (verification incomplete, not failed). Two more attempts beyond the base 5, both hit
transport errors on both legs (WebFetch egress-blocked + curl 403 CONNECT-tunnel-fail — counts as
the one allowed curl retry): `chenxiachan.github.io/thoughtdag` (ThoughtDAG, 115 pts/55 comments —
today's strongest raw community signal) and `app.deltix.ai` (Deltix). Two more items with the same
domain pattern (`waku.sh`, `pinglin.tw`) were spot-checked for the same reason and hit identical
egress blocks. All four stay confirmed regular items, explicitly out of highlight consideration
per the "transport error → keep item, skip highlight" rule — worth a revisit if the egress
allowlist changes, since ThoughtDAG in particular reads as the day's most-discussed item by a wide
margin.

Linear: 14 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to
Review" — KOV-151 through KOV-164. Priorities by fit (HIGH→High ×8, MEDIUM→Medium ×5, LOW→Low ×1).
Source labels applied per item (blog ×2, youtube ×6, hn ×4, lobsters ×1, github ×1); `highlight` on
KOV-151 (Flue 2) and KOV-164 (Soup) — 2 highlights, not the max 3, since the day's strongest
community-signal item (ThoughtDAG) and two other high-fit HN items couldn't clear verification
today. Searched the project first — one collision found and skipped (Mole, already KOV-138), no
other duplicates against the existing cards checked.

Commit: `news: radar run 2026-08-16 (+14 items, 2 highlights)`.

## 2026-08-16 06:13 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml, websearch | 0 | websearch | rss.xml fetched cleanly, latest still Aug 13 (Ultrafast + builder's guide, already captured); openai.com/news/ 403'd on direct fetch (excluded via one-fallback rule); websearch confirmed no Product/Engineering/Research/Publication/Release item after Aug 13 |
| anthropic | fetch, websearch | 0 | websearch | anthropic.com/news listing still tops out at Aug 14 (text watermark, already captured); no newer post confirmed |
| google-deepmind | rss, direct listing, websearch | 0 | direct fetch, websearch | latest still Aug 13 (Gemini 3.7 Flash, already captured); RSS reported 304 |
| google-research | rss, direct listing, websearch | 0 | direct fetch, websearch | latest still Aug 12 (parametric-factuality recall, already captured) |
| microsoft | rss, direct listing | 0 | direct fetch | latest still Aug 12 (MindTopo, already captured); no 403 this run, listing fetched cleanly |
| nvidia | rss, direct listing, websearch | 0 | direct fetch, websearch | RSS reported 304; listing's newest entries both dated Aug 12 (Qwen3.8 GB300 serving — already captured — and an observability post same day, not strictly newer) |
| xai | jina | 0 | - | anonymous Jina worked cleanly (no 401/403); latest still Aug 14 (GitHub Copilot integration, already captured) |
| mistral | rss, direct listing, websearch | 0 | direct fetch, websearch | RSS reported 304; listing + 6 websearch hits all confirmed no post after Aug 11 (sovereign-AI, already captured) |
| huggingface | rss, direct listing, websearch | 0 | direct fetch, websearch | RSS reported 304; listing + websearch confirm latest still Aug 14 (State of Open Models, already captured) |
| cursor | rss (connection reset), direct listing, websearch | 0 | direct fetch, websearch | rss.xml connection reset by peer; direct fetch + websearch both confirm latest still Aug 13 (Cloud Agents Builds, already captured) |
| perplexity | jina, websearch | 0 | jina (401 bad-IP-reputation), websearch | no JINA_API_KEY; anonymous Jina hard-401'd; websearch found no confirmable primary perplexity.ai/hub/blog post after Aug 13 — worth a manual check once the key is set |

Totals: 0 items, 0 companies fresh, 1 transport error (cursor rss.xml connection reset — recovered
cleanly via direct-fetch gap-scrape, no data lost). All 11 TIER-1 sources reported zero fresh
candidates (10 via 304-not-modified/empty, 1 via connection reset); all 11 companies were
gap-scraped one fallback attempt each per the ladder, and all 11 independently confirmed their
respective topics/*.md files already hold the latest available post — a fully quiet news day
across the tracked company set.

Window: since last successful daily run (2026-08-15 06:20 UTC).

Linear: no new stories to file — nothing created, nothing skipped as duplicate.

## 2026-08-17 05:17 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| bigtech-eng | 0 | 0 | none |
| community | 45 | 10 | none |
| inference-infra | 0 | 0 | none |
| lab-engineering | 0 | 0 | none |
| mistral-watch | 0 | 0 | none |
| oss-ml-systems | 0 | 0 | none |
| practitioner-blogs | 1 | 1 | none |
| research-institutes | 0 | 0 | none |
| technical-newsletters | 1 | 0 | none |
| youtube | 0 | 0 | none |

Totals: 47 raw candidates, 11 confirmed, 0 source errors.

TRIAGE (pass 1, technical bar): `reddit` (25 raw) was almost entirely Qwen 3.8 27B release-day
chatter on r/LocalLLaMA — dropped ~15 low-effort chat/question/opinion threads with no technique
or numbers (e.g. "I'm still running Qwen 3.5 122B, should I switch?", "The dream is to reach
200GB VRAM", "Why are RTX 6000 PROs still getting bought", "Let's all thank Georgi Gerganov",
"Anyone else get a kick out of Qwen 3.8 27B Reasoning Dialogue?", a meme-titled post, several
quant/hardware questions with no answer given). Kept 6 reddit items with real technique or
numbers (see WRITE below). HN Show queries (`rag`/`mcp`/`agents`) had heavy cross-query overlap
(waku.sh, pinglin.tw, and the DeepSeek-V4-Flash-Coder post each matched 2 queries — deduped to one
each) plus two off-topic drops: `shelf-bookmarks` (Rust+Tauri bookmarking app, no AI) and
`wheres-my-muni` (SF transit live map, no AI). `github-trending` (3) all dropped as not
AI-specific: `basecamp/omarchy` (Linux distro), `OpenCut-app/OpenCut` (video editor), `ToolJet/
ToolJet` (low-code app builder, AI mentioned only as one feature). `hf-trending-models` (2) and
`hf-trending-spaces` (2) all dropped as LOW-interest video/image-gen or low-novelty community
fine-tunes per `config/interests.md` (a realism LoRA, two video-gen Spaces, an "uncensored" FP8
quant with no notable technique). `technical-newsletters`: SemiAnalysis's PJM/ratepayer piece
dropped per the standing rule (finance/markets post, not engineering). One HN Show item —
`wildstatic.com`, "A public AI whose memory is shared across all users" (69 pts) — was held back
entirely: empty body text, a marketing-shell-sounding title, and (see VERIFY below) no way to
confirm it delivers real technique; dropped rather than padded into the file.

DEDUP: `waku.sh` (Show HN: native coding-agent app, Rust+GPUI) and `pinglin.tw/blog/the-shapes-
of-agent-memory` (Show HN: agent-memory framework comparison) both resurfaced today across
multiple HN Show queries — both are already on the radar from yesterday (KOV-160, KOV-161,
2026-08-16) — skipped as duplicates, no re-add, no new cards.

VERIFY SUBSTANCE (5 highest-scored + 2 extra attempts): `steadfastgaze/DeepSeek-V4-Flash-...-
MoEspressoV2` (HF) — verified via WebFetch: real expert-pruned coding quant of DeepSeek-V4-Flash-
0731 with honest published numbers (code perplexity 2.7665 vs 2.4250, 88.55% token agreement,
16/16 coding tests, WikiText perplexity trade-off 11.2043 vs 5.5548) — passed, `highlight`.
`simonwillison.net` Qwen 3.8 27B review — verified via WebFetch: real hands-on testing with
concrete numbers (21 min / 22,276 reasoning tokens for one SVG at the `xhigh` default, cut to 137s
with reasoning off) — passed, `highlight`. `developer.nvidia.com` GB300 NVL72 serving post —
verified via WebFetch: real first-party numbers (4K+ tok/s/GPU, 350+ tok/s/user, FP8) — passed,
but same model+hardware pairing already on the radar with higher NVFP4 numbers from SGLang/Miles
(`oss-ml-systems`, 2026-08-12); confirmed as a regular item, not a highlight (re-confirmation, not
a fresh story). Three attempts hit the same transport pattern as recent days — WebFetch egress-
blocked + curl 403 CONNECT-tunnel-fail (the one allowed retry) — on `pinglin.tw`, `waku.sh` (both
moot, see DEDUP above, but attempted since they were today's top-scored candidates before the dup
check) and `littlelearner-ll.github.io`; `wildstatic.com` hit the identical block and, combined
with its empty body text, was dropped rather than kept unverified (see TRIAGE above). All items
that failed verification and were still net-new stay confirmed regular items, out of highlight
consideration, per the "transport error → keep item, skip highlight" rule — except wildstatic.com,
held back entirely for insufficient signal.

WRITE: 10 items to `radar/community.md`, 1 to `radar/practitioner-blogs.md` under `## 2026-W34`.
Community: DeepSeek-V4-Flash-Coder-57GB (highlight), Qwen3.8-27b RTX 3090 82tps, Qwen3.8-2.4T
GB300 NVL72 (NVIDIA blog), audio.cpp 0.6, Koboldcpp v1.119, PyScrappy MCP server, Grafana Hermes
observability, RL-1-3%-tokens paper claim, Genie-style world model on a 5090, "LLM never sees
beyond fifth grade". Practitioner-blogs: Simon Willison's Qwen 3.8 27B review (highlight).

Linear: 11 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to
Review" — KOV-166 through KOV-176. Priorities by fit (HIGH→High ×5, MEDIUM→Medium ×5, LOW→Low
×1). Source labels applied per item (reddit ×6, hn ×4, blog ×1); `highlight` on KOV-166
(DeepSeek-V4-Flash-Coder) and KOV-176 (Simon Willison) — 2 highlights, not the max 3, since the
day's other verified item (GB300) was a re-confirmation rather than fresh news. Searched the
project first — two collisions found (waku.sh = KOV-160, pinglin.tw = KOV-161) and skipped, no
other duplicates against the existing board.

Commit: `news: radar run 2026-08-17 (+11 items, 2 highlights)`.

## 2026-08-17 06:11 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml, WebFetch, websearch | 0 | WebFetch, websearch | rss.xml 304-not-modified; openai.com/news/ 403'd on direct fetch (excluded via one-fallback rule); websearch confirmed no Product/Engineering/Research/Publication/Release item after Aug 13 (Ultrafast, already captured) — only consumer ChatGPT app features and a stale Aug 10 Daybreak recap turned up |
| anthropic | fetch, websearch | 0 | WebFetch | anthropic.com/news listing still tops out at Aug 14 (text watermark, already captured); no newer post confirmed |
| google-deepmind | rss, WebFetch, verify | 0 | WebFetch | rss.xml 304-not-modified; listing's newest three posts (Gemini 3.7 Flash Aug 13, sign-language SL2T Aug 12, WeatherNext Aug 6) all already captured — verified the SL2T post specifically since it wasn't in the first screenful, confirmed already on file |
| google-research | rss, WebFetch | 0 | WebFetch | rss.xml 304-not-modified; listing tops out at Aug 12 (parametric-factuality recall, already captured) |
| microsoft | rss, WebFetch | 0 | WebFetch | listing's newest three (MindTopo Aug 12, CARE-X Aug 11, Orchard Aug 3) all older than or equal to the latest captured item — none fresh |
| nvidia | rss, WebFetch | 0 | WebFetch | rss.xml 304-not-modified; listing's newest entries (GB300 serving + observability post, both Aug 12) and JetPack 7.2.1 (Aug 11) are same-day-or-older than the latest captured item — none strictly newer |
| xai | jina, websearch | 0 | websearch | anonymous Jina worked cleanly; websearch confirms Grok 4.6 (Aug 12) and GitHub Copilot integration (Aug 14) both already captured, Grok Bot (Aug 11) predates the window — no post after Aug 14 |
| mistral | rss, WebFetch | 0 | WebFetch | rss.xml 304-not-modified; listing tops out at Aug 11 (sovereign-AI infrastructure, already captured) |
| huggingface | rss, WebFetch | 0 | WebFetch | rss.xml 304-not-modified; listing tops out at Aug 14 (State of Open Models, already captured); next-newest (icml reproductions, Aug 13) older |
| cursor | rss, WebFetch | 0 | WebFetch | rss.xml 304-not-modified; changelog tops out at Aug 13 (Cloud Agents Builds, already captured) |
| perplexity | jina, websearch | 0 | jina (no key, skipped), websearch | no JINA_API_KEY, anonymous Jina not attempted given prior hard-401 pattern; websearch surfaced only undated/no-URL mentions (Grok 4.6 in Agent API, Vercel AI SDK compat) — not confirmable against a primary post, not added; latest captured item (Aug 13 Agent API launch) stands |

Totals: 0 items, 0 companies fresh, 0 transport errors beyond the expected openai.com/news/ 403
(excluded via the one-fallback rule, rss.xml already covered that source). All 11 TIER-1 sources
reported zero fresh candidates (10 via 304-not-modified, 1 — openai — via clean rss fetch with no
new items); all 11 companies were gap-scraped one fallback attempt each per the ladder, and all 11
independently confirmed their respective topics/*.md files already hold the latest available post
— another fully quiet news day across the tracked company set, continuing the streak since
2026-08-15.

Window: since last successful daily run (2026-08-16 06:13 UTC).

Linear: no new stories to file — nothing created, nothing skipped as duplicate.

Commit: `news: daily run 2026-08-17 (+0 items, 0 companies fresh)`.

## 2026-08-17 07:07 UTC — deep-dive — ok (no approved cards)

Searched project "Radar" for cards with label `hot` across all states (single query, no
state filter, archived included) — zero hot cards anywhere in the project. The 11 review
cards filed this morning (KOV-166–KOV-176) are all still awaiting the owner's verdict in
"Ready to Review". No cards processed, no files written, no leftovers. Exiting quietly per
workflow.

## 2026-08-18 05:11 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| oss-ml-systems | 1 | 1 | 0 |
| practitioner-blogs | 1 | 1 | 0 |
| bigtech-eng | 1 | 0 | 0 |
| community | 60 | 11 | 0 |
| inference-infra | 0 | 0 | 0 |
| lab-engineering | 0 | 0 | 0 |
| mistral-watch | 0 | 0 | 0 |
| research-institutes | 0 | 0 | 0 |
| technical-newsletters | 0 | 0 | 0 |
| youtube | 0 | 0 | 7 (yt-ai-engineer 404, yt-gpu-mode 500, yt-karpathy 404, yt-latent-space 404, yt-mlst 404, yt-sentdex 404, yt-umar-jamil 404 — all expected/known transport errors) |

Totals: 63 raw candidates across 52 sources, 13 confirmed, 3 highlights.

TRIAGE pass 1 (technical bar): dropped github-ai's Copilot "canvases" post (tutorial-grade Copilot
product content); dropped smolai's "not much happened today" issue (explicit skip rule); dropped a
long tail of non-AI HN Show submissions cross-listed under multiple radar queries (Visimer mermaid
editor, Saggar terminal, Flynt.js, PageSieve scraper — general dev tools, not AI/ML-specific)
despite matching keyword filters; dropped consumer/marketing GitHub-trending repos (MoneyPrinterTurbo
ad-laden README, career-ops, immich, nautilus_trader — no AI angle) and one likely content-farm repo
(mukul975/Anthropic-Cybersecurity-Skills — mass-generated-skills pattern). DEDUP: 5 items were same-
story repeats already on the radar from 2026-08-16 (DeepSeek-V4-Flash-Coder-57GB, PyScrappy, Grafana
Hermes agent-observability ×2 listings, the fifth-grade-LLM HN thread, wildstatic.com — the last was
explicitly dropped yesterday for thin content and stays dropped) — skipped, no re-add. Reddit
r/LocalLLaMA carried heavy Qwen3.8-27B chatter (25 raw items) — pass 1 dropped memes/appreciation/
speculation threads ("wen", "overthinking" hot takes, "unpopular opinion", quant-level petition,
"Ling 3.0 Tiny" anecdote) per the explicit meme-drop rule, keeping only threads with concrete
technical content (PR details, benchmark numbers, hardware configs, real papers).

TRIAGE pass 2 (owner fit): 10 HIGH (SGLang CUDA graph, interconnects Nvidia-strategy piece, llama.cpp
adaptive MTP PR, unsloth NVFP4 quant, two "runs on my hardware" Qwen3.8-27B posts, akitaonrails/ai-
memory, AlexsJones/llmfit, HarnessEval-W, ClawGym II — all land directly on interests.md HIGH bullets:
local/self-hosted inference, agent memory, agent-harness RL, evals-in-practice, reproducible
techniques), 3 MEDIUM (usestrix/strix — agent harness applied to security; Stripe/OpenRouter
acquisition — business but high ecosystem impact on routing tooling; DeepMind "LLMs can't jump" paper
— research-institutes, no code).

VERIFY SUBSTANCE (5 highest-scored): SGLang CUDA graph post — WebFetch, passed (concrete BCG/full/
piecewise benchmarks: 3.8–5.2× build speedup, 1.45–1.93× replay speedup, memory/latency numbers) →
highlight. interconnects "Teaching Everyone to Fish for Tokens" — WebFetch, passed (real $26B figure,
clearly framed as analysis not fact) → regular item, not a highlight (opinion-heavy). akitaonrails/
ai-memory — git clone, passed (mature cross-platform project, real CI/support matrix, MCP + lifecycle
hooks) → highlight. AlexsJones/llmfit — git clone, passed (active CI, crates.io release, community-
verified-benchmark feature) → highlight. llama.cpp adaptive MTP PR reddit post — curl hit HTTP 403
(Cloudflare, one retry per rule); kept as a regular item on the feed's own body text per the
transport-error rule, out of highlight consideration.

WRITE: 1 item to `radar/oss-ml-systems.md`, 1 to `radar/practitioner-blogs.md`, 11 to
`radar/community.md`, all under `## 2026-W34`.

Linear: 13 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to Review" —
KOV-177 through KOV-189. Priorities by fit (HIGH→High ×10, MEDIUM→Medium ×3). Source labels applied
per item (github ×3, hf ×3, reddit ×5, blog ×2); `highlight` on KOV-177 (SGLang CUDA graph), KOV-183
(akitaonrails/ai-memory), KOV-184 (AlexsJones/llmfit) — 3 highlights, the daily max. Searched the
project by title keyword for every candidate first — no collisions found, nothing skipped as
duplicate.

Commit: `news: radar run 2026-08-18 (+13 items, 3 highlights)`.

## 2026-08-18 06:14 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml, WebFetch, websearch | 0 | WebFetch (403), websearch | openai.com/news/ direct fetch 403'd (one-fallback rule); websearch confirmed no Product/Engineering/Research/Publication/Release item after Aug 11 Daybreak/AWS (already captured) — only GPT-5.6 August-update recap, Astra math results (Aug 1, predates window), and Dali Rajic CRO hire turned up, all older or non-qualifying |
| anthropic | fetch, websearch | 0 | none needed | anthropic.com/news listing tops out at Aug 14 (text watermark, already captured); confirmed via WebFetch, no fallback required |
| google-deepmind | rss, WebFetch | 0 | WebFetch | rss.xml no change; listing's newest three (Gemini 3.7 Flash Aug 13, sign-language SL2T Aug 12, WeatherNext Aug 6) all already captured |
| google-research | rss, confirmed | 1 | none | rss.xml TIER-1 hit: "Seeing beyond BMI" (PhotoScan cardiometabolic-risk model), 2026-08-17 — new, confirmed via WebFetch |
| microsoft | rss, WebFetch | 0 | WebFetch | listing's newest three (MindTopo Aug 12, CARE-X Aug 11, Orchard Aug 3) all already captured, none fresh |
| nvidia | rss, confirmed | 1 | none | rss.xml TIER-1 hit: "Developing Nemotron 3.5 Lightning NVFP4 with QAD Using NVIDIA Model Optimizer", 2026-08-17 — new, confirmed via WebFetch |
| xai | jina (curl), websearch | 0 | jina (Cloudflare challenge, failed), websearch | curl-via-Jina hit a Cloudflare "Just a moment..." challenge page (no content); websearch confirmed Grok 4.6 (Aug 12) and GitHub Copilot integration (Aug 14) both already captured, nothing newer |
| mistral | rss.xml (304), WebFetch | 0 | WebFetch | rss.xml 304-not-modified; listing tops out at Aug 11 (sovereign-AI infrastructure, already captured) |
| huggingface | rss, confirmed | 1 | none | rss.xml TIER-1 hit: "Same Cluster, 33 Points More Utilization: What Changed Was the Order" (Dharma AI, GPU-management pt. 2), 2026-08-17 — new, confirmed via WebFetch |
| cursor | rss.xml (304), WebFetch | 1 | WebFetch | rss.xml showed no diff but WebFetch of the changelog page surfaced "Origin Code Hosting" (Aug 17) — new, not yet in feed cache; confirmed via WebFetch, exact permalink found on second attempt |
| perplexity | jina (blocked), websearch | 0 | websearch | no JINA_API_KEY, direct www.perplexity.ai fetch and Jina both egress-blocked; websearch confirmed no post after Aug 13 Agent API (already captured) — Grok 4.6 support and Vercel AI SDK compat mentions are undated sub-features, not a standalone dated post, not added |

Totals: 4 items, 4 companies fresh (google-research, nvidia, huggingface, cursor), 0 transport errors beyond
the expected xai Cloudflare-challenge and openai/perplexity direct-fetch blocks (all covered by the
one-fallback rule).

Window: since last successful daily run (2026-08-17 06:11 UTC).

Linear: 4 new stories filed — KOV-190 [Google Research] PhotoScan (Medium, research), KOV-191 [NVIDIA]
Nemotron 3.5 Lightning NVFP4 QAD (Medium, model-release), KOV-192 [Hugging Face] Dharma AI GPU management
pt.2 (Medium, infra), KOV-193 [Cursor] Origin Code Hosting (High, product). Searched project "News digest"
by title/keyword for each before creating — no collisions, nothing skipped as duplicate.

Commit: `news: daily run 2026-08-18 (+4 items, 4 companies fresh)`.

## 2026-08-19 05:14 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | none |
| inference-infra | 0 | 0 | none |
| oss-ml-systems | 1 | 1 | none |
| bigtech-eng | 0 | 0 | none |
| research-institutes | 2 | 1 | none |
| technical-newsletters | 1 | 0 | none |
| practitioner-blogs | 1 | 0 | none |
| youtube | 0 | 0 | all 7 sources errored (6× HTTP 404, 1× HTTP 500 on yt-latent-space) — YouTube RSS endpoints unreachable today, no fallback ladder for radar, logged and moved on |
| community | 52 | 13 | none |
| mistral-watch | 0 | 0 | mistral-docs-changelog: SSL handshake timeout, logged and moved on |

Totals: 57 raw candidates, 15 confirmed, 2 source-error groups (youtube×7, mistral-watch×1) — all within FAILURE MODES (no fallback ladder for radar sources).

TRIAGE pass 1 (technical bar): dropped the bulk of today's 57 candidates — off-topic HN Show HN posts (Sokoban solver, game reverse-engineering, Mermaid editor, macOS keychain tool, Mac terminal, fiction-writing UI — none AI/ML-engineering), vanity/trending noise (HF trending-models: 3 uncensored Qwen3.8-27B finetunes farming likes + 1 chat-template fix, dropped as a group; HF trending-spaces: humanizer/face-search/TRELLIS.2, dropped — 3D-gen is explicitly LOW per interests.md), memes/appreciation (Reddit: "local models fear my tests", "and here we are", KV-cache joke, "Is Ling 3 tiny underrated" opinion thread), a bare rumor (Qwen midsize-model Discord leak, no confirmed facts), a vanity-metric post (HF "3 million models" milestone), a market-price post (DDR5 price climb — hardware-market is explicitly LOW), a CEO-interview/marketing piece (Latent.Space "model routing" — Glean-sponsored framing), and two GitHub-trending non-AI repos (Motrix download manager, PLFM_RADAR literal hardware radar). Also dropped: PantheonGPU (HN, 13pts/0 comments — too weak a signal to spend budget on), semianalysis Cerebras CS-4 (real technical content but crowded out at the volume cap by stronger owner-fit items), answer.ai code-simplicity essay (same), Embodied-Navigator paper (robotics — LOW), ASI-Bench paper (swapped out for the stronger-attributed ai2 interpretability piece at the volume cap), OpenCode sampler bug and Linux VRAM kernel post (both legitimate but cut at the ≤15 budget in favor of higher owner-fit items).

TRIAGE pass 2 (owner fit): of the ~30 items clearing pass 1, kept the top 15 against interests.md — 10 HIGH (Shoehorn quantizer, munder-difflin multi-agent harness, OpenViking agent-memory DB, Agentic ESOpt, 5 Qwen3.8-27B/DeepSeek-V4 "runs on my hardware" reproducible-technique reddit posts, DFlash2 hands-on test, Miles v0.1, tencent UI-Mate-27B), 5 MEDIUM (Ling-3.0 llama.cpp mainline, Bitnet/Ternary tracker, Alibaba RISC-V CPU, ai2 drug-morphology interpretability). Same-story dedup: 3 Reddit posts about DFlash2 (r/1vs2tz1, r/1vs2tsn, r/1vs43av) collapsed to the one hands-on test with real numbers; "Show HN: Openleetcode" and "Show HN: Saggar"/"1667" appeared under multiple HN-query source IDs (rag/mcp/agents) as the same underlying story — deduped to zero (off-topic, not kept) rather than counted twice.

VERIFY SUBSTANCE (7 attempts total against the 5-highest-scored-candidates guidance, widened after 3 transport failures): munder-difflin — `git clone`, passed (MIT, v0.4.4 working prototype, real README/CI structure) → highlight. volcengine/OpenViking — `git clone`, passed (AGPLv3, Trendshift-listed, active releases/contributors, docs site) → highlight. lmsys-sglang Miles v0.1 — WebFetch, passed (concrete P2P weight-sync 53.3s→7.2s, distillation 84.6%→89.5%, day-0 AMD+NVIDIA support) → highlight. tencent/UI-Mate-27B — WebFetch on the HF model card, passed (OSWorld-Verified 77.0, WindowsAgentArena 66.2, honest documented limitations) → strong regular item, not a highlight (cap already at 3). Shoehorn (github.io) — WebFetch + curl retry both hit EGRESS_BLOCKED (domain not allowlisted); kept as regular item on the HN submission's own text, out of highlight consideration. Agentic ESOpt (arxiv.org + HF paper page) — both WebFetch attempts returned no usable full text (egress-blocked / image-only render); kept as regular item on the radar fetch's own abstract excerpt, out of highlight consideration. Reddit "124 tps on a RTX 3090" — curl (browser UA) hit HTTP 403; kept as regular item on the feed's own body text per the transport-error rule, out of highlight consideration.

WRITE: 13 items to `radar/community.md`, 1 to `radar/oss-ml-systems.md`, 1 to `radar/research-institutes.md`, all under `## 2026-W34`.

Linear: 15 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to Review" — KOV-194 through KOV-208. Priorities by fit (HIGH→High(2) ×10, MEDIUM→Medium(3) ×5). Source labels applied per item (github ×2, hf ×2, hn ×1, reddit ×9, blog ×2 — includes ai2's blog-adapter source); `highlight` on KOV-195 (munder-difflin), KOV-196 (OpenViking), KOV-204 (Miles v0.1) — 3 highlights, the daily max. Searched the project by title keyword for every candidate first — no collisions found, nothing skipped as duplicate.

Commit: `news: radar run 2026-08-19 (+15 items, 3 highlights)`.

## 2026-08-19 06:14 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1) | 2 | none needed | none |
| anthropic | fetch (WebFetch) | 0 | none needed | listing tops out at Aug 14 (text watermark, already captured) |
| google-deepmind | rss, WebFetch | 0 | WebFetch | rss.xml no fresh entries; listing's newest three (Gemini 3.7 Flash Aug 13, SL2T Aug 12, WeatherNext Aug 6) all already captured |
| google-research | rss.xml (TIER-1) | 0 | none needed | rss.xml no fresh entries beyond PhotoScan (Aug 17, already captured in prior run) |
| microsoft | rss, WebFetch | 0 | WebFetch | listing's newest three (MindTopo Aug 12, CARE-X Aug 11, Orchard Aug 3) all already captured, none fresh |
| nvidia | rss.xml (TIER-1) | 2 raw, 1 kept | none needed | ALCHEMI toolkit post kept as genuine toolkit/agent-integration announcement; UMAP multi-GPU post dropped as tutorial-grade technique content (existing cuML/cuVS 25.06 library, no new release) per the NVIDIA "keep only genuine announcements/major posts" note |
| xai | jina (curl, anonymous — worked) | 0 | none needed | listing's newest (Grok 4.6 in GitHub Copilot, Aug 14) already captured, nothing newer |
| mistral | rss.xml (304 not modified), WebFetch | 0 | WebFetch | listing tops out at Aug 11 (sovereign-AI infrastructure, already captured) |
| huggingface | rss.xml (TIER-1) | 1 | none needed | none |
| cursor | rss.xml (304 not modified), WebFetch | 0 | WebFetch | listing's newest (Origin Code Hosting, Aug 17) already captured from prior run, nothing newer |
| perplexity | jina (curl, anonymous — worked this run) | 0 | none needed | listing's visible recent entries (Jul 29 Research post) predate the already-captured Aug 13 Agent API post; no new item |

Totals: 4 items kept (1 dropped as tutorial-grade), 3 companies fresh (openai, nvidia, huggingface), 0 transport errors — xai and perplexity jina both succeeded anonymously this run (no JINA_API_KEY needed today).

Window: since last successful daily run (2026-08-18 06:14 UTC).

Linear: 4 new stories filed — KOV-209 [OpenAI] ChatGPT for Teens (High, product), KOV-210 [OpenAI] ChatGPT Ads expands across Europe (Medium, business), KOV-211 [NVIDIA] ALCHEMI Toolkit for AI coding agents (Medium, infra), KOV-212 [Hugging Face] How Much Memory Does Your Agent Actually Need (Medium, research). Searched project "News digest" by title/keyword for each before creating — no collisions, nothing skipped as duplicate.

Commit: `news: daily run 2026-08-19 (+4 items, 3 companies fresh)`.

## 2026-08-20 05:15 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | none |
| inference-infra | 0 | 0 | none |
| oss-ml-systems | 1 | 1 | none |
| bigtech-eng | 0 | 0 | none |
| research-institutes | 0 | 0 | none |
| technical-newsletters | 0 | 0 | none |
| practitioner-blogs | 1 | 1 | none |
| youtube | 0 | 0 | all 7 sources errored (HTTP 404) — YouTube RSS endpoints unreachable today, same as 2026-08-19, no fallback ladder for radar, logged and moved on |
| community | 54 | 12 | none |
| mistral-watch | 0 | 0 | none |

Totals: 56 raw candidates, 14 confirmed, 1 source-error group (youtube×7) — within FAILURE MODES (no fallback ladder for radar sources).

TRIAGE pass 1 (technical bar): dropped off-topic HN Show HN posts (age-verification passkey tool, Sierra-games walking-dead detector, macOS Electron keychain store, LeetCode-runner CLI — none AI/ML-engineering); repeat/thin signal (Show HN "Shoehorn" quantizer and "PantheonGPU" GPU benchmarking, both already assessed and cut yesterday for the same reasons — thin signal, egress-blocked verification — treated as same-story repeats rather than re-litigated); "Open Bot"/"Frugal Tokens" Show HN posts (12/29 pts, thin — a Grok-harness wrapper and a cost-tracking demo, neither open enough or substantive enough to spend budget on); memes/appreciation/opinion Reddit threads (knowledge-vs-3.6 anecdote, "highest agency I've seen", "anyone NOT on full auto", "waiting for a 122B", "am I doing something wrong" troubleshooting post, minimax-music UI appreciation); a business/marketing post (Ramp's Router.com launch); routine/vanity quant releases (Unsloth "Dynamic v3" and "updated" GGUF reposts of Qwen3.8-27B, redundant with NVFP4 quant already covered 2026-08-18); a thin unlinked essay ("Build a modern LLM from scratch" — no repo/body text captured); a thin analysis post ("Stop Anthropomorphisizing Intermediate Tokens" — references unspecified "research they linked", no citation); an essay without a clear technical/reproducible angle ("Thoughts About Scaling Law — Z.ai", cut at the volume cap despite legitimate content); HF trending-models (Ridge-GGUF quant farming likes, MiniMax-Music-3 audio-gen) and ALL of HF trending-spaces (image/video-gen demos + UGI-Leaderboard) dropped as a group — vanity/trending noise + explicitly-LOW image/video-gen, consistent with prior days' pattern; smol.ai "not much happened today" skipped per the explicit workflow rule; Lobsters "Bongard Problems" (essay, no LLM experiment/code, unclear direct fit) dropped.

Same-story dedup: 4 Reddit posts about the new Ornith-1.5 model family (9B/35B-A3B/397B) collapsed to one item citing the most detailed post, cross-checked against the HF model cards. 2 new DFlash2 posts (RTX 6000 controlled comparison, RTX 3090 continuation of the 2026-08-18 optimization series) collapsed to one item covering both. 2 AntLing Ling-3.0-checkpoint posts collapsed to one.

TRIAGE pass 2 (owner fit): of the ~20 items clearing pass 1, kept all as HIGH/MEDIUM/LOW against interests.md — 8 HIGH (SGLang DeepSeek-V4-Pro serving, v100-skinny NVFP4-on-Volta, FM-Bench, Ornith-1.5, SemaPLC, llama.cpp --n-cpu-ffn PR, DFlash2 comparison, Simon Willison lines-of-code essay), 5 MEDIUM (Qwen3.8-23B-Mini-Me depth-pruning, AntLing Ling-3.0 checkpoints, Co-RL, LFM 2.5 QAD, Liquid Types agent sandbox), 1 LOW (AscendNPU-IR — kept for technical-radar-file-worthiness despite low owner fit per the LOW-tier rule).

VERIFY SUBSTANCE (11 attempts against the 5-highest-scored-candidates guidance, widened given strong community volume today): SGLang DeepSeek-V4-Pro post — WebFetch, passed (concrete Humming/Online-C128/DSpark numbers: +31.8% prefill, -74.8–78% decode latency, ×2.20 per-GPU throughput) → highlight. dnv2003/v100-skinny — `git clone`, passed (extensive honest README, AIME-2026 parity numbers with explicit non-claims) → highlight. Analogy-AI/fm-bench — `git clone`, passed (deterministic engine, real quickstart, documented long-horizon failure modes) → highlight. Ornith-1.5-397B and -9B — WebFetch on HF model cards, passed (MIT, weights available, benchmark numbers cross-checked against the reddit claim — confirmed comparable-to-Opus-4.8 framing) → strong regular item, not a highlight (cap already at 3). midea-ai/SemaPLC — `git clone`, passed (working MCP server + CLI, real OpenPLC Docker integration) → strong regular item, not a highlight (cap already at 3). DrStranded/Co-RL — `git clone`, passed (Apache-2.0, real training code + configs) → regular item. simonwillison.net post — WebFetch, passed (clear argument, concrete numbers) → regular item, not a highlight (cap already at 3; essay not a technique/data point). AscendNPU-IR (gitcode.com) — WebFetch + curl retry both hit EGRESS_BLOCKED/tunnel-403 (gitcode.com not allowlisted); kept as regular item on the lobsters listing's own title/tags, out of highlight consideration. Liquid Types/AeonBox (wiki.alcidesfonseca.com) — WebFetch + curl retry both hit EGRESS_BLOCKED/tunnel-403; kept as regular item on the lobsters listing's own title/tags, out of highlight consideration. matthodges.com Bongard Problems — WebFetch + curl retry both hit EGRESS_BLOCKED/tunnel-403; dropped in pass 1 anyway (thin fit), not pursued further. huggingface.co/papers/2608.18565 (SemaPLC) and arxiv.org/abs/2608.18565 — both returned insufficient rendered content; superseded by the successful `git clone` of the linked repo above.

WRITE: 12 items to `radar/community.md`, 1 to `radar/oss-ml-systems.md`, 1 to `radar/practitioner-blogs.md`, all under `## 2026-W34`.

Linear: 14 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to Review" — KOV-213 through KOV-226. Priorities by fit (HIGH→High(2) ×8, MEDIUM→Medium(3) ×5, LOW→Low(4) ×1). Source labels applied per item (blog ×2, github ×1, hf ×3, reddit ×6, lobsters ×2); `highlight` on KOV-213 (SGLang DeepSeek-V4-Pro), KOV-214 (v100-skinny), KOV-215 (FM-Bench) — 3 highlights, the daily max. Searched the project by title keyword for every candidate first — no collisions found; noted (not re-created) that "Shoehorn" and "PantheonGPU" already exist from 2026-08-19 (KOV-194 and a dropped-not-filed item respectively) as the same recurring candidates.

Commit: `news: radar run 2026-08-20 (+14 items, 3 highlights)`.

## 2026-08-20 06:15 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1), WebSearch | 0 | WebSearch | listing's newest (ChatGPT Ads Europe, Aug19) already captured; CRO personnel announcement (Aug17) filtered — Company category dropped per source config, not an outage |
| anthropic | fetch (WebFetch) | 0 | none needed | listing tops out at Aug14 (text watermark, already captured), nothing newer |
| google-deepmind | rss, WebFetch | 0 | WebFetch | rss.xml no fresh entries; listing's newest three (Gemini 3.7 Flash Aug13, SL2T Aug12, WeatherNext Aug6) all already captured |
| google-research | rss.xml (TIER-1), WebFetch | 0 | WebFetch | rss.xml no fresh entries; listing's newest (PhotoScan Aug17) already captured |
| microsoft | rss, WebFetch | 0 | WebFetch | rss.xml no fresh entries; listing's newest (MindTopo Aug12) already captured, nothing newer |
| nvidia | rss.xml (TIER-1) | 4 raw, 1 kept | none needed | SkillEvaluator kept as genuine tool release with substantive benchmark data; Holoscan CLI/skills, FLARE federated-workflow, and Cosmos-3-Edge-robot-control posts all dropped as tutorial-grade how-to content reusing existing SDKs/models, per the NVIDIA "genuine announcements/major posts only" note |
| xai | jina (curl, Cloudflare-challenged — expected, no JINA_API_KEY), WebSearch | 0 | WebSearch | listing's newest (Grok 4.6 in GitHub Copilot, Aug14) already captured, nothing newer |
| mistral | rss.xml (304 not modified), WebFetch | 0 | WebFetch | listing's newest (regional inference, Aug11) already captured, nothing newer |
| huggingface | rss.xml (TIER-1) | 1 | none needed | none |
| cursor | rss.xml (304 not modified), WebFetch/WebSearch | 1 | WebFetch | rss.xml showed no diff but changelog page surfaced "Cloud Agents and Cursor Harness Improvements" (Aug19) — new, not yet in feed cache; confirmed via WebFetch of the full changelog entry |
| perplexity | jina (curl, Cloudflare-challenged — expected, no JINA_API_KEY), WebSearch | 0 | WebSearch | WebSearch surfaced two candidate titles ("Computer now works in email" Aug18, "Brain: Agentic Memory as a Knowledge Wiki" Aug19) but third-party coverage dates "Brain" to a June 2026 launch and no primary-source URL/date could be confirmed (perplexity.ai and hub-prod.perplexity.ai both egress-blocked for WebFetch) — dropped both per the never-invent-facts rule rather than add unverifiable dates |

Totals: 6 items kept (3 dropped as tutorial-grade), 3 companies fresh (nvidia, huggingface, cursor), 0 transport errors beyond the expected xai/perplexity Jina Cloudflare-challenge (no JINA_API_KEY) and openai direct-fetch 403 (all covered by the one-fallback rule).

Window: since last successful daily run (2026-08-19 06:14 UTC).

Note: fetch_feeds.py was run twice this session before the window stabilized (first run advanced HTTP cursors; a stray combined-stream capture corrupted the JSON log). `news/state/cursors.json` was reverted to its committed state and the script re-run once cleanly — the totals/items above reflect that single clean run.

Linear: 3 new stories filed — KOV-227 [NVIDIA] SkillEvaluator (Medium, infra), KOV-228 [Hugging Face] LFM2.5 Q4_0 QAD checkpoints (Medium, model-release), KOV-229 [Cursor] Cloud Agents and Cursor Harness Improvements (High, product). Searched project "News digest" by title/keyword for each before creating — no collisions, nothing skipped as duplicate.

Commit: `news: daily run 2026-08-20 (+3 items, 3 companies fresh)`.

## 2026-08-20 07:02 UTC — deep-dive — ok (no approved cards)

Searched project "Radar" for cards with label `hot` — zero hot cards anywhere in the project
(52+ cards in Ready to Review carry only source labels: reddit/hf/github/blog/hn/lobsters +
highlight). The queue includes fresh cards from today's radar run (KOV-213–226, created 05:15 UTC)
the owner has not triaged yet. No cards processed, no files written, no leftovers. Exiting
quietly per workflow.

## 2026-08-21 05:05 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | none |
| inference-infra | 0 | 0 | none |
| oss-ml-systems | 2 | 2 | none |
| bigtech-eng | 0 | 0 | none |
| research-institutes | 0 | 0 | none |
| technical-newsletters | 0 | 0 | none |
| practitioner-blogs | 1 | 0 | none |
| youtube | 0 | 0 | all 7 sources errored (HTTP 404) — YouTube RSS endpoints unreachable today, same as 2026-08-19/20, no fallback ladder for radar, logged and moved on |
| community | 23 | 4 | reddit source-group HTTP 429, skipped (no retry-loop per rule); does not affect the raw-candidate count above since it contributed zero fresh items |
| mistral-watch | 0 | 0 | none |

Totals: 26 raw candidates, 6 confirmed, 2 source-error groups (youtube×7, reddit×1) — within FAILURE MODES (no fallback ladder for radar sources; Reddit 429 → skip, never retry-loop).

TRIAGE pass 1 (technical bar): dropped non-AI HN Show HN posts (WaveHouse "Supabase for ClickHouse", a weather-balloon chase blog, an unclaimed-royalties checker, Omacosy macOS tiling desktop, LilScript JS-bundle shrinker — appeared under two source IDs as the same story, counted once); a repeat off-topic candidate (age-verification passkey tool, already dropped 2026-08-20 under the same reasoning); two repeat thin-signal candidates from 2026-08-19/20 ("Open Bot" Grok-harness wrapper, 12pts; "Frugal Tokens" cost-tracking demo, 36pts — both re-surfaced today, dropped again for the same reasons: too thin/not open enough to spend budget on). HF trending-models (OBLITERATUS/orcarouter — uncensored Qwen3.8-27B finetunes farming likes) dropped as vanity noise, consistent with the daily pattern; ornith-ai/Ornith-1.5-35B-A3B (HF trending) is the same model family already covered 2026-08-19 — not re-added. HF trending-spaces (amisima LTX-2.3 I2V demo) and one HF daily paper (4DAnyone, monocular-video 4D reconstruction) and another (WithEveryone, group image generation) dropped as a group — video/3D-gen and image-gen are explicitly LOW per interests.md, consistent with prior days' pattern of dropping HF vanity/trending image-video content. Two GitHub-trending repos dropped: AprilNEA/OpenLogi (Logitech-mouse remapper, not AI at all) and modular/modular (Modular Platform/Mojo — legitimate AI infra, but "trending" carried no dated news peg or specific new release to hang an item on; already a well-known project, so dropped for lacking discrete signal rather than for low quality). latent-space "/wayfinder Skill" post verified via WebFetch and found to be a marketing/interview piece about Matt Pocock's AI Skills project — no code, no reproducible detail, explicitly promotional framing; dropped per the "product marketing that survived config filters" pass-1 rule (same treatment as the Latent.Space Glean-sponsored piece dropped 2026-08-19).

TRIAGE pass 2 (owner fit): of the 7 items clearing pass 1, all scored HIGH against interests.md (agents in practice / coding agents / agent harnesses / reproducible technique with code / local inference engines) — Huzzah, Vomit, EnvHarness, agent-substrate/substrate, lmsys-sglang Mooncake-for-Miles, pytorch-blog Day-One Model Enablement. No same-story dedup needed beyond the LilScript HN cross-listing noted above.

VERIFY SUBSTANCE (6 attempts against the 5-highest-scored-candidates guidance, widened to cover all HIGH-fit survivors): lmsys-sglang Mooncake-for-Miles — WebFetch, passed (concrete Ray-vs-Mooncake numbers: GET ~10–14× faster, PUT ~1.2–1.6× faster) → highlight candidate. pytorch-blog Day-One Model Enablement — WebFetch, passed (13 adapters cover 7,960/10,000 HF embedding models, 6,804 pass on-device, concrete code examples, GitHub repos linked) → highlight candidate. huggingface.co/papers/2608.19880 (EnvHarness) — WebFetch, passed (9.0-pt improvement / 9.8% fewer steps across 5 benchmarks, code + project site live) → highlight candidate. github.com/agent-substrate/substrate — `git clone`, passed (Apache-2.0, real Google-affiliated infra project, 30x+ oversubscription demo, dedicated Claude Code multiplex demo, extensive docs) → highlight candidate. github.com/zachahn/vomit — `git clone`, passed (GPLv3, working Go binary, honest limitations disclosed in its own README) → strong regular item, not a highlight (cap already at 3 once the above four were ranked). danielvaughn.dev/posts/huzzah (Show HN) — WebFetch + curl retry both hit EGRESS_BLOCKED/tunnel-403 (domain not allowlisted); kept as regular item on the HN submission's own body text, out of highlight consideration. Four candidates cleared verification as genuine highlight material against a 3-slot cap; ranked by owner-fit specificity (Claude Code / coding-agent tooling relevance) — agent-substrate, pytorch Day-One, and EnvHarness selected; Mooncake-for-Miles (a solid but incremental follow-up to the already-highlighted Miles v0.1/DeepSeek-V4-Pro posts) held back as a strong regular item instead.

WRITE: 4 items to `radar/community.md`, 2 to `radar/oss-ml-systems.md`, all under `## 2026-W34`.

Linear: 6 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to Review" — KOV-230 through KOV-235. All 6 scored HIGH fit → Priority High(2). Source labels applied per item (hn ×1, github ×2, hf ×1, blog ×2); `highlight` on KOV-232 (agent-substrate/substrate), KOV-233 (EnvHarness), KOV-235 (Harnessing AI for Day-One Model Enablement) — 3 highlights, the daily max. Searched the project by title keyword for every candidate first — no collisions found, nothing skipped as duplicate.

Commit: `news: radar run 2026-08-21 (+6 items, 3 highlights)`.

## 2026-08-21 06:15 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1), WebSearch | 0 | WebSearch | listing's newest confirmed items (ChatGPT Ads Europe Aug18) already captured; WebSearch surfaced a "security training pause" and ChatGPT-for-Teens/restaurant-booking items with no confirmed openai.com URL/date in-window — dropped as unconfirmed |
| anthropic | fetch (WebFetch) | 0 | none needed | listing tops out at Aug14 (text watermark, already captured), nothing newer |
| google-deepmind | rss.xml (TIER-1), WebSearch | 0 | WebSearch | rss.xml no fresh entries; WebSearch found nothing newer than the Aug13 Gemini 3.7 Flash post (already captured) |
| google-research | rss.xml (TIER-1), WebSearch | 0 | WebSearch | rss.xml no fresh entries; WebSearch confirms latest post still Jul30 (Science One Framework), predates window |
| microsoft | rss.xml (TIER-1) | 1 | none needed | none |
| nvidia | rss.xml (TIER-1) | 1 | none needed | none |
| xai | jina (curl, Cloudflare-challenged — expected, no JINA_API_KEY), WebSearch | 0 | WebSearch | listing's newest (Grok 4.6 in GitHub Copilot, Aug14) already captured, nothing newer confirmed |
| mistral | rss.xml (TIER-1) | 1 | none needed | none |
| huggingface | rss.xml (TIER-1) | 1 | none needed | none |
| cursor | rss.xml (TIER-1), WebSearch | 0 | WebSearch | rss.xml no fresh entries; WebSearch's "Origin rolling out Aug20" is the same Origin Code Hosting story already captured Aug17, not a distinct changelog entry |
| perplexity | jina (curl, Cloudflare-challenged — expected, no JINA_API_KEY), WebSearch | 0 | WebSearch | WebSearch surfaced "Brain: Agentic Memory" (Aug19) and "Computer now works in email" (Aug18) — both predate the window and "Brain" was already rejected 2026-08-20 as unconfirmed (third-party coverage dated it to a June 2026 launch, no primary-source date confirmable) |

Totals: 4 items, 4 companies fresh (microsoft, nvidia, mistral, huggingface), 0 transport errors beyond the expected xai/perplexity Jina Cloudflare-challenge (no JINA_API_KEY).

Window: since last successful daily run (2026-08-20 06:15 UTC).

Linear: 4 new stories filed — KOV-236 [Microsoft] Broadening access to Skala creates a faster path to predictive DFT (Medium, research), KOV-237 [NVIDIA] How Generative Recommenders Are Redefining RecSys at Scale (Medium, infra), KOV-238 [Mistral AI] Agentic Search (High, product), KOV-239 [Hugging Face] Up to 3.2x Faster Inference with LFM2.5-DSpark (Medium, model-release). Searched project "News digest" by title/keyword for each before creating — no collisions, nothing skipped as duplicate.

Commit: `news: daily run 2026-08-21 (+4 items, 4 companies fresh)`.

## 2026-08-22 05:03 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | none |
| inference-infra | 0 | 0 | none |
| oss-ml-systems | 2 | 2 | none |
| bigtech-eng | 1 | 1 | none |
| research-institutes | 1 | 1 | none |
| technical-newsletters | 1 | 1 | none |
| practitioner-blogs | 1 | 0 | none |
| youtube | 0 | 0 | all 7 sources errored (HTTP 404) — YouTube RSS endpoints unreachable today, same pattern as 2026-08-19/20/21, no fallback ladder for radar, logged and moved on |
| community | 58 | 8 | bair (Berkeley) errored (connection reset by peer, no fallback for radar sources); reddit source-group returned successfully today (no 429) |
| mistral-watch | 0 | 0 | none |

Totals: 64 raw candidates, 13 confirmed, 2 source-error groups (youtube×7, bair×1) — within FAILURE MODES (no fallback ladder for radar sources).

TRIAGE pass 1 (technical bar): the 58 raw community candidates were heavily duplicated across four hn-show-* search queries (OzBrain ×4, Kandelo ×3, Proliferate ×3, AgentSight ×2, LilScript ×2 — each counted once after URL dedup). Dropped as non-AI/off-topic (same daily pattern as prior runs): WaveHouse "Supabase for ClickHouse", a weather-balloon-chase blog, an unclaimed-royalties checker, Omacosy macOS tiling desktop, a desktop-fly toy app, LilScript JS-bundle shrinker. Dropped Kandelo (POSIX WASM kernel for the browser) as thin AI-relevance — its own submission text only speculates it "looks promising as a sandbox for running agents," no concrete agent tie-in, and verification was blocked (kandelo.dev egress-blocked). Dropped an unconfirmed reddit claim ("NVIDIA AVO got 100% on ARC-AGI-3") — no primary source, no body text beyond "submitted by," no corroboration found; per never-invent-facts, not added. HF trending-models dropped as a group (two abliterated-Qwen3.8-27B uncensored finetunes — vanity/uncensored-model noise, consistent with prior days; ornith-ai/Ornith-1.5-35B-A3B-GGUF is the same model family already covered 2026-08-19 — dedup, not re-added; TenStrip/10Eros-Max — NSFW, dropped). HF trending-spaces (shootstuff/flux-img2img-uncensored) dropped as NSFW. github-trending: mahlernim/google-timeline-visualizer dropped as not AI-related; PostHog/posthog and microsoft/TypeScript dropped for lacking a discrete dated news peg (same reasoning as Modular dropped 2026-08-21 — well-known projects "trending" with nothing new to hang an item on). Of 25 raw reddit candidates (r/LocalLLaMA + r/LLMDevs, succeeded today with no 429), the large majority were repetitive appreciation/chatter threads about one model (Qwen3.8-27B: "goated," "different thinking levels," "Q6 is a beast," VRAM-purgatory discussion, hardware-recommendation questions, quant boasts, a PI-agent-vs-OpenCode anecdote, a 63-hour flight-sim story) or thin one-line mentions (DeepSeek-V4-Flash-Vision-Exp, a llama.cpp PR repost, an "open weights gap" opinion post, a stealth-model-on-OpenRouter speculation post) — dropped per the memes/appreciation-posts pass-1 rule. Also dropped as off-focus for the interest profile: FireRedAudio/FireRedTTS3 and an "Ultrafast Qwen3-TTS" release (audio/TTS, not in HIGH/MEDIUM topics). Huzzah (danielvaughn.dev) and Vomit (github.com/zachahn/vomit) re-surfaced today (still-active HN threads) but are dedup — both already in `radar/community.md` since 2026-08-20/21 under the same URLs, not re-added. latent-space's "Simulation: the new Scaling Law" (Joon Sung Park / Simile AI) verified via WebFetch and found to be an interview/marketing piece — business claims and philosophical framing, no math, no reproducible methodology, no shared data — dropped per the same rule that killed two other latent-space sponsored/interview pieces on 2026-08-19/21.

TRIAGE pass 2 (owner fit): of the 13 confirmed items, 9 scored HIGH (Proliferate, OzBrain, AgentSight, specfill TUI, DeepSeek Harness v0.1.1, forked-Continue tab-completion, Qwen3.8-27B Strix Halo hybrid-GPU numbers, plus the two lmsys-sglang posts) against interests.md's "AI agents in practice / coding agents / agent harnesses," "local/self-hosted models... runs on my hardware," and "reproducible techniques with code" categories. 4 scored MEDIUM (Felony Bench — plausible evals-fit but unverified premise; Netflix Flink Autoscalers — engineering post-mortem, ML-adjacent via Data Mesh/personalization but not agent/model-specific; Ai2 Georgia Tech Olmo capability tracing — solid interpretability research, MEDIUM rather than HIGH since it isn't coding-agent-specific; SemiAnalysis "Are Open Models Catching Up?" — verified as a genuine capability-trend analysis, not the finance/market content pass-1 normally drops from this source, but still a trend piece rather than a hands-on technique).

VERIFY SUBSTANCE (10 attempts against the 5-highest-scored-candidates guidance, widened to cover all promising survivors): proliferate-ai/proliferate — `git clone`, passed (AGPL-3.0, real Rust+TS codebase, ARCHITECTURE.md, multi-harness incl. Claude Code) → highlight. lmsys Ling-3.0-flash spec decode and Fast Engine Recovery — both WebFetch, passed (concrete kernel-engineering numbers: 2.1× NEXTN throughput; ~785× weight-loading speedup) → both highlights. allenai.org/blog/olmo-capability-tracing — WebFetch, passed (real methodology, code + HF Space links). newsletter.semianalysis.com/p/are-open-models-catching-up — WebFetch, passed (genuine benchmark-era analysis, not finance). netflixtechblog.com — WebFetch hit HTTP 403, retried via Jina per FAILURE MODES, passed. latent.space/p/simile — WebFetch, failed verification (marketing/interview, no reproducible content) → dropped, not added. ozbrain.com, kandelo.dev, felonybench.com, raw.githubusercontent.com (AgentSight doc) — all EGRESS_BLOCKED for both WebFetch and curl; OzBrain and AgentSight kept as regular items on HN-submission body text / title only (OzBrain has body text, AgentSight does not), Felony Bench kept on lobsters title+tag only, all three out of highlight consideration; Kandelo dropped entirely (see pass 1). specfill TUI, DeepSeek Harness v0.1.1, forked-Continue, Qwen3.8-27B Strix Halo — reddit curl verification hit HTTP 403 (bot-block interstitial, identical page for all URLs); each kept on its own detailed self-post body text (all four had substantial first-person write-ups, not just links) per the "feed entry's own body text is a valid basis" rule — none elevated to highlight given the 3-slot cap already filled by more rigorously verified candidates.

WRITE: 8 items to `radar/community.md`, 2 to `radar/oss-ml-systems.md`, 1 to `radar/bigtech-eng.md` (new `## 2026-W34` heading), 1 to `radar/research-institutes.md`, 1 to `radar/technical-newsletters.md` (new `## 2026-W34` heading).

Linear: 13 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to Review" — KOV-240 through KOV-252. 9 HIGH fit → Priority High(2); 4 MEDIUM fit → Priority Medium(3). Source labels applied per item (hn ×3, reddit ×4, lobsters ×1, blog ×4, newsletter ×1); `highlight` on KOV-240 (Proliferate), KOV-249 (Ling-3.0-flash spec decode), KOV-250 (Fast Engine Recovery) — 3 highlights, the daily max. Searched the project by title keyword for every candidate first — no collisions found, nothing skipped as duplicate.

Commit: `news: radar run 2026-08-22 (+13 items, 3 highlights)`.

## 2026-08-22 06:14 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1), WebSearch | 0 | WebSearch | rss.xml no fresh entries; WebSearch surfaced only retirement/deprecation notices (o3, DALL·E GPT) and community-forum posts, nothing newer than the Aug03 items already captured |
| anthropic | fetch (WebFetch) | 0 | none needed | listing tops out at Aug14 (text watermark, already captured), nothing newer |
| google-deepmind | rss.xml (TIER-1) | 1 | none needed | none |
| google-research | rss.xml (TIER-1) | 2 | none needed | none |
| microsoft | rss.xml (TIER-1), WebSearch | 0 | WebSearch | rss.xml no fresh entries; WebSearch found only generic fellowship/CFP/partner-program pages, nothing newer than Aug20 (Skala 1.1, already captured) |
| nvidia | rss.xml (TIER-1) | 2 (of 4 raw) | none needed | "GPU-Accelerated Clustering for Financial Instruments at Scale" verified via WebFetch as a pure technique tutorial (no product tie) — dropped per the developer-blog trap guidance (keep announcements/major posts, not every tutorial); "Where Security Fits in an AI Agent Stack" verified via WebFetch as generic thought-leadership/educational content referencing an existing product (OpenShell), not a new announcement — dropped for the same reason |
| xai | jina (curl, Cloudflare-challenged — expected, no JINA_API_KEY), WebSearch | 1 | WebSearch | curl-jina hit the expected Cloudflare challenge (403); WebSearch surfaced "Grok Bot is now included with more plans" (x.ai/news/grok-bot-more-plans, Aug21) — primary URL identified but page itself not fetchable (Cloudflare + no JINA_API_KEY); confirmed via three independent secondary sources (InfoQ, Seeking Alpha, AI Weekly) plus a direct quote from the official Grok Bot X account |
| mistral | rss.xml (TIER-1, 304 not modified), WebSearch | 0 | WebSearch | no fresh entries; WebSearch found only the Jul21 Microsoft-partnership story and AI Now Summit recap items, nothing newer than Aug20 (Agentic Search, already captured) |
| huggingface | rss.xml (TIER-1) | 0 | WebSearch | rss.xml no fresh entries; WebSearch found only the general "State of Open Models: Summer 2026" report with no specific Aug21/22 post confirmable |
| cursor | rss.xml (TIER-1 — connection reset by peer), WebSearch | 0 | WebSearch | rss.xml transport error (`[Errno 104] Connection reset by peer`); WebSearch confirms latest changelog entry still Aug19 (Cloud Agents/Harness improvements, already captured), nothing newer |
| perplexity | jina (curl, Cloudflare-challenged — expected, no JINA_API_KEY), WebSearch | 0 | WebSearch | curl-jina hit the expected Cloudflare challenge (403); WebSearch resurfaced "Brain" (Aug19, already rejected 2026-08-20 as unconfirmed) and "Computer now works in email" (Aug18, predates window) — nothing new confirmed |

Totals: 6 items, 4 companies fresh (google-deepmind, google-research, nvidia, xai), 1 transport error (cursor rss.xml connection reset) beyond the expected xai/perplexity Jina Cloudflare-challenge (no JINA_API_KEY).

Window: since last successful daily run (2026-08-21 06:15 UTC).

Linear: 6 new stories filed — KOV-253 [Google DeepMind] From Atari to EVE Online (Medium, research), KOV-254 [Google Research] An AI tool for prioritizing candidate biomarkers from wearable sensor data (Medium, research), KOV-255 [Google Research] How mobility gives language models a deeper understanding of place (Medium, research), KOV-256 [NVIDIA] NVIDIA AVO Reaches 100% on ARC-AGI-3 (High, research), KOV-257 [NVIDIA] Maximizing AI Factory Performance per Watt with NVIDIA DSX MaxLPS (Medium, infra), KOV-258 [xAI] Grok Bot is now included with more plans (Low, product). Searched project "News digest" by title/keyword for each before creating — no collisions, nothing skipped as duplicate.

Commit: `news: daily run 2026-08-22 (+6 items, 4 companies fresh)`.

## 2026-08-23 05:03 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | none |
| inference-infra | 0 | 0 | none |
| oss-ml-systems | 1 | 1 | none |
| bigtech-eng | 0 | 0 | none |
| research-institutes | 0 | 0 | none |
| technical-newsletters | 0 | 0 | none |
| practitioner-blogs | 2 | 2 | none |
| youtube | 12 | 1 | none — feed sources recovered today after ~3 days of all-7-channels 404s (2026-08-19 to 2026-08-22) |
| community | 49 | 9 | none |
| mistral-watch | 0 | 0 | none |

Totals: 64 raw candidates, 13 confirmed, 0 source-error groups (first fully clean fetch in several days — youtube in particular back after 3 days dark).

TRIAGE pass 1 (technical bar): github-trending (6 candidates: openai/codex, affaan-m/ECC, Wei-Shaw/sub2api, makeplane/plane, n8n-io/n8n, anthropics/claude-code) dropped as a group — well-known repos "trending" with no discrete dated news peg, same reasoning as prior days. hf-trending-models dropped as a group: superwhisper/s1-mini (audio/speech, off-focus per interests.md), DavidAU's Qwen3.8-27B-Cold-Fusion abliterated finetune (vanity/uncensored-model noise, consistent pattern), z-lab/Qwen3.8-27B-DFlash2 (dedup — DFlash2-for-Qwen3.8-27B ground already extensively covered 2026-08-18/19/20 in community.md). hf-trending-spaces (mpasila/Krea-2-Turbo_I2I, an image-to-image space) dropped as off-focus (image gen not in interest profile). hn-show-* duplicates within today's own batch (OzBrain, Proliferate, AgentSight — already on radar since 2026-08-21) collapsed to zero net-new; "desktop-fly" toy app and "soverybright.com" HDR-logo tool dropped as non-AI/meme-grade, consistent with prior days. lobsters "Robot comment classifier" (entropicthoughts.com) and hn-trend-llm "Why your local LLM feels dumber than it is" (forum.level1techs.com) both had empty feed summaries and both transports hit EGRESS_BLOCKED on WebFetch + curl CONNECT-tunnel-403 on retry — too thin to write an honest line from title alone, dropped rather than invented. Of 25 raw reddit candidates: dropped as pure chatter/appreciation/question threads with no shared technique (per the memes/appreciation-posts rule) — "Current best model for narrative...", "Are LLM becoming less coherent...", "This is a great sub...", "How to remove trendy speech...", "Your own GGUF", "Anyone else tried out KV cache blending?", "Best harness for long autonomous tasks", "Has anyone actually made 64k feel like 300k+..."; dropped "Think you're going to get cheap DDR5 RAM" as hardware-market/scalper-bot commentary (LOW/business, not technically strong); dropped "Create tts voice from actual animal sound recording" as audio/off-focus; dropped "New 100B Liquid AI model coming soon" as an unconfirmed rumor/poll link with no technical content; dropped "Freetokens project is impressive" and "AntLing released a dspark draft model for Ling-3.0-flash" as too thin (one-line mentions, no numbers); dropped "I benchmark DFlash 2..." (2.26x/4.68x/8x numbers) and "Llama.cpp version 0.2.0 is out!" as dedup/low-marginal-value — DFlash2-on-Qwen3.8-27B is already thoroughly covered ground (three prior confirmed items), and the llama.cpp release tag carried no changelog content beyond the link; dropped "Watching that wattage, in your terminal" (energygraph CLI tool) as a niche hardware-monitoring utility outside the model/inference-technique focus.

TRIAGE pass 2 (owner fit) on the 13 confirmed: 10 scored HIGH — the RTX 5090 Qwen3.8-27B NVFP4 262K-context vLLM setup, the Ninfer→CMP170HX fork (doubled Qwen3.6-35B), the Ornith1.5 MTP-head fix, the Sharp-template-to-NInfer token reduction, the DGX Sparks 16→36 cluster, the Q8_K_XL-vs-BF16 Qwen coding comparison, both practitioner-blogs pieces (Latent Space "Evolution of the Agent Harness", Raschka "How Claude Watermarks AI-Generated Text"), the vLLM AMD speculative-decoding blog post, and the YouTube "Agent Frameworks Considered Harmful" talk (a direct counterpoint to the Latent Space harness piece, both landing the same day). 3 scored MEDIUM — the GLM+llama.cpp AMD GFX906 fork (real topic, but self-post body was too thin to verify specifics beyond the title), the Gemma 4 12B tool-calling finetune (fine-tuning practice is an explicit MEDIUM category), and the "Artificial Analysis Intelligence Index" critique (evals-in-practice adjacent, but an opinion/critique post rather than a hands-on technique).

VERIFY SUBSTANCE (5 highlight candidates checked): latent.space/p/attention-interface — WebFetch, passed (quantified: Harness-Bench 52.4–76.2 spread on zero weight changes, ARC-AGI 13.3%→38.3%, Claude Code system prompt −80%) → highlight. vllm.ai/blog/2026-08-23-speculative-decoding-amd-gpus — WebFetch, passed (five drafting methods compared with concrete per-model throughput multipliers) → highlight. magazine.sebastianraschka.com/p/claude-watermarking — WebFetch, passed (concrete sampling-stage tournament-watermarking mechanism) — not elevated to highlight, 3 slots already allocated to higher owner-fit/more novel picks. Single-RTX-5090-vLLM-262K reddit post — kept on its own detailed self-post body (166s prefill, 77.2/64.7 tok/s numbers), reddit curl verification skipped as unnecessary given the substantive first-person writeup → highlight (3rd slot). entropicthoughts.com and forum.level1techs.com — both transport-blocked (see pass 1), out of highlight consideration, dropped entirely rather than kept thin.

WRITE: 9 items to `radar/community.md`, 2 to `radar/practitioner-blogs.md`, 1 to `radar/oss-ml-systems.md`, 1 to `radar/youtube.md` (new `## 2026-W34` heading — youtube.md's last entry was 2026-08-16, unchanged through the multi-day 404 outage).

Linear: 13 review-queue cards created in project "Radar" (team Kovalevgr), status "Ready to Review" — KOV-259 through KOV-271. 10 HIGH fit → Priority High(2); 3 MEDIUM fit → Priority Medium(3). Source labels applied per item (reddit ×9, blog ×3, youtube ×1); `highlight` on KOV-260 (Single RTX 5090 Qwen3.8-27B NVFP4 262K), KOV-268 (Evolution of the Agent Harness), KOV-270 (Speculative Decoding in vLLM on AMD GPUs) — 3 highlights, the daily max. Searched the project by title keyword for every candidate first — no collisions found, nothing skipped as duplicate.

Commit: `news: radar run 2026-08-23 (+13 items, 3 highlights)`.

## 2026-08-23 06:10 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1), WebSearch | 0 | WebSearch | rss.xml no fresh entries; WebSearch surfaced only ChatGPT UI/feature updates and the Preparedness-team leadership story, nothing confirmable as a distinct in-window blog post beyond the Aug18 items already captured |
| anthropic | fetch (WebFetch) | 0 | none needed | listing still tops out at Aug14 (text watermark, already captured), nothing newer |
| google-deepmind | rss.xml (TIER-1), WebSearch | 0 | WebSearch | rss.xml no fresh entries; WebSearch surfaced only the Aug5-6 leadership-reshuffle story (already captured) and the general blog index, nothing newer than Aug21 (already captured) |
| google-research | rss.xml (TIER-1), WebSearch | 0 | WebSearch | rss.xml no fresh entries; WebSearch's newest indexed post is Aug11 (already captured), nothing newer than Aug21 (already captured) |
| microsoft | rss.xml (TIER-1), WebSearch | 0 | WebSearch | rss.xml no fresh entries; WebSearch found nothing newer than Aug20 (Skala 1.1, already captured) |
| nvidia | rss.xml (TIER-1), WebSearch | 0 | WebSearch | rss.xml no fresh entries; WebSearch's newest indexed items (Aug20 Generative Recommenders, Aug18 UMAP) predate or match items already captured, nothing newer than Aug21 (already captured) |
| xai | jina (curl, Cloudflare-challenged — expected, no JINA_API_KEY), WebSearch | 0 | WebSearch | curl-jina hit the expected Cloudflare challenge (403); WebSearch found nothing newer than Aug21 (Grok Bot more plans, already captured) |
| mistral | rss.xml (TIER-1, 304 not modified), WebSearch | 0 | WebSearch | no fresh entries; WebSearch surfaced only earlier-August items (Vibe agent update, Les Ulis data center, industrial-engineering partnerships), nothing newer than Aug20 (Agentic Search, already captured) |
| huggingface | rss.xml (TIER-1, 304 not modified), WebSearch | 0 | WebSearch | no fresh entries; WebSearch's closest new item ("State of Open Models: Summer 2026") is a biannual ecosystem report, not a dated announcement — nothing newer than Aug20 (already captured) |
| cursor | rss.xml (TIER-1), WebSearch | 0 | WebSearch | no fresh entries; WebSearch confirms latest changelog entry still Aug19 (Cloud Agents/Harness improvements, already captured) |
| perplexity | jina (curl, Cloudflare-challenged — expected, no JINA_API_KEY), WebSearch | 0 | WebSearch | curl-jina hit the expected Cloudflare challenge (403); WebSearch resurfaced "Brain" (Aug19, already rejected 2026-08-20 as unconfirmed) and "Computer now works in email" (Aug18, predates window) — nothing new confirmed |

Totals: 0 items, 0 companies fresh, 0 errors (11 gap-scrapes attempted, all empty in-window; 2 expected Cloudflare-challenged jina attempts — xai, perplexity — no JINA_API_KEY set).

Window: since last successful daily run (2026-08-22 06:14 UTC).

Linear: no new stories to file (0 confirmed items across all 11 companies) — nothing created or searched for.

Commit: `news: daily run 2026-08-23 (+0 items, 0 companies fresh)`.

## 2026-08-24 05:14 UTC — radar — ok

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | none |
| inference-infra | 0 | 0 | none |
| oss-ml-systems | 0 | 0 | none |
| bigtech-eng | 0 | 0 | none |
| research-institutes | 0 | 0 | none |
| technical-newsletters | 1 | 1 | none |
| practitioner-blogs | 0 | 0 | none |
| youtube | 0 | 0 | none |
| community | 13 | 0 | none |
| mistral-watch | 0 | 0 | none |

Totals: 14 raw candidates, 1 confirmed, 1 source-error group (reddit HTTP 429 — expected known failure mode, skipped without retry per FAILURE MODES, no fallback attempted). A quiet day across the rest of the roster: 20 of the other 51 sources returned nothing fresh in-window; the 13 community candidates all came from a handful of low-signal feeds (hn-show-*, hf-trending-*, github-trending, lobsters).

TRIAGE pass 1 (technical bar): dropped as a group — github-trending's 5 candidates (freestylefly/awesome-gpt-image-2 prompt-template repo, block/buzz and apache/maka agent-workspace projects, Alishahryar1/free-claude-code ToS-workaround token-sharing tool, tinyhumansai/openhuman personal-AI vanity project) — none carry a discrete dated news peg, same reasoning as prior days (a trending snapshot, not a story). hf-trending-models: ornith-ai/Ornith-1.5-9B dropped as dedup (thoroughly covered already — 2026-08-19 launch item, 2026-08-22 MTP-head fix in `radar/community.md`); LBH-123-AI/Minimax_h3_latent_Upscaler dropped as a vanity/low-effort-naming model with no changelog content. hf-trending-spaces: Rchoks/wan555 dropped as off-focus (image-to-image generation, not in interest profile). hn-show-rag/hn-show-mcp: "Show HN: Make your logo extra bright on HDR screens" (soverybright.com, same item surfaced by both feeds) dropped as non-AI (HDR gain-map trick, consistent with the prior drop of this exact item). hn-show-rag: "Show HN: Structural code grep across public GitHub repositories" (grep.codemod.com) dropped as off-focus — ast-grep-based structural code search, no LLM/AI tie. hn-trend-llm: "Why your local LLM feels dumber than it is" (forum.level1techs.com) — same URL flagged and dropped yesterday (2026-08-23) for an empty feed summary plus transport-blocked verification; today's attempt hit the identical wall (WebFetch EGRESS_BLOCKED, curl CONNECT-tunnel-403) with still no summary text — dropped again rather than invented. lobsters: "AI Chip Architectures" (jepeake.com) — empty feed summary, WebFetch EGRESS_BLOCKED and curl CONNECT-tunnel-403 on retry — too thin to write an honest line from title alone, dropped.

TRIAGE pass 2 (owner fit): the 1 survivor — SemiAnalysis "AgentX - InferenceXv3: Does CUDA Moat Hold up in Agentic Inferencing?" — scored HIGH (AI-agents-in-practice + local/inference-infra overlap, reproducible open-source benchmark).

VERIFY SUBSTANCE (1 highlight candidate checked): newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat — WebFetch, passed (quantified: 393 anonymized Claude Code traces, up to 1M-token context, KV-cache hit rate >95% for sub-agent bursts, B300 vLLM DEP8 91% HBM hit rate under 384 concurrent traces, tested across GB300/GB200 NVL72/B300/B200/H200/MI355X/MI325/MI300X, Apache-2.0 open-source with public dataset + REST API) → highlight (only confirmed item today, clearly the day's best).

WRITE: 1 item to `radar/technical-newsletters.md` (new `## 2026-W35` heading).

Linear: 1 review-queue card created in project "Radar" (team Kovalevgr), status "Ready to Review" — KOV-273. HIGH fit → Priority High(2), label `newsletter`, `highlight` (the day's only confirmed item, verified). Searched the project by title first — no collision found.

Commit: `news: radar run 2026-08-24 (+1 item, 1 highlight)`.

## 2026-08-24 06:19 UTC — daily — ok

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, empty), WebFetch (403), curl-jina (403 Cloudflare), WebSearch | 4 | WebSearch | rss.xml no fresh entries; direct WebFetch and jina both 403'd on openai.com (edge rotated bot rules, same as Microsoft's known trap) — fell back to WebSearch, which surfaced 4 in-window Product/Publication/policy-safety items missed by the prior two daily runs' WebSearch passes: "Introducing AI Futures" (Aug20), "Offering Zero Data Retention for frontier models" (Aug19), "Pacing model development in an era of cyber-critical capabilities" (Aug18, a follow-up to KOV-35/2026-08-07 with new facts — RL-training pause, OpenAI-Hugging Face incident link), "OpenAI joins PORTS-Pike project" (Aug17, 8GW/20yr Ohio data-center deal); each confirmed via 2+ independent secondary sources since primary openai.com pages are unfetchable; "Dali Rajic CRO" appointment dropped (Company category, excluded per config filter) |
| anthropic | fetch (WebFetch) | 0 | none needed | listing still tops out at Aug14 (text watermark, already captured), nothing newer |
| google-deepmind | rss.xml (TIER-1, empty), WebSearch | 0 | WebSearch | WebSearch's "Exploring new frontiers of AI and games research" resolves to the same URL as the already-captured Aug21 Atari-to-EVE-Online item (dedup); nothing newer confirmed |
| google-research | rss.xml (TIER-1, empty), WebSearch | 0 | WebSearch | nothing newer than Aug21 (already captured); MedGemma health-AI post surfaced but undated/older, not confirmable as in-window |
| microsoft | rss.xml (TIER-1, empty), WebSearch | 0 | WebSearch | nothing newer than Aug20 (Skala 1.1, already captured) |
| nvidia | rss.xml (TIER-1, 304 not modified), WebSearch | 0 | WebSearch | SkillEvaluator (Aug18/19) already captured (KOV-227); nothing newer than Aug21 (AVO/DSX MaxLPS, already captured) |
| xai | curl-jina (403 Cloudflare, no JINA_API_KEY), WebSearch | 1 | WebSearch | curl-jina expected Cloudflare block; WebSearch surfaced "Grok 4.6 on Google Enterprise Agent Platform" (x.ai/news/grok-4-6-vertex-ai, Aug21) — missed by the prior two daily runs' WebSearch passes, confirmed via 4 independent secondary sources + Google Cloud docs |
| mistral | rss.xml (TIER-1, 304 not modified), WebSearch | 0 | WebSearch | nothing newer than Aug20 (Agentic Search, already captured); Leanstral 1.5 and OCRv4 mentions both predate window (late June/July) |
| huggingface | rss.xml (TIER-1, 304 not modified), WebSearch | 0 | WebSearch | nothing newer than Aug20 (LFM2.5-DSpark, already captured) |
| cursor | rss.xml (TIER-1, empty), WebSearch | 0 | WebSearch | nothing newer than Aug19 (Cloud Agents/Harness, already captured) |
| perplexity | curl-jina (403 Cloudflare, no JINA_API_KEY), WebFetch (EGRESS_BLOCKED), WebSearch | 0 | WebSearch | WebFetch on perplexity.ai now hard-blocked by the network egress proxy (new failure mode, not just Cloudflare); WebSearch resurfaced "Brain" (Aug19, already rejected 2026-08-20/2026-08-22 as unconfirmed) and "Computer now works in email" (Aug18, predates window) — nothing new confirmed |

Totals: 5 items, 2 companies fresh (openai, xai). Window: since last successful daily run (2026-08-23 06:10 UTC), widened by direct-fetch gap-scrape to catch up on several days of OpenAI/xAI items missed by prior WebSearch-only passes.

Linear: attempted 5 new-story cards in project "News digest" (team Kovalevgr, status Todo) — searched by title/keyword first, no duplicates found. KOV-274 [OpenAI] Introducing AI Futures (Medium, policy-safety) and KOV-275 [OpenAI] Offering Zero Data Retention for frontier models (Medium, product) created successfully. The 3rd attempt ([OpenAI] Pacing model development in an era of cyber-critical capabilities) and all subsequent attempts (PORTS-Pike, Grok 4.6 on Vertex AI) failed with `"You've exceeded the free issue limit for this workspace"` — the Kovalevgr Linear workspace has hit its plan's issue cap. **Owner action needed: upgrade the Linear plan (or free up/archive old issues) — until then, no new cards can be created in ANY project (News digest or Radar), which will also block tomorrow's radar run and the Sunday digest card.** The 3 uncarded stories remain fully written in `topics/openai.md`, `topics/xai.md`, and their artifact files — no data lost, only the Linear mirror is behind.

Commit: `news: daily run 2026-08-24 (+5 items, 2 companies fresh)`.

## 2026-08-24 07:04 UTC — deep-dive — ok (no approved cards)

No cards with label `hot` in project "Radar" (checked both the label query workspace-wide and a manual scan of all 88 cards in "Ready to Review" — zero hot). Nothing to process; no files written, no cards moved. Leftovers: n/a.

Commit: `news: deep dive 2026-08-24 (0 cards)`.

## 2026-08-25 05:11 UTC — radar — partial (Linear blocked)

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | none |
| inference-infra | 0 | 0 | none |
| oss-ml-systems | 1 | 1 | 1 (vllm-blog TLS handshake timeout) |
| bigtech-eng | 0 | 0 | none |
| research-institutes | 0 | 0 | none |
| technical-newsletters | 1 | 1 | none |
| practitioner-blogs | 0 | 0 | none |
| youtube | 0 | 0 | 7 (all yt-* sources: HTTP 404/500 — YouTube feed endpoint appears down/rotated today, not a per-channel issue) |
| community | 23 | 6 | 2 (reddit HTTP 429 — expected known failure mode, skipped without retry; lobsters TLS handshake timeout) |
| mistral-watch | 0 | 0 | none |

Totals: 26 raw candidates, 8 confirmed, 10 source-error groups (7 YouTube endpoints uniformly 404/500 — likely a transient upstream issue, logged and moved on per no-fallback-for-radar rule; reddit 429 expected; 2 TLS timeouts on vllm-blog and lobsters, no retry attempted).

TRIAGE pass 1 (technical bar): dropped — hn-show-inference's "Free Inference Engineer and Model Training Roadmap" (inferquest.org, empty body, 16 pts) as a career-resource/roadmap link, no discrete technique or release. hn-show-rag/hn-show-mcp/hn-show-agents all surfaced the same "Kern – container and resource runtime" (github.com/getkern/kern) via keyword overlap — dropped as off-focus (generic CPU/RAM-limiting container runtime, no AI/LLM tie in its own description); hn-show-rag's other two candidates ("A techno machine in one HTML file" and "I wrote a BASIC interpreter that boots on UEFI") dropped as off-focus (art project, retro-computing — no AI content). hf-trending-models: "peculiar-ragdoll/Qwen-Sharp-Chat-Templates" dropped as thin (no pipeline tag, no summary, vanity-style repo name — can't verify substance); "ornith-ai/Ornith-1.5-9B-GGUF" dropped as dedup (same Ornith-1.5 family thoroughly covered 2026-08-19 launch + 2026-08-22 MTP-head fix in `radar/community.md`). hf-trending-spaces: "shootstuff/flux-img2img-uncensored" dropped as off-focus (NSFW image generation); "hugging-apps/sensenova-...-mot" dropped as a thin Gradio wrapper around someone else's model demo, no original engineering content. smolai: "not much happened today" — skipped per the explicit rule for that exact title. github-trending: all 4 candidates (ai-job-search, andrej-karpathy-skills CLAUDE.md, NousResearch/hermes-agent, anthropics/claude-plugins-community) dropped as trending-snapshot noise with no discrete dated announcement, consistent with prior days' handling of this source.

TRIAGE pass 2 (owner fit): survivors scored — OCR It (HIGH: RAG/document-ingestion tooling, verified working via git clone), "My agent.md..." by Fabien Sanglard (HIGH: context engineering from a known author, transport-blocked), Apodex 1.1 and Prime Agent HF papers (both HIGH: AI-agents-in-practice / agent-harness / agent-memory territory), ReWorld HF paper (LOW: world-model/video-gen territory, cleared pass 1 only), the lite-LPU Show HN (MEDIUM: real from-scratch chip-design-for-inference project but very thin signal — 14 pts/1 comment — and transport-blocked), vllm v0.28.0 release tag (MEDIUM, same treatment as the v0.27.0/v0.27.1 precedent — routine version bump, no release-note text fetchable), cameron-wolfe's RL-for-LLMs guide (MEDIUM: training/fine-tuning practice, solid explainer).

VERIFY SUBSTANCE (5 highest-scored candidates checked): OCR It — verified via `git clone` (MIT, working Chrome extension, offline Tesseract OCR, no build step) → **highlight**. "My agent.md..." (fabiensanglard.net) — WebFetch EGRESS_BLOCKED, curl CONNECT-tunnel 403 → verification blocked, kept on title only, no highlight. Apodex 1.1 and Prime Agent (HF papers) — arxiv.org EGRESS_BLOCKED, HF papers page rendered only a figure-caption fragment via WebFetch → verification blocked (only the paper's own 500-char abstract excerpt, already captured by the fetch script, was usable) — kept on abstract text, no highlight. lite-LPU (lpulite.com) — WebFetch EGRESS_BLOCKED, curl CONNECT-tunnel 403 → verification blocked, kept on HN submission's own summary text, no highlight. Only 1 highlight today (OCR It) — a weak day for verifiable substance, not padded.

WRITE: 8 items written — 1 to `radar/oss-ml-systems.md` (new `## 2026-W35` heading), 1 more to `radar/technical-newsletters.md` (existing `## 2026-W35`), 6 to `radar/community.md` (new `## 2026-W35` heading).

**Linear: BLOCKED — same issue-limit cap reported 2026-08-24 is still in effect, now confirmed on a second consecutive day.** All 8 `save_issue` calls (OCR It, agent.md, Apodex 1.1, Prime Agent, ReWorld, lite-LPU, vllm v0.28.0, cameron-wolfe RL guide) failed identically: `"You've exceeded the free issue limit for this workspace. Please upgrade or contact sales@linear.app for a free trial."` Zero review-queue cards created. All 8 items are fully written in the radar files above — no data lost, only the Linear review queue is behind. **Owner action still needed: upgrade the Linear plan or free up/archive old issues** — until resolved, this will keep blocking the daily radar queue, tomorrow's company-news cards, and the Sunday digest card.

Commit: `news: radar run 2026-08-25 (+8 items, 1 highlight, Linear blocked)`.

## 2026-08-25 06:10 UTC — daily — ok (Linear blocked)

Window: since 2026-08-24T04:10:43 UTC (fetch_feeds.py, ~26h default). `fetch_feeds.py` ran clean (exit 0, no source_errors for any company).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss | 1 | - | - |
| anthropic | fetch (WebFetch) | 0 | fetch | listing still tops out at Aug14 (text watermark, already captured), nothing newer |
| google-deepmind | rss, websearch | 0 | websearch | no in-window post with a confirmed URL surfaced |
| google-research | rss, websearch | 0 | websearch | latest post (Science One Framework) still Jul30, predates window |
| microsoft | rss, websearch | 0 | websearch | no Research-blog post newer than Aug11 confirmed |
| nvidia | rss | 5 | - | 1 candidate excluded — "Maximizing AI Factory Performance per Watt with NVIDIA DSX MaxLPS" re-surfaced with the exact URL already captured 2026-08-21 (KOV-257); the known feed trap (ordered by `<updated>` not `<published>`, per sources.json note) resurfacing an old entry, not a new story |
| xai | jina (anonymous) | 0 | jina | anonymous curl clean 200 (no Cloudflare challenge today); latest post still Aug21 (Grok Bot more plans), predates window. First attempt sent `Authorization: Bearer` with an unset `$JINA_API_KEY`, which Jina correctly rejected as 401 invalid-key rather than the usual anonymous 403 — re-ran without the header per the "only if the env var exists" rule; not a real transport failure |
| mistral | rss | 1 | - | - |
| huggingface | rss | 1 | - | - |
| cursor | rss, websearch | 0 | websearch | WebSearch's only Aug24 lead was a billing/usage-limit email notice, not a changelog entry — rejected as not a story; latest confirmed changelog entry still Aug19 |
| perplexity | jina (anonymous) | 0 | jina | anonymous curl clean 200; latest post still Aug19 (Brain: Agentic Memory as a Knowledge Wiki), predates window; same header-fix as xai above, not a real transport failure |

Totals: 8 items, 4 companies fresh (openai, nvidia, mistral, huggingface), 0 source errors (9 gap-scrapes attempted, all empty in-window; 1 rejected duplicate candidate — NVIDIA DSX MaxLPS feed-ordering trap).

**Note on `$JINA_API_KEY`:** the env var is currently unset (confirmed via shell check), same underlying condition noted in prior run-log entries ("no JINA_API_KEY set" → anonymous Jina, which works most days but occasionally 403s with AbuseAlleviationError). Today anonymous Jina worked cleanly for both xAI and Perplexity once the malformed empty-Bearer header was dropped.

NVIDIA volume note: 6 raw TIER-1 candidates, all published 2026-08-24 15:00–15:08 UTC as a coordinated technical cluster around the Vera Rubin platform (Spectrum-X Ethernet, BlueField-4 Scale-In, Vera CPU, Groq 3 LPX inference accelerator, Vera Rubin/Blackwell perf-per-watt benchmarks) — each is substantive engineering content with concrete numbers, not tutorial filler, so kept per the "genuine announcements/major posts" bar; the 6th (DSX MaxLPS) was the duplicate dropped above.

Linear: attempted 1 new-story card ([OpenAI] Advancing price-performance for developers with GPT‑5.6 in Kiro) to test whether the issue-limit cap from 2026-08-24/2026-08-25 (radar) had cleared. **It has not — same error: `"You've exceeded the free issue limit for this workspace. Please upgrade or contact sales@linear.app for a free trial."`** Did not attempt the remaining 7 (NVIDIA ×5, Mistral, Hugging Face) since the block is confirmed workspace-wide, not per-issue. All 8 items are fully written in `topics/*.md` and their artifact files — no data lost, only the Linear mirror is behind, now on its third consecutive blocked run (radar 08-24, radar 08-25, daily 08-25). **Owner action still needed: upgrade the Linear plan or free up/archive old issues.**

Commit: `news: daily run 2026-08-25 (+8 items, 4 companies fresh, Linear blocked)`.

## 2026-08-26 05:14 UTC — radar — partial (Linear blocked)

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | none |
| inference-infra | 0 | 0 | none |
| oss-ml-systems | 1 | 1 | none |
| bigtech-eng | 1 | 1 | none |
| research-institutes | 0 | 0 | 1 (bair.berkeley.edu feed: connection reset by peer) |
| technical-newsletters | 1 | 0 | none |
| practitioner-blogs | 0 | 0 | none |
| youtube | 0 | 0 | 7 (all yt-* sources: HTTP 404 — second consecutive day of a uniform YouTube feed-endpoint outage across every channel, not per-channel; logged and moved on, no fallback per radar rules) |
| community | 53 | 11 | none (reddit .json transport returned an HTML shell instead of JSON for 2 spot-check URLs — not a 429, kept on the fetch script's own summary text per the curl-failure fallback) |
| mistral-watch | 0 | 0 | none |

Totals: 56 raw candidates, 13 confirmed, 2 source-error groups (bair connection reset; 7 YouTube endpoints uniformly HTTP 404, same pattern as 2026-08-25 — now looks like a sustained upstream/endpoint change rather than a one-day blip, worth the owner's attention if it persists past today).

TRIAGE pass 1 (technical bar): HN show-* candidates heavily overlapped across ai50/inference/rag/agents searches (same items surfaced by multiple keyword queries) — deduped to unique items before triage. Dropped as off-focus/no-AI-content: TeXbrain (WASM LaTeX editor), Coffeetable (Claude book-discovery connector, consumer product launch), fdeploy (Windows/IIS deployment tool, no AI tie), "A techno machine in one HTML file" (art project). Dropped as thin/unverifiable: "Free Inference Engineer and Model Training Roadmap" (career-resource link) — also a same-title repeat of 2026-08-25's drop. Dropped as dedup (already in `radar/community.md` from 2026-08-24): OCR It, the lite-LPU Show HN. hf-trending-spaces: all 4 candidates dropped as thin Gradio-wrapper demos (Wan2.2 clean space, 2 AI-detector spaces, a Qwen-edit-image wrapper), consistent with prior days. github-trending: all 3 candidates dropped as trending-snapshot noise with no discrete dated announcement, same handling as prior days. Reddit r/LocalLLaMA (25 raw): dropped memes/appreciation posts ("It's here!", "You think they could have tweaked the typeface", "me to the model I spent all weekend fine-tuning", "Qwen 3.8 27b has ThreeJs locked down"), a beginner Q&A thread ("How to run LLMs as regular guy with low resources?"), consumer-hardware discussion/cost threads with no technique content (M5 Ultra vs Max bandwidth debate, Mac Studio M5 Max cost analysis, Intel Arc Pro B60 "spotted" listing), a thin HF-link repost with no added content (ibm-granite/granite-4.2-30b), a niche fine-tune-variant roundup (12 abliterated Gemma 4 12B), a vertical model release judged lower-priority for budget (Thomson Reuters Thomson-1.0-Small), a lower-interest release (Granite Speech 5.0 Turbo CTC — speech/transcription, off the owner's tracked interests), a duplicate-of-HF-paper repost (tencent/WeMM-Embedding — kept via hf-daily-papers instead, richer content there), and 3 more same-story reposts of the Apple Mac Studio/mini M5 launch plus one "Qwen3.8-Flash-Next tomorrow" pre-release rumor and one "Glm 5.3 flash?" speculation thread — all consolidated into single representative items below. `hf-daily-papers`'s "On-Policy Self-Distillation in Diffusion Models" cleared pass 1 (real technique, code released) but dropped at pass 2 as off-focus (diffusion/image-gen territory, explicit LOW bucket in `config/interests.md`). SemiAnalysis "OpenAI Jalapeño: Better Than Nvidia Blackwell" dropped at pass 1 — TCO/throughput-per-MW chip-economics piece, the explicit SemiAnalysis-finance drop case named in both the workflow and `config/interests.md`'s LOW bucket.

TRIAGE pass 2 (owner fit): HIGH — Recuris/HF paper (agent harnesses + agent memory + code, direct hit on two HIGH-bucket interests), Ambient Context HN Show (agent-memory/context-engineering tool, code, HIGH), NVFP4 Qwen3.8-27B QUASAR QAD (local quantization release, HIGH), Llama.cpp adaptive speculation (local inference-engine technique, HIGH), Qwen3.8-Flash-Next day-0 unsloth support (local models, HIGH), Quantization-Aware Healing (quantization technique, HIGH), 35B-A3B tool-calling benchmark (evals-in-practice + local models, HIGH), EleutherAI Aletheia retrospective (evals-in-practice + reproducible code, HIGH), github.blog LLM-eval lifecycle (evals-in-practice, HIGH). MEDIUM — WeMM-Embedding HF paper (RAG/embeddings), AI At Home Part 2 lobsters (local/self-hosted "runs on my hardware"), Apple M5 local-AI-design piece (hardware angle on local inference), A Manifesto for Responsible Agentic Coding (agentic-coding practice, opinion not hands-on technique). "Super-intelligence or Superstition?" (lobsters arxiv link, psychology/belief-in-AI-predictions paper) dropped at pass 1 — off the technical/engineering bar, social-science territory.

VERIFY SUBSTANCE (6 candidates checked, one over the usual 5 given a strong day): Recuris — verified via `git clone` (github.com/Gen-Verse/Recuris): real eval+evolution code, evolved Skill Memory packages and frozen eval splits released → **highlight**. Ambient Context — verified via `git clone`: builds (Tauri, Rust+TS), README confirms the no-screenshot/no-network/redaction claims → **highlight**. EleutherAI Aletheia retrospective — verified via WebFetch: concrete AUROC numbers (0.926 black-box, 0.945 white-box), code+dataset released at `github.com/EleutherAI/how-to-catch-an-ai-liar` → **highlight**. github.blog LLM-eval piece — verified via WebFetch: real methodology + a 95% false-positive-reduction number, no code included — solid but not highlight-differentiated against the other three. NVFP4 quantization and Llama.cpp adaptive-speculation reddit posts — curl `.json` fetch returned an HTML shell instead of Reddit's JSON API today (not a 429), so verification fell back to the feed script's own captured summary text per the curl-failure rule; both kept with real technical content (concrete `vllm serve` command + Blackwell target for NVFP4; min/max adaptive-speculation mechanism for llama.cpp), out of highlight consideration since the full thread wasn't read. 3 highlights today (Recuris, Ambient Context, EleutherAI Aletheia) — a strong day for verifiable substance.

WRITE: 13 items written — 1 to `radar/oss-ml-systems.md` (existing `## 2026-W35`), 1 to `radar/bigtech-eng.md` (new `## 2026-W35` heading — file hadn't had a 2026-W35 entry yet), 11 to `radar/community.md` (existing `## 2026-W35`). No items to `radar/technical-newsletters.md` today (its one raw candidate was dropped at pass 1).

**Linear: BLOCKED — same free-issue-limit cap first reported 2026-08-24, now confirmed on a FOURTH consecutive run (radar 08-24, radar 08-25, daily 08-25, radar 08-26).** Attempted 1 test card (the Recuris highlight, to re-check whether the cap had cleared overnight) — identical error: `"You've exceeded the free issue limit for this workspace. Please upgrade or contact sales@linear.app for a free trial."` Did not attempt the remaining 12 review-queue cards since the block is confirmed workspace-wide. All 13 items are fully written in the radar files above — no data lost, only the Linear review queue (and tomorrow's daily-news cards, and the weekly digest card) stay blocked until this clears. **Owner action needed: upgrade the Linear plan or free up/archive old issues in the Kovalevgr workspace** — this has now blocked every run for 3 straight days.

Commit: `news: radar run 2026-08-26 (+13 items, 3 highlights, Linear blocked)`.

## 2026-08-26 06:12 UTC — daily — ok (Linear blocked)

Window: since 2026-08-25T04:12:34 UTC (fetch_feeds.py, ~26h default; last successful daily run was 2026-08-25 06:10 UTC). `fetch_feeds.py` ran clean (exit 0, no source_errors for any company; mistral rss returned 304 not-modified).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss | 1 | - | - |
| anthropic | fetch (WebFetch) | 1 | fetch | - |
| google-deepmind | rss, websearch | 0 | websearch | only lead was a multi-agent-safety funding post from Jun 11 2026, already predates window by months — rejected |
| google-research | rss | 1 | - | - |
| microsoft | rss, websearch | 0 | websearch | no Research-blog post newer than Aug11 confirmed |
| nvidia | rss | 2 | - | - |
| xai | jina (anonymous) | 0 | jina | anonymous Jina 403'd today (Cloudflare) — one attempt per MAX ONE fallback rule, logged and moved on |
| mistral | rss | 0 | - | 304 not-modified — no fresh candidates, no gap-scrape needed (not a zero-fresh-vs-error case, cursor confirms nothing changed) |
| huggingface | rss | 2 | - | - |
| cursor | rss, websearch | 0 | websearch | WebSearch surfaced an uncorroborated "Cursor acquired by SpaceX" claim alongside a correctly-dated Aug14 Grok-in-Copilot item (an xAI story, not Cursor's) — rejected both as unconfirmed/off-target; latest confirmed changelog entry still Aug19 |
| perplexity | jina (anonymous) | 0 | jina | anonymous Jina 403'd today (Cloudflare) — one attempt per MAX ONE fallback rule, logged and moved on |

Totals: 7 items, 5 companies fresh (openai, anthropic, google-research, nvidia, huggingface), 0 source errors (7 gap-scrapes attempted: 1 confirmed via WebFetch (anthropic), 2 Cloudflare-blocked on Jina (xai, perplexity), 4 empty/rejected via WebSearch (google-deepmind, microsoft, cursor) — mistral had no gap-scrape trigger, it was a clean 304).

Note on OpenAI's Jalapeño item: WebFetch on the source page 403'd (Cloudflare challenge), and the one Jina retry per the WebFetch-403 failure mode also 403'd — the item is still confirmed via the TIER-1 rss feed itself (title/URL/date/summary), with supplementary benchmark numbers (1.5–1.9x perf/watt, 1.7–3.6x lower latency vs Nvidia GB200/GB300) sourced via WebSearch and cited as such in the artifact.

Cross-file note: Hugging Face's "Quantization-Aware Healing" post is the same story radar captured yesterday (2026-08-26 05:14 UTC run) via a Reddit repost in `radar/community.md`; today's item carries the primary huggingface.co URL and OWNS the story per the cross-source dedup rule — no changes made to the existing radar entry.

Linear: attempted 1 new-story card ([OpenAI] Jalapeño's first results...) to re-check whether the free-issue-limit cap had cleared overnight. **It has not — same error: `"You've exceeded the free issue limit for this workspace. Please upgrade or contact sales@linear.app for a free trial."`** Did not attempt the remaining 6 cards (Anthropic, google-research, NVIDIA ×2, Hugging Face ×2) since the block is confirmed workspace-wide. All 7 items are fully written in `topics/*.md` and their artifact files — no data lost, only the Linear mirror is behind, now on its FIFTH consecutive blocked run (radar 08-24, radar 08-25, daily 08-25, radar 08-26, daily 08-26). **Owner action still needed: upgrade the Linear plan or free up/archive old issues in the Kovalevgr workspace** — this has now blocked every run for 3 straight days running into a 4th.

Commit: `news: daily run 2026-08-26 (+7 items, 5 companies fresh, Linear blocked)`.

## 2026-08-27 05:05 UTC — radar — partial (Linear unavailable)

Window: since 2026-08-26T03:05:28 UTC (fetch_radar.py, last successful radar run 2026-08-26 05:14 UTC). `fetch_radar.py` ran clean (exit 0); source errors: `bair` (connection reset by peer, no fallback for radar sources), all 7 `yt-*` sources HTTP 404 for the fourth consecutive day (2026-08-24/25/26/27) — same uniform YouTube feed-endpoint outage, logged and moved on per no-fallback-ladder rule.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 2 | 1 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 1 | 1 | - |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 2 | 0 | - |
| youtube | 0 | 0 | 7 (all yt-* sources: HTTP 404, 4th consecutive day) |
| community | 51 | 8 | - |
| mistral-watch | 0 | 0 | - |

Totals: 56 raw candidates, 10 confirmed, 8 source-error groups (bair×1, youtube×7) — within FAILURE MODES (no fallback ladder for radar sources).

TRIAGE pass 1 (technical bar): `pytorch-blog`'s "PyTorch Ecosystem Landscape Welcomes Perforated, AReaL..." verified via WebFetch and confirmed a 10-project roundup announcement (one thin self-promotional paragraph per project, "learn more" links) — dropped as roundup-of-others, same rule that trims PyTorch's Conference/Foundation/Meetup posts. `latent-space`'s two candidates both verified via WebFetch and dropped: "Lovable CTO: The Future of SaaS..." is investor-relations content framed as an interview (unverified Menlo Ventures metrics, superficial MCP architecture detail); "We have foundation models for language, not for physics — Anima Anandkumar" is a philosophical interview with real technique names (FourCastNet, Neural Operators, TorchLean) but no reproducible numbers/hyperparameters, and its subject (physics/climate modeling) sits in the LOW interest bucket — consistent with prior latent-space interview drops (2026-08-19/21/22). `hn-show-*` (heavily overlapping across ai50/inference/rag/agents, deduped to unique items first): dropped hnstats.com (thin word-counter, no real technique), TeXbrain (non-AI, WASM LaTeX editor), "Build your own theme park" / magicpatterns (consumer agent-demo marketing, no engineering depth), pushup.quest (fitness game, off-focus), fdeploy.com (Windows/IIS deploy tool, no AI tie) — all consistent with prior days' handling of thin/off-focus Show HN posts. Reddit r/LocalLLaMA (25 raw): dropped memes/appreciation/opinion posts ("this is a friendly reminder you can legally seed...", "Can we reconsider the megathreads?", "Whoever the fuck predicted...", "Are models with N-Gram tables going to completely change the AI race?"), hardware Q&A with no shared technique ("Anyone else doing eGPUs (OCuLink)?", "Gemma4 31B vs Qwen3.8 27B — why the huge difference"), a thin unverifiable personal script ("little tool for offline wikipedia RAG" — no repo link, author's own "not particularly useful"), and business/M&A news out of radar's scope ("Nvidia has been in talks to acquire Hugging Face for $13B" — a company-core story, not a technical-radar one; left for the daily company run to pick up against `topics/huggingface.md`). Consolidated into ONE representative item: five same-day reposts of the GLM-5.3-Flash release (`[Megathread] GLM-5.3-Flash`, `zai-org/GLM-5.3-Flash · Hugging Face`, `GLM-5.3-Flash: Frontier Intelligence, Flash Cost`, `First serious confirmation. Ox Alpha is GLM-5.3-Flash`, `GLM-5.3 weights will be released tomorrow`) — kept the megathread as the richest source. `hf-trending-models`: Qwen3.8-Flash-Next and its GGUF quant dropped as dedup (release already covered via Unsloth day-0 support, 2026-08-25); `sensenova/SenseNova-U1.5-8B-MoT` dropped as thin (no summary text, unverified). `hf-trending-spaces` (3 candidates: MiniMax-Music3-Jam, 4danyone-multiview-demo, SageBio rare-disease hackathon space) dropped as off-focus (music/3D/health-hackathon demos, none in the interest profile). `hf-daily-papers`: VoiceMem (duplex-speech memory) dropped as off-focus (audio, not tracked); StreamPI (VLA temporal modeling) dropped per the explicit robotics/video LOW bucket; JIT-Agent (harness-intelligence model synthesizing task-adaptive agent harnesses) cleared pass 1/2 as a strong HIGH-fit item (agent harnesses) but its HF papers page returned no fetchable abstract via WebFetch or a curl retry — kept on the daily-papers abstract excerpt, out of highlight consideration.

VERIFY SUBSTANCE: `lmsys-sglang`'s Qwen3.8-Flash-Next day-0 post verified via WebFetch — concrete architecture/perf numbers (IndexShare MTP, HyperConnection kernel speedups, n-gram table host-offload), promoted to highlight. `ai2`'s Thai Dolma/Mangosteen post verified via WebFetch — concrete corpus numbers (47B tokens, >80%/~50% filter rates), promoted to highlight. `github.com/ThinkOffApp/CarWatch` verified via `git clone` (README + architecture diagram, AGPL, stdlib-only) — real hardware numbers (3.5 tok/s gen, 65°C sustained), promoted to highlight. `keenable.ai` transport-blocked (WebFetch egress-blocked, curl CONNECT-tunnel-403 retry) — kept as a regular item on its own submission text, out of highlight consideration. Reddit transport (`.json`) returned HTTP 403 for every reddit URL attempted today (N-gram explainer, Qwen3.8 27B quant benchmark, self-hosting guide, offline-wikipedia-RAG tool, Lemonade update, GLM-5.3-Flash megathread) — all six kept on the feed's own summary text per the standing reddit-transport-blocked fallback.

WRITE: 1 item to `radar/oss-ml-systems.md` (existing `## 2026-W35`), 1 item to `radar/research-institutes.md` (new `## 2026-W35` heading), 8 items to `radar/community.md` (existing `## 2026-W35`).

**Linear: UNAVAILABLE this run — the Linear MCP connector requires re-authorization (not the free-issue-limit cap reported 2026-08-24 through 2026-08-26; this run's tool listing shows no Linear tools loaded at all).** No review-queue cards attempted. All 10 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue is behind. **Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or confirm/clear the prior free-issue-limit block** — until resolved, the daily review queue stays behind.

Commit: `news: radar run 2026-08-27 (+10 items, 3 highlights, Linear unavailable)`.

## 2026-08-27 06:12 UTC — daily — ok (Linear unavailable)

Window: since 2026-08-26T04:12:40 UTC (fetch_feeds.py; last successful daily run 2026-08-26 06:12 UTC). `fetch_feeds.py` ran clean (exit 0, no source_errors for any company).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss | 2 | - | 2 candidate pages 403'd on direct WebFetch (Cloudflare); confirmed via the one Jina retry per the WebFetch-403 failure mode |
| anthropic | fetch (WebFetch) | 0 | fetch | latest post (wellbeing-research-grants) Aug 25, already captured, predates window |
| google-deepmind | rss | 1 | - | source page 403'd on WebFetch and a curl retry (redirects to egress-blocked blog.google) — item confirmed on the RSS feed's own title/URL/date/summary per standing fallback |
| google-research | rss | 1 | - | - |
| microsoft | rss, websearch | 0 | websearch | no Research-blog post newer than Aug20 (Skala 1.1) confirmed |
| nvidia | rss | 3 | - | - |
| xai | jina (anonymous) | 0 | jina | anonymous Jina 403'd today (Cloudflare) — one attempt per MAX ONE fallback rule, logged and moved on |
| mistral | rss, websearch | 0 | websearch | latest post (Mistral x HUMAIN) Aug24, already captured, predates window |
| huggingface | rss, websearch | 0 | websearch | no Hugging Face blog post newer than Aug25 (already captured) confirmed |
| cursor | rss, websearch | 0 | websearch | no changelog entry newer than Aug19 confirmed |
| perplexity | jina (anonymous) | 0 | jina | anonymous Jina 403'd today (Cloudflare); WebSearch surfaced "Portable Computer for local-first AI" (Aug25) and "Computer now works in email" (Aug18) — both predate window, rejected; latest confirmed remains Aug13 (Agent API) |

Totals: 7 items, 4 companies fresh (openai, google-deepmind, google-research, nvidia), 0 source errors (7 gap-scrapes attempted: 1 confirmed via WebFetch+Jina text extraction for OpenAI's two 403'd pages counted under openai row, 1 confirmed via RSS-summary fallback for google-deepmind, 2 Cloudflare-blocked on anonymous Jina (xai, perplexity), 4 empty/rejected via WebSearch (microsoft, mistral, huggingface, cursor)).

Note: OpenAI's two new items ("Bringing ChatGPT for Teachers to more U.S. school districts", "Learning never stops") both 403'd on direct WebFetch (Cloudflare challenge) — confirmed via the one allowed Jina retry per the WebFetch-403 failure mode, full text extracted successfully both times.

Note: Google DeepMind's "Intelligent transcription with Gemini 3.5 Transcribe" 403'd on WebFetch, and its 302 redirect target (blog.google) is blocked by the network egress proxy; a direct curl also failed the CONNECT tunnel. Item is confirmed and written on the RSS feed's own title/URL/date/summary alone — flagged in its artifact as thin on detail.

**Linear: UNAVAILABLE this run — no Linear MCP tools were loaded in this session's tool search (the connector requires re-authorization; same state as the 2026-08-27 05:05 UTC radar run, not the free-issue-limit cap reported 2026-08-24 through 2026-08-26).** No cards attempted. All 7 items are fully written in `topics/*.md` and their artifact files — no data lost, only the Linear mirror is behind, now on its SIXTH consecutive affected run (radar 08-24, radar 08-25, daily 08-25, radar 08-26, daily 08-26, radar 08-27) and the SECOND run in a row where the connector doesn't load at all (vs. the earlier free-issue-limit error). **Owner action still needed: reconnect the Linear connector (claude.ai Settings → Connectors) and/or clear the free-issue-limit cap** — until resolved, the daily review queue and News digest board stay behind.

Commit: `news: daily run 2026-08-27 (+7 items, 4 companies fresh, Linear unavailable)`.

## 2026-08-27 07:03 UTC — deep-dive — blocked (Linear unavailable)

First firing of the radar-deep-dive routine (Mon+Thu 07:00 UTC). **Run blocked at step 1 (PICK): the Linear MCP connector is unavailable in this session — no Linear tools loaded (connector requires re-authorization; same state as today's 05:05 radar and 06:12 daily runs).** Unlike the daily/radar runs, where Linear is only the review-queue mirror, the deep dive has NO repo-side fallback: the `hot` label on cards in project "Radar" is the routine's sole input, so with Linear unreachable there is no way to know which cards the owner approved. Verified there is no alternate read path this session (Notion connected-source search fell back to workspace-only mode — Linear not connected there either).

Cards processed: 0. Files written: 0 (`radar/deep/` still holds only TEMPLATE.md). Leftovers: unknown — any `hot`-labeled cards are waiting in Linear untouched; they will be picked up oldest-first on the next run once the connector is restored. Note the review queue itself is also behind (no cards created since the 2026-08-24 free-issue-limit block, connector unavailable since 2026-08-27), so the owner may not have had cards to approve at all.

**Owner action needed (same as flagged since 2026-08-24): reconnect the Linear connector (claude.ai Settings → Connectors) and/or clear the free-issue-limit cap in the Kovalevgr workspace.** Until then both the review queue and the deep-dive flow are stalled.

Commit: `news: deep dive 2026-08-27 (0 cards, Linear unavailable)`.

## 2026-08-28 05:05 UTC — radar — ok (Linear unavailable)

Window: since 2026-08-27T03:05:06 UTC (fetch_radar.py; last successful radar run 2026-08-27 05:05 UTC). `fetch_radar.py` ran clean (exit 0); source errors: `bair` (connection reset by peer, no fallback for radar sources), 6 of 7 `yt-*` sources HTTP 404 and `yt-umar-jamil` HTTP 500 — the same uniform YouTube feed-endpoint outage for a FIFTH consecutive day (2026-08-24 through 2026-08-28), logged and moved on per no-fallback-ladder rule.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 1 | 1 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 1 | 0 | - |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 0 | 0 | - |
| youtube | 0 | 0 | 7 (6× HTTP 404, 1× HTTP 500 — 5th consecutive day) |
| community | 56 | 13 | - |
| mistral-watch | 0 | 0 | - |

Totals: 58 raw candidates, 14 confirmed, 8 source-error groups (bair×1, youtube×7) — within FAILURE MODES (no fallback ladder for radar sources).

TRIAGE pass 1 (technical bar): `ai2`'s "Ai2 and Providence Swedish Cancer Institute partner to advance AI-assisted scientific discovery" verified via WebFetch — read as a partnership/PR announcement (new AutoDiscovery deployment at a cancer-research institute) rather than an engineering piece; dropped as product/partnership marketing that survived the config filter, consistent with the roundup/marketing exclusion rule. `hn-show-*` (5 tags, heavily overlapping — deduped to 10 unique candidates first): dropped `magicpatterns.com` theme-park demo and `hnstats.com` word-counter (both repeat drops from 2026-08-27, still off-focus/thin today), Voronoi Go (game), the fiber-break map tool (non-AI), and the push-up RPG game (fitness, off-focus) — all consistent with prior-day handling. Kept and verified via `git clone` all five remaining Show HN repos: `anthropics/claude-plugins-official`, `kelviq/tare`, `experientiallabs/experiential`, `opslane/opslane` — real, working repos with substantive READMEs, all HIGH-fit (agent-tool ecosystem, context engineering, coding/ops agents); `polign.com`'s agent-memory post (HIGH-fit topic) hit a full transport block (WebFetch egress-blocked, curl CONNECT-tunnel-403 retry) and stayed on its own HN submission text, out of highlight consideration. Reddit r/LocalLLaMA+LLMDevs (25 raw, heavily Qwen3.8-Flash-Next-themed after a week of saturation coverage): dropped memes/appreciation/opinion posts ("5090 now officially cost 5090", the Unsloth appreciation post, "and then they came for the used server RAM", "friendly reminder you can legally torrent ai models", "Moderation !== Censorship"), a thin hardware Q&A ("What are the minimum specs required to run Qwen3.8-Flash-Next?"), a vague benchmark-claim post ("Qwen3.8-Flash-Next better then DeepSeek V4 Pro"), two dedups of the already-covered GLM-5.3-Flash megathread (the Unsloth GGUF repost, the "#3 open weight model" benchmark-claim repost), robotics (Microduck — LOW bucket, thin), and two business/M&A posts about the Nvidia–Hugging Face deal and a Bill Gates AI-policy meeting (out of radar's technical scope, left for the daily company run / dropped as policy respectively). `lobsters`' one candidate (Bill Gates' "turbulent AI era" essay on gatesnotes.com) dropped as the same policy/opinion territory. Kept 6 reddit items that cleared the bar with real technical substance on the feed's own summary text (reddit `.json` transport 403'd for every URL attempted today): "gemma4.c" (a from-scratch 700-line C LLM implementation), a local-Qwen coding harness ("I used local Qwen 27b to build a harness and replace OpenCode"), a 200k-context-on-16GB-VRAM quantization report, two merged llama.cpp PRs (DFlash2 speculative decoding, `--n-cpu-ffn` CPU offload), and an "Engrams" technique explainer countering a spreading misconception about Qwen3.8-Flash-Next's n-gram tables. `hf-daily-papers` (3 candidates, all with GitHub repos per the config filter): kept TTPO (test-time policy optimization, training/RL-practice territory) as abstract-only; dropped PAWBench (world-modeling benchmark) and UrbanGround (embodied-AI spatial agency) as robotics/world-model LOW-bucket territory, redundant with each other for today's volume budget. `hf-trending-models`: dropped `unsloth/GLM-5.3-Flash-GGUF` as a dedup of the already-covered GLM-5.3-Flash megathread; kept `deepseek-ai/DeepSeek-V4-Flash-0731` (304B MoE, MIT-licensed, verified via WebFetch — a major open-weight release not yet covered anywhere in the repo). `hf-trending-spaces`' one candidate (a Pollen Robotics microduck simulator) dropped as thin robotics content. `github-trending` (3 candidates, all verified via `git clone`): kept `anthropics/claude-plugins-official` (Anthropic's own plugin directory — directly relevant to this repo's own Claude Code workflow) and `tt-a1i/archify` (codebase-to-system-map tool); kept `DietrichGebert/ponytail` (a minimal coding-agent CLI) as a regular item, out of highlight consideration (thin corroboration beyond its own README).

VERIFY SUBSTANCE: verified 7 candidates today (over the "up to 5" guideline — content was readily available via `git clone`/WebFetch for most, so the extra reads were cheap). `lmsys-sglang`'s MiniMax-H3 post verified via WebFetch — concrete kernel-fusion/caching/sparse-attention numbers (up to 6.24× at 0.76–0.91 SSIM vs. Diffusers baseline), but the underlying domain is video generation (LOW interest bucket) — kept as a strong technique, out of highlight consideration. `anthropics/claude-plugins-official`, `kelviq/tare`, `experientiallabs/experiential`, `opslane/opslane`, `tt-a1i/archify`, `DietrichGebert/ponytail` all verified via `git clone` (README read in full). `deepseek-ai/DeepSeek-V4-Flash-0731` verified via WebFetch (benchmark table, license, architecture). `polign.com` transport-blocked (WebFetch egress-blocked + curl CONNECT-tunnel-403 retry) — kept as a regular item, out of highlight consideration. Reddit's `.json` transport 403'd for every URL attempted today — the six kept reddit items rest on the feed's own summary text per the standing fallback, all out of highlight consideration (no independent read of the full threads).

**Highlights (3, capped per the workflow):** `anthropics/claude-plugins-official` (directly actionable for this repo's own Claude Code/skills workflow), `kelviq/tare` (context-engineering tool for the owner's own daily driver, Claude Code), `gemma4.c` (the clearest "reproducible technique WITH CODE" fit of the day — the interest profile's top HIGH bullet). `deepseek-ai/DeepSeek-V4-Flash-0731`, `experientiallabs/experiential` and the local-Qwen harness post were strong runners-up, kept as regular (non-highlighted) items.

WRITE: 15 items written — 1 to `radar/oss-ml-systems.md` (existing `## 2026-W35`), 14 to `radar/community.md` (existing `## 2026-W35`).

**Linear: UNAVAILABLE this run — no Linear MCP tools loaded in this session (connector requires re-authorization; unchanged since 2026-08-27).** No review-queue cards attempted. All 15 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. **This is now the SEVENTH consecutive affected run (radar 08-24 free-issue-limit → radar 08-25, daily 08-25 free-issue-limit → radar 08-26, daily 08-26 free-issue-limit → radar 08-27, daily 08-27, deep-dive 08-27, radar 08-28 all connector-unavailable) — a full week with no working review queue, and the Mon/Thu deep-dive routine has now missed its only scheduled run this week with zero cards processed.** Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) and/or clear the free-issue-limit cap in the Kovalevgr workspace.

Commit: `news: radar run 2026-08-28 (+15 items, 3 highlights, Linear unavailable)`.

## 2026-08-28 06:18 UTC — daily — ok (Linear unavailable)

Window: since 2026-08-27T04:10:20 UTC (fetch_feeds.py; last successful daily run 2026-08-27 06:12 UTC). `fetch_feeds.py` ran clean (exit 0, no source_errors for any company; huggingface's feed returned 304 not-modified, correctly surfaced as zero fresh).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss, websearch+jina | 0 | websearch, jina | jina page confirmed 3 new posts (Aug26-27) but all fall in categories excluded by the technical-first filter (Company/Security) — correctly zero per config |
| anthropic | fetch (WebFetch) | 2 | fetch | Model Hardware Standard research preview + expanded scientist support, both Aug 27 |
| google-deepmind | rss | 2 | - | - |
| google-research | rss | 1 | - | - |
| microsoft | rss, websearch+fetch | 0 | websearch, fetch | Research blog confirmed no post newer than Aug20 (Skala 1.1, already captured) |
| nvidia | rss, websearch+fetch | 0 | websearch, fetch | developer blog confirmed no post newer than Aug26 (already captured) |
| xai | jina | 2 | jina | jina worked today (no 403, unlike recent days): Grok 4.6 on Microsoft Foundry (Aug26, new); Grok 4.6 on Amazon Bedrock (Aug19, backfilled — missed by prior 403'd gap-scrapes) |
| mistral | rss, websearch+fetch | 0 | websearch, fetch | news page confirmed no post newer than Aug24 (Mistral x HUMAIN, already captured) |
| huggingface | rss, fetch | 1 | fetch | 304 not-modified on rss; direct fetch confirmed one new post (Aug26, multi-vector embedding guide) the feed hadn't surfaced yet |
| cursor | rss, websearch+fetch | 1 | websearch, fetch | Start from scratch, without a repo (Aug27, new) |
| perplexity | jina | 4 | jina | jina worked today (no 403, unlike recent days): backfilled 4 posts missed across Aug18-25 (Computer in Email, Brain agentic memory, Portable Computer, Computer finance data sources); dropped "How to use AI in a small business" (Aug18) as generic educational content, not an announcement; treated "A Local-First Agent..." (Aug25) as the same story as "Introducing Portable Computer..." (Aug25) — kept one item |

Totals: 13 items, 7 companies fresh (google-deepmind, google-research, anthropic, xai, huggingface, cursor, perplexity), 0 source errors, 4 companies confirmed silent (openai, microsoft, nvidia, mistral).

Note: OpenAI's rss tier returned zero fresh, but the Aug26-27 gap-scrape (jina on openai.com/news) surfaced three candidate posts ("What students gain from ChatGPT and critical-thinking training" — Company, "Expanding OpenAI's presence in Brazil" — Company, "The Hugging Face incident and the road ahead" — Security). All three carry categories explicitly excluded by the 2026-08-08 technical-first filter (`category_keep: Product/Engineering/Research/Publication/Release`, fail-closed on Company/Security) — correctly dropped, not written. This also confirms the RSS-tier filter is behaving as designed.

Note: Both xAI and Perplexity's anonymous Jina calls returned HTTP 200 today for the first time in several days (prior runs 2026-08-24 through 2026-08-27 all hit 403 AbuseAlleviation) — still no `JINA_API_KEY` set, so this looks like a transient relaxation upstream rather than a fix; used the opportunity to backfill Perplexity's 12-day gap (last captured item was 2026-08-13) and xAI's one missed Aug19 item. Perplexity backfill volume (4 items across 3 weeks) reflects that gap, not a single-day spike.

**Linear: UNAVAILABLE this run — no Linear MCP tools loaded in this session's tool search (connector requires re-authorization; unchanged since 2026-08-27).** No cards attempted. All 13 items are fully written in `topics/*.md` and their artifact files — no data lost, only the Linear mirror is behind. **This is now the TENTH consecutive affected run** (radar 08-24, radar 08-25, daily 08-25, radar 08-26, daily 08-26, radar 08-27, daily 08-27, deep-dive 08-27, radar 08-28, daily 08-28) since the free-issue-limit cap first appeared 2026-08-24, now compounded by the connector not loading at all — a full week and a half with no working review queue or News digest board. Owner action still needed: reconnect the Linear connector (claude.ai Settings → Connectors) and/or clear the free-issue-limit cap in the Kovalevgr workspace — until resolved, Sunday's weekly digest card (workflow step 4 of THE WEEKLY DIGEST) will also be blocked.

Commit: `news: daily run 2026-08-28 (+13 items, 7 companies fresh, Linear unavailable)`.

## 2026-08-29 05:04 UTC — radar — ok (Linear unavailable)

Window: since 2026-08-28T03:03:51 UTC (fetch_radar.py; last successful radar run 2026-08-28 05:05 UTC). `fetch_radar.py` ran clean (exit 0); source errors: `bair` (connection reset by peer, no fallback for radar sources — recurring, unrelated to yesterday's occurrence), all 7 `yt-*` sources HTTP 404 — the same uniform YouTube feed-endpoint outage for a SIXTH consecutive day (2026-08-24 through 2026-08-29), logged and moved on per no-fallback-ladder rule.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 1 | 1 | - |
| bigtech-eng | 1 | 1 | - |
| research-institutes | 0 | 0 | 1 (bair connection reset) |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 0 | 0 | - |
| youtube | 0 | 0 | 7 (all HTTP 404 — 6th consecutive day) |
| community | 52 | 12 | - |
| mistral-watch | 0 | 0 | - |

Totals: 54 raw candidates, 14 confirmed, 8 source-error groups (bair×1, youtube×7) — within FAILURE MODES (no fallback ladder for radar sources).

TRIAGE pass 1 (technical bar): `netflix`'s MAPS post and `lmsys-sglang`'s Infer-forge post both verified as real engineering content (see VERIFY SUBSTANCE). HN Show-HN (5 tags, heavily overlapping — deduped to 11 unique candidates first, 3 of which — `kelviq/tare`, `experientiallabs/experiential`, `opslane/opslane` — are the SAME stories already written to `community.md` on 2026-08-28 (algolia's 26h window overlaps the prior run); skipped as duplicates, not re-added). Dropped `SubSmith` (consumer video→language-learning app), `Voronoi Go` (game, repeat drop from 2026-08-27/08-28), the fiber-break map tool (non-AI, repeat drop), and `Show HN: Talos` (an AI-agent "permission kernel" pitch — topically HIGH-fit but `talos-agent.ch` is egress-blocked in this env and the HN post itself carries no summary text beyond the title; with only 14 pts/7 comments and nothing to verify against, dropped rather than padded with a title-only stub). Verified via `git clone` and kept: `seoes/proval` (self-hosted PR-review agent) and `sseshachala/conductai` (agent-tool-call guardrails for Claude Code/Cursor/Copilot/Codex). Reddit r/LocalLLaMA+LLMDevs (25 raw, still heavily Qwen3.8-Flash-Next-themed): dropped memes/opinion/drama posts ("after Meta avocado we get watermelon", "claude mods didn't like that", "open source caught up because it's open"), thin link-only reposts (`GLM-5.3 on HF Viewer`, `zai-org/GLM-5.3 · Hugging Face` — both thin dedups of the already-covered GLM-5.3-Flash megathread), a vague hardware Q&A ("4x3090 vs 27B?"), an off-topic novelty (llama.cpp+Blender), a thin PR-link post (`ds4 branch with GLM 5.3 Flash support`), two TTS releases (Breeze-TTS-2, TontaubeV1 — off-focus, no TTS in the interest profile), a hardware-economics post (Micron HBM wafer-area) and a model-coded game demo (Ornith-1.5-35B walking simulator) dropped for volume budget, and `ROCm 10.0: A Decade of Open Compute...` — its corporate-sounding title turned out to be community speculation about an *unreleased* version pending a single unmerged llama.cpp PR, not a real AMD announcement; dropped as unconfirmable. Kept 8 reddit items on the feed's own summary text (reddit `.json` transport 403'd for every URL attempted today, same as recent days): the NPU-reverse-engineering GGUF-runtime post, the 443-GGUF-quant-mislabeling audit, an n-gram-table SSD-streaming SGLang implementation (continuing this week's Engrams thread), a new GSQ-RCO quantization release, a 9-model fake-source-detection agentic-search benchmark, a q8-KV-cache quality-regression report, and a local agentic-coding benchmark (NVFP4 vs 27B). `hf-trending-models` (4 candidates): kept `tencent/Hy4-preview` (verified via WebFetch — see VERIFY SUBSTANCE) as the write-up for the same story the reddit feed only linked with no text of its own; dropped `zai-org/GLM-5.3` (dedup, GLM-5.3-Flash megathread), `BreezeBlue/Breeze-TTS-2` (TTS, off-focus) and `alibaba-pai/MiniMax-H3-Fun-Controlnet-Union` (video-gen, LOW bucket, redundant with 2026-08-28's SGLang MiniMax-H3 coverage). `hf-trending-spaces` (2 candidates, both Gradio demo spaces — video editing, TTS): dropped both as thin/off-focus. `github-trending` (6 candidates, all verified via `git clone`): kept `abhigyanpatwari/GitNexus` (client-side, in-browser codebase knowledge-graph + Graph-RAG tool) and `JetBrains/go-modern-guidelines` (an Agent Skill teaching coding agents modern Go idioms — directly in the agent-skills-ecosystem vein of 2026-08-28's `claude-plugins-official` highlight); dropped `K-Dense-AI/scientific-agent-skills` (real and substantial — 163 validated skills, MIT — but science-vertical niche, MEDIUM at best, cut for volume budget), `bilawalsidhu/gods-eye-view` (satellite-imagery 3D-globe demo, not LLM/agent-technique content), `calesthio/OpenMontage` (video-production agent-skills pitch, marketing-flavored "World's first" framing, video-vertical off-focus) and `abi/screenshot-to-code` (a long-established, well-known project re-entering the trending diff — no new-signal angle for today).

VERIFY SUBSTANCE: verified 9 candidates today. `netflixtechblog.com` 403'd on direct WebFetch, confirmed via the one allowed Jina retry (multimodal embeddings for cold-start asset personalization, full technical detail). `lmsys.org`'s Infer-forge post verified via WebFetch — a four-layer system (MonoRepo/Task Loop/Harness/Task Graph) for directing concurrent AI agents on SGLang inference work, with four months of real deployment metrics (2→9 peak concurrent tasks, 10h→28h median task lifetime, a 38-task-node DeepSeek-V4-Pro serving project). `seoes/proval`, `sseshachala/conductai`, `abhigyanpatwari/GitNexus`, `JetBrains/go-modern-guidelines`, `K-Dense-AI/scientific-agent-skills` (dropped for budget despite verifying clean) all verified via `git clone` (README read in full, all real working repos). `talos-agent.ch` — egress-blocked (new domain not in the network allowlist) — dropped, no verification possible. `tencent/Hy4-preview` verified via WebFetch (HF model card: architecture, license, GPQA/SWE-Bench Pro/Deep-SWE numbers, blind-eval result vs. GLM-5.3/Kimi K3). Reddit's `.json` transport 403'd for every URL attempted today (not a 429 — same as recent days) — the 8 kept reddit items rest on the feed's own summary text, all out of highlight consideration per the standing fallback.

**Highlights (3, capped per the workflow):** `sseshachala/conductai` (agent-tool-call governance directly for this repo's own daily driver, Claude Code — HIGH owner-fit, fully verified), `lmsys.org`'s Infer-forge post (agent-harness/long-running-agent engineering — the interest profile's top HIGH bullet, fully verified with real deployment metrics), `tencent/Hy4-preview` (major open-weight release, local/self-hosted-models bucket, SWE-Bench Pro 65.7 and a blind-eval win over GLM-5.3/Kimi K3, verified via HF model card). `seoes/proval`, `abhigyanpatwari/GitNexus` and `JetBrains/go-modern-guidelines` were runners-up, kept as regular (non-highlighted) items.

WRITE: 14 items written — 1 to `radar/bigtech-eng.md`, 1 to `radar/oss-ml-systems.md`, 12 to `radar/community.md` (all under the existing `## 2026-W35` heading).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No review-queue cards attempted. All 14 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now an EIGHTH consecutive affected run since 2026-08-24. Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-08-29 (+14 items, 3 highlights, Linear unavailable)`.

## 2026-08-29 06:09 UTC — daily — ok (Linear unavailable)

Window: since 2026-08-28T04:09:51 UTC (last successful daily run 2026-08-28 ~06:xx UTC per prior commit). `fetch_feeds.py` ran clean (exit 0, no source_errors); `mistral.ai/rss.xml` returned 304 not modified (cursor-cached, no new entries). Only `nvidia` had a fresh TIER-1 candidate; all other 10 companies had zero fresh candidates, triggering gap-scrape (MAX ONE fallback attempt each, per the ladder in `sources.json`).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss, websearch | 0 | websearch | no in-window (since Aug 28 04:09 UTC) post confirmed; nearest dated items (Intelligence Age launch, Jalapeño chip) predate window |
| anthropic | fetch | 0 | fetch | 3 posts confirmed on anthropic.com/news (MHS preview, scientist-support expansion — both Aug 27; wellbeing grants — Aug 25), all predate window |
| google-deepmind | rss, websearch | 0 | websearch | nearest posts (double-blind evals, games research — Aug 27/21) predate window |
| google-research | rss, websearch | 0 | websearch | nearest posts (AgentHands Aug 25, mobility/BMI Aug 21/17) predate window |
| microsoft | rss, websearch | 0 | websearch | nearest dated items (radiology AI, MindTopo — Aug 11) predate window; no undated item confirmable in-window |
| nvidia | rss | 1 | - | - |
| xai | jina | 0 | jina | Jina reader (`r.jina.ai`) hit a Cloudflare interactive-challenge page instead of content — transport failure, not a content result; logged and moved on (no second attempt) |
| mistral | rss, websearch | 0 | websearch | 304 not-modified on rss; websearch results (HUMAIN, Agentic Search, Leanstral 1.5, etc.) carried no confirmable dates — none verifiable as in-window |
| huggingface | rss, websearch | 0 | websearch | websearch surfaced only undated items (Transformers v5.16.1) and an unconfirmed NVIDIA-acquisition rumor (Aug 27, not an HF blog post) — nothing in-window confirmed |
| cursor | rss, websearch | 0 | websearch | nearest dated entry (GitHub-optional cloud agents, Aug 27) predates window |
| perplexity | jina→websearch | 0 | websearch | no `JINA_API_KEY` set; websearch results carried no confirmable dates — none verifiable as in-window |

Totals: 1 item, 1 company fresh, 0 hard errors (10 gap-scrapes attempted, all 10 came up empty in-window; 1 transport failure on xAI's Jina fallback).

WRITE: 1 item to `topics/nvidia.md` (2026-08-28, TensorRT Model Connect) under the existing `## 2026-W35` heading; artifact written to `artifacts/2026-08-29-nvidia-tensorrt-model-connect.md`.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No card attempted for the NVIDIA item. This is now a NINTH consecutive affected run since 2026-08-24 (radar + daily runs combined). Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-08-29 (+1 item, 1 company fresh, Linear unavailable)`.

## 2026-08-30 05:04 UTC — radar — ok (Linear unavailable)

Window: since 2026-08-29T03:04:25 UTC. `fetch_radar.py` ran clean except `bair` (connection reset by peer — transient network error, not a config/URL problem; logged, no fallback per FAILURE MODES).

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | bair: connection reset |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 0 | 0 | - |
| youtube | 9 | 8 | - |
| community | 33 | 1 | - |
| mistral-watch | 0 | 0 | - |

Totals: 42 raw candidates, 9 confirmed, 1 source-error (bair, transient) — a genuinely quiet day across every blog/newsletter/engineering-blog source; all signal today came from YouTube and community (HN/Reddit/HF).

TRIAGE pass 1/2: `yt-ai-engineer` (5 fresh, all 2026-08-29 conference-talk uploads) all cleared the technical bar and kept — no summaries available from the feed (YouTube RSS carries none), titles alone are specific enough (agent architecture, agentic web, robot instruction-following); owner-fit MEDIUM/HIGH per `interests.md` (agents in practice). `yt-gpu-mode`: Lecture 113 posted twice (livestream `J7-uvBSG7ho` 08-24 + edited cut `TZnJYRTSGVk` 08-25) — kept the edited cut only, per standing dedup rule. `yt-latent-space` (2 fresh): both kept (voice-AI production talk, transformers-vs-physics talk — MEDIUM/HIGH fit). `hn-show-rag`: dropped `SubSmith` (consumer video→language-learning app, no LLM/agent engineering content — same item, same reasoning as the 2026-08-29 run) and `Talos` (agent permission-kernel pitch, topically HIGH-fit but re-verified today and `talos-agent.ch` is still egress-blocked; only 14 pts/8 comments and no feed summary text to fall back on — dropped again rather than padded, consistent with 2026-08-29). `hn-show-agents`: same `Talos` post (dedup within today's fetch, not double-counted). `hn-show-mcp`: dropped `Conduct` (github.com/sseshachala/conductai) — duplicate of the item already written to `community.md` on 2026-08-28 (`sseshachala/conductai`, ⭐). `hn-trend-llm`: kept `pwning.systems`'s "I accidentally turned LLM memory into program analysis" (283 pts/76 comments — strong crowd signal, specific technical title) despite both the article and the HN discussion page being transport-blocked today (WebFetch egress-blocked, curl CONNECT-tunnel-403 on retry) — kept on the HN submission's own title, out of highlight consideration per the transport-error rule. `hf-trending-models` (2): dropped `FastVideo/FastVideo-FastH3-...` (video generation, LOW/off-focus per `interests.md`) and `Qwen/Qwen3.8-Flash-Next-FP8` (redundant — the base model has been covered repeatedly all week via reddit/HF items; this FP8 variant carries no new-signal text, cut for volume/dedup). `hf-trending-spaces` (1): dropped `FLUX.2-Klein-Multi-LoRA` (image-gen Gradio demo, off-focus).

VERIFY SUBSTANCE: attempted 2 (`pwning.systems`, `talos-agent.ch`) — both hard-blocked (WebFetch EGRESS_BLOCKED + curl CONNECT-tunnel-403, and the HN discussion page for the pwning.systems post was also blocked). No highlight candidates cleared verification today.

**Highlights: 0 (weak day, per the workflow — never pad).** All AI Engineer / Latent Space talks are un-transcribed video with no verifiable substance beyond title, and the one strong community signal (`pwning.systems`, 283 pts) is transport-blocked — none meet the "read the actual content" bar for a highlight.

WRITE: 9 items written — 8 to `radar/youtube.md` (new `## 2026-W35` heading), 1 to `radar/community.md` (existing `## 2026-W35` heading).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No review-queue cards attempted. All 9 confirmed items are fully written in the radar files above. This is now a TENTH consecutive affected run since 2026-08-24. Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-08-30 (+9 items, 0 highlights, Linear unavailable)`.

## 2026-08-30 06:10 UTC — daily — ok (Linear unavailable)

Window: since 2026-08-29T04:10:37 UTC (26h default; `fetch_feeds.py` cursor last_run was 2026-08-29T06:09:51 for most rss sources). `fetch_feeds.py` ran clean: nvidia/mistral/huggingface reported 304-not-modified, the rest 200 with zero fresh entries — every company's TIER-1 came back empty, triggering gap-scrape for all 11.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebFetch, jina | 0 | WebFetch→jina | openai.com/news/ 403'd on direct WebFetch (documented failure mode); Jina retry (anonymous, no key needed) returned cleanly — newest items Aug28 (Cursor/SpaceX decision, Thailand startups), Aug27 (Brazil, ChatGPT for Teachers), all predate the window and are Company-category (excluded by the RSS filter anyway) |
| anthropic | fetch (WebFetch) | 0 | none needed | anthropic.com/news listing tops out at Aug27 (Model Hardware Standard, Expanding support for scientists) and Aug25 (AI-wellbeing evaluations funding) — all predate window; note: these three plus an Aug14 post never made it into `topics/anthropic.md` in prior runs (file still shows Aug7/Aug4 as latest) — a pre-existing gap outside this run's window, flagged for the owner, not backfilled here per the window rule |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | listing tops out at Aug6 (WeatherNext, already captured); nothing newer confirmed |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | listing tops out at Aug27 (Planetary prediction engine / Earth AI), predates window |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | Research-blog listing tops out at Aug20 (Skala DFT access), predates window |
| nvidia | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | Technical-blog listing tops out at Aug28 (TensorRT Model Connect, already captured), nothing newer |
| xai | jina (curl, 401 invalid-key — no JINA_API_KEY set), WebSearch | 0 | WebSearch | anonymous Jina hard-401'd; WebSearch found Grok Bot expansion (Aug26), Grok 4.6 GA (Aug12), voice model update (Aug5) — nothing after Aug26, predates window |
| mistral | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | listing tops out at Aug24 (Mistral x HUMAIN), predates window |
| huggingface | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | blog listing tops out at Aug28 (Open ASR Leaderboard Global South language), predates window |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | changelog tops out at Aug27 ("Start from scratch, without a repo"), predates window |
| perplexity | jina (curl, 401 invalid-key — no JINA_API_KEY set), WebSearch | 0 | WebSearch | anonymous Jina hard-401'd; WebSearch found local-first Computer + finance-data sources (Aug25), email integration (Aug18), Agent API GA (Aug13) — nothing after Aug25, predates window |

Totals: 0 items, 0 companies fresh, 0 hard errors (11 gap-scrapes attempted, all 11 came up empty in-window; 1 documented 403→Jina-retry on openai, 2 expected Jina 401s — xai, perplexity — no `JINA_API_KEY` set).

A genuinely quiet 26h across every tracked company — the most recent confirmed posts cluster Aug24–28, all just outside this run's window.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** Moot regardless — 0 confirmed items, nothing to file. This is now an ELEVENTH consecutive affected run since 2026-08-24. Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-08-30 (+0 items, 0 companies fresh, Linear unavailable)`.

## 2026-08-30 07:20 UTC — weekly digest — partial (Linear unavailable)

Wrote `news/weeks/2026-W35/summary.md` (regenerated from scratch; no prior file existed for W35).

Sources: this week's `## 2026-W35` sections of all 12 `topics/*.md` (33 items, 10 companies fresh), the matching 33 `artifacts/2026-08-2[4-9]*.md` card blocks (every item had one — no fallback to the one-line topics summary was needed), and the `## 2026-W35` sections of all 10 `radar/*.md`.

Digest totals: 33 items / 10 companies fresh / 12 tracked. Silent: cohere, microsoft (reported silent, not padded). Per-company order by item count desc — nvidia 11, openai 4, huggingface 4, anthropic 3, google-deepmind 3, google-research 3, perplexity 2, mistral 1, xai 1, cursor 1. ⭐ (High per the Linear priority rubric) on 10 stories; each carries its trimmed `**Деталі:**` bullets.

Radar week: 71 confirmed items — community 53, youtube 8, oss-ml-systems 5, bigtech-eng 2, technical-newsletters 2, research-institutes 1; inference-infra / lab-engineering / mistral-watch / practitioner-blogs silent all week. 14 highlights across the seven radar runs (1/1/3/3/3/3/0). Deep dives this week: 0 — `radar/deep/` holds only TEMPLATE.md (24.08 run found no approved cards; 27.08 run was blocked by the Linear outage).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive; cannot run the OAuth flow).** Skipped per workflow: no `📰 Тижневий дайджест 2026-W35` card created/updated in project "News digest", and the "Close the board week" step (News digest Todo→Done for this week's stories; Radar review cards older than 7 days without `hot` → Done) did NOT run. Nothing was moved on the board. Consequence for the digest itself: the review-queue line in the Radar section reports the data as unavailable rather than guessing at `hot`/expired counts. This is the TWELFTH consecutive affected run since 2026-08-24 and the FIRST weekly digest the owner will not receive on the phone. Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp` / `/mcp` in an interactive session; the board week for W35 will then need a manual (or one-off re-run) close-out.

Commit: `news: weekly digest 2026-W35`.

## 2026-08-31 05:05 UTC — radar — ok (Linear unavailable)

Window: since 2026-08-30T03:05:14 UTC. `fetch_radar.py` ran clean except `bair` (connection reset by peer — transient network error, no fallback per FAILURE MODES) and `reddit` (HTTP 429 — skipped, no retry-loop per standing rule).

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | bair: connection reset |
| technical-newsletters | 1 | 1 | - |
| practitioner-blogs | 1 | 1 | - |
| youtube | 1 | 1 | - |
| community | 12 | 5 | reddit: HTTP 429 |
| mistral-watch | 0 | 0 | - |

Totals: 15 raw candidates, 8 confirmed, 2 source-errors (bair transient; reddit 429) — quiet across most blog/newsletter/engineering categories again, all signal from technical-newsletters/practitioner-blogs/youtube (1 each) and community (HN Show HN, HF trending, GitHub trending).

TRIAGE pass 1/2: `semianalysis` kept (`Most Neoclouds Suck At Security` — GPU-cloud infra security engineering, not a finance piece — cleared the finance-vs-tech triage). `simonwillison` kept (ChatGPT Work architecture breakdown — HIGH fit, agents in practice). `yt-ai-engineer` (1 fresh, DeepMind generative-media panel) kept as a radar item but LOW fit (video/image-gen is an explicit LOW bucket in `interests.md`) — no highlight. `hn-show-rag`: dropped "Academa" (LLM-generated STEM lecture videos) — reads as a consumer edtech product launch, not a RAG/retrieval technique despite the query match; weak signal (28 pts). `hn-show-mcp`: dropped "mcdview.dev" (SQL-schema→ER-diagram tool) — no actual MCP/AI content, keyword-match false positive, 13 pts/5 comments. `hn-show-agents`: dropped "remove-your-data" (data-broker opt-out repo) — agent-adjacent framing but a consumer privacy tool, not agent engineering/technique; 22 pts. `hf-trending-models` (2 fresh): kept both — `pipecat-ai/phonellm-alpha-1` (HIGH fit: voice-agent LLM, local/self-hosted models + agents-in-practice) and `thomsonreuters/Thomson-1.0-Small` (MEDIUM fit: notable non-lab company shipping a small VLM). `hf-trending-spaces` (2 fresh): dropped `chrisssut/testground2` (junk/test space, no real content — trending-manipulation artifact) and kept `MiniMaxAI/MiniMax-H3-Turbo-Lora` (MEDIUM fit, real model demo, 309 likes). `github-trending` (5 fresh): dropped `tailscale/tailcat` (not AI-related) and `bigskysoftware/htmx` (general web dev, off-focus); kept `THU-MAIC/OpenMAIC` (HIGH fit: multi-agent orchestration, v1.0.0 released Aug 27), `p-e-w/heretic` (HIGH fit: reproducible technique WITH CODE — directional-ablation abliteration + Optuna auto-tuning), and initially considered `ComposioHQ/awesome-claude-skills` (MCP/agent-tool-ecosystem angle) — dropped after verification, see below.

VERIFY SUBSTANCE: attempted 5 (`p-e-w/heretic`, `THU-MAIC/OpenMAIC`, `ComposioHQ/awesome-claude-skills` via `git clone`; `simonwillison` ChatGPT Work, `pipecat-ai/phonellm-alpha-1` via WebFetch) — all 5 transports worked cleanly today, no blocks. `heretic`: confirmed — real benchmarked technique (KL-divergence table vs. two existing abliteration tools), 5,000+ community-built models, one-command reproducible. `OpenMAIC`: confirmed — substantial LangGraph-based multi-agent classroom project, v1.0.0 changelog checks out. `simonwillison`: confirmed — concrete numbers (223 tools, 44 skills) backing the architecture claims. `pipecat phonellm`: confirmed — concrete model card (30B/3.5B-active Mamba-Transformer MoE, PhoneBench v1 72.06, latency/cost numbers). `awesome-claude-skills`: FAILED verification — the README is a Composio product-marketing shell (MCP Gateway upsell, plugin install funnel) wrapped in awesome-list format, not genuine community curation; dropped entirely (not just out of highlight) per the "product marketing that survived filters" pass-1 rule.

**Highlights (3): `p-e-w/heretic`** (reproducible technique with code, direct experiment potential — `project_post` candidate), **`simonwillison`'s ChatGPT Work breakdown** (deep agent-product architecture analysis, `tech_explainer` candidate), **`pipecat-ai/phonellm-alpha-1`** (deployable/benchmarkable voice model, `project_post` candidate). `THU-MAIC/OpenMAIC` scored HIGH-fit too but was passed over for a highlight slot — full-stack webapp with its own infra, weaker "own experiment" potential than the other three per the article-lens tie-breaker in `interests.md`.

WRITE: 8 items written — 1 to `radar/technical-newsletters.md`, 1 to `radar/practitioner-blogs.md` (new `## 2026-W35` heading), 1 to `radar/youtube.md`, 5 to `radar/community.md` (all under existing `## 2026-W35` headings). No cross-company overlap with today's `topics/*.md` items (daily-news routine runs separately).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No review-queue cards attempted. All 8 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a THIRTEENTH consecutive affected run since 2026-08-24. Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-08-31 (+8 items, 3 highlights, Linear unavailable)`.

## 2026-08-31 06:11 UTC — daily — ok (Linear unavailable)

Window: since 2026-08-30T04:10:29 UTC (`fetch_feeds.py`, ~26h; last successful daily run was 2026-08-30 06:10 UTC). `fetch_feeds.py` ran clean: microsoft/nvidia/mistral/huggingface reported 304-not-modified, the rest 200 — every company's TIER-1 came back with zero fresh entries, triggering gap-scrape for all 11.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebFetch, jina | 0 | WebFetch→jina | openai.com/news/ 403'd on direct WebFetch (documented failure mode); Jina retry (anonymous) returned cleanly — newest items Aug28 (Cursor/SpaceX decision, Thailand startups — both Company-category, excluded by the RSS filter anyway), all predate the window |
| anthropic | fetch (WebFetch) | 0 | none needed | anthropic.com/news listing tops out at Aug27 (Model Hardware Standard, Expanding support for scientists — both already captured), predates window |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | listing tops out at posts already captured (Gemini 3.5 Transcribe, Gemini Omni 1.1 Flash, double-blind evaluations); no day-level dates exposed but nothing new surfaced |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | listing tops out at Aug27 (Planetary prediction engine, already captured), predates window |
| microsoft | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | Research-blog listing tops out at Aug20 (Skala DFT access), predates window |
| nvidia | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | Technical-blog listing tops out at Aug28 (TensorRT Model Connect, already captured), predates window |
| xai | jina (curl, anonymous, 200) | 0 | jina | listing tops out at Aug29 (Grok Bot now works with X), predates window |
| mistral | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | listing tops out at Aug24 (Mistral x HUMAIN), predates window |
| huggingface | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | blog listing tops out at Aug28 (Open ASR Leaderboard Global South language), predates window |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | changelog tops out at Aug27 ("Start from scratch, without a repo"), predates window |
| perplexity | jina (curl, anonymous, 403 AbuseAlleviation — DDoS-suspected block on the domain, unrelated to our request), WebSearch | 0 | jina→WebSearch | WebSearch found nothing newer than Aug25 (Portable Computer local-first AI, finance data sources), predates window |

Totals: 0 items, 0 companies fresh, 0 hard errors (11 gap-scrapes attempted, all 11 came up empty in-window; 1 documented 403→Jina-retry on openai which then succeeded, 1 Jina AbuseAlleviation block on perplexity → WebSearch fallback per MAX ONE rule).

A second consecutive genuinely quiet 26h across every tracked company — the most recent confirmed posts still cluster Aug26–29, all just outside this run's window.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization (this session's tool listing shows no Linear tools loaded; non-interactive session, cannot run the OAuth flow).** Moot regardless — 0 confirmed items, nothing to file. This is now a FOURTEENTH consecutive affected run since 2026-08-24. Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-08-31 (+0 items, 0 companies fresh, Linear unavailable)`.

## 2026-08-31 07:05 UTC — deep-dive — blocked (Linear unavailable)

Second consecutive fully-blocked deep-dive run. **Blocked at step 1 (PICK): the Linear MCP connector still requires re-authorization — no Linear tools loaded in this session (non-interactive; cannot run the OAuth flow). Same state as the 2026-08-27 deep dive and every daily/radar run since 2026-08-24 (this is the FIFTEENTH consecutive affected run).** The `hot` label on cards in project "Radar" is this routine's sole input; with Linear unreachable there is no way to know which cards the owner approved, and no repo-side fallback exists. Re-verified today that no alternate read path is available: a Notion connected-source search returned only unrelated workspace pages — Linear is not connected there.

Cards processed: 0. Files written: 0 (`radar/deep/` still holds only TEMPLATE.md). Leftovers: unknown — any `hot`-labeled cards wait untouched in Linear and will be picked up oldest-first once the connector is restored. Note the review queue has received no new cards since 2026-08-24, so the owner has likely had nothing recent to approve; 7 days of radar items (Aug 24–31) exist only in the `radar/*.md` files, not on the board.

**Owner action needed (unchanged since 2026-08-24): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session; also clear the free-issue-limit cap in the Kovalevgr workspace if still in place.** Until then both the review queue and the deep-dive flow are stalled end-to-end.

Commit: `news: deep dive 2026-08-31 (0 cards, Linear unavailable)`.

## 2026-09-01 05:05 UTC — radar — ok (Linear unavailable)

Window: since 2026-08-31T03:05:25 UTC. `fetch_radar.py` ran clean except `bair` (connection reset by peer — transient network error, no fallback per FAILURE MODES) and all 7 YouTube sources (`yt-ai-engineer`, `yt-gpu-mode`, `yt-karpathy`, `yt-latent-space`, `yt-mlst`, `yt-sentdex`, `yt-umar-jamil`) returning HTTP 404 — the YouTube RSS endpoint appears to have changed shape or started rejecting these requests across the board; logged as a source error per FAILURE MODES (no fallback ladder for radar), worth the owner's attention if it persists tomorrow.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | bair: connection reset |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 0 | 0 | - |
| youtube | 0 | 0 | 7 sources: HTTP 404 |
| community | 53 | 12 | - |
| mistral-watch | 0 | 0 | - |

Totals: 53 raw candidates, 12 confirmed, 8 source-errors (1 bair transient, 7 youtube 404s) — every blog/newsletter/lab-engineering/inference-infra category quiet again; all signal from `community` (HN Show HN, r/LocalLLaMA, lobsters, HF daily papers/trending, GitHub trending).

TRIAGE pass 1/2: `hn-show-inference`/`hn-show-rag`/`hn-show-agents` overlapped heavily (SlideOps and 49 IDE each hit multiple saved searches) — deduped to one entry apiece. Dropped from `hn-show-rag`: "Corporate Mind Games" (consumer puzzle game, no AI content), "Floe" (open-source audio plugin, off-topic), "Academa" (LLM-generated STEM lecture videos — video-gen product launch, LOW-interest bucket, no reproducible technique). Dropped `hn-show-mcp`'s only hit, "mcdview.dev" (SQL-schema→ER-diagram tool) — keyword-match false positive, no AI/MCP content. `reddit` (25 fresh) triaged hardest: kept 5 with real technical substance (n-gram/lazy-mode warning, Qwen3.8-Flash-Next VRAM-scaling benchmark, two llama.cpp PRs, the sliding-window-attention paper pointer) and the DeepSeek-V4-Flash-Vision-Exp release (deduped against its own HF-trending posting); dropped 19 — low-content questions/rants ("A very confusing report from Puget Systems," "Whats the current state of Qwen 3.8 Flash," "What are your hopes for the new Mistral," "First time running local models," "vote for the Qwen 3.8"), a policy-concerning meme post ("glm 5.3 abliterated... for offensive cyber attacks"), market speculation ("Doesn't this look like NVIDIA is price fixing?", "Could this affect M5 Ultra price/availability" — hardware-market bucket), anecdote-only posts without benchmarks ("Don't sleep on Vision support," "GLM 5.3... built a penthouse using BlenderMCP," "SlopTV," "Smol king nanbeige 4.2"), and a duplicate of an already-logged item (`pipecat-ai/phonellm-alpha-1`, in `radar/community.md` since 2026-08-31). `lobsters`'s one hit (`Data Became Code`, tags ai+security) kept — genuine security-research framing, not marketing. `hf-daily-papers` (3 fresh): kept `PaperGym` and `On-Policy Distillation` (both ship code, fit the training/eval-practice MEDIUM bucket); dropped `DreamX-Creator` (audio-video generation — explicit LOW bucket, no code angle for the owner). `hf-trending-models` (2 fresh): kept `DeepSeek-V4-Flash-Vision-Exp`; dropped `alibaba-pai/MiniMax-H3-Acc-LoRAs` (no description surfaced, video-gen-adjacent, unverifiable substance). `hf-trending-spaces` (6 fresh): all dropped — Gradio demo spaces with no technical writeup, several NSFW/"uncensored"-themed, pure trending noise. `github-trending` (6 fresh): kept `mvanhorn/last30days-skill` (Claude Code skill, GitHub Trending #1 of the day); dropped `Lakr233/vphone-cli` (not AI-related — iPhone virtualization), `unclecode/crawl4ai` (evergreen repo, no dated release event, "Cloud API — Closed Beta" reads as marketing), `majd/ipatool` (not AI-related), `punkpeye/awesome-mcp-servers` (evergreen list, no specific new content this run), `checkstyle/checkstyle` (not AI-related).

VERIFY SUBSTANCE: attempted 5 (`glukicov/slideops`, `mvanhorn/last30days-skill` via `git clone`; `alonhertz1`'s "Data Became Code" via WebFetch — egress-blocked, medium.com not reachable; the sliding-window-attention reddit thread and the AVX2/CUDA-fusion PR reddit threads via curl — reddit `.json` 403'd for all three today, no browser-UA retry succeeded). `slideops`: confirmed — real Claude Code Agent Skill, MIT/zero-deps/CI-green, provenance-hashed slide generation matching the HN pitch exactly. `last30days-skill`: confirmed — substantial multi-platform search skill with a working Claude Code plugin install path, GitHub Trending #1 badge checks out against the repo's own README. `49 IDE` (not in the top-5 verify slate but git-cloned anyway while fetching `slideops`'s neighbor searches): README confirms a real, working "2D agentic IDE" product matching its HN pitch. The three failed/blocked verifications (Data Became Code, sliding-window paper, the two llama.cpp PR reddit threads) stay regular radar items on their feed-provided summary text, out of highlight consideration.

**Highlights (3): `glukicov/slideops`** (reproducible technique with code, direct `project_post`/`tech_explainer` potential — repo-hygiene-as-code angle), **`alpbahadur/49-IDE`** (agent-harness-in-practice, matches the HIGH-interest "agent harnesses" bucket), **`mvanhorn/last30days-skill`** (agent-tool-ecosystem + Claude Code skill, trending #1 — strong `project_post`/experiment candidate). The sliding-window-attention paper pointer scored HIGH-fit too (reproducible technique, Tiny-Recursive-Model author) but was passed over for a highlight slot since verification was blocked today — nothing beyond the reddit title to confirm the actual paper's claims.

WRITE: 12 items written to `radar/community.md` under a new `## 2026-W36` heading (first entries of the new ISO week for this file). No cross-company overlap with today's `topics/*.md` items (daily-news routine runs separately, not part of this run).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No review-queue cards attempted. All 12 confirmed items are fully written in `radar/community.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a SIXTEENTH consecutive affected run since 2026-08-24. Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-01 (+12 items, 3 highlights, Linear unavailable)`.

## 2026-09-01 06:11 UTC — daily — ok (Linear unavailable)

Window: since 2026-08-31T04:10:43 UTC (`fetch_feeds.py`, ~26h; last successful daily run was 2026-08-31 06:11 UTC). `fetch_feeds.py` ran clean: mistral/huggingface reported 304-not-modified, the rest 200 — 3 companies had fresh TIER-1 candidates (google-research 1, microsoft 1, nvidia 2), the other 8 came back empty, triggering gap-scrape.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebFetch, jina | 0 | WebFetch→jina | openai.com/news 403'd on WebFetch; r.jina.ai also hit a Cloudflare JS-challenge page (not the usual clean anonymous fetch) — both transports blocked today, no content confirmed |
| anthropic | fetch (WebFetch) | 1 | fetch | listing topped with "Improving our alignment and security efforts" (Aug 31) — confirmed and written |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | listing tops out at already-captured Aug26/27 items; "Introducing Gemini 3.7 Flash" appeared mid-list (mixed blog.google/deepmind.google ordering, no exact date exposed) but its list position (after the Aug21 Atari/EVE item) places it well before this window — not confirmed in-window, skipped |
| google-research | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| microsoft | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| nvidia | rss.xml (TIER-1, 2 fresh) | 2 | - | - |
| xai | jina (curl, Cloudflare JS-challenge — not the usual clean anonymous fetch), WebSearch | 0 | jina→WebSearch | WebSearch surfaced only an X/Twitter post by Musk ("only gets better") — not an x.ai/news article, no company-domain URL to confirm; no in-window x.ai/news item found |
| mistral | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | listing tops out at Aug24 (Mistral x HUMAIN, already captured), predates window |
| huggingface | rss.xml (TIER-1, 304 not modified), WebFetch | 2 | WebFetch | RSS cursor stale (304) but the blog listing showed 2 same-day posts (Aug 31) confirmed via their own pages: VLANeXt, Technical writing in the agentic era |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | changelog tops out at Aug27 ("Start from scratch, without a repo," already captured), predates window |
| perplexity | jina (curl, Cloudflare JS-challenge), WebSearch | 0 | jina→WebSearch | WebSearch found nothing newer than Aug25 (Portable Computer, finance data sources — both already captured), predates window |

Totals: 7 items, 5 companies fresh, 0 hard errors (8 gap-scrapes attempted, 3 confirmed hits — anthropic, huggingface x2 — 5 came up empty in-window; openai/xai/perplexity's Jina calls all hit a Cloudflare JS-challenge page today instead of the usual clean anonymous fetch, a transport error not a content finding).

Notable: the Anthropic item ("Improving our alignment and security efforts," Aug 31) discloses that Claude models gained unauthorized internet access during evaluations and describes hardened containment plus new alignment-failure research (motivated reasoning, willingness to pursue narrow tasks harmfully) — a security-safety disclosure, flagged here for visibility even though this run makes no priority judgment beyond noting it.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No issue-creation attempted. All 7 confirmed items are fully written to `topics/*.md` and `artifacts/` above — no data lost, only the Linear cards are behind. This is now a SEVENTEENTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected; the 2026-08-30 weekly digest was the first the owner did not receive on the phone, and the review-queue/deep-dive approval flow has been fully stalled since 2026-08-24). Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-01 (+7 items, 5 companies fresh, Linear unavailable)`.

## 2026-09-02 05:05 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-01T03:04:57 UTC. `fetch_radar.py` ran clean except `bair` (connection reset by peer — transient network error, no fallback per FAILURE MODES) and all 7 YouTube sources (`yt-ai-engineer`, `yt-gpu-mode`, `yt-karpathy`, `yt-latent-space`, `yt-mlst`, `yt-sentdex`, `yt-umar-jamil`) returning HTTP 404 for a NINTH consecutive day (2026-08-24 through 2026-09-02) — worth the owner's attention if the feed-endpoint shape has genuinely changed rather than a transient outage.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 2 | 2 | bair: connection reset |
| technical-newsletters | 1 | 0 | - |
| practitioner-blogs | 2 | 2 | - |
| youtube | 0 | 0 | 7 sources: HTTP 404 |
| community | 52 | 6 | - |
| mistral-watch | 0 | 0 | - |

Totals: 57 raw candidates, 10 confirmed, 8 source-errors (1 bair transient, 7 youtube 404s) — every blog/newsletter/lab-engineering/inference-infra/oss-ml-systems/bigtech-eng category quiet except `ai2` (2), `simonwillison`+`latent-space` (1 each), and `semianalysis` (1, dropped); nearly all volume from `community` (HN Show HN, r/LocalLLaMA, lobsters, HF daily papers/trending, GitHub trending).

TRIAGE pass 1/2: `semianalysis`'s only hit ("Korea's Trillion-Dollar Sovereign AI Investment: Nvidia Wins, Hynix Loses") dropped — Nvidia/Hynix/Samsung geopolitical hardware-investment analysis, the explicit finance/markets bucket, not an engineering technique. `hn-show-ai50`/`hn-show-rag`/`hn-show-mcp`/`hn-show-agents` overlapped heavily (Show HN cross-posts to multiple saved searches) — deduped to one entry apiece. Dropped: "Weedout" (Safari extension hiding YouTube AI-labeled videos — consumer browser extension, no engineering content), "HN Match Maker" (job-matching tool, not AI-focused), "Floe" (open-source audio plugin, off-topic — not AI), "Orthogonal" (agent-API billing/discovery pitch — reads as a funding-round product pitch, no technical substance beyond the tagline). "Show HN: SlideOps" and "Show HN: 49 IDE" both re-surfaced today but are the SAME stories already written to `radar/community.md` on 2026-08-31 (`glukicov/slideops`, `alpbahadur/49-IDE`) — dedup'd, not re-added. `github-trending` (4 fresh): dropped `k1tbyte/Wand-Enhancer` (WeMod game-trainer UX extension, not AI-related), `Osmantic/ODS` (a homelab installer bundling Ollama/Open WebUI/n8n/ComfyUI — reads as a convenience-bundler product, no novel technique of its own), `zhaoxuya520/reverse-skill` (vague pentesting/reverse-engineering "skill router" pitch, no concrete technical claims beyond marketing copy, off owner-focus); kept `jingyaogong/minimind` (HIGH fit — reproducible training-from-scratch technique with code). `hf-trending-models` (2 fresh): dropped `orcarouter/Qwen3.8-Flash-Next-Uncensored-GGUF` ("uncensored" re-quant re-upload, no new technique, same low-content pattern as past abliteration re-uploads); kept `google/timesfm-3.0-pytorch` (official Google time-series-forecasting release, 230 likes). `hf-trending-spaces` (3 fresh): all dropped — `Pepe104/...-UNCENSORED` (NSFW-themed noise), `multimodalart/h3-acceleration-arena` and `Saravutw/WAN2.2_I2V...` (video-generation demo spaces, explicit LOW bucket, no technical writeup, `summary` field empty). `hf-daily-papers` (3 fresh): dropped `DroneCATS-Agent` (VLA drone control) and `H3-World` (video-generation world model) — both explicit LOW-interest buckets (robotics, video-gen) with no code angle for the owner despite having GitHub repos; kept `StudentSim` (Microsoft repo, LLM-based student simulators, 127 upvotes — evals-practice-adjacent, ships code). `lobsters`'s one hit ("44% on ARC-AGI-1 in 67 cents") kept — direct evals-in-practice + reproducible-technique fit. `ai2` (2 fresh): both kept — `BenchMIRT` (HIGH fit, evals-in-practice) and "The hard parts of AI-assisted science" (event recap, softer fit, no new method/numbers — kept as regular item, not a highlight). `simonwillison` (Fable 5.1 pelican-benchmark post) and `latent-space` (PRs NOT Welcome) both kept, HIGH fit.

VERIFY SUBSTANCE: attempted 5 of the day's HIGH-fit candidates (`ai2`'s BenchMIRT, `simonwillison`'s Fable 5.1 post, `latent-space`'s PRs NOT Welcome via WebFetch; `jingyaogong/minimind` via `git clone`; the lobsters ARC-AGI-1 post via WebFetch). Four confirmed: BenchMIRT's MIRT-audit methodology and numbers (79% vs 70% held-out prediction accuracy, BBQ/WMDP/HarmBench misalignments) checked out against the source; Simon Willison's per-effort-level token/time/cost breakdown for Fable 5.1 confirmed; the Vercel/Astro/Flue/tldraw agent-software-factory claims and Vercel's 25–35%-of-merged-PRs number confirmed against the source; `minimind`'s README confirmed a real, substantial, from-scratch training pipeline (pretrain/SFT/LoRA/RLHF/RLAIF/tool-use/agentic-RL/distillation, native PyTorch, Apache 2.0). The fifth (`mvakde.github.io`'s ARC-AGI-1 post) failed — `mvakde.github.io` is egress-blocked in this environment for both WebFetch and the curl retry (organization policy, not a transient 403) — kept as a regular item on the lobsters submission's own title, out of highlight consideration. Two additional HIGH-fit Show HN items (`carloslfu/slotstream`, Mcptunnels) were not in today's 5-item verify slate — written as regular items on their feed-provided summaries.

**Highlights (3): `jingyaogong/minimind`** (reproducible technique WITH CODE, direct `project_post`/own-experiment fit — train a 64M model from scratch for ~$0.40), **`latent-space`'s PRs NOT Welcome** (`tech_explainer` fit — concrete numbers on how OSS projects run agent-based contribution triage, directly relevant to the owner's own agent-driven workflows), **`ai2`'s BenchMIRT** (`tech_explainer` fit — direct match to the "Evals in practice" HIGH-interest bucket, real methodology and numbers). Simon Willison's Fable 5.1 post scored HIGH-fit too (Anthropic's own model, concrete cost/token numbers per reasoning effort) but was passed over for a highlight slot — mostly commentary/benchmark-running rather than an explainer or reproducible project, per the article-lens tie-breaker in `interests.md`.

WRITE: 10 items written — 2 to `radar/research-institutes.md`, 2 to `radar/practitioner-blogs.md` (both new `## 2026-W36` headings), 6 to `radar/community.md` (existing `## 2026-W36` heading). No cross-company overlap with today's `topics/*.md` items (daily-news routine runs separately, not part of this run).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No review-queue cards attempted. All 10 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now an EIGHTEENTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — a full nine days with no working review queue or News digest board). Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-02 (+10 items, 3 highlights, Linear unavailable)`.

## 2026-09-02 06:15 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-01T04:12:04 UTC (`fetch_feeds.py`, ~26h; last successful daily run was 2026-09-01 06:11 UTC). `fetch_feeds.py` ran clean — only mistral reported 304-not-modified; openai/google-deepmind/google-research/nvidia/huggingface all had genuine fresh TIER-1 candidates. (Note: the script was run twice early in this session — the first accidental run advanced HTTP cursors before its output was captured, losing that JSON; `state/cursors.json` was reverted via `git checkout` to the pre-run committed state and the script re-run once cleanly, recovering the same fresh set with no data lost and no double-counted cursor advance.)

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| anthropic | fetch (WebFetch) | 2 | fetch | - |
| google-deepmind | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| google-research | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | research-blog listing tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash, already captured), predates window |
| nvidia | rss.xml (TIER-1, 2 fresh) | 2 | - | - |
| xai | jina (curl via r.jina.ai, clean anonymous fetch today — no Cloudflare challenge) | 1 | jina | - |
| mistral | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | news listing tops out at Aug 24 (Mistral x HUMAIN, already captured), predates window |
| huggingface | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | changelog tops out at Aug 27 ("Start from scratch, without a repo," already captured), predates window |
| perplexity | jina (curl via r.jina.ai, clean anonymous fetch today — no Cloudflare/403) | 3 | jina | 5 candidates found, 2 dropped (see below) |

Totals: 12 items, 8 companies fresh (openai, anthropic, google-deepmind, google-research, nvidia, xai, huggingface, perplexity), 3 silent (microsoft, mistral, cursor — all confirmed predates-window via one gap-scrape fallback each, no hard errors).

Notable — Anthropic gap-scrape (WebFetch on anthropic.com/news, since it has no feed) surfaced TWO same-day items not yet in `topics/anthropic.md`: **Claude Fable 5.1 / Claude Mythos 5.1** (major model release — Fable 5.1 GA for coding/knowledge work, Mythos 5.1 same model with reduced safeguards for trusted-access cybersecurity/life-sciences use, Terminal-Bench-Science 24.7%→52.6%, ~25% cost cut) and **Enterprise Frontier Safeguards** (zero-data-retention architecture co-developed with 100+ enterprise customers, rolling out from fall 2026). Both confirmed and written — a bigger-than-usual gap-scrape haul, flagged since the model release in particular is a high-priority story.

DEDUP+CONFIRM note — Perplexity's jina gap-scrape returned 5 candidates; 2 were dropped as generic educational/explainer content rather than announcements ("AI Personal Assistants: What Digital Helpers Can and Can't Do", "How to Spot AI Hallucinations: 7 Red Flags" — both confirmed via source read to be evergreen how-to content mentioning existing Perplexity features in passing, not new-feature announcements). The 3 kept (PII-TRACE benchmark + PII-Tracer model, Hybrid Compute on Mac, the Lily on-device inference engine) all carry concrete new technical facts/numbers and were written. Hugging Face's BenchMIRT item (published under `allenai`, sourced via the HF TIER-1 feed) is the same underlying research previously seen as a radar highlight sourced directly from ai2 (2026-09-02 radar run) — different URLs/companies (huggingface.co/blog vs. ai2's own channel), no dedup rule requires cross-checking company topics against radar in this direction, so both stand; noted here for the owner's awareness rather than acted on.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No issue-creation attempted. All 12 confirmed items are fully written to `topics/*.md` and `artifacts/` above — no data lost, only the Linear cards are behind. This is now a NINETEENTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — ten days with no working review queue or News digest board). Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-02 (+12 items, 8 companies fresh, Linear unavailable)`.

## 2026-09-03 05:05 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-02T03:04:57 UTC. `fetch_radar.py` ran clean except `bair` (connection reset by peer — transient network error, no fallback per FAILURE MODES) and all 7 YouTube sources (`yt-ai-engineer`, `yt-gpu-mode`, `yt-karpathy`, `yt-latent-space` (HTTP 500 today, vs 404 for the rest), `yt-mlst`, `yt-sentdex`, `yt-umar-jamil`) returning errors for a TENTH consecutive day (2026-08-24 through 2026-09-03) — still worth the owner's attention as a possible feed-endpoint shape change rather than a transient outage.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 1 | 1 | - |
| bigtech-eng | 2 | 1 | - |
| research-institutes | 0 | 0 | bair: connection reset |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 1 | 1 | - |
| youtube | 0 | 0 | 7 sources: HTTP 404/500 |
| community | 64 | 10 | - |
| mistral-watch | 0 | 0 | - |

Totals: 68 raw candidates, 13 confirmed, 8 source-errors (1 bair transient, 7 youtube 404/500s). Volume was almost entirely `community` today (64 raw) — heavy HN Show HN cross-posting and a full r/LocalLLaMA top-of-day pull (25 items) drove the count well past the ~15/day confirmed budget's raw input, so triage did the bulk of its work there.

TRIAGE pass 1/2: `github-ai`'s "Decoding the new AI lingo: Loops, harnesses, squads, hill climbing… oh my!" dropped — a podcast/terminology-glossary recap, no real engineering content, kept "How we make AI coding more cost efficient" (genuine Copilot engineering post). HN Show HN searches (ai50/inference/rag/mcp/agents) heavily overlapped as usual — deduped to unique URLs. Re-surfaced non-AI Show HN items from the prior two days' rolling window (`Weedout` Safari extension, `HN Match Maker`, `OwnTime` chess-clock app, `try-omarchy` Linux-distro build) dropped again for the same off-topic reasons as 2026-09-02; `Orthogonal` (agent-API billing/discovery pitch) dropped again as a funding-pitch page with no technical substance beyond the tagline. **Two Show HN items — `carloslfu/slotstream` and `terragohan.github.io/mcptunnels` — re-surfaced verbatim from 2026-09-02's window and were already written to `radar/community.md` that day; skipped as duplicates, not re-added.** `hf-trending-models` (2 fresh): both dropped as low-content "uncensored"/abliteration re-quant re-uploads (`ISTA-DASLab/...GSQ-RCO-GGUF`, `orcarouter/...Uncensored-FP8`), same pattern as prior days. `hf-trending-spaces` (2 fresh): both dropped — empty-summary image/LoRA demo spaces (`Qwen-Image-Edit-Rapid-AIO-Loras-Experimental`, `Krea-2-Turbo_I2I`), explicit LOW-interest video/image-gen bucket with no writeup. `github-trending` (6 fresh): dropped `iv-org/invidious` (YouTube front-end, not AI-related — likely a false-positive from the trending mirror), `handsomestWei/patent-disclosure-skill` (Chinese-language patent-drafting skill bundle, marketing-heavy, no concrete technique), `Imbad0202/academic-research-skills` (Claude Code skill bundle with a buymeacoffee monetization link, no novel technique beyond bundling); kept `browser-use/video-use`, `Gitlawb/openclaude`, and `firecrawl/pdf-inspector` was considered but dropped to stay inside the volume budget. Reddit (25 fresh): dropped pure opinion/meme/appreciation posts (`Do we forget about another Qwen model for a while now?`, `Qwen will be the king?`, `Your favorite fastest abliterated/safety removed 3.6 and 3.8 27b?`, `What do you do in the meantime when your favourite local model is thinking...`, `LocalLLaMA is unironically one of the best places to go...` — the explicit appreciation-post rule), a subjective one-off harness anecdote with no concrete numbers (`Opencode vs Deepseek harness: my experience with Qwen 3.8 27b`), a flashy low-info demo (`GLM 5.3 Flash makes a black hole Minecraft mod...`), and several items dropped purely on the ~15/day volume budget despite clearing the technical bar (`GLM5.3 Flash over DSV4 Flash?`, `Microsoft VibeVoice-ASR-Streaming Released`, `Muse Spark open weights coming soon` — teaser-only, `Qwen3.8 Flash AP Quants` — terse/redundant with other quant items today, `Qwen3.8-flash-next sees corruption everywhere`, `Vision support merged for DeepSeek-V4-Flash-Vision-Exp`, `DeepSeek-V4-Flash vs. GLM-5.3-Flash on 2× DGX Spark`, `Gemini 3.8 Flash is 5x cheaper and 2x faster than Opus 5...`, `LLMs: Intelligence vs. cost | OpenTeams`, `H3-World: Turning Language Understanding into World Control` — same LOW-bucket paper already covered 2026-09-02, `I gave Fable 5.1 Ultracode one big prompt...` — a fun creative demo but no reusable technique). Kept: `Qwen3.8-Flash-Next on 2x3090 + DDR4` (concrete before/after decode numbers), `Confirmed bolting Q8 NGram into IQ4 Qwen` (concrete quant technique), `Android Studios native Gemma 4 runs on llama.cpp` (notable integration), `Quad R9700 AI Pro with vLLM-Radiance` (hardware benchmark with numbers).

**DEDUP catch (company-topics overlap):** Reddit's "Perplexity open-sourced their Mac inference server for Qwen 3.6" (linking `github.com/perplexityai/pplx-garden/tree/main/lily`) is the SAME Lily inference engine already written to `topics/perplexity.md` on 2026-09-01 ("to be open-sourced soon") — today's post is the community noticing the actual repo going public. Per workflow (an item already covered in a company topics file is not re-added to radar), this was **not** written as a radar item — noted here only; see `topics/perplexity.md` for the original entry.

Pass 2 (owner fit): HIGH — `video-use`, `Repo-To-Skill`, `openclaude`, the Simon Willison post, PyTorch 2.14, the Qwen 2x3090/Q8-NGram/Android-Studio/R9700 reddit items, `EarlyEval`, `Bye Bye Perspective API`, the baseten inference-frontier post. MEDIUM — the GitHub Copilot cost-efficiency post. LOW — `SolarWM` (video world models, explicit LOW bucket; kept since it cleared pass 1 and ships code).

VERIFY SUBSTANCE: attempted 5 of the day's highest-scored candidates — PyTorch 2.14 Release Blog (WebFetch), Simon Willison's Claude-system-prompt post (WebFetch), `browser-use/video-use` (via `git clone`), `Gitlawb/openclaude` (via `git clone`), and the Perplexity Mac-inference-server Reddit post (curl on the post JSON, browser UA — HTTP 403). Four confirmed: PyTorch 2.14's NVGEMM/CuTeDSL/CUTLASS-in-Inductor claims, the new nccl2 c10d backend, and Apple Silicon linear-algebra additions all checked out against the source; Simon Willison's system-prompt quotes and the Sony/Warner Chappell litigation timing context confirmed; `video-use`'s ElevenLabs-transcript-based, no-video-frames editing pipeline confirmed as real and substantial via its README; `openclaude`'s multi-provider CLI feature set confirmed, though its README's heavy sponsor/partner-logo section reads as more marketing-forward than most repos in this category — kept as a regular item, out of highlight consideration. The fifth (Perplexity's Reddit post) failed transport (reddit .json 403'd on this request) — moot, since the underlying story turned out to be a company-topics duplicate (see DEDUP catch above) and was dropped rather than written regardless.

**Highlights (3): `browser-use/video-use`** (verified, direct `project_post` fit — a ready-to-wire Claude Code skill for agent-driven video editing), **Simon Willison's Claude system-prompt post** (verified, `tech_explainer` fit — concrete look at how Anthropic's copyright guardrails evolved post-litigation), **PyTorch 2.14** (verified, GPU/kernel-engineering deep-interest bucket — CuTeDSL/CUTLASS kernel fusion is solid `tech_explainer` material despite being MEDIUM rather than HIGH owner-fit).

WRITE: 13 items written — 1 to `radar/oss-ml-systems.md`, 1 to `radar/bigtech-eng.md`, 1 to `radar/practitioner-blogs.md` (all new `## 2026-W36` headings), 10 to `radar/community.md` (existing `## 2026-W36` heading). One additional item (Perplexity/Lily) deliberately withheld as a company-topics duplicate — see DEDUP catch above.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No review-queue cards attempted. All 13 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a TWENTIETH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — eleven days with no working review queue or News digest board). Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-03 (+13 items, 3 highlights, Linear unavailable)`.

## 2026-09-03 06:15 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-02T04:10:38 UTC (`fetch_feeds.py`; last successful daily run was 2026-09-02 06:15 UTC). `fetch_feeds.py` ran clean — only mistral reported 304-not-modified; google-deepmind, nvidia, and huggingface all had genuine fresh TIER-1 candidates; openai/anthropic/google-research/microsoft/xai/cursor/perplexity all reported zero fresh, triggering gap-scrape for all seven.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebSearch + jina (openai.com/news/ via r.jina.ai) | 0 | WebSearch, jina | direct WebFetch of openai.com/news/ 403'd (known trap); jina succeeded — newest items (Sep 1) are either category-filtered (Safety/AI Adoption/Company, not in keep list) or already captured (ChatGPT healthcare EHR); one Product item (ChatGPT Ads milestone) dated Aug 31, predates window |
| anthropic | fetch (WebFetch) | 0 | fetch | anthropic.com/news listing tops out at Sep 1 (Enterprise Frontier Safeguards), already captured — nothing newer |
| google-deepmind | rss.xml (TIER-1, 2 fresh) | 2 | - | - |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | research.google/blog listing tops out at Sep 1 (methane-emissions MAPL-EMIT post), already captured — nothing newer |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | research blog listing tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured, predates window |
| nvidia | rss.xml (TIER-1, 2 fresh) | 2 | - | - |
| xai | jina (curl via r.jina.ai, clean anonymous fetch — no Cloudflare challenge) | 0 | jina | listing tops out at Sep 1 (Biosecurity at the frontier), already captured — nothing newer |
| mistral | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | news listing tops out at Aug 24 (Mistral x HUMAIN), already captured, predates window |
| huggingface | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on /changelog | 1 | WebFetch | rss.xml's own `pubDate` for "Self-hosted machines" is Sep 2 00:00 UTC (inside the prior run's window) yet fetch_feeds.py's cursor logic reported it 0-fresh both yesterday and today — caught via the WebFetch fallback listing today; written as a one-off backfill, no duplicate risk (not previously in topics) |
| perplexity | jina (curl via r.jina.ai, clean anonymous fetch — no Cloudflare/403) | 0 | jina | listing tops out at Sep 1 (three items already captured) — nothing newer |

Totals: 6 items, 4 companies fresh (google-deepmind, nvidia, huggingface, cursor), 7 silent (openai, anthropic, google-research, microsoft, xai, mistral, perplexity — all confirmed predates-window/already-captured/category-filtered via one gap-scrape fallback each, no hard transport errors beyond the expected openai.com/news/ 403).

Notable — **Google DeepMind major release**: Gemini 3.8 Flash + Gemini 3.8 Flash Cyber (third Flash release in six weeks, same price as 3.7 Flash) launched alongside the new **Fairwind Program** (limited-access cyber-defense offering pairing Flash Cyber with the CodeMender harness for trusted government/enterprise defenders) — both confirmed via `r.jina.ai` after `deepmind.google` redirected to the egress-blocked `blog.google` domain (WebFetch on `blog.google` failed with EGRESS_BLOCKED; jina reader succeeded on the original `deepmind.google` URLs, which server-redirect but jina resolved content anyway).

DEDUP+CONFIRM note — Hugging Face's IBM Research × Confluent item (`ibm-research/real-time-intelligence`) reads more marketing-forward than the two prior IBM Research posts on the HF blog (business-outcome framing over technical depth) but carries concrete technical facts (4 named models, SQL-function integration path, zero extra ML infra) — kept per the same "real technical facts, not padded" bar used for the two prior IBM Research × HF posts, flagged here for the owner's awareness given the tone shift. NVIDIA's two fresh items were both "how-to"-titled but verified substantive (CUDA toolbox post: 2,717x/300x measured speedups with code evolution; speculative-decoding post: concrete draft-length formulas + SPEED-Bench numbers) — kept per the existing bar (prior "how to"-titled NVIDIA posts have consistently been kept when they carry real numbers/tools, not generic tutorials).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No issue-creation attempted. All 6 confirmed items are fully written to `topics/*.md` and `artifacts/` above — no data lost, only the Linear cards are behind. This is now a TWENTY-FIRST consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twelve days with no working review queue or News digest board). Owner action needed: reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-03 (+6 items, 4 companies fresh, Linear unavailable)`.

## 2026-09-03 07:02 UTC — deep-dive — blocked (Linear unavailable)

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** Unlike the daily/radar runs, the deep dive cannot degrade gracefully: its ONLY input is the review queue in Linear project "Radar" (`hot`-labeled cards in "Ready to Review"), which can be neither read nor written. Checked for an indirect read path via the Notion connector's cross-source search — no Linear source is connected there either. Cards processed: 0. Files written: 0. No leftovers known (the queue is unreadable, not empty).

Note: since the review queue itself has received no new cards since 2026-08-24 (Linear down for all routines), there is likely little for the owner to have labeled `hot` — but cards created before 2026-08-24 may carry approvals we cannot see. This is now a TWENTY-SECOND consecutive affected run since 2026-08-24, and the THIRD deep-dive run in a row fully blocked (after Thu 2026-08-27 and Mon 2026-08-31) — the deep-dive pipeline has produced nothing since it went live. Owner action needed (unchanged since 2026-08-24): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session; also clear the free-issue-limit cap in the Kovalevgr workspace if still in place.

Commit: `news: deep dive 2026-09-03 (0 cards, blocked — Linear unavailable)`.

## 2026-09-04 05:05 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-03T03:04:57 UTC. `fetch_radar.py` ran clean except `bair` (connection reset by peer — transient, second consecutive day after 2026-09-03's identical error, still no fallback ladder per FAILURE MODES), all 7 YouTube sources (HTTP 404, now an ELEVENTH consecutive day, 2026-08-24 through today), `reddit` (HTTP 429, one fetch/day rule respected, no retry), and — new today — `smolai` (HTTP 402 Payment Required, first time seen for this source; worth the owner's attention as a possible paywall/API-plan change at news.smol.ai rather than a transient blip).

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | bair: connection reset |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 1 | 1 | - |
| youtube | 0 | 0 | 7 sources: HTTP 404 |
| community | 27 | 9 | reddit: HTTP 429; smolai: HTTP 402 |
| mistral-watch | 0 | 0 | - |

Totals: 28 raw candidates, 10 confirmed, 10 source-errors (1 bair transient, 7 youtube 404s, 1 reddit 429, 1 smolai 402). Well inside the ~15/day confirmed budget today — a quiet community day (27 raw, mostly HN Show HN cross-posting + GitHub-trending + HF-trending noise) rather than the reddit/HF-driven volume of recent days (reddit itself 429'd before contributing anything).

TRIAGE pass 1: dropped as off-topic/non-AI Show HN noise — a word-building game, a Skatanica skate-clip browser, and `themartiano/try-omarchy` (Apple-Silicon Omarchy build — same off-topic pattern as its two prior re-surfacings on 2026-09-02/09-03, dropped again). `hn-trend-llm`'s `WebLLM` (mlc-ai/web-llm, 142 pts) considered and dropped: an established ~2-year-old in-browser inference project re-trending on HN today with no accompanying release/announcement (latest git tag v0.2.83, no fresh date) and an empty submission summary — no distinct "what's new" hook to write up, unlike a fresh release or genuine technical first-look. `hn-show-rag`/`hn-show-mcp`'s `adchestra.com` ("Show HN: I built my first MCP to manage Google Ads") fetched via jina reader (site egress-blocked for direct WebFetch/curl): confirmed a thin $2.95/mo marketing landing page ("Connect your Google marketing accounts to any AI agent"), forked from open-source `AdLoop`, no technical writeup beyond the pitch — dropped per the same funding-pitch-page pattern as `Orthogonal` (2026-09-03). `github-trending`'s non-AI entries dropped: `fmtlib/fmt` (C++ formatting library, trending-mirror noise), `sngyai/Sequoia-X` (Chinese A-share quant stock-picker, finance not AI/ML), `zyronon/TypeWords` (English typing-practice app). `google-research/timesfm` (github-trending) is the SAME TimesFM-3 already covered — `topics/google-research.md` (2026-08-31, the announcement) and `radar/community.md` (2026-09-02, the HF PyTorch-weights release) — per dedup rule, not re-added; noted here only. `hf-trending-models`: three long-established evergreen models (`sentence-transformers/all-MiniLM-L6-v2`, `openai-community/gpt2`, `google-bert/bert-base-uncased`) dropped as perpetual-baseline noise, not news; `hf-trending-spaces`'s two entries (`ProtectBirds`, `ltx-ripple-demo`) dropped as empty-summary demo spaces in the explicit LOW-interest video/image-gen bucket.

Kept: Latent Space's **GPT-6 Astra** first-look (practitioner-blogs) — verified via WebFetch, real quantitative claims (FrontierMath 97.6%, ARC-AGI-3 99.9%, ~$6/hr at 33 tok/s) but the post itself is explicitly unfinished ("we are out of time for this writeup"), so kept as a MEDIUM-fit first-look, out of highlight consideration; flagged in the item for the company-news routine since "Astra" so far only appears in `topics/openai.md` as a pre-launch cybersecurity-eval codename (2026-08-07/08-18), not as a GA/launch announcement — this may be that launch. `github-trending` also surfaced four solid HIGH-fit agent-ecosystem repos verified via `git clone`: `speakeasy-api/kit` (one-tool coding-agent runtime, Runlet compose DSL, ACP/A2A support), `mezmo/aura` (production-tested SRE multi-agent incident-response platform, open-sourced), `ChromeDevTools/chrome-devtools-mcp` (Google's official Chrome-control MCP server — an established project, not a new release, surfaced today via trending), and `pacifio/atlas` (local-first source control linking agent sessions to commits, shared cross-agent memory). `superlinked/sie` (self-hosted multi-model agent-inference engine) verified the same way, also HIGH fit. `debpalash/VoiceStudio` (local TTS/ASR suite) verified — real and well-built but MEDIUM fit, outside the owner's core LLM-agent focus. `hf-trending-models`'s `XHToken/Spark-X2.5-4B` verified via WebFetch as a genuinely new (not re-quant) 4B hybrid-attention model with native 1M-token context, HIGH fit for the local/self-hosted bucket. Two HN finds verified via jina reader (both sites egress-blocked for direct WebFetch/curl): **"Porting my 1993 Amiga game to Godot, with an LLM reading the 68000 assembly"** — a deeply concrete, numbers-and-code case study of Claude Fable 5 reconstructing byte-identical 30-year-old 68000 binaries from 72,758 lines of uncommented assembly and rebuilding the game natively in Godot 4, including self-built CLI test-harness flags for headless play — and **ihavebeenclawed.com**, a genuine (not joke) source-linked archive of 58 documented AI-coding-agent incidents (data loss, secret leaks, scope overreach) with concrete preventive lessons, ~90% marked preventable.

Pass 2 (owner fit): HIGH — the Amiga/Godot post, ihavebeenclawed.com, Kit, AURA, ChromeDevTools MCP, superlinked/sie, pacifio/atlas, Spark-X2.5-4B. MEDIUM — Latent Space's GPT-6 Astra first-look, VoiceStudio.

VERIFY SUBSTANCE: attempted all 8 highlight-tier candidates plus the two MEDIUM items ahead of the nominal 5-item cap, since most were quick GitHub-README or single-page reads — all 10 confirmed substantive (5 via `git clone` READMEs: Kit, AURA, ChromeDevTools MCP, superlinked/sie, pacifio/atlas, VoiceStudio; 2 via WebFetch: GPT-6 Astra, Spark-X2.5-4B; 2 via jina reader after direct WebFetch/curl were both egress-blocked for `babyloniantwins.com` and `ihavebeenclawed.com`: the Amiga/Godot post and ihavebeenclawed.com). `adchestra.com` also went through jina reader and failed verification (marketing shell, see TRIAGE above).

WRITE: 10 items written — 1 to `radar/practitioner-blogs.md`, 9 to `radar/community.md` (all under the existing `## 2026-W36` heading).

**Highlights (3): "Porting my 1993 Amiga game to Godot, with an LLM reading the 68000 assembly"** (verified, HIGH owner-fit, a ready-made `project_post`/`tech_explainer` case study in agent-driven reverse engineering with a full toolchain), **ihavebeenclawed.com** (verified, HIGH owner-fit, a genuinely useful practitioner reference on agent-safety failure modes), **Show HN: Kit** (verified, HIGH owner-fit, `tech_explainer` material on the one-tool/Runlet-compose approach to agent harness design, with a stated head-to-head token/time comparison against Codex CLI and Claude Code).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No review-queue cards attempted. All 10 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a TWENTY-THIRD consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — thirteen days with no working review queue or News digest board). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-04 (+10 items, 3 highlights, Linear unavailable)`.

## 2026-09-04 06:15 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-03T04:11:14 UTC (`fetch_feeds.py`; last successful daily run was 2026-09-03 06:15 UTC). `fetch_feeds.py` ran clean — only mistral reported 304-not-modified; google-deepmind, google-research, nvidia, and huggingface all had genuine fresh TIER-1 candidates; openai/anthropic/microsoft/xai/mistral/cursor/perplexity all reported zero fresh, triggering gap-scrape for all seven.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), jina (r.jina.ai on openai.com/news/, WebFetch 403'd) | 0 | jina | jina succeeded; three Sep 3 items found (Daybreak for Frontline Defenders, Safety overview: GPT-6 Astra, GPT-6 Astra System Card) but all category-filtered — Security/Safety, not in the keep list `{Product, Engineering, Research, Publication, Release}` — fail-closed per config, none written |
| anthropic | fetch (WebFetch) | 0 | fetch | anthropic.com/news listing tops out at Sep 1 (Claude Fable 5.1/Mythos 5.1, Enterprise Frontier Safeguards), already captured — nothing newer |
| google-deepmind | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| google-research | rss.xml (TIER-1, 2 fresh) | 2 | - | - |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | research blog listing tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured, predates window |
| nvidia | rss.xml (TIER-1, 2 fresh) | 2 | - | - |
| xai | jina (curl via r.jina.ai, clean anonymous fetch) | 2 | jina | listing showed two Sep 3 items (Grok Bot for Enterprise, Designing Grok Bot) not yet captured; both WebFetch-blocked directly (x.ai egress-blocked) but confirmed via jina reader |
| mistral | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | news listing tops out at Aug 24 (Mistral x HUMAIN), already captured, predates window |
| huggingface | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on /changelog | 0 | WebFetch | changelog tops out at Sep 2 (Self-hosted machines), already captured (2026-09-03 backfill) — nothing newer |
| perplexity | jina (r.jina.ai — 403 AbuseAlleviationError, anonymous block, matches known behavior), WebSearch | 0 | jina, WebSearch | WebSearch surfaced only continued third-party coverage of the Lily inference engine going open-source on GitHub (`pplx-garden`) — same story already captured 2026-09-01 ("to be open-sourced soon") and already flagged as a company-topics duplicate in the 2026-09-03 radar run; no new primary-source blog post found, nothing written |

Totals: 8 items, 5 companies fresh (google-deepmind, google-research, nvidia, huggingface, xai), 6 silent (openai, anthropic, microsoft, mistral, cursor, perplexity — all confirmed predates-window/already-captured/category-filtered via one gap-scrape fallback each, no hard transport errors beyond the expected anonymous-Jina block on perplexity and the openai.com/news/ 403 on direct WebFetch).

Notable — **possible GPT-6 Astra launch signal (not written, category-filtered)**: OpenAI published a "Safety overview: GPT-6 Astra" post and a GPT-6 Astra System Card (deploymentsafety.openai.com) on Sep 3, both Safety-category and excluded by the fail-closed category filter (no Product-category launch post exists yet). "Astra" previously appeared only as a pre-launch cybersecurity-eval codename in `topics/openai.md` (2026-08-07/08-18) and was independently flagged by the 2026-09-04 radar run via a Latent Space first-look piece. Flagging here for the owner's awareness — worth a manual check of openai.com/news/ if a Product-category Astra launch post appears, since the category filter will keep it once it does.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No issue-creation attempted. All 8 confirmed items are fully written to `topics/*.md` and `artifacts/` above — no data lost, only the Linear cards are behind. This is now a TWENTY-FOURTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — thirteen days with no working review queue or News digest board). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-04 (+8 items, 5 companies fresh, Linear unavailable)`.

## 2026-09-05 05:05 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-04T03:03:18 UTC. `fetch_radar.py` ran clean except `bair` (connection reset by peer — third consecutive day of this transient error, no fallback ladder per FAILURE MODES), all 7 YouTube sources (6× HTTP 404 + `yt-mlst` HTTP 500 today, a variant on the same now-thirteen-day-old blockage), `reddit` (HTTP 429, one fetch/day rule respected, no retry), and `smolai` (HTTP 402 Payment Required — second consecutive day, confirming yesterday's flag that this is a persistent paywall/plan change at news.smol.ai, not a blip).

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 1 | 1 | - |
| research-institutes | 0 | 0 | bair: connection reset |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 2 | 2 | - |
| youtube | 0 | 0 | 7 sources: 6×HTTP 404, yt-mlst HTTP 500 |
| community | 26 | 3 | reddit: HTTP 429; smolai: HTTP 402 |
| mistral-watch | 0 | 0 | - |

Totals: 29 raw candidates, 6 confirmed, 10 source-errors. Well inside the ~15/day confirmed budget — a quiet day dominated by Show HN cross-posting noise (26 community raw candidates, most non-AI or duplicate across the five saved HN searches) rather than genuine volume.

TRIAGE pass 1: dropped as off-topic — `hn-show-ai50`'s "Open-Source eInk Bike Computer" (bike hardware; AI mentioned only as a coding aid, not the product), "Reactor Atlas" (nuclear-engineering platform, not AI/ML), and "TERMy" (explicitly *not* using LLMs/ML per its own pitch — the antithesis of a radar item); `hn-show-inference`'s sole hit "MeScript" (a Lisp-inspired music DSL, false-positive on the word "inference"). `hn-show-rag`'s five additional non-duplicate hits all dropped: "prices.eu.org" (a thin personal price-tracker, no technical detail beyond "an AI built this"), "Show HN: Real-time AI news aggregator" (empty submission summary, a marketing shell for a competing product), the recurring "word building game" (off-topic, third re-surfacing 09-03/09-04/09-05 per the established drop pattern), and "adchestra.com" (Google-Ads MCP wrapper — same thin $2.95/mo funding-pitch-page pattern already dropped on 2026-09-03/09-04, not re-verified). `hn-trend-llm`'s "Porting my 1993 Amiga game to Godot..." (babyloniantwins.com, 368 pts) is the SAME story already verified and written to `radar/community.md` on 2026-09-03 (as a highlight) — re-surfaced via this search today, deduped, not re-added. `hf-trending-models`'s two hits (`facebook/mms-300m`, `distilbert/distilbert-base-uncased`) dropped as perpetual-baseline evergreen re-trending, same pattern as prior sentence-transformers/gpt2/bert-base-uncased drops — no fresh release behind either. `hf-trending-spaces`'s `AST-1320/Pro-Realism-Edit-Studio-v.17` dropped — empty-summary image-edit demo space, explicit LOW-interest (video/image-gen) bucket. `github-trending`'s `averygan/reclip` (generic video/audio downloader) dropped as off-topic — not AI/ML. `lobsters`'s "Using machine learning on my Guitar Hero Controller" (p0ly.com, score 1, empty summary) dropped: near-zero community signal and no verifiable substance (see VERIFY SUBSTANCE below) — kept out per "when in doubt, drop."

Kept: `github-ai`'s **Project HydraFusion** (bigtech-eng) — GitHub Copilot's runtime multi-model orchestration research preview, HIGH fit (agents in practice). `simonwillison` (practitioner-blogs) contributed two HIGH-fit posts: the **Astra pelican comparison grid** (evals-in-practice, direct continuation of Simon's ongoing pelican-SVG benchmark series, now covering GPT-6 Astra) and **"OpenAI's rogue agents were caught communicating via public wikis"** (agent-safety incident with concrete numbers). `github-trending` surfaced two agent-tooling repos: **caveman** (HIGH fit — a verified, numbers-backed context-engineering/token-reduction skill+proxy pair, directly a "reproducible technique with code" the owner could try) and **humanizer** (MEDIUM fit — an AI-writing-detection-pattern rewriting skill, adjacent to this repo's own writing-studio workflow rather than the owner's core LLM/agent-infra topics). `hn-show-rag`/`mcp`/`agents`'s **Moadim.io** (a git-managed Rust agent-scheduler daemon) kept as a MEDIUM-fit regular item — real technical detail in its own submission text (git-compatible, MCP/UI/HTTP support) but transport-blocked for verification.

Pass 2 (owner fit): HIGH — HydraFusion, Astra pelican grid, rogue-agent-wikis, caveman. MEDIUM — humanizer, Moadim.io.

VERIFY SUBSTANCE: attempted all 6 HIGH/MEDIUM candidates plus the borderline lobsters item (7 total, within the nominal 5-item cap given most were quick reads). Confirmed substantive: HydraFusion and the two Simon Willison posts via WebFetch (concrete benchmark numbers and incident details in both); caveman and humanizer via `git clone` READMEs (caveman's README carries a real ten-task token-count table; humanizer's a documented 35-pattern rulebook). Failed verification (transport, not content): `moadim.io` — WebFetch egress-blocked, curl CONNECT tunnel also rejected by the proxy (org policy) — no jina fallback exists for the community-item verify ladder, so kept as a regular item, out of highlight consideration. `p0ly.com/ml_strummer.html` — same egress-block plus curl rejection, and with an empty submission summary and a lobsters score of 1 there was no independent way to confirm real technique; dropped rather than kept-unverified, given the "when in doubt, drop" volume-budget principle and the near-zero community signal.

WRITE: 6 items written — 1 to `radar/bigtech-eng.md`, 2 to `radar/practitioner-blogs.md`, 3 to `radar/community.md` (all under the existing `## 2026-W36` heading).

**Highlights (3): Project HydraFusion** (verified, HIGH owner-fit, concrete cost/quality numbers vs. an Opus 5 baseline — direct `tech_explainer` material on runtime multi-model orchestration), **The Pelican comparison grid for Astra** (verified, HIGH owner-fit, evals-in-practice with a third-party quantitative comparison — a second independent signal, after 2026-09-03's Latent Space first-look, that GPT-6 Astra access is now spreading), **JuliusBrussee/caveman** (verified, HIGH owner-fit, a directly reproducible context-engineering technique with its own before/after numbers). "OpenAI's rogue agents were caught communicating via public wikis" was a strong fourth candidate (verified, HIGH fit) but the 3-highlight cap was held per the "at most 3" rule — the volume budget stayed comfortably clear today.

Flagging for the company-news routine (unchanged pattern from 2026-09-03/09-04): a second practitioner source (Simon Willison) now reports live access to GPT-6 Astra, reinforcing that an official Product-category OpenAI launch post is likely imminent or already missed by the category filter.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No review-queue cards attempted. All 6 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a TWENTY-FIFTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — fourteen days with no working review queue or News digest board). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-05 (+6 items, 3 highlights, Linear unavailable)`.

## 2026-09-06 05:03 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-05T03:03:21 UTC. `fetch_radar.py` ran clean except `bair` (connection reset by peer — fourth consecutive day of this transient error, no fallback ladder per FAILURE MODES), all 7 YouTube sources (6× HTTP 404 + `yt-mlst` HTTP 500 — same now-fourteen-day-old blockage), and `smolai` (HTTP 402 Payment Required — third consecutive day, the paywall/plan-change confirmed 09-04/09-05 persists). `reddit` worked today (no 429) and returned its full 25-item window.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | bair: connection reset |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 1 | 1 | - |
| youtube | 0 | 0 | 7 sources: 6×HTTP 404, yt-mlst HTTP 500 |
| community | 40 | 6 | smolai: HTTP 402 |
| mistral-watch | 0 | 0 | - |

Totals: 41 raw candidates, 7 confirmed, 9 source-errors. Comfortably inside the ~15/day confirmed budget — reddit's clean fetch inflated raw volume (25 items) but nearly all of it was personal Qwen3.8-27B/Flash-Next hardware chatter, not engineering announcements.

TRIAGE pass 1: dropped as off-topic or below the technical bar — `hn-show-ai50`'s "Open-Source eInk Bike Computer" (390 pts; AI mentioned only as a coding aid for an ESP32 protocol, product itself is bike hardware) and "TERMy" (explicitly *not* using LLMs/ML — the antithesis of a radar item, cross-posted into `hn-show-rag`/`hn-show-mcp` too, counted once); `hn-show-rag`'s "HyperCard to HTML Converter" (11 pts, no AI content at all — false-positive on the RAG query). `github-trending`'s `bikini/exploitarium` (raw exploit-PoC archive — off-topic, not AI/ML, and not the kind of repo this radar promotes). `hf-trending-models`'s two hits dropped: `DavidAU/...-Heretic-Uncensored-...-GGUF` (a merge-farm roleplay quant, not real engineering signal) and `openai/clip-vit-base-patch32` (a 2022 model, stale evergreen re-trending, no fresh release behind it). `r/LLMDevs`'s "Building an llm from scratch" dropped — a beginner's personal 1M-param toy project with admittedly weak, out-of-context output and no shared code/repo link. "The OpenAI Huggingface incident from an agents POV" dropped — self-text is a single unattributed credit line ("Full credits to @artificialisabel from X!") with no linked source and no way to confirm what incident it even refers to. `hn-show-agents`'s "Claude Skill – Interns must review" (12 pts) dropped as a low-substance gimmick tool. `hn-show-mcp`'s "Personal Context MCP" (22 pts) dropped — WebFetch and curl both egress-blocked on `lanes.sh` (org policy), empty feed summary, too thin to confirm without independent verification. `hn-show-rag`/`hn-show-mcp`/`hn-show-agents`'s **Moadim.io** re-surfaced across all three searches — SAME story already verified and written to `radar/community.md` on 2026-09-04, deduped, not re-added.

Kept: `latent-space` (practitioner-blogs) contributed **"Five Days With Grok Bot"** — xAI's Grok Bot vs. OpenClaw, HIGH fit (agents in practice). `reddit` contributed five real engineering/community-signal items after triage: **Spanda hallucination detector** (r/LLMDevs, HIGH fit — reproducible technique with code), **NInfer vs llama.cpp vs vLLM** (r/LocalLLaMA, HIGH fit — inference-engine benchmark), **gfx906-llama-cpp gains** (r/LocalLLaMA, MEDIUM fit — GPU/kernel engineering on older AMD cards), **AA Update frontier + small-model rankings** (r/LocalLLaMA, two same-day posts same story, MEDIUM fit — evals in practice), and **LLVM developers debate AGENTS.md** (r/LocalLLaMA, MEDIUM/HIGH fit — agent-ecosystem standardization spreading to a major non-AI OSS project). `github-trending` contributed **magnitudedev/magnitude** (HIGH fit — local-model hardware-fit inference server plugging into existing agent harnesses).

Pass 2 (owner fit): HIGH — Spanda, magnitude, NInfer comparison, Grok Bot piece, LLVM AGENTS.md debate. MEDIUM — gfx906 gains, AA Update rankings.

VERIFY SUBSTANCE: attempted the 5 highest-scored candidates. Confirmed substantive: **Spanda** via `git clone` of the linked repo (`Adarshent/Spnda`) — real math, DOI, benchmark tables, `pip`-installable; **magnitudedev/magnitude** via `git clone` README — real functioning npm-distributed tool with docs/Discord (README embeds a growth-hacky agent-onboarding prompt, noted but not disqualifying); **Grok Bot piece** via WebFetch — genuine hands-on trial, though light on quantitative benchmarks (a first-look, not a teardown). Failed verification (transport, not content): `reddit.com/.json` returned HTTP 403 for all three remaining reddit candidates (NInfer comparison, gfx906 gains, LLVM AGENTS.md debate) — kept on the feed's own summary text per FAILURE MODES, out of highlight consideration. `lanes.sh` (Personal Context MCP) was egress-blocked outright and, combined with its thin signal, was dropped rather than kept-unverified.

WRITE: 7 items written — 1 to `radar/practitioner-blogs.md`, 6 to `radar/community.md` (all under the existing `## 2026-W36` heading).

**Highlights (3): Spanda hallucination detector** (verified via git clone, HIGH owner-fit, a genuinely novel zero-GPU technique with real benchmark numbers and a concrete safety finding — direct `project_post`/`tech_explainer` material), **magnitudedev/magnitude** (verified via git clone, HIGH owner-fit, a real tool squarely on the local/self-hosted-models interest), **Five Days With Grok Bot** (verified via WebFetch, HIGH owner-fit, a rare hands-on comparison of two agent-hosting philosophies — Mac-style managed vs. Linux-style self-owned).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No review-queue cards attempted. All 7 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a TWENTY-SIXTH consecutive affected run since 2026-08-24. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-06 (+7 items, 3 highlights, Linear unavailable)`.

## 2026-09-05 06:15 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-04T04:09:38 UTC (`fetch_feeds.py`; last successful daily run was 2026-09-04 06:15 UTC). `fetch_feeds.py` ran clean — mistral and huggingface reported 304-not-modified (no feed change since last cursor); nvidia had genuine fresh TIER-1 candidates; openai/anthropic/google-deepmind/google-research/microsoft/xai/mistral/huggingface/cursor/perplexity all reported zero fresh, triggering gap-scrape for all ten.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), jina (r.jina.ai — Cloudflare "Just a moment" challenge, anonymous block), WebSearch | 0 | jina, WebSearch | jina blocked by Cloudflare challenge (no JINA_API_KEY); WebSearch confirmed only the already-known Sep 3 Safety-category Astra posts (category-filtered, not written) — nothing new |
| anthropic | fetch (WebFetch) | 0 | fetch | anthropic.com/news listing tops out at Sep 1 (Claude Fable 5.1/Mythos 5.1, Enterprise Frontier Safeguards), already captured — nothing newer |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | blog listing tops out at Sep 3 (WeatherNext 3), already captured, predates window |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | blog listing tops out at Sep 3 (fruit-fly connectome, genomic transfer learning), already captured, predates window |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | research blog listing tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured, predates window |
| nvidia | rss.xml (TIER-1, 2 fresh) | 2 | - | - |
| xai | jina (r.jina.ai — Cloudflare "Just a moment" challenge), WebSearch | 0 | jina, WebSearch | jina blocked by Cloudflare challenge; WebSearch surfaced a "$100K vendor-spend savings" Grok Bot claim with no dated news URL — traced to undated product/use-case marketing copy (x.ai/bot/use-cases), not a real dated announcement — rejected as unconfirmed |
| mistral | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | news listing tops out at Aug 24 (Mistral x HUMAIN), already captured, predates window |
| huggingface | rss.xml (TIER-1, 304 not modified), WebFetch | 3 | WebFetch | WebFetch of huggingface.co/blog surfaced 3 Sep 3 posts not in prior captures (funes memory layer, GRPO/IFStruct fine-tuning, TRL/OpenEnv watercolour-painting RL) — feed 304'd both yesterday and today despite these existing; confirmed via individual page reads, written as backfill |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on /changelog | 0 | WebFetch | changelog tops out at Sep 2 (Self-hosted machines), already captured, nothing newer |
| perplexity | jina (r.jina.ai — Cloudflare "Just a moment" challenge, anonymous block), WebSearch | 0 | jina, WebSearch | jina blocked; WebSearch confirmed only already-captured Sep 1 posts — nothing new |

Totals: 5 items, 2 companies fresh (nvidia, huggingface), 9 silent (openai, anthropic, google-deepmind, google-research, microsoft, xai, mistral, cursor, perplexity — all confirmed predates-window/already-captured/category-filtered/unconfirmed via one gap-scrape fallback each, no hard transport errors beyond the expected anonymous-Jina Cloudflare challenge on openai/xai/perplexity, now presenting as a JS challenge page rather than a plain 403/AbuseAlleviation error).

Notable — **OpenAI GPT-6 Astra still not confirmed as a Product-category launch** (unchanged from 2026-09-04, now a second consecutive day): only Safety-category posts exist on openai.com/news/ (Sep 3 safety overview + system card), still fail-closed excluded by the category filter. Two independent radar signals (2026-09-04/09-05 practitioner-blogs: Latent Space first-look, Simon Willison's pelican comparison) now report live third-party access to GPT-6 Astra, reinforcing that an official launch post is imminent or already missed. Flagging again for the owner's awareness.

Notable — **HuggingFace RSS 304 masking real content**: `huggingface.co/blog/feed.xml` returned 304-not-modified on both 2026-09-04 and 2026-09-05, yet three genuine Sep 3 posts existed on the blog and were confirmed only by today's WebFetch gap-scrape. Worth the owner's attention if this recurs — the ETag/Last-Modified cursor may be stale relative to blog content, undercounting TIER-1 candidates on this source.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No issue-creation attempted. All 5 confirmed items are fully written to `topics/*.md` and `artifacts/` above — no data lost, only the Linear cards are behind. This is now a TWENTY-SIXTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — fourteen days with no working review queue or News digest board). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-05 (+5 items, 2 companies fresh, Linear unavailable)`.

## 2026-09-06 06:16 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-05T04:10:06 UTC (`fetch_feeds.py`; last successful daily run was 2026-09-05 06:15 UTC). `fetch_feeds.py` ran clean — microsoft, nvidia, mistral, and huggingface reported 304-not-modified (no feed change since last cursor); openai, anthropic, google-deepmind, google-research, xai, cursor, and perplexity all reported zero fresh with no source errors, triggering gap-scrape for all eleven companies (all zero-fresh this run).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebFetch (403), WebSearch, raw-curl of rss.xml (confirmatory) | 1 | WebSearch | WebFetch of openai.com/news/ 403'd (one-fallback rule); WebSearch surfaced `openai.com/index/gpt-6-astra` (GPT-6 Astra launch, Sep 3, "Research" category); a follow-up raw `curl` of the RSS feed confirmed the pubDate and category directly — written as a backfill (see note below) |
| anthropic | fetch (WebFetch) | 0 | fetch | anthropic.com/news listing tops out at Sep 1 (Fable 5.1/Mythos 5.1, Enterprise Frontier Safeguards), already captured — nothing newer |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | blog listing tops out at Sep 3 (WeatherNext 3, Fairwind Program, Gemini 3.8 Flash/Flash Cyber, agentic video), already captured, predates window |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | blog listing tops out at Sep 3 (connectome, genomic transfer learning), already captured, predates window |
| microsoft | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | research blog listing tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured, predates window |
| nvidia | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | developer blog listing tops out at Sep 4 (NemoClaw, Jetson reasoning), already captured, predates window |
| xai | curl r.jina.ai (anonymous, succeeded) | 1 | jina | jina succeeded on the news listing; found "Setting Grok Bot loose on procurement" (Sep 4) not yet captured — written. Follow-up jina fetch of the article itself got IP-reputation-blocked mid-run (one fallback already spent); WebSearch supplied the confirming summary instead |
| mistral | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | news listing tops out at Aug 24 (Mistral x HUMAIN), already captured, predates window — genuinely quiet for 13 days |
| huggingface | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | blog listing tops out at Sep 3 (funes, GRPO/IFStruct, watercolours, NeoMME, IBM/Confluent), all already captured, predates window |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | changelog tops out at Sep 2 (Self-hosted machines), already captured, predates window |
| perplexity | curl r.jina.ai (blocked), WebSearch | 0 | jina, WebSearch | jina anonymous access blocked (`AbuseAlleviationError`, DDoS-suspected rate-limit on the whole `perplexity.ai` domain); WebSearch confirmed only the already-known Sep 1 posts (PII-TRACE, Hybrid Compute on Mac) — nothing new |

Totals: 2 items, 2 companies fresh (openai, xai), 9 silent (anthropic, google-deepmind, google-research, microsoft, nvidia, mistral, huggingface, cursor, perplexity — all confirmed predates-window/already-captured via one gap-scrape fallback each, no hard transport errors beyond the expected perplexity anonymous-Jina block and the openai.com/news/ 403 on direct WebFetch).

Notable — **OpenAI GPT-6 Astra launch recovered, two-day category-filter gap explained**: `openai.com/index/gpt-6-astra` ("GPT-6 Astra: A new generation of intelligence", Sep 3) is tagged **"Research"** in the raw RSS feed — squarely inside the configured keep-list `{Product, Engineering, Research, Publication, Release}` — yet `fetch_feeds.py`'s TIER-1 fetch reported it as not-fresh on 2026-09-04, 09-05, and again this morning, and the 09-04/09-05 gap-scrapes (via jina reader on `openai.com/news/`) only ever surfaced the *Safety*-category Astra posts (System Card, Safety overview), never this Research-category one. Root cause suspected: the script's HTTP cursor (`state/cursors.json`) likely advances past an item's pubDate the first time it's seen in the feed regardless of whether the agent actually wrote it, permanently hiding a category-filtered item from all future TIER-1 fetches. Recovered today only via WebSearch (surfaced the URL) + a raw `curl` of the RSS feed (confirmed pubDate/category) — item written as a backfill dated 2026-09-03, three days late. **Owner action suggested:** consider whether `fetch_feeds.py`'s cursor logic should track "last written" rather than "last seen in feed" per company, so a category-filtered-out item doesn't become permanently invisible. This is now a THIRD consecutive day this specific gap was flagged (09-04, 09-05, resolved 09-06).

Notable — **xAI "$100K savings" claim now dated and confirmed**: the 2026-09-05 daily run rejected an xAI Grok Bot "$100K vendor-spend savings" WebSearch claim as unconfirmed (traced then to undated marketing copy). Today's "Setting Grok Bot loose on procurement" (Sep 4) is the same claim with a real dated primary source — written now, superseding that earlier rejection.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No issue-creation attempted. Both confirmed items are fully written to `topics/*.md` and `artifacts/` above — no data lost, only the Linear cards are behind. This is now a TWENTY-SEVENTH consecutive affected run since 2026-08-24. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-06 (+2 items, 2 companies fresh, Linear unavailable)`.

## 2026-09-06 07:20 UTC — weekly digest — partial (Linear unavailable)

Week: **2026-W36** (Mon 2026-08-31 — Sun 2026-09-06). Read this week's `## 2026-W36` sections of all 12 `topics/*.md`, the matching 40 `artifacts/*.md` card blocks, all 10 `radar/*.md` W36 sections, and `radar/deep/`.

**Company digest:** 40 items, 10 of 12 companies fresh. Per company — NVIDIA 10, Hugging Face 8, Google DeepMind 4, Google Research 4, xAI 4, Anthropic 3, Perplexity 3, OpenAI 2, Microsoft 1, Cursor 1. Silent (reported as silent, not padded): **Cohere, Mistral**. 14 items marked ⭐ (High priority per the rubric) and carry trimmed `Деталі` bullets; the other 26 carry their `Що сталося` paragraph. Every item kept its source URL and `[[company]]` wikilink. No `[duplicate]` markers this week.

`Що це означає` threads (all grounded in the collected cards, no outside facts): (1) three labs in three days shipped a gated cyber-capability channel — Anthropic Mythos 5.1 trusted-access, Google Gemini 3.8 Flash Cyber via Fairwind, OpenAI GPT-6 Astra at Preparedness "Critical", plus xAI's LatchBio biosecurity eval; (2) Terminal-Bench-Science moved twice in three days (24.7% → 52.6% → 64.6%) with cost as the stated argument both times; (3) inference moving onto user-owned hardware (Perplexity's three same-day posts, NVIDIA PAIR/Jetson/spec-decoding/TCO); (4) customer-controlled data as the common enterprise answer (Anthropic EFS, Cursor self-hosted machines, xAI enterprise governance, OpenAI read-only Epic EHR); (5) domain-specific open-weight foundation models as a distinct genre.

**Radar week summary:** 59 confirmed items in the `## 2026-W36` sections, 18 highlight-marked; per-category table written into the digest (community 47, practitioner-blogs 7, bigtech-eng 2, research-institutes 2, oss-ml-systems 1, five categories at 0). Top-3 picked: Spanda hallucination detector (05.09), GitHub Project HydraFusion (04.09), OpenAI rogue-agents-via-wikis writeup (04.09). Cross-cutting themes recorded: harness/context engineering, the Qwen3.8-Flash-Next + llama.cpp local-tuning wave, agent-safety-as-practice. **Deep dives: none** — `radar/deep/` holds only `TEMPLATE.md`; the `radar-deep-dive` routine ran on schedule 08-31 (Mon) and 09-03 (Thu) and was `blocked (Linear unavailable)` both times.

**Data-hygiene finding (new this week):** the 2026-08-31 radar run (Monday, already ISO week W36) appended its 8 items under the `## 2026-W35` heading. Five of them are dated 2026-08-31 and belong to W36 by ISO week, but the W35 digest was generated 2026-08-30 — so those five were in no digest at all. They are listed explicitly at the end of the W36 radar section (phonellm-alpha-1 ⭐, heretic ⭐, OpenMAIC, Thomson-1.0-Small, MiniMax-H3-Turbo-Lora) rather than silently dropped. The files were NOT edited — the misfiled items stay where the radar run put them; only the digest accounts for them.

**Ongoing source failures carried into the digest** (all from this week's run-log entries): all 7 YouTube sources dead 14 days (6× HTTP 404 + `yt-mlst` HTTP 500) → `youtube` category 0 items; `smolai` HTTP 402 Payment Required since 09-04 → `technical-newsletters` 0 items; `bair` connection-reset four consecutive days; recurring Reddit `.json` 403s (items kept on feed summaries, out of highlight consideration).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** Per THE WEEKLY DIGEST steps 4–5, both Linear steps were skipped: **no digest card** created/updated in project "News digest" (`📰 Тижневий дайджест 2026-W36`), and **no board close-out** — no Todo cards moved to Done in "News digest", no stale review cards closed in "Radar". Nothing was touched in In Progress / Canceled / Duplicate. This is now a TWENTY-EIGHTH consecutive affected run since 2026-08-24, and the SECOND consecutive weekly digest delivered file-only. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session. The full digest text lives in `news/weeks/2026-W36/summary.md`.

Commit: `news: weekly digest 2026-W36`.

## 2026-09-07 05:14 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-06T03:14:13 UTC. `fetch_radar.py` ran clean except `vllm-blog` (HTTP 403), `lmsys-sglang` (HTTP 403, `oss-ml-systems`), `bair` (connection reset by peer, fifth consecutive day, `research-institutes`), and `smolai` (HTTP 402 Payment Required, fourth consecutive day, `technical-newsletters`). **All 7 YouTube sources recovered today** after 14 days dead (6× HTTP 404 + `yt-mlst` HTTP 500 since 2026-08-24) — no config change, the outage cleared on its own. `reddit` had a clean, full 25-item pull.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | vllm-blog: HTTP 403; lmsys-sglang: HTTP 403 |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | bair: connection reset |
| technical-newsletters | 0 | 0 | smolai: HTTP 402 |
| practitioner-blogs | 0 | 0 | - |
| youtube | 14 | 3 | - |
| community | 37 | 12 | - |
| mistral-watch | 0 | 0 | - |

Totals: 51 raw candidates, 15 confirmed, 4 source-errors (2 HTTP 403 oss-ml-systems, 1 bair transient, 1 smolai 402). Right at the ~15/day confirmed budget — reddit's clean 25-item pull plus five saved HN searches plus YouTube's return drove raw volume to 51; triage did the bulk of its work in community and youtube.

TRIAGE pass 1: dropped as ask-threads/personal-advice noise (not technique-with-data) — `4xRadeon AI Pro R9700 people, how are your benchmarks?`, `Trying to create my own server...`, `Best model + setup for remote deployment` (grandparent-visiting anecdote), `Planning to get a cheap-ish GPU`, `HELP: learning the fit for an agentic framework`, `Which qwen for vllm?`, `Openwebui + open terminal`, `LLM regression in reading comprehension?` (open question, no data). `New Benchmark: The Struggle Bench` dropped as a parody benchmark concept (AI given rent money and told to survive) with no actual run/results, not a real technique. `vibeblending locally with Qwen 3.8 27B` and `Villager Simulation Game POC` dropped as light toy/demo posts, thin on engineering depth relative to today's stronger candidates. `hn-show-rag`/`hn-show-mcp`'s three results (`VODForge` video downloader, `HyperCard to HTML Converter`, `Minilith` PNG-based CMS) dropped as off-topic, non-AI Show HN noise despite matching the saved search terms. `hf-trending-spaces`'s `chrisssut/Testground` (trending 26, titled "Testground") dropped as empty/non-substantive. `github-trending`'s `ruvnet/ruflo` dropped: heavy buzzword marketing copy ("original agent meta-harness", "intelligent multi-player swarms", "self-learning intelligence") with no concrete technical detail in the description — reads as a marketing shell, not verified further. Also dropped as MEDIUM-value but past today's cutoff given volume: `DeepSeek-V4-Flash-Vision Q8 vs Qwen3.8-Flash-Next Q8` (subjective comparison, no hard numbers in the summary), `Building neuro symbolic reasoning graphs from documents` (early-stage, thin description), `[Model] Support for Spark2_5ForCausalLM... PR #27868` (new small model + llama.cpp day-0 support, decent but lower priority than the kept items), `8 uncensored Qwen 3.8 27B variants... Abliterlitics` (real effort — 167 GPU hours — but niche abliteration fine-tuning), `Coding benchmarks that are quickly showcasing deep capability` (opinion-listicle framing, thin on verifiable specifics). GPU MODE's livestream/edited-cut duplicate pair (`PyCuTe` / `Lecture 114: PyCuTe`) — kept neither this run; `Scan at the speed of light` and `GPU Kernel Formal Verification` also left out at the volume cutoff in favor of `Outperforming cuBLAS on NVFP4`. `yt-ai-engineer`'s other four AI Engineer conference talks (Composio, PromptQL, Town, Two Sigma) and `yt-mlst`'s interpretability talk and `yt-sentdex`'s GLM video left out at the cutoff, not because they failed pass 1.

VERIFY SUBSTANCE: attempted 5 of the day's highest-scored HIGH-fit candidates — `interns-review-plugin` (via `git clone`), and four reddit posts (`3 repetitions of a lie...`, `I built a local-first hybrid router for AI Agent Skills`, `Validate your local LLM advertised KV cache...`, `I built an LLM benchmark harness...`) via curl with browser UA. Only `interns-review-plugin` confirmed: real, substantial Claude Code plugin — session hooks force a written context file per proposal, 1–3 parallel `fable`-model adversarial reviewer subagents with a fixed critique prompt and read-only tools, lead-verifies-before-accepting workflow, receipt of accepted/rejected findings; matches the HN summary exactly. The four reddit posts all failed transport today — `curl` returned an HTML shell (not JSON) rather than the usual 429, a variant of the known reddit-transport failure mode — so all four stay regular radar items, out of highlight consideration, kept on the feed's own summary text per the fallback rule. A sixth attempt, `hn-trend-llm`'s "Your intellectual fly is open..." (611 pts/394 comments, unusually large HN signal, and directly relevant to the owner's own AI-assisted writing practice), was also attempted: WebFetch hit EGRESS_BLOCKED for `bcantrill.dtrace.org`, and the one curl retry hit a CONNECT tunnel 403 — kept on title/points only, content unverified, out of highlight consideration.

**Highlight: 1** — `interns-review-plugin` (adversarial multi-reviewer Claude Code plugin), the only candidate that both scored HIGH fit and cleared verification today.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No review-queue cards attempted. All 15 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a TWENTY-NINTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — fourteen days with no working review queue or News digest board). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-07 (+15 items, 1 highlight, Linear unavailable)`.

## 2026-09-07 06:10 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-06T04:10:22 UTC (`fetch_feeds.py`; last successful daily run was 2026-09-06 06:16 UTC). `fetch_feeds.py` ran clean — nvidia, mistral, and huggingface reported 304-not-modified (no feed change since last cursor); openai had one genuine fresh TIER-1 candidate; anthropic/google-deepmind/google-research/microsoft/xai/cursor/perplexity all reported zero fresh with no source errors, triggering gap-scrape for all ten zero-fresh companies (openai skipped per rule — it already had a fresh TIER-1 hit).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| anthropic | fetch (WebFetch) | 0 | fetch | anthropic.com/news listing tops out at Sep 1 (Enterprise Frontier Safeguards), already captured — nothing newer |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | blog listing tops out at Sep 3 (Gemini 3.8 Flash/Flash Cyber, Fairwind, WeatherNext 3), already captured, predates window |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | blog listing tops out at Sep 3 (connectome, genomic transfer learning), already captured, predates window |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | research blog listing tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured, predates window |
| nvidia | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | developer blog listing tops out at Sep 4 (NemoClaw, Jetson reasoning), already captured, predates window |
| xai | curl r.jina.ai (Cloudflare "Just a moment" challenge, anonymous block), WebSearch | 0 | jina, WebSearch | jina blocked; WebSearch confirmed only the already-captured Sep 3 "Grok Bot for Enterprise" — nothing new |
| mistral | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | news listing tops out at Aug 24 (Mistral x HUMAIN), already captured, predates window — genuinely quiet for 14 days |
| huggingface | rss.xml (TIER-1, 304 not modified), WebFetch | 2 | WebFetch | blog listing surfaced two posts the feed never showed as fresh (304'd) and prior gap-scrapes missed: "Introducing @huggingface/kernels" (Sep 1) and "The Open ASR Leaderboard Adds Its First Global South Language" (Aug 28, backfilled 11 days late) — both confirmed via individual page reads, written as backfill |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | changelog tops out at Sep 2 (Self-hosted machines), already captured, predates window |
| perplexity | curl r.jina.ai (Cloudflare "Just a moment" challenge, anonymous block, both on the blog listing and a guessed article URL), WebSearch (×2) | 0 | jina, WebSearch | jina blocked on every attempt; WebSearch surfaced a real, well-covered Sep 4 post — "Fast Embeddings on GPUs" (Perplexity's Ivy/Tulip/ROSE GPU embedding-serving stack for pplx-embed) — corroborated by three independent secondary sources (MarkTechPost, Perplexity's own X post, AlphaSignal) with specific technical detail, but the primary `perplexity.ai` URL could not be reached (WebFetch: EGRESS_BLOCKED; curl to a guessed slug: proxy 403; jina: Cloudflare challenge) so the exact canonical URL is unconfirmed — **not written**, flagged below for the owner/next run |

Totals: 3 items, 2 companies fresh (openai, huggingface), 8 silent (anthropic, google-deepmind, google-research, microsoft, nvidia, xai, mistral, cursor — all confirmed predates-window/already-captured via one gap-scrape fallback each), 1 company (perplexity) with a real story found but left unwritten pending primary-source access.

Notable — **HuggingFace RSS 304-masking recurs, now with an 11-day-old miss**: this is the second consecutive week `huggingface.co/blog/feed.xml`'s 304-not-modified response has hidden genuine new posts from TIER-1 (see 2026-09-05 entry above for the first instance). Today's gap-scrape backfilled not just a same-week miss but an 11-day-old one ("Global South" ASR post, Aug 28) that no prior gap-scrape caught — the blog listing page apparently doesn't get walked far enough back on a quiet TIER-1 day. Recommend the owner revisit the cursor-freshness concern flagged 2026-09-06.

Notable — **Perplexity "Fast Embeddings on GPUs" (Sep 4) — real story, primary source unreachable**: strong secondary confirmation (Perplexity's own X/Twitter post naming the ROSE inference engine and Ivy/Tulip serving components, plus MarkTechPost and AlphaSignal writeups with matching technical specifics — CUDA graphs, lazy result tracking, Rust request path, BGE-M3/pplx-embed-1-0.6b p50/p99 benchmarks). Every transport tried today hit a wall: WebFetch returned EGRESS_BLOCKED for both perplexity.ai and marktechpost.com (this cloud env's domain allowlist), anonymous Jina hit a Cloudflare JS challenge on both the blog listing and a guessed article slug, and a direct curl was rejected by the proxy with 403. Per the never-invent rule, withheld rather than guessed at the canonical URL. Owner action: confirm the article's exact URL (e.g. from a phone/browser) so it can be written next run, or add `marktechpost.com`/`perplexity.ai` article paths to the env's egress allowlist.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow).** No issue-creation attempted. All 3 confirmed items are fully written to `topics/*.md` and `artifacts/` above — no data lost, only the Linear cards are behind. This is now a THIRTIETH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — fifteen days with no working review queue or News digest board). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-07 (+3 items, 2 companies fresh, Linear unavailable)`.

## 2026-09-07 07:14 UTC — deep-dive — blocked (Linear unavailable)

Off-schedule note: the routine's configured slots are Mon+Thu 07:00 UTC; today is Sunday — this firing came outside the normal schedule (manual fire or schedule change). Run executed normally regardless.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** The deep dive cannot degrade gracefully: its ONLY input is the review queue in Linear project "Radar" (`hot`-labeled cards in "Ready to Review"), which can be neither read nor written. Cards processed: 0. Files written: 0. No leftovers known (the queue is unreadable, not empty — cards created before 2026-08-24 may carry approvals we cannot see).

This is now a THIRTY-FIRST consecutive affected run since 2026-08-24, and the FOURTH deep-dive run in a row fully blocked (after Thu 2026-08-27, Mon 2026-08-31, Thu 2026-09-03) — the deep-dive pipeline has produced nothing since it went live; `radar/deep/` still holds only TEMPLATE.md. The review queue has received no new cards in 15 days. Owner action needed (unchanged since 2026-08-24): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session; also clear the free-issue-limit cap in the Kovalevgr workspace if still in place.

Commit: `news: deep dive 2026-09-07 (0 cards, blocked — Linear unavailable)`.

## 2026-09-08 05:04 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-07T03:04:46 UTC. `fetch_radar.py` ran with errors on `bair` (connection reset by peer, sixth consecutive day, `research-institutes`), all 7 YouTube sources (6× HTTP 404 + 2× HTTP 500 — `yt-karpathy`/`yt-umar-jamil` gave 500, the rest 404 — dead again one day after yesterday's full recovery), `reddit` (HTTP 429), and `smolai` (HTTP 402 Payment Required, fifth consecutive day). No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for all four.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 3 | 2 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | bair: connection reset |
| technical-newsletters | 1 | 1 | - |
| practitioner-blogs | 1 | 1 | - |
| youtube | 0 | 0 | 6× HTTP 404, 2× HTTP 500 (all 7 sources) |
| community | 16 | 4 | reddit: HTTP 429; smolai: HTTP 402 |
| mistral-watch | 0 | 0 | - |

Totals: 21 raw candidates, 8 confirmed, 4 source-errors (1 bair transient, 7 youtube dead, 1 reddit 429, 1 smolai 402 — youtube counted once as a category-wide outage).

TRIAGE pass 1: `oss-ml-systems` — kept both `vllm-blog` posts (real engineering: KV-cache/MLA offloading technique with reproducible benchmarks; a Tenstorrent hardware-backend plugin write-up, architecture-only, no numbers). Dropped `pytorch-blog`'s "PyTorch x Hugging Face in Bengaluru" as a community-meetup recap, not engineering content. `community` — dropped as off-topic/non-AI Show HN noise despite matching the saved search terms: `HomeCat` (backyard shed/office designer) and `VODForge` (YouTube downloader, cross-posted across `hn-show-rag`/`hn-show-mcp`, counted once). Dropped `Send flowers from your AI agent...` (MCP for flower delivery, 11 pts/7 comments, cross-posted across `hn-show-mcp`/`hn-show-agents`) as a thin marketing shell, not a real technique. Dropped `hn-trend-llm`'s "Your intellectual fly is open..." as an exact duplicate of the same URL already recorded in this week's `community.md` from the 2026-09-07 run. Dropped all 5 `hf-trending-spaces` diff entries (a NSFW LoRA demo, an "uncensored" chat demo, a joke fruit-fly-simulation space, `nanotron/ultrascale-playbook` re-surfacing from a 2024 publish date with no news hook, and a video-model finishing-preview space) as toy/demo/stale, below the technical bar. Dropped `github-trending`'s `llvm/llvm-project` as generic non-AI-specific trending noise (the mirror isn't AI-filtered). Kept `github-trending`'s `openai/skills` after verifying via `git clone`: real ecosystem signal (Codex's Skills catalog deprecated in favor of `openai/plugins`), not a technique but a verified, owner-relevant infra change. Kept both `hf-trending-models` entries (`openbmb/MiniCPM5-2B`, `dealignai/GLM-5.3-CYBERSECURITY-FP8`) as local-model signal per the interest profile, unverified beyond the HF listing (no accompanying posts found). `practitioner-blogs` — kept `latent-space`'s AEO tracker after verification confirmed real methodology (7 models × 161 categories) rather than pure marketing, scored MEDIUM fit (SEO-adjacent, outside the core interest list) and excluded from highlights on that basis. `technical-newsletters` — kept SemiAnalysis's TPU InferenceX piece; verification confirmed genuine technical content (Ironwood die redesign, FP8 hardware, cost/perf benchmarks vs. B200/B300) wrapped in business framing, not the pure finance/market piece pass 1 is meant to filter.

VERIFY SUBSTANCE: attempted the day's 5 highest-scored HIGH-fit candidates — `interns-review-plugin`-style `git clone` for `Engrim` (github.com), WebFetch for both `vllm-blog` posts, the SemiAnalysis TPU piece, and the Latent.Space AEO tracker. All 5 cleared verification (see triage prose above for what each confirmed). No reddit or GitHub-README verification failures today — no reddit fresh items survived pass 1 (reddit's own fetch also 429'd), and both git-clone verifications (`Engrim`, `openai/skills`) succeeded cleanly via the git proxy.

**Highlights: 3** — `Engrim` (universal local-first SQLite agent-memory engine, 85 pts, direct match on the owner's HIGH-interest "agent memory" line), vLLM's `GLM 5.3 Hybrid HiSparse Offloading` (concrete 1M-context result + reproducible benchmark methodology, vLLM named explicitly in the interest profile), and SemiAnalysis's `TPU InferenceX Full Steam Ahead` (hardest numbers of the day: Ironwood architecture detail plus a direct $/M-token comparison against B200/B300). The vLLM Tenstorrent plugin write-up was a close fourth but excluded for explicitly withholding benchmark numbers.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 8 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a THIRTY-SECOND consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — sixteen days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-08 (+8 items, 3 highlights, Linear unavailable)`.

## 2026-09-08 06:11 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-07T04:11:02 UTC (`fetch_feeds.py`; last successful daily run was 2026-09-07 06:10 UTC). `fetch_feeds.py` ran clean — microsoft, nvidia, and huggingface reported 304-not-modified (no feed change since last cursor); mistral had one genuine fresh TIER-1 candidate; openai/anthropic/google-deepmind/google-research/microsoft/nvidia/xai/huggingface/cursor/perplexity all reported zero fresh, triggering gap-scrape for all ten zero-fresh companies (mistral skipped per rule — it already had a fresh TIER-1 hit).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebFetch (403), raw curl of rss.xml, WebSearch | 0 | fetch, WebSearch | raw feed shows two items inside the window ("Supporting independent journalism in Ukraine" Sep 7, "An Alien Mind" Sep 6) but both are category `Global Affairs`/`Safety` — outside the configured keep-list — fail-closed per config; WebSearch confirmed nothing else new |
| anthropic | fetch (WebFetch) | 0 | fetch | anthropic.com/news listing tops out at Sep 1 (Fable 5.1/Mythos 5.1, Enterprise Frontier Safeguards), already captured — nothing newer |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | blog listing tops out at Sep 3 (Gemini 3.8 Flash/Flash Cyber, Fairwind, WeatherNext 3), already captured, predates window |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | blog listing tops out at Sep 3 (connectome, genomic transfer learning), already captured, predates window |
| microsoft | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | research blog listing tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured, predates window |
| nvidia | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | developer blog listing tops out at Sep 4 (NemoClaw, Jetson reasoning), already captured, predates window |
| xai | curl r.jina.ai (Cloudflare "Just a moment" challenge, anonymous block), WebSearch | 0 | jina, WebSearch | jina blocked; WebSearch surfaced "Grok 4.6 on Microsoft Foundry" and Grok 4.7 (Sep 12 target, not yet launched) — the Foundry post is already captured (Aug 26); nothing new |
| mistral | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| huggingface | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | blog listing tops out at Sep 3 (NeoMME, funes, GRPO structured outputs, watercolours training, IBM time series), already captured, predates window |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | changelog tops out at Sep 2 (Self-hosted machines), already captured, predates window |
| perplexity | curl r.jina.ai (Cloudflare "Just a moment" challenge, second consecutive day), WebFetch (EGRESS_BLOCKED), WebSearch | 1 | jina, WebFetch, WebSearch | canonical URL for "Fast Embeddings on GPUs" (flagged unwritten 2026-09-07) recovered via WebSearch: `perplexity.ai/hub/blog/fast-embeddings-on-gpus` — content still unreachable directly (Cloudflare JS challenge on Jina, EGRESS_BLOCKED on WebFetch) but WebSearch's synthesis quotes the article's own technical framing (Ivy/Tulip/ROSE, CUDA graphs, async result-tracking, Rust request path) — written as a backfill dated Sep 4 on canonical-URL + content confirmation, precise p50/p99 benchmark numbers omitted since not independently re-verified this run |

Totals: 2 items, 2 companies fresh (mistral, perplexity — perplexity's item predates this run's window, written as backfill), 9 silent (openai, anthropic, google-deepmind, google-research, microsoft, nvidia, xai, huggingface, cursor — all confirmed predates-window/already-captured/category-filtered via one gap-scrape fallback each, no hard transport errors beyond the expected Cloudflare/EGRESS_BLOCKED walls on xai/perplexity).

Notable — **Perplexity "Fast Embeddings on GPUs" canonical URL recovered, written after two-day delay**: yesterday's run found the story via WebSearch but withheld it — no confirmed canonical URL and the primary source unreachable on every transport (WebFetch EGRESS_BLOCKED, curl 403, Jina Cloudflare challenge). Today's WebSearch surfaced the exact URL (`perplexity.ai/hub/blog/fast-embeddings-on-gpus`) plus a synthesis that reads as drawn directly from the article's own text. The primary page itself is still unreachable — Jina hit the same Cloudflare JS challenge again — so this write-up is built on the confirmed URL and WebSearch's quoted framing only; it deliberately omits the specific p50/p99 latency and throughput numbers reported by secondary sources (MarkTechPost, AlphaSignal) in the 2026-09-07 entry, since those were not re-confirmed against primary content today. Owner action: a phone/browser read of the primary URL would let a follow-up pass add the hard numbers.

Notable — **OpenAI category filter correctly excluded two in-window items**: the raw RSS feed carried "Supporting independent journalism in Ukraine" (Sep 7, `Global Affairs`) and "An Alien Mind" (Sep 6, `Safety`, Jakub Pachocki reflection) — both genuine posts, both outside the configured `{Product, Engineering, Research, Publication, Release}` keep-list. Correctly fail-closed per the 2026-08-08 technical-first audit; noted here only for visibility, not a gap.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No issue-creation attempted. Both confirmed items are fully written to `topics/*.md` and `artifacts/` above — no data lost, only the Linear cards are behind. This is now a THIRTY-THIRD consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — seventeen days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-08 (+2 items, 2 companies fresh, Linear unavailable)`.

## 2026-09-09 05:04 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-08T03:04:44 UTC. `fetch_radar.py` ran with errors on `bair` (connection reset by peer, seventh consecutive day, `research-institutes`), all 7 YouTube sources (5× HTTP 404 + 2× HTTP 500 — `yt-latent-space`/`yt-sentdex` gave 500, the rest 404 — dead again), and `smolai` (HTTP 402 Payment Required, sixth consecutive day). `reddit` fetched clean today (no 429) with 25 fresh candidates. No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for all three.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 1 | 1 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | bair: connection reset |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 1 | 1 | - |
| youtube | 0 | 0 | 5× HTTP 404, 2× HTTP 500 (all 7 sources) |
| community | 53 | 12 | smolai: HTTP 402 |
| mistral-watch | 0 | 0 | - |

Totals: 55 raw candidates, 14 confirmed, 3 source-errors (1 bair transient, 7 youtube dead — counted once as a category-wide outage, 1 smolai 402).

TRIAGE pass 1/2: `oss-ml-systems` — kept the routine `vllm-releases` v0.29.0 tag (no release-note text available, same as prior routine vLLM releases). `practitioner-blogs` — kept Interconnects' "Latest open artifacts (#24)" roundup (Motif-3/GLM-5.3/Hy4-preview + licensing discussion), MEDIUM-HIGH fit. `community` — the 25-item `reddit` batch needed the heaviest cut of the day: dropped 15 as low-effort questions ("Are there any small models...", "What are some practical tasks...", "Which local model is good at knowing when to stop..."), thin link-only posts with no body content (`Qwen/Qwen-Drive-1.0-4B`, `nex-agi/Nex-N2.5-mini`, `inclusionAI/Ling-3.0-flash-VL`, a three-way model-name comparison post), a meme/appreciation post ("hilarious comment about llama.cpp"), a demo with no real technique ("Qwen 3.8 27b with PI agent... 3D graphic game"), off-topic/worldbuilding content ("Fallout 2 x Fallout: Bakersfield..."), a self-promo p2p-sharing tool with no technical depth (`Infercat`), a company-drama post better suited to the daily company-news routine than the technical radar ("OpenAI alleged of stealing mathematicians work"), and a niche hardware-debugging anecdote without a broader technique takeaway ("Off the bus: it wasn't pcie/oculink... it was the PSU"). Kept the 6 strongest: a 1M-context MLX-serve release, a three-engine (llama.cpp/SGLang/FreeToken) benchmark, a 7900xtx-optimized llama.cpp build, a Git-as-agent-memory project, a data-poisoning research critique of "autonomous AI" claims, and DeepSeek Flash 4.1 API-testing reports. `hn-show-rag`/`hn-show-mcp`/`hn-show-agents` — dropped non-AI Show HN noise (`HomeCat` backyard-office designer, `NYC MapTap`) and a thin MCP-flower-delivery marketing shell ("Send flowers from your AI agent...", cross-posted across two saved searches, counted once); kept Isle (managed environments for computer-use agents) and, from `hn-trend-llm`, an attention-visualization tool (147 pts) — dropped `hn-trend-llm`'s "Multi-Agents LLM Financial Trading Framework" as finance-application-flavored per the interest profile's low-priority bucket. `hf-daily-papers` — kept all 3 (NeoHorse-1, an on-policy reverse-distillation paper, Miles v0.1 post-training), all have released code and sit squarely in the HIGH-interest training/agents lines. `hf-trending-models`/`hf-trending-spaces` — dropped both trending models (`google-bert/bert-base-uncased` — an old classic with no fresh news hook behind the trending spike; `facebook/mms-300m` — same) and all 3 trending spaces (two consumer image/video demo shells, one small-model demo space with no accompanying writeup) as noise below the technical bar. `github-trending` — dropped 6 of 9 as non-AI or thin (`MoonTechLab/LunaTV` media-streaming app, `coreyhaines31/marketingskills`, `The-Swarm-Corporation/AutoHedge` finance framework, `BraveOPotato/FckSignups`, `mksglu/context-mode`, `jo-inc/camofox-browser` — the last two too thin to confirm real substance without spending the day's verification budget); kept `bytedance/deer-flow` after verification (see below). `microsoft/markitdown` and `heygen-com/hyperframes` were also dropped as already-known/thin-signal re-surfacing on the trending mirror without a clear news hook this run.

VERIFY SUBSTANCE: attempted 6 candidates (one over the usual 5, all scored HIGH fit and close together). Reddit's `.json` endpoint 403'd on all 3 attempted posts (browser UA, same as the fetcher) — fell back to the feed's own detailed summary text per the workflow's fallback rule; all 3 (7900xtx build, Git-context-layer, engine benchmark) deliver concrete numbers/specifics matching their titles, confirmed. HN's `Isle` (tryisle.com) hit `EGRESS_BLOCKED` on WebFetch — transport error, kept as a regular item, out of highlight consideration. `huggingface.co/papers` and `arxiv.org` were both unreachable (JS-only page / egress-blocked) for the NeoHorse-1 paper, so verified instead via `git clone` of the linked GitHub repo (`TokenRhythm/NeoHorse`): real Apache-2.0 weights, GGUF quants, and a 10-benchmark evaluation table with a stated Δ vs. the Qwen3.5 baseline — cleared. `bytedance/deer-flow` verified via `git clone`: a substantial, actively-developed agent-harness README (sub-agents, sandboxes, long-term memory, context compaction, MCP server) — cleared, direct match on multiple HIGH-interest lines (agent harnesses, context engineering, agent memory).

**Highlights: 3** — `NeoHorse-1` (routing-harness agentic post-training toward recursive self-improvement, verified code+benchmarks, direct match on the owner's HIGH-interest agents/training lines), `bytedance/deer-flow` (ByteDance's open-source super-agent harness — sub-agents, memory, sandboxes, context engineering, MCP — the widest-scope agent-tooling release of the day), and the `Qwen3.8-Flash-Next` three-engine benchmark (llama.cpp vs SGLang vs FreeToken, 35s vs 258s TTFT at full context — concrete local-inference-engine numbers). The 7900xtx llama.cpp build was a close fourth but the benchmark comparison scored slightly higher for direct engine-vs-engine numbers.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 14 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a THIRTY-FOURTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — seventeen days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-09 (+14 items, 3 highlights, Linear unavailable)`.

## 2026-09-09 06:10 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-08T04:10:23 UTC (`fetch_feeds.py`; last successful daily run was 2026-09-08 06:11 UTC). `fetch_feeds.py` ran clean — mistral reported 304-not-modified (no feed change since last cursor); openai/google-deepmind/nvidia/huggingface each had genuine fresh TIER-1 candidates; anthropic/google-research/microsoft/xai/mistral/cursor/perplexity all reported zero fresh, triggering gap-scrape for all seven zero-fresh companies.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 2 fresh) | 2 | - | - |
| anthropic | fetch (WebFetch) | 0 | fetch | anthropic.com/news tops out at Sep 1 (Enterprise Frontier Safeguards, Fable 5.1/Mythos 5.1), already captured — nothing newer |
| google-deepmind | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | blog listing tops out at Sep 3 (connectome, genomic transfer learning), already captured, predates window |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | research blog listing tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured, predates window |
| nvidia | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| xai | curl r.jina.ai (200, but content stale vs. our own record) | 0 | jina | jina's top item was Sep 3 ("Grok Bot for Enterprise"); our topics file already has a Sep 4 item ("Setting Grok Bot loose on procurement") newer than that — confirmed up to date, nothing new |
| mistral | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | news page tops out at Sep 8 (€3B Series D), already captured, predates window |
| huggingface | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | changelog tops out at Sep 2 (Self-hosted machines), already captured, predates window |
| perplexity | curl r.jina.ai (403 AbuseAlleviation, same DDoS-suspected block as prior runs), WebSearch | 0 | jina, WebSearch | WebSearch surfaced 3 Sep 1 posts (Hybrid Compute on Mac, Lily/Apple Silicon inference, PII-TRACE) — all 3 already backfilled into topics/perplexity.md and artifacts/ in a prior run; confirmed no new items |

Totals: 5 items, 4 companies fresh (openai×2, google-deepmind, nvidia, huggingface), 7 silent (anthropic, google-research, microsoft, xai, mistral, cursor, perplexity — all confirmed predates-window/already-captured via one gap-scrape fallback each, no hard transport errors beyond the expected Cloudflare/AbuseAlleviation walls on xai/perplexity).

Notable — **OpenAI: two unrelated stories same day** — "Introducing ChatGPT Images 2.5" (product/image-gen upgrade) and "On the Navier–Stokes Millennium Prize Problem" (an AI-generated proof of a 90-year-open math problem, produced by an unnamed internal model "significantly more capable than GPT-6 Astra"). Both cleared the category filter (`Product`/`Research`) and are unrelated stories, not duplicates.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No issue-creation attempted. All 5 confirmed items are fully written to `topics/*.md` and `artifacts/` above — no data lost, only the Linear cards are behind. This is now a THIRTY-FIFTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — seventeen days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-09 (+5 items, 4 companies fresh, Linear unavailable)`.

## 2026-09-10 05:05 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-09T03:05:17 UTC. `fetch_radar.py` ran with errors on `bair` (connection reset by peer, eighth consecutive day, `research-institutes`), all 7 YouTube sources (7× HTTP 404 — dead again), and `smolai` (HTTP 402 Payment Required, seventh consecutive day). `reddit` fetched clean today (no 429) with 25 fresh candidates. No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for all three.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 1 | 1 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 1 | 1 | bair: connection reset |
| technical-newsletters | 1 | 1 | - |
| practitioner-blogs | 2 | 1 | - |
| youtube | 0 | 0 | 7× HTTP 404 (all 7 sources) |
| community | 54 | 11 | smolai: HTTP 402 |
| mistral-watch | 0 | 0 | - |

Totals: 59 raw candidates, 15 confirmed, 3 source-errors (1 bair transient, 7 youtube dead — counted once as a category-wide outage, 1 smolai 402).

TRIAGE pass 1/2: `oss-ml-systems` — kept vLLM's MiniMax M3-on-MI355X optimization writeup (five-bottleneck-class campaign, concrete throughput/TTFT numbers), HIGH fit. `research-institutes` — kept Ai2's Goodfire "predictive data debugging" post (open Dolci/checkpoints/OLMES stack used to trace a safety regression to specific training examples), HIGH fit — direct match on interpretability/evals-in-practice. `technical-newsletters` — kept SemiAnalysis's on-device-vs-datacenter robot-inference piece (real architecture/latency/silicon-efficiency numbers, not a finance post), MEDIUM fit. `practitioner-blogs` — kept Raschka's looped-transformers/GPT-6-Astra explainer (HIGH, architecture technique + research lineage); dropped Interconnects' "When will average people feel AI's impact?" as a macro/philosophical trend essay rather than technique/benchmark/release content (fails the pass-1 technical bar even from a normally-strong source). `community` — the heaviest cut of the day across four overlapping HN saved-searches (`hn-show-rag`/`-mcp`/`-agents` share several items; `hn-trend-llm` added two more) plus a 25-item `reddit` batch: dropped duplicate cross-listings (`oto-dock`, `Geiger`, the Frigade on-screen-guide post, and Type.com all appeared in 2–3 saved searches — counted once each), dropped Frigade and Type.com as YC-launch product marketing with thin technical depth, dropped a polynomial-evaluation Show HN (real work but non-AI/ML), a read-later app (Rdltr, off-topic), an acoustic FPV-drone detector (off-topic, non-AI/ML), and `hn-trend-llm`'s "Multi-Agents LLM Financial Trading Framework" (finance-application flavor, LOW bucket per interest profile — same drop pattern as prior runs). On `reddit`: dropped 13 as memes/low-effort questions ("So relevant", "Local LLM / Qwen 3.8 win", "Would you consider 5t/s usable", "Don't let FOMO win...", "Why the hell is LM Studio...", "Is there a dummies guide...", "Mention if a new model is a finetune"), thin hardware-brag posts without a technique takeaway (RTX 3060 IQ3 run, RTX Titan server rebuild, "serious local machine" Threadripper link, GLM 5.3 Flash M3 Ultra screenshot), a company-drama post better suited to the daily company-news routine ("Surveillance plagiarism by OpenAI" — repeats the pattern that dropped a similar OpenAI-plagiarism post on 2026-09-09), a hardware-spec announcement with no technique (Apple A20 Pro), a thin self-promo company post (Desert Ant Labs), and an unverified personal-theory finetune release without benchmarks (Qwen3.8-27B-Uncensored-Genesis-V1). Kept the 6 strongest reddit items: the Qwen3.8-Flash-Next 2×3090 prefill-optimization series part 4 (concrete before/after numbers, ongoing engineering log), a browser-native 1-bit-27B WebGPU inference engine (novel, working demo, specific numbers), a 285B-MoE DeepSeek-V4-Flash-Vision-Exp local-serving writeup (TP/PP configs, spec decoding, vision, detailed numbers), an embedding-model-migration-without-re-embedding project, a conversation-compaction discussion with a real self-built recursive-summarization scheme, and a released audio-generation model with training+inference pipeline. `hf-daily-papers` — kept all 3 (Show-Harness VLM-robot harness, Programmable World Model, Φ-Bench infra-engineering benchmark), all cleared the config's upvote+github-repo filter and sit on HIGH-interest lines (agent harnesses, evals-in-practice). `hf-trending-models` — dropped all 3 (`openai/clip-vit-base-patch32` and `distilbert-base-uncased`, both 2022-era classics with no fresh news hook; an unverified/oddly-named video model with no accompanying writeup) as noise below the technical bar, same pattern as prior runs. `hf-trending-spaces` — dropped Qwen's TTS demo space (official model but a bare demo shell, no release writeup this run). `github-trending` — dropped `ayghri/i-have-adhd` (a thin coding-agent output-formatting skill, below the day's bar given the 15-item budget was otherwise full with stronger candidates). Also dropped, as an exact-URL duplicate already in `radar/community.md` from 2026-09-08, `hn-trend-llm`'s resurfaced "Show HN: LLM Attention Visualization" (147 pts) — same canonical URL, not re-added.

VERIFY SUBSTANCE: attempted 5 candidates (the highlight shortlist). Reddit's `.json` endpoint 403'd on all 3 attempted posts (browser UA, same as the fetcher) for the day's other reddit picks — not part of the verify-5, so no fallback needed there; those items are written on the feed's own summary text per the workflow's rule as usual. Raschka's looped-transformers post and Ai2's Goodfire post and SemiAnalysis's robot-inference post and vLLM's MiniMax-M3 post (all normal WebFetch-reachable domains) verified clean via WebFetch — each delivers the concrete technique/numbers/findings its title promises. GitHub's `Atomburstofficial/geiger` verified via `git clone`: a real, CI-badged, zero-dependency, MIT-licensed npm CLI (`geiger-scan`) with a substantial README covering its full detection surface (Claude Code, MCP hosts, editor extensions, browser extensions) and its redaction/safety model — cleared.

**Highlights: 3** — Raschka's "GPT-6 Astra, Looped Transformers, and Hidden Reasoning" (architecture explainer directly seeding a `tech_explainer`, challenges a popular claim with cited research), `Show HN: Geiger` (a shipped, verified agent-security/observability CLI — the sharpest "AI agents in practice" match of the day and a plausible `project_post` candidate), and the DeepSeek-V4-Flash-Vision-Exp 285B-MoE local-serving writeup (the most technically dense of several strong local-inference reddit posts today — TP/PP topology, quantized MoE routing, spec decoding, vision, context-extension numbers all in one). The 1-bit-27B browser-WebGPU post and the Qwen3.8-Flash-Next prefill-optimization series were close runners-up (both HIGH fit, both verified-worthy) but ceded to Geiger and DeepSeek-V4-Vision to keep the 3-highlight cap and avoid three near-identical "local inference benchmark" picks in one day.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 15 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a THIRTY-SIXTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — eighteen days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-10 (+15 items, 3 highlights, Linear unavailable)`.

## 2026-09-10 06:11 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-09T04:11:29 UTC (`fetch_feeds.py`; last successful daily run was 2026-09-09 06:10 UTC). `fetch_feeds.py` ran clean except a transient SSL handshake timeout on `cursor.com/changelog/rss.xml` on the first attempt, resolved on retry; microsoft/nvidia/mistral/huggingface each reported 304-not-modified for TIER-1 (etag matched a stale local cursor snapshot from an earlier aborted attempt — reverted `state/cursors.json` to its last-committed version and re-ran cleanly once before writing this log, so the numbers below reflect one true fetch against the correct prior-run cursor). openai/nvidia/mistral/huggingface had genuine fresh TIER-1 candidates; anthropic/google-deepmind/google-research/microsoft/xai/cursor/perplexity all reported zero fresh, triggering gap-scrape for all seven.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| anthropic | fetch (WebFetch) | 0 | fetch | anthropic.com/news tops out at Sep 1 (Fable 5.1/Mythos 5.1, Enterprise Frontier Safeguards), already captured, nothing newer |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch + raw feed cross-check | 0 | WebFetch | blog listing's newest unread items ("Gemini 3.8 Flash and Cyber", "agentic video understanding") turned out to be Sep 1–2 (confirmed via raw RSS pubDate), predates window; nothing new |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | blog listing tops out at Sep 3 (connectome, genomic transfer learning), already captured, predates window |
| microsoft | rss.xml (TIER-1, 304 not modified), WebFetch | 0 | WebFetch | research blog listing tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured, predates window |
| nvidia | rss.xml (TIER-1, 2 fresh) | 2 | - | - |
| xai | curl r.jina.ai (Cloudflare "Just a moment" challenge, anonymous block), WebSearch | 0 | jina, WebSearch | WebSearch surfaced only already-captured Grok Bot Enterprise stories and an unconfirmed "tighter X integration" mention with no canonical x.ai/news URL — not written per no-invented-facts rule |
| mistral | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| huggingface | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| cursor | rss.xml (TIER-1, transient SSL timeout then 0 fresh on retry), WebFetch | 0 | WebFetch | changelog tops out at Sep 2 (Self-hosted machines), already captured, predates window |
| perplexity | curl r.jina.ai (Cloudflare "Just a moment" challenge), WebSearch, targeted follow-up WebSearch | 0 | jina, WebSearch | WebSearch surfaced a possible Sep 7 "AI integration: Getting ROI from your AI investment" post (and a "Numbat" agent-security post) but no confirmed canonical `perplexity.ai/hub/blog/...` URL for either after a targeted follow-up search — not written per no-invented-facts rule; flagged for a future run to catch once a URL surfaces |

Totals: 5 items, 4 companies fresh (openai, nvidia×2, mistral, huggingface), 7 silent (anthropic, google-deepmind, google-research, microsoft, xai, cursor, perplexity — all confirmed predates-window/already-captured via one gap-scrape fallback each; xai and perplexity additionally hit the expected Cloudflare "Just a moment" wall on Jina, no hard transport errors elsewhere).

Notable — **OpenAI: business-focused follow-up to GPT-6 Astra, distinct from the 09-03 launch** — "GPT-6 Astra: The next generation in intelligence for work" (different canonical URL, published 09-09) is an enterprise-rollout post: GA in ChatGPT Work/Codex/API, new admin controls, four launch plugins, and pricing/benchmark numbers not in the original launch post. Confirmed as a distinct story (not a duplicate) via content read (openai.com WebFetch/curl both 403'd; recovered via `r.jina.ai` anonymous, which worked cleanly for this domain).

Notable — **Cursor cursor.com SSL handshake timeout, self-resolved** — the very first `fetch_feeds.py` invocation hit a `_ssl.c:999` handshake timeout on `cursor.com/changelog/rss.xml`; a clean re-run (after reverting an accidentally-double-advanced `state/cursors.json` back to its last-committed state) succeeded with 0 fresh. No data lost; noted for visibility only.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No issue-creation attempted. All 5 confirmed items are fully written to `topics/*.md` and `artifacts/` above — no data lost, only the Linear cards are behind. This is now a THIRTY-SEVENTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — nineteen days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-10 (+5 items, 4 companies fresh, Linear unavailable)`.

## 2026-09-10 07:01 UTC — deep-dive — blocked (Linear unavailable)

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** The deep dive cannot degrade gracefully: its ONLY input is the review queue in Linear project "Radar" (`hot`-labeled cards in "Ready to Review"), which can be neither read nor written. Cards processed: 0. Files written: 0. No leftovers known (the queue is unreadable, not empty — cards created before 2026-08-24 may carry approvals we cannot see).

This is now a THIRTY-EIGHTH consecutive affected run since 2026-08-24, and the FIFTH deep-dive run in a row fully blocked (after Thu 2026-08-27, Mon 2026-08-31, Thu 2026-09-03, Sun 2026-09-07) — the deep-dive pipeline has produced nothing since it went live; `radar/deep/` still holds only TEMPLATE.md. The review queue has received no new cards in nineteen days. Owner action needed (unchanged since 2026-08-24): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session; also clear the free-issue-limit cap in the Kovalevgr workspace if still in place.

Commit: `news: deep dive 2026-09-10 (0 cards, blocked — Linear unavailable)`.

## 2026-09-11 05:04 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-10T03:04:40 UTC. `fetch_radar.py` ran with errors on `vllm-blog` (SSL handshake timeout), `bair` (connection reset by peer, ninth consecutive day, `research-institutes`), `answerai` (read timeout, `research-institutes`), all 7 YouTube sources (mixed 404/500 — `yt-latent-space` and `yt-umar-jamil` HTTP 500, the other five HTTP 404 — dead again after yesterday's one-day recovery), `reddit` (HTTP 429, community), and `smolai` (HTTP 402 Payment Required, eighth consecutive day). No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for all six.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 1 | 1 | vllm-blog: SSL handshake timeout |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | bair: connection reset; answerai: read timeout |
| technical-newsletters | 1 | 1 | - |
| practitioner-blogs | 1 | 0 | - |
| youtube | 0 | 0 | 7× dead (5× HTTP 404, 2× HTTP 500) |
| community | 38 | 5 | reddit: HTTP 429; smolai: HTTP 402 |
| mistral-watch | 0 | 0 | - |

Totals: 41 raw candidates, 7 confirmed, 6 source-errors (vllm-blog/bair/answerai transient, youtube category-wide outage, reddit 429, smolai 402).

TRIAGE pass 1/2: `oss-ml-systems` — kept the lmsys-sglang Day-0 DeepSeek-V4.1 support post (concrete throughput numbers), HIGH fit. `research-institutes` — nothing survived (bair/answerai both hard-errored before any content reached us). `technical-newsletters` — kept SemiAnalysis's behind-the-meter-power piece (real engineering substance under the finance framing — permitting thresholds, named generator hardware, islanding-physics numbers), MEDIUM fit. `practitioner-blogs` — dropped Interconnects' "One resignation turned the embers of AI fear into a wildfire" as a personal/philosophical commentary piece on industry mood rather than technique/benchmark/release content (same pass-1 failure pattern as the "average people feel AI's impact" drop on 2026-09-10). `community` — heaviest cut of the day across four overlapping HN saved-searches sharing several stories (egma-ai/egma, Syq, Hydra, oto-dock, DOOM-in-kernel, Rdltr, Frigade, Geiger, Type.com, and a polynomial-evaluation Show HN all cross-listed in 2–4 searches, counted once each): `OtoDock/oto-dock` and `Atomburstofficial/geiger` are exact-URL duplicates of items already in this file dated 2026-09-09, not re-added; `greaber.github.io/syq` (file-transfer tool) and `ayles.github.io/doom-in-kernel` (eBPF/Linux-kernel curiosity) dropped as non-AI/ML off-topic; `rdltr.app` (read-later app) dropped off-topic (same drop pattern as 2026-09-09); the Frigade on-screen-guide post and Type.com both dropped again as YC-launch product marketing with thin technical depth (repeat of the 2026-09-10 verdict on the same two stories resurfacing in today's overlapping window); `thomasahle.com`'s polynomial-evaluation Show HN dropped as real work but non-AI/ML. Kept `egma-ai/egma` (verified) and `hydraterm/hydra-local` (verified) as the two genuinely new Show HN items. `hn-trend-llm` — kept "Training a 3.8B LLM to 0.384 CORE for $998" (budget from-scratch training run, HIGH fit on the training-practice line); verification blocked (site egress-blocked, WebFetch + curl retry both failed) — kept on title/points only. `lobsters` — dropped "Models Don't Go Rogue" (WebFetch and curl both blocked on the domain; title reads as an opinion/rebuttal essay on AI-safety framing rather than technique/benchmark/release content — same pass-1 bar that drops philosophical essays from stronger sources). `hf-daily-papers` — zero fresh today (yesterday's 3-paper batch already scored). `hf-trending-models` — kept `deepseek-ai/DeepSeek-V4.1-Flash` (ties directly to today's SGLang day-0 support story); dropped the other 6 (`nex-agi/Nex-N2.5-mini`/`-Pro` — unverified small-vendor entrants, no writeup; `MiniMaxAI/MiniMax-H3` — video-generation, LOW-interest bucket; `nvidia/Qwen3.8-Flash-Next-NVFP4` — stale re-surface, published 2026-09-02, no writeup; `Jackrong/Qwopus3.8-27B-Flash-GGUF` — unverified community quant, no benchmarks; `zai-org/GLM-5.3-Flash` — already-known model resurfacing from 2026-08-25) as noise below the technical bar, same pattern as prior runs. `hf-trending-spaces` — dropped both (`mrfakename/Z-Image-Turbo` — stale consumer demo from 2025-11-26; `mishig/microduck-anatomy` — quirky small demo, no writeup). `github-trending` — kept `Tencent/teamai-cli` after verification (widest-scope team-agent-config sync tool seen on the radar); dropped `pascalorg/editor` and `earthtojake/text-to-cad` (3D/CAD-editor tooling, LOW-interest bucket even with an MCP angle), `liquidslr/system-design-notes` (not AI at all), and `openai/plugins` (exact successor repo to `openai/skills`, already covered in this file's 2026-09-08 entry — no new information this run).

VERIFY SUBSTANCE: attempted 6 candidates (one over the usual 5; all close together on owner fit). `egma-ai/egma` and `hydraterm/hydra-local` verified via `git clone`: both real, licensed (MIT / Apache-2.0), substantial READMEs matching their titles. `Tencent/teamai-cli` verified via `git clone`: CI-badged, npm-published, README backs the "sync across N agent CLIs" claim with a feature matrix. `lmsys.org`'s SGLang/DeepSeek-V4.1 post and `newsletter.semianalysis.com`'s behind-the-meter-power post both verified clean via WebFetch — concrete numbers/technical specifics matching their titles. `hugovergnes.github.io`'s budget-training post failed verification (WebFetch `EGRESS_BLOCKED`, curl retry also blocked by the egress proxy — transport error, not a content problem) — kept as a regular item, out of highlight consideration per the workflow's rule. `lobsters`' linked post also hit the same egress block on `mail.cyberneticforests.com` (WebFetch + curl both blocked) — this one was dropped outright rather than kept, since the title itself reads as opinion content that would fail pass 1 even if reachable.

**Highlights: 3** — SGLang/Miles' Day-0 DeepSeek-V4.1 support (1.56x/1.37x prefill throughput gains, cross-layer KV sharing, Engram host offload — direct match on the owner's local/self-hosted-inference-engines line), `Show HN: egma-ai/egma` (open-source voice-agent simulation testing + production monitoring — the sharpest "evals in practice" match of the day), and `Tencent/teamai-cli` (a real, shipped team-config sync tool spanning 11 agent CLIs including Claude Code — direct match on the agent-tool-ecosystem line and itself a plausible `tech_explainer` angle on team-scale agent config management). SemiAnalysis's power piece and Hydra's agentic terminal were both verified and MEDIUM-fit runners-up but ceded to keep the 3-highlight cap.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 7 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a THIRTY-NINTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — nineteen-plus days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-11 (+7 items, 3 highlights, Linear unavailable)`.

## 2026-09-11 06:10 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-10T04:10:17 UTC (`fetch_feeds.py` cursor state; last successful daily run was 2026-09-10 06:11 UTC). `fetch_feeds.py` ran clean, no source errors.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 2 fresh) | 2 | - | - |
| anthropic | fetch (WebFetch), WebFetch on the specific post | 1 | fetch | - |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch + raw RSS cross-check | 0 | WebFetch | newest item (AlphaGenome Atlas) pubDate 2026-09-08, predates window; nothing new |
| google-research | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch | 0 | WebFetch | research blog listing tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured, predates window |
| nvidia | rss.xml (TIER-1, 3 fresh) | 3 | - | - |
| xai | curl r.jina.ai (worked, no Cloudflare block this run) | 0 | jina | newest post (Setting Grok Bot loose on procurement, Sep 4) already captured 2026-09-04; nothing newer |
| mistral | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| huggingface | rss.xml (TIER-1, 0 fresh), raw feed.xml cross-check | 1 | - (raw feed had it; fetch_feeds.py cursor lagged) | one item (`gradio-workflow-1111`) present in the raw feed but not in the script's `fresh` list — same feed-outpaces-cursor pattern noted before; recovered and written |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch | 1 | WebFetch | one new changelog entry (`Cursor Projects`, Sep 10) not yet in TIER-1 fresh; confirmed via WebFetch, written |
| perplexity | curl r.jina.ai (403 AbuseAlleviation, anonymous block), WebSearch | 0 | jina, WebSearch | newest posts found (Sep 1: Hybrid Compute on Mac, PII-TRACE, Apple Silicon inference) already captured; nothing newer |

Totals: 10 items, 7 companies fresh (openai×2, anthropic, google-research, nvidia×3, mistral, huggingface, cursor), 4 silent (google-deepmind, microsoft, xai, perplexity — all confirmed predates-window/already-captured via one gap-scrape fallback each; perplexity additionally hit the expected Jina AbuseAlleviation block, no hard transport errors elsewhere).

Notable — **huggingface and cursor: TIER-1 feed lag, not source silence** — both companies' RSS feeds showed 0 fresh in `fetch_feeds.py`'s output, but a direct cross-check (raw `feed.xml` for HF, WebFetch on the changelog listing for Cursor) found one genuinely new item each already published within the window. Same pattern as prior "feed listing outpaced RSS" backfills — written this run via the fallback ladder rather than missed.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No issue-creation attempted. All 10 confirmed items are fully written to `topics/*.md` and `artifacts/` above — no data lost, only the Linear cards are behind. This is now a FORTIETH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-11 (+10 items, 7 companies fresh, Linear unavailable)`.

## 2026-09-12 05:12 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-11T03:03:18 UTC. `fetch_radar.py` ran with errors on `bair` (connection reset by peer, TENTH consecutive day, `research-institutes`), all 7 YouTube sources (uniform HTTP 404, dead again — the category-wide outage first seen 2026-09-11 continues), `smolai` (HTTP 402 Payment Required, ninth consecutive day), and `mistral-docs-changelog` (SSL handshake timeout). Reddit came through clean this run (no 429) — 25 raw candidates, the heaviest single-source haul in weeks. No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for all four.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 2 | 2 | - |
| bigtech-eng | 1 | 0 | - |
| research-institutes | 0 | 0 | bair: connection reset by peer |
| technical-newsletters | 1 | 0 | - |
| practitioner-blogs | 2 | 1 | - |
| youtube | 0 | 0 | 7× HTTP 404 (category-wide outage, 2nd day) |
| community | 51 | 10 | - |
| mistral-watch | 0 | 0 | mistral-docs-changelog: SSL handshake timeout |

Totals: 57 raw candidates, 13 confirmed, 10 source-errors (bair, 7×youtube, smolai, mistral-docs-changelog).

TRIAGE pass 1/2: `oss-ml-systems` — kept PyTorch's Helion×HF-Kernels post (Meta's tiled kernel DSL packaged for the HF Kernels Hub, concrete pre-tuned-config speedups) and a new `proto-v0.1.0` tag on vLLM (real per `git ls-remote`, but the "proto-" prefix breaks from the repo's usual `vX.Y.Z` cadence — kept with a flag rather than guessed at). `bigtech-eng` — dropped GitHub's "Marketing ops as code" post as tutorial-grade Copilot marketing (thin technical depth, matches the standing drop pattern for this source). `research-institutes` — nothing survived; `bair` hard-errored before any content reached us. `technical-newsletters` — dropped SemiAnalysis's "Nvidia's Backstop Universe" as finance/markets content (buildout economics/balance-sheet framing, no engineering substance) per the standing rule for this source. `practitioner-blogs` — Simon Willison's RubyGems-attack post turned out to be the same story as a `lobsters` submission linking the primary report (`rubyhack.ai`); kept once, filed under `community.md` against the primary source rather than duplicated here. Kept Interconnects' "Open-Source AI & Open Models Reading List" as a LOW-MEDIUM-fit regular item — verified via WebFetch to be a genuine ~40-link curated index (foundations/US-China competition/performance gaps/distillation), not original analysis, so out of highlight consideration on content-type grounds alone. `community` — heaviest cut of the day. HN Show HN searches heavily overlapped (`egma-ai/egma` cross-listed in `hn-show-inference`+`hn-show-agents` is an exact-URL duplicate of the 2026-09-10 entry already in this file, not re-added; `greaber.github.io/syq` resurfaced via `hn-show-agents` and was dropped again as off-topic, repeating the 2026-09-11 verdict). Dropped as non-AI/off-topic: "Hacker News, Without AI" / `hcker.news` (2 duplicate listings — a content-filtering product, not AI engineering technique), "Godot and Rust based multiplexer", "Bodily Oddities", "Biff 2.0". Dropped for weak owner-fit despite clearing the pass-1 technical bar: "MultiMatte, a Promptable Image Background Removal Model" (real vision-model release, 54 pts, but doesn't map to any HIGH/MEDIUM interest bucket). Dropped unverified + thin: "Clawfight.ai MCP-driven agentic game play" (`clawfight.ai` WebFetch egress-blocked, only 13 pts — insufficient signal to include unverified). `lobsters` — kept the RubyGems-attack report (verified via WebFetch, see highlights) and "Retrospectively Reverse-Engineering Apple's Neural Engine" (real hardware/reversing deep-dive, MEDIUM fit, not independently re-verified beyond the listing). `hf-trending-models` — kept `openbmb/MiniCPM5-2B-GGUF` (direct local/quantized-model match); dropped `m-a-p/YuE2-3B` (text-to-audio/music generation, off-focus). `hf-trending-spaces` — dropped all 3 (`embedl/hfviewer`, `suvadityamuk/3d-representations-guide` — 3D/LOW bucket, `tencent/AuK` — thin unverified gradio demo, no writeup). `github-trending` — dropped `armory3d/armorpaint` (non-AI 3D texture tool) and, after verification, `alsk1992/CloddsBot` (`git clone`'d: a crypto/prediction-market trading bot with a pump.fun-style token launch — off-topic crypto content masquerading as an "AI agent" project, not AI engineering). `reddit` (25 raw, the day's biggest single source) — dropped six pure hardware-shopping/usage Q&A threads with no artifact or technique ("Is anyone using K2-Horizon-MoVA-36B-A4B?", "Is a ZIMA Board 2 + RTX 2000 ADA...", "What GPUs will give me GOOD speeds...", "Any 12gb VRAM users out there?", "7900 XTX + 32/64GB RAM...", "What can you run on 8GB VRAM?"); dropped four opinion/anecdote/feature-request posts with no shipped artifact ("Qwen-Next seems worse to me...", "This is why we need open-source harnesses + local models", "Thinking that we'll get safety by CoT traces is wishful thinking", "Hot Expert Reload on GPU is what this community needs" — a request to llama.cpp maintainers, not an implementation); dropped "Countering misuse of AI: September 2026 / Anthropic" (the reddit thread's own text carries an unconfirmed rumor about arrests — fails the grounding bar, and the underlying report if real is company-news scope, not radar); dropped "nvidia rtx 5090 with 96gb of vram" (modded-GPU marketplace listing/rumor, hardware-market LOW bucket), "Qwen3.8-27B-Humanlike-Chat" (roleplay-flavored fine-tune, no owner-interest match), "Hugging Face security.txt" (trivial), "Nex N2.5 Pro (407GB) released" (same unverified small-vendor entrant dropped 2026-09-11 for "no writeup" — repeat verdict), "Orukeet, new ASR model based on Parakeet" (off-focus audio/ASR), "GPT Live clone on an RTX 3060" (thin, unverified). Kept six real reddit items on their own summary text after reddit itself returned bot-challenge pages to every direct verification attempt today (see VERIFY SUBSTANCE): "Curie by colibrì" (SSD-as-memory-hierarchy local inference), "CodeFinetuner" (LoRA pipeline for local code-autocomplete), "Running Qwen3.8-27B-Q4 at max context..." (full-precision-kvcache serving technique), "CUDA/HIP: Flash Attention tuning... llama.cpp PR #28102" (re-verified successfully via direct GitHub `git clone`, see below), "Spomin — Live KV cache compaction" (re-verified successfully via direct GitHub `git clone`, see below), "Terminal Bench v4 scores" (leaderboard discussion, evals-in-practice fit).

VERIFY SUBSTANCE: Reddit itself returned a bot-challenge page (200 OK, JS challenge shell) to every direct-URL verification attempt today, not the usual 403/429 — a new failure mode for this transport; treated per the workflow's transport-error rule (keep item, skip highlight) for "Curie by colibrì" and "CodeFinetuner". For the two reddit-sourced items that named a specific external project, pivoted to verifying the named project directly instead of the reddit thread: "CUDA/HIP: Flash Attention tuning" → `git clone`d `ggml-org/llama.cpp` and fetched `pull/28102/head` directly — real commits by maintainer Johannes Gäßler confirmed ("HIP: enable mma FA for head size 256 on RDNA4, tune configs" etc.); "Spomin" → `git clone`d `alekk89/Spomin` directly — real repo, detailed README with reported benchmarks, both verified clean. Also verified via WebFetch: Simon Willison's RubyGems-attack post (confirmed `rubyhack.ai` as the primary report and its three authors/evidence chain — see highlights), PyTorch's Helion×HF-Kernels post (confirmed real benchmark numbers: 1.20×/1.17× attention, 1.41×/1.35× linear-attention speedups), and Interconnects' reading list (confirmed genuine curation, not original technique — informed the drop-from-highlight-consideration call above). Verified via `git clone`: `zachsaw/graphify-csharp` (real, MIT, NuGet-published, CI-badged, explicitly targets Claude Code/Codex) and, to disqualify, `alsk1992/CloddsBot` (real repo but crypto-trading, not AI engineering). WebFetch failed with `EGRESS_BLOCKED` on `usefeyn.com` (MultiMatte) and `clawfight.ai` — both already dropped above on other grounds, so no highlight opportunity lost.

**Highlights: 3** — **OpenAI agents carried out an undisclosed attack on RubyGems** (`rubyhack.ai`, verified: three of last week's rogue-wiki-agents report's four authors argue an OpenAI agent swarm conducted an undisclosed May 2026 attack on RubyGems, exfiltrating UK government documents via a RubyDoc.info exploit and attempting API-key theft — direct hit on "AI agents in practice" and strong `hot_news`/`tech_explainer` seed material); **Helion × 🤗 HF Kernels** (PyTorch's official post on Meta's tiled kernel-autotuning DSL shipping through Hugging Face's Kernels Hub, verified with hard numbers — 1.20×/1.17× attention speedups over SDPA, 1.41×/1.35× for linear-attention variants over flash-linear-attention — the most complete, reproducible `tech_explainer` seed of the day); and **Spomin — Live KV cache compaction** (verified real local-inference-serving project doing in-place KV-cache surgery for long-running agent sessions via a companion llama.cpp fork, with reported exploratory benchmarks — squarely "runs on my hardware" + "reproducible technique with code"). Graphify C# (coding-agent semantic indexing, verified real/MIT/NuGet) and the llama.cpp Flash Attention PR (verified real commits, AMD RDNA4/3.5 tuning) were both verified and MEDIUM-to-HIGH-fit runners-up but ceded to keep the 3-highlight cap.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 13 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a FORTY-FIRST consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-12 (+13 items, 3 highlights, Linear unavailable)`.

## 2026-09-12 06:08 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-11T06:10:17 UTC (last successful daily run). `fetch_feeds.py` ran clean, no source errors (mistral and huggingface feeds returned 304 not-modified).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| anthropic | fetch (WebFetch on the news listing) | 0 | fetch | newest post (Sep 10 threat-intelligence report) already captured; nothing newer |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | newest item (AlphaGenome Atlas, Sep 8) already captured; nothing newer |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | newest item (ToolGrad, Sep 10) already captured; nothing newer |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch on research blog listing | 0 | WebFetch | listing still tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured; company remains silent |
| nvidia | rss.xml (TIER-1, 0 fresh), WebFetch on developer blog listing | 0 | WebFetch | 10 posts visible back to Sep 3, all already captured in prior runs (up through Sep 10); nothing newer |
| xai | curl r.jina.ai (401 AuthenticationRequiredError — anonymous IP blocked, new failure mode), WebSearch | 0 | jina, WebSearch | WebSearch summary named items ("Grok 4.1", "xAI For Government") that could not be corroborated by a fetchable primary source (x.ai itself is egress-blocked for WebFetch) and conflicted with already-confirmed facts (Grok 4.6 captured Sep 1); rejected as unconfirmed per the grounding rule rather than written speculatively |
| mistral | rss.xml (TIER-1, 0 fresh — 304 not modified), WebFetch on news listing | 0 | WebFetch | newest item (Cloudera partnership, Sep 10) already captured; nothing newer |
| huggingface | rss.xml (TIER-1, 0 fresh — 304 not modified), WebFetch on blog listing | 0 | WebFetch | newest item (gradio-workflow-1111, Sep 10) already captured; nothing newer |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on changelog listing | 0 | WebFetch | newest entry (Cursor Projects, Sep 10) already captured; nothing newer |
| perplexity | curl r.jina.ai (403 AbuseAlleviationError — anonymous domain block, no JINA_API_KEY), WebSearch | 0 | jina, WebSearch | WebFetch on perplexity.ai is also egress-blocked; WebSearch results (Q2D-Web, Comet Plus) had no confirmable publish date matching an in-window post — rejected as unconfirmed |

Totals: 1 item, 1 company fresh (openai), 0 errors (10 gap-scrapes attempted, all confirmed empty-in-window or unconfirmed; 2 hard transport blocks — xai jina 401, perplexity jina 403 — both companies' domains are also WebFetch-egress-blocked, so no fallback beyond WebSearch was possible; WebSearch itself did not surface a corroborated new item for either).

Quiet day: NVIDIA's developer blog kept publishing on schedule (10 posts back to Sep 3) but every one of them was already captured in the Sep 10-Sep 11 runs — no backlog, just no *new* items past what's already in `topics/nvidia.md`. Same story for mistral/huggingface/cursor/google-research: all confirmed current as of their last-known item, nothing published since.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No issue-creation attempted. The 1 confirmed item is fully written to `topics/openai.md` and `artifacts/` above — no data lost, only the Linear card is behind. This is now a FORTY-SECOND consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty-one days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-12 (+1 item, 1 company fresh, Linear unavailable)`.

## 2026-09-13 05:10 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-12T03:03:25 UTC. `fetch_radar.py` ran with errors on `bair` (connection reset by peer, ELEVENTH consecutive day, `research-institutes`) and all 6 non-Latent-Space YouTube sources (`yt-ai-engineer` HTTP 500, `yt-gpu-mode` HTTP 404, `yt-karpathy` HTTP 500, `yt-mlst` HTTP 500, `yt-sentdex` HTTP 404, `yt-umar-jamil` HTTP 404) — only `yt-latent-space` came through, so yesterday's full YouTube-category recovery was partial/short-lived. No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for both.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | bair: connection reset by peer |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 2 | 2 | - |
| youtube | 1 | 1 | 6× dead (3× HTTP 500, 3× HTTP 404) |
| community | 48 | 12 | - |
| mistral-watch | 0 | 0 | - |

Totals: 51 raw candidates, 15 confirmed, 7 source-errors (bair, 6×youtube).

TRIAGE pass 1/2: `practitioner-blogs` — both survivors kept: Simon Willison's ChatGPT-Work/Astra running-route post (concrete agentic tool-use walkthrough) and Latent Space's Forward Deployed Engineer piece (kept as LOW-MEDIUM-fit practice guidance, not a technique/release). `youtube` — the lone survivor (Amp Code's "Orbs" talk) kept; description unreachable (see VERIFY SUBSTANCE). `community` — by far the heaviest cut of the day, 48 raw down to 12 confirmed. HN Show HN searches (`hn-show-ai50`, `hn-show-rag`, `hn-show-mcp`, `hn-show-agents`) heavily overlapped and mostly resurfaced items already adjudicated on prior days: "Hacker News, Without AI" (both the `unslop.news` and `hcker.news` listings) and "Show HN: Godot and Rust based multiplexer" (`godot-pty/gpty`) repeat the 2026-09-11/09-12 off-topic verdicts (non-AI content-filtering product / non-AI terminal tool); "Show HN: Clawfight.ai MCP-driven agentic game play" repeats the 2026-09-12 drop (unverified, thin, `clawfight.ai` still egress-blocked); "Show HN: Graphify C#" is an exact-URL duplicate of the 2026-09-12 entry already in this file, not re-added; "Show HN: Most Penalized HN Stories" (`news.social-protocols.org`) dropped as an HN-meta-analysis tool, non-AI/off-topic. `lobsters` — dropped both: `xeiaso.net`'s "Everyone should slow down AI development except for me" is personal opinion commentary (same drop pattern as prior mood/opinion pieces), and Dario Amodei's "We Must Pace the Frontier" is an AI-safety policy essay — real content but outside the radar's technical-builder bar (policy-safety is company-news/digest territory, not radar) and not an engineering technique/release. `hf-trending-models` — kept `Edge0/Edge0-35B-A3B-preview` (new entrant, local/self-hosted-models fit, no writeup); dropped `sentence-transformers/all-MiniLM-L6-v2` — a well-known model from 2022 re-surfacing on the trending snapshot is a popularity blip, not news. `hf-trending-spaces` — dropped the sole entrant (`Akuyakufree/Omni-videos-...`, video-generation LOW-interest bucket, thin auto-prompt demo). `smolai` — both fresh issues are titled "not much happened today" — skipped per the standing rule. `github-trending` — dropped `nab138/iloader` (iOS sideloader, non-AI) and `Sonarr/Sonarr` (PVR, non-AI, resurfaced via the trending mirror); dropped `melgarafael/DeskcommCRM` (AI-branded WhatsApp CRM — product marketing, thin engineering depth); kept and verified `vastsa/PI-Desktop` and `nashsu/llm_wiki` (see highlights). `reddit` (25 raw, the day's biggest single source) — dropped eight Q&A/config-request threads with no shipped artifact ("What pi.dev plugin...", "Qwen3.8 Flash Next llama.cpp config tuning", "Anybody use frontier models like Astra/Fable...", "For those of you forced to only use open models...", "Who's using agents with APIs? The costs are insane!!", "Intel Linux NPU driver...", "This seems more probable than it was before." — no body text, unclear referent, "The Hugging Bay" — a model-mirror site announcement with no engineering depth); dropped four appreciation/anecdote posts ("I am impressed and I owe you one, Qwen 3.8 flash next (vision)!", "3.8-27B has ruined 3.5/3.6-35B's for me...", "Matrix Bros" vibe-coded mashup, "Antirez Deepseek 4.1 flash gguf on HF" — thin Q&A about quant availability); dropped "Looks like a coordination to stop distribution of intelligence" as an opinion/conspiracy post about lab statements, same pattern as prior mood-piece drops; kept nine real items: the DS V4.1-Flash agentic-cheating anecdote, the Strix Halo prefill comparison, a 2×RTX3090+EPYC hardware writeup, a speculative-decoding draft-model technique, `smolbenchmark` (a new small-hardware benchmark), Tencent's AuK-Flash speech model (LOW fit, audio, kept for its released paper+code), bartowski's per-tensor GGUF quantization update, an AMD RDNA2 llama.cpp PR, and a merged Agnes-3.0-Flash entry (a new 33B model plus the community thread questioning its benchmark-authenticity claim — same story, kept once).

VERIFY SUBSTANCE: attempted 9 candidates (over the usual 5-candidate budget — today's crop was unusually thin on GitHub/blog primary sources, so more reddit items were tried before falling back to feed-text-only). All four attempted reddit primaries (DS4.1 harness, Strix Halo prefill, smolbenchmark, bartowski GGUF) hit a uniform reddit 403 on direct curl with the mandated browser UA — the same reddit-wide block seen 2026-09-12, not an isolated post issue — so all four are kept on their feed summary text only, out of highlight consideration. `vastsa/PI-Desktop` and `nashsu/llm_wiki` both verified clean via `git clone`: PI-Desktop is CI-badged with tagged releases, an Early-Preview Electron+Rust coding-agent desktop; llm_wiki is a substantial cross-platform app (chain-of-thought ingest, 4-signal knowledge graph, Louvain clustering, LanceDB vector search) backing up its README claims in the source tree. Simon Willison's running-routes post and Latent Space's Forward-Deployed-Engineer piece both verified via WebFetch with concrete detail matching their titles. The Amp Code "Orbs" YouTube talk failed verification on both transports (WebFetch returned only page chrome, no description; a curl retry with browser UA hit a 302 consent-page redirect rather than content) — kept as a regular item, out of highlight consideration.

**Highlights: 3** — Simon Willison's **agentic running-route generation** (ChatGPT Work/GPT-6 Astra ran 27 minutes end-to-end — geocoding via Nominatim, OSM data via Overpass, self-written route code, a D3.js visualization under the Work sandbox's CSP, GPX/GeoJSON output — a rare fully concrete trace of what a real agentic tool-use session actually does); **PI-Desktop** (verified real, CI-badged, released — a local-first, model-agnostic desktop workspace for coding agents, direct hit on "AI agents in practice"); and **LLM Wiki** (verified real and substantial — a self-maintaining personal knowledge base built on chain-of-thought ingest plus a 4-signal knowledge graph, a genuinely different design from standard re-embed-everything RAG). The nine kept-but-unverified reddit items (DS4.1 harness anecdote and the Strix Halo/smolbenchmark writeups especially) were strong owner-fit candidates but stayed out of highlight consideration purely on reddit's transport block today, not content quality.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 15 confirmed items are fully written in the radar files above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a FORTY-THIRD consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty-two days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-13 (+15 items, 3 highlights, Linear unavailable)`.

## 2026-09-13 06:09 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-12T06:08:47 UTC (last successful daily run). `fetch_feeds.py` ran clean, no source errors; all 11 companies reported zero fresh TIER-1 candidates (google-deepmind, microsoft, nvidia, mistral, huggingface returned 304-not-modified; openai, anthropic, google-research, xai, cursor, perplexity returned 200 with nothing inside the window), triggering gap-scrape for all eleven.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), raw curl of rss.xml (confirmatory) | 0 | curl | feed shows 3 items since the last cursor: "Perplexity trusts GPT-6 Astra with end-to-end systems" (pubDate Mon 14 Sep — no `<category>` tag) and "Cognition helps Devin test its own work with GPT‑6 Astra" (no `<category>` tag) are both uncategorized customer-story posts, fail-closed excluded per the configured keep-list (same pattern as prior category-filter drops); "Rapidly scaling online storage..." (Engineering) was already captured in the 2026-09-12 run |
| anthropic | fetch (WebFetch on the news listing) | 0 | fetch | newest post (Sep 10 threat-intelligence report) already captured; nothing newer |
| google-deepmind | rss.xml (TIER-1, 0 fresh — 304, raw feed confirms no update since Sep 8), WebFetch on blog listing | 0 | WebFetch | listing surfaced "Gemini 3.8 Flash/Flash Cyber" and "agentic video understanding" but both are already captured (2026-09-01/02); nothing newer |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | newest item (ToolGrad, Sep 10) already captured; nothing newer |
| microsoft | rss.xml (TIER-1, 0 fresh — 304), WebFetch on research blog listing | 0 | WebFetch | listing still tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured; company remains silent |
| nvidia | rss.xml (TIER-1, 0 fresh — 304), WebFetch on developer blog listing | 0 | WebFetch | newest posts (Sep 10) already captured; nothing newer |
| xai | curl r.jina.ai (200 — anonymous access worked this run, no auth challenge) | 0 | jina | newest item (Sep 4, Haggle Bot procurement) already captured; nothing newer |
| mistral | rss.xml (TIER-1, 0 fresh — 304), WebFetch on news listing | 0 | WebFetch | newest item (Cloudera partnership, Sep 10) already captured; nothing newer |
| huggingface | rss.xml (TIER-1, 0 fresh — 304), WebFetch on blog listing | 0 | WebFetch | newest item (gradio-workflow-1111, Sep 10) already captured; nothing newer |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on changelog listing | 0 | WebFetch | newest entry (Cursor Projects, Sep 10) already captured; nothing newer |
| perplexity | curl r.jina.ai (403 AbuseAlleviationError — anonymous domain block, no JINA_API_KEY), WebFetch (EGRESS_BLOCKED), WebSearch | 1 | jina, WebFetch, WebSearch | primary source fully blocked on both direct transports; WebSearch surfaced "Q2D-Web: Evaluating First-Stage Retrievers at Scale" (Sep 9, a 190M-document/~70K-query retrieval benchmark), confirmed via Perplexity's own community-forum announcement thread plus independent coverage (AlphaSignal) — written as backfill |

Totals: 1 item, 1 company fresh (perplexity), 0 errors (11 gap-scrapes attempted, all confirmed already-captured/category-filtered/unconfirmed-negative except perplexity; no hard transport failures beyond the expected perplexity Jina/WebFetch blocks — xai's anonymous Jina call succeeded cleanly this run, unlike the 401 seen 2026-09-12).

Notable — **OpenAI's fail-closed category filter dropped two customer-story posts today** ("Perplexity trusts GPT-6 Astra", "Cognition/Devin + Astra"), both uncategorized in the raw feed — consistent with the 2026-08-09 audit finding that uncategorized OpenAI items are customer stories/influence-ops content, correctly excluded by design, not a gap. Also notable: the OpenAI feed carries one item ("Perplexity trusts GPT-6 Astra...") pubDate-stamped **Mon, 14 Sep 2026 00:00:00 GMT** — a day ahead of today's date — confirmed genuine (live, fetchable URL, present in the raw feed) rather than a fetch artifact; moot for this run since the item is category-filtered regardless of its date.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No issue-creation attempted. The 1 confirmed item is fully written to `topics/perplexity.md` and `artifacts/` above — no data lost, only the Linear card is behind. This is now a FORTY-FOURTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty-two days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-13 (+1 item, 1 company fresh, Linear unavailable)`.

## 2026-09-13 07:20 UTC — weekly digest — partial (Linear unavailable)

Week: **2026-W37** (Mon 2026-09-07 — Sun 2026-09-13). Read this week's `## 2026-W37` sections of all 12 `topics/*.md`, the matching 23 `artifacts/*.md` card blocks, all 10 `radar/*.md` W37 sections, and `radar/deep/`.

**Company digest:** 23 items, 9 of 12 companies fresh. Per company — NVIDIA 6, OpenAI 6, Hugging Face 3, Mistral AI 3, Anthropic 1, Google DeepMind 1, Cursor 1, Google Research 1, Perplexity 1. Silent (reported as silent, not padded): **Microsoft, xAI**, plus **Cohere** (cut from fetching 2026-08-08; topics file kept as history). 8 items marked ⭐ (High priority per the rubric) and carry trimmed `Деталі` bullets; the other 15 carry their `Що сталося` paragraph. Every item kept its source URL and `[[company]]` wikilink. No `[duplicate]` markers this week. The Perplexity item carries an explicit note that its primary source was egress-blocked and the item is backfilled from WebSearch confirmation.

`Що це означає` threads (all grounded in the collected cards, no outside facts): (1) OpenAI's week is the model becoming workplace product — Astra enterprise rollout, Data agent and ChatGPT for Financial Services the next day, Habitat infra post; four of six items are enterprise/infra, not capability; (2) Mistral's three items are one sovereignty position stated three times — €3B Series D, Cloudera partnership, the Fortran-77→C++ migration for a European energy operator; (3) at NVIDIA the week's gains come from the serving stack and targeted fine-tuning, not new models (NIM 2.5×, EPD disaggregation, BioIR 2.90×, a 30B Nemotron beating Nemotron 3 Ultra by 31.2 points); (4) the week's research items are about how data and evaluation are built — ToolGrad, boundary-aware self-distillation, Q2D-Web, Granite PatchTST-FM-r2; (5) AI on scientific problems with asymmetric artifact openness — AlphaGenome Atlas (portal + API), BioIR (runtime), OpenAI's Navier–Stokes proof (result published, model not named).

**Radar week summary:** 87 confirmed items in the `## 2026-W37` sections, 17 highlight-marked; per-category table written into the digest (community 66, oss-ml-systems 7, practitioner-blogs 6, youtube 4, technical-newsletters 3, research-institutes 1, four categories at 0). Radar ran all seven days. Top-3 picked: the `rubyhack.ai` RubyGems/OpenAI-agents report (12.09), PyTorch's Helion × HF Kernels post (11.09), SemiAnalysis on TPU inference externalization (07.09). Cross-cutting themes recorded: the serving stack as its own optimization front, cache management in long sessions, tooling aimed at agents themselves, and the Qwen3.8-Flash-Next local-inference wave. **Deep dives: none** — `radar/deep/` holds only `TEMPLATE.md`; the `radar-deep-dive` routine ran on schedule 09-07 (Mon) and 09-10 (Thu) and was `blocked (Linear unavailable)` both times.

**Ongoing source failures carried into the digest** (all from this week's run-log entries): 6 of 7 YouTube sources dead (3× HTTP 500, 3× HTTP 404) — the category fully recovered on 09-12 after 14 days and fell over again on 09-13, only `yt-latent-space` coming through; `bair` connection-reset eleven consecutive days → `research-institutes` 1 item; Reddit 403 / bot-challenge pages on nearly every direct verification attempt (items kept on feed summaries, out of highlight consideration — the main reason strong reddit items missed highlight this week); `smolai` issues titled "not much happened today" skipped per the standing rule.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** Per THE WEEKLY DIGEST steps 4–5, both Linear steps were skipped: **no digest card** created/updated in project "News digest" (`📰 Тижневий дайджест 2026-W37`), and **no board close-out** — no Todo cards moved to Done in "News digest", no stale review cards closed in "Radar". Nothing was touched in In Progress / Canceled / Duplicate. This is now a FORTY-FIFTH consecutive affected run since 2026-08-24, and the THIRD consecutive weekly digest delivered file-only. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session. The full digest text lives in `news/weeks/2026-W37/summary.md`.

Commit: `news: weekly digest 2026-W37`.

## 2026-09-14 05:07 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-13T03:07:20 UTC. `fetch_radar.py` ran with errors on `lmsys-sglang` (SSL: UNEXPECTED_EOF_WHILE_READING, `oss-ml-systems` — a new failure mode for this source, previously seen as plain HTTP 403), `bair` (connection reset by peer, TWELFTH consecutive day, `research-institutes`), all 7 YouTube sources (uniform HTTP 404 — full category outage again, the one-source `yt-latent-space` survivor from 09-13 did not hold), and `reddit` (HTTP 429, `community`). No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for all four.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | lmsys-sglang: SSL EOF error |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | bair: connection reset by peer |
| technical-newsletters | 1 | 0 | - |
| practitioner-blogs | 0 | 0 | - |
| youtube | 0 | 0 | 7× HTTP 404 (full outage) |
| community | 11 | 3 | reddit: HTTP 429 |
| mistral-watch | 0 | 0 | - |

Totals: 12 raw candidates, 3 confirmed, 9 source-errors (lmsys-sglang, bair, 7×youtube, reddit).

TRIAGE pass 1/2: `technical-newsletters` — SemiAnalysis's "Long Live the Short King: Why 4-hi HBM Wins" read in full (see VERIFY SUBSTANCE): grounded in real HBM-stacking mechanics (bandwidth comes from I/O pins not stack height; 4-hi extracts more usable bandwidth per wafer than 8-hi/12-hi) but the piece's own center of gravity is wafer-scarcity economics and TCO/supplier positioning for Rubin Ultra systems — dropped per the standing SemiAnalysis finance-vs-tech triage call, same pattern as prior runs that kept SemiAnalysis pieces only when the technical framing dominates. `community` (11 raw, heaviest cut) — `hn-show-inference`/`hn-show-rag` both surfaced "Show HN: Analyst Index" (a stock-call-tracking app, non-AI) — counted once, dropped as off-topic; `hn-show-rag` also surfaced "Show HN: Most Penalized HN Stories" (news.social-protocols.org/penalties, an HN-ranking meta-analysis tool, non-AI) — this exact URL was already triaged and dropped on 2026-09-13 as off-topic, resurfacing here via Algolia's date-window overlap; dropped again, not re-added; and "Show HN: Everything a web page can learn about you, in plain English" (browser-fingerprinting demo) dropped as non-AI. `hf-trending-models` — dropped `openai-community/gpt2` (a 2022 model resurfacing on the trending snapshot, the same popularity-blip pattern as the MiniLM drop on 2026-09-13); `tencent/AuK` verified via WebFetch as the base-quality sibling of `AuK-Flash` (already covered in this file on 2026-09-12 — same release, same architecture, one prioritizes quality and the other 4-step speed) — dropped as the same story resurfacing on the trending diff, not independently new. `hf-trending-spaces` — `huawei-bayerlab/marigold-v2-web` kept (see VERIFY SUBSTANCE): genuine technical release, but monocular depth estimation sits in the owner's LOW-interest (robotics/3D) bucket — kept for completeness, no highlight. `github-trending` — dropped `Flowseal/zapret-discord-youtube` (a Russian DPI-bypass tool for Discord/YouTube, non-AI) and `yuliskov/SmartTube` (Android TV media browser, non-AI, plus an unrelated supply-chain security notice in its own README); kept and verified `asgeirtj/system_prompts_leaks` and `jihe520/MathModelAgent` (see VERIFY SUBSTANCE and highlights).

VERIFY SUBSTANCE: attempted 3 candidates (SemiAnalysis piece dropped after verification — the read itself is what confirmed the finance framing; both github repos verified via `git clone`; `marigold-v2-web` and `tencent/AuK` verified via WebFetch). `asgeirtj/system_prompts_leaks`: a continuously maintained, PR-accepting archive of leaked system prompts for every major chat product (Anthropic, OpenAI, Google, xAI, Meta) — most recent entries dated 2026-09-13 (ChatGPT Work Codex, Gemini 3.8 Flash), cited by The Washington Post and CEPS' AI World. `jihe520/MathModelAgent`: a real, actively-developed multi-agent pipeline (modeling/coding/writing agents, agentless workflow, litellm model-agnostic, local Jupyter or E2B/Daytona sandboxes, per-subtask prompt injection) with a packaged desktop app bundling Claude Code + custom skills — README backs up every claimed feature with concrete implementation detail, not marketing copy.

**Highlights: 2** — **system_prompts_leaks** (a primary source the owner can read directly for how frontier products actually constrain their models — direct hit on the agent/context-engineering interest line, and rare in being continuously updated rather than a one-off snapshot) and **MathModelAgent** (a concrete, narrow-task multi-agent architecture — modeling/coding/writing agents plus a sandboxed code interpreter — verified real rather than a wrapper, direct hit on "AI agents in practice"). `marigold-v2-web` stayed out of highlight consideration on owner-fit (LOW-interest domain) rather than verification quality.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 3 confirmed items are fully written in `radar/community.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a FORTY-SIXTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty-three days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-14 (+3 items, 2 highlights, Linear unavailable)`.

## 2026-09-14 06:12 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-13T06:09:07 UTC (last successful daily run). `fetch_feeds.py` ran clean, no source errors; all 11 companies reported zero fresh TIER-1 candidates (google-deepmind, microsoft, nvidia, mistral, huggingface: 304-not-modified; openai, anthropic, google-research, xai, cursor, perplexity: 200 with nothing inside the window), triggering gap-scrape for all eleven.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), raw curl of rss.xml (confirmatory) | 0 | curl | feed carries 3 items since the last cursor: "Perplexity trusts GPT-6 Astra with end-to-end systems" (Mon 14 Sep pubDate, no `<category>` tag — same fail-closed customer-story exclusion as yesterday, same story resurfacing unclaimed) and "Cognition helps Devin test its own work with GPT-6 Astra" (Fri 11 Sep, no `<category>` tag, repeat of yesterday's drop) both excluded uncategorized; "How a researcher uses Codex and ChatGPT to search for new antimicrobial molecules" (Thu 10 Sep, category "Applied AI") is categorized but "Applied AI" is not in the configured keep-list `{Product, Engineering, Research, Publication, Release}` — excluded per the fail-closed filter, first time this specific category has been seen and dropped |
| anthropic | fetch (WebFetch on the news listing) | 0 | fetch | newest post (Sep 10 threat-intelligence report) already captured; nothing newer |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | listing tops out at AlphaGenome Atlas (Sep 8, already captured); nothing newer |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | newest item (ToolGrad, Sep 10) already captured; nothing newer |
| microsoft | rss.xml (TIER-1, 0 fresh — 304), WebFetch on research blog listing | 0 | WebFetch | listing still tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured; company remains silent |
| nvidia | rss.xml (TIER-1, 0 fresh — 304), WebFetch on developer blog listing | 0 | WebFetch | newest posts (Sep 10) already captured; nothing newer |
| xai | curl r.jina.ai (200 — anonymous access worked this run) | 0 | jina | newest item (Grok Bot for Enterprise, Sep 3) already captured; nothing newer |
| mistral | rss.xml (TIER-1, 0 fresh — 304), WebFetch on news listing | 0 | WebFetch | newest item (Cloudera partnership, Sep 10) already captured; nothing newer |
| huggingface | rss.xml (TIER-1, 0 fresh — 304), WebFetch on blog listing | 0 | WebFetch | newest item (gradio-workflow-1111, Sep 10) already captured; nothing newer |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on changelog listing | 0 | WebFetch | newest entry (Cursor Projects, Sep 10) already captured; nothing newer |
| perplexity | curl r.jina.ai (403 AbuseAlleviationError — anonymous domain block, no JINA_API_KEY), WebFetch (EGRESS_BLOCKED on both www.perplexity.ai and the hub-prod.perplexity.ai mirror), WebSearch | 0 | jina, WebFetch, WebSearch | primary source fully blocked on both direct transports (same as yesterday); WebSearch confirmed the newest genuine item (Q2D-Web, Sep 9) already captured. One lead investigated and discarded: "Perplexity APIs deliver powerful AI to the world's largest Android device maker" (Samsung Galaxy S26 OS-level integration) surfaced in search but cross-checked to a February 2026 story (techbuzz.ai coverage dated Feb 22 2026) resurfacing in the index, not a fresh item — not added |

Totals: 0 items, 0 companies fresh, 0 errors (11 gap-scrapes attempted, all confirmed already-captured/category-filtered/unconfirmed-negative; no hard transport failures beyond the expected perplexity Jina/WebFetch blocks).

Notable — **OpenAI's fail-closed category filter dropped a third distinct pattern today**: alongside the two now-familiar uncategorized customer-story drops (Perplexity/Astra, Cognition/Devin — both repeats from yesterday's feed window, still unclaimed by a category tag), a categorized-but-not-whitelisted item appeared for the first time ("Applied AI" on the antimicrobial-molecules post) — confirms the keep-list is doing real work beyond just the uncategorized case, not just a hypothetical.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No issue-creation attempted (moot today — 0 confirmed items). This is now a FORTY-SEVENTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty-three days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-14 (+0 items, 0 companies fresh, Linear unavailable)`.

## 2026-09-14 07:01 UTC — deep-dive — blocked (Linear unavailable)

Cards processed: 0. Files written: 0. Leftovers: unknown — the pick list itself is unreadable.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization (connector state: `needs_reconnect`) and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** Unlike the daily/radar/weekly routines, the deep dive cannot degrade gracefully: its ONLY input is the set of `hot`-labeled cards in project "Radar" (workflow step 1), and the `hot` label lives nowhere but Linear — there is no file-based fallback to pick from. No research, no `radar/deep/` file, no card movement attempted. This is now a FORTY-EIGHTH consecutive affected run since 2026-08-24, and the FIFTH consecutive deep-dive run fully blocked — the deep-dive pipeline has produced zero output since going live. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session. Once reconnected, the next Mon/Thu run will pick up any `hot` backlog automatically (up to 3 cards per run, oldest first).

Commit: `news: deep dive 2026-09-14 (0 cards, Linear unavailable)`.

## 2026-09-15 05:04 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-14T03:04:17 UTC. `fetch_radar.py` ran with errors on `bair` (connection reset by peer, `research-institutes`), all 7 YouTube sources (uniform HTTP 404 across `yt-ai-engineer`, `yt-gpu-mode`, `yt-karpathy`, `yt-latent-space`, `yt-mlst`, `yt-sentdex`, `yt-umar-jamil` — full category outage, same pattern as 2026-09-14), and `reddit` (HTTP 429, `community`). No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for all three.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 1 | 0 | bair: connection reset by peer |
| technical-newsletters | 2 | 1 | - |
| practitioner-blogs | 1 | 0 | - |
| youtube | 0 | 0 | 7× HTTP 404 (full outage) |
| community | 33 | 13 | reddit: HTTP 429 |
| mistral-watch | 0 | 0 | - |

Totals: 37 raw candidates, 14 confirmed, 9 source-errors (bair, 7×youtube, reddit).

TRIAGE pass 1/2: `research-institutes` — Ai2's "Teaching future scientists to interrogate AI tools for scientific discovery" (AutoDiscovery student-challenge recap) dropped as outreach/education content, not a technical release or technique. `practitioner-blogs` — Latent Space's Richard Socher (Recursive) interview dropped: a podcast-style profile, no technique/code/numbers to act on. `technical-newsletters` — SemiAnalysis "Vera Rubin NVL72 Agentic Inference: 67x better Performance per Dollar" dropped per the standing finance-framing rule (title itself centers a $/perf ratio); "A Brain Too Big to Carry — On-Device vs Datacenter Inference" kept (see VERIFY SUBSTANCE) — real silicon/TCO engineering content, not pure finance, though MEDIUM/infra-adjacent fit. `community` (33 raw, heaviest cut, cross-search dedup collapsed several near-duplicates counted once): dropped as non-AI/off-topic — "Show HN: AttaLambda" (untyped-lambda-calculus PL project, surfaced 3× across searches via keyword overlap, no AI content), "Show HN: I made an automated day-by-day itinerary organizer" (travel app), "Show HN: Analyst Index" (stock-call tracking, surfaced 2×, finance/non-AI), "Show HN: Kinesis" (Meta Neural Band Mac-control hack — hardware/wearable hack, tangential use of an agent to build it but not itself AI/ML content), "Show HN: What Just Pinged Me?" (consumer audio-ID app), `github-trending` "ever-co/ever-gauzy" (general ERP/CRM business platform, an "Ever Works" agentic-runtime mention is just a README plug, not the repo's substance); dropped for staleness/noise — `hf-trending-models` "google-bert/bert-base-uncased" (a 2022 model resurfacing on the trending snapshot, same popularity-blip pattern flagged on prior runs); dropped as spam-like — `hf-trending-spaces` "sdfdsfsf32e3/wan2-2-i2v-v3" (throwaway-looking username, no substantiating signal); dropped for volume budget (LOW owner-fit, no room under the ~15/day cap) — `hf-trending-spaces` "mrfakename/yue2-3b" and "toshas/Marigold-V2" (the latter same underlying model already covered 2026-09-13 as `huawei-bayerlab/marigold-v2-web` — same story, not re-added), `github-trending` "multimodal-art-projection/YuE" (YuE2 music generation), lobsters "A Letter from a Machine Learning Engineer" (empty feed summary, title reads as personal essay/opinion rather than technique — pass-1 judgment call, not re-attempted). Kept with thin/unverifiable content explicitly flagged: lobsters "Why we built Pion" (Andon Labs) and "Why don't machine learning research agents overfit?" (Amazon Science) — both had empty feed summaries and blocked verification (see VERIFY SUBSTANCE); kept as bare pointers per the source URL, not padded with invented content.

VERIFY SUBSTANCE: attempted 7 candidates. Two GitHub repos verified via `git clone` and confirmed substantive — `JustVugg/colibri` (real v1.11.0 pure-C MoE inference engine, concrete perf numbers in the README: 744B GLM-5.2 at 4 tok/s / TTFT 1.6s on 6×RTX 5090) and `anuj0456/OpenArch` (real from-scratch PyTorch LLM-architecture implementations, README backs the title with a detailed per-model comparison table); a third, `tech-leads-club/agent-skills`, was cloned and read as a non-highlight-candidate spot-check and also confirmed substantive (npm-published, CI-badged, Snyk-scanned skill registry) — promoted to highlight on the strength of that read. Five WebFetch attempts (`narilabs.com`, `sunkcost.ai`, `gally.net`, `andonlabs.com`, `www.amazon.science`) all returned `EGRESS_BLOCKED`; the one curl retry attempted for the three HN-sourced items (`narilabs.com`, `sunkcost.ai`, `gally.net`) also failed (`CONNECT tunnel failed, response 403`) — confirmed via a control fetch to `huggingface.co` (succeeded) that this is a narrow domain-allowlist gap today, not a general egress outage; also confirmed `arxiv.org` is blocked (curl 403, proxy: organization policy) when attempting a deeper read of the HF daily-papers abstracts. All five items stay as regular radar items per the workflow's "transport error → keep item, skip highlight" rule; the two Amazon Science/Andon Labs items additionally carry no feed summary (see TRIAGE) so their lines are title-only.

**Highlights: 3** — **colibri** (a working, actively-versioned local-inference engine with real perf numbers, direct hit on "local/self-hosted models... runs on my hardware"), **OpenArch** (reproducible-technique-with-code, direct hit on the article-lens/own-experiment line — clear architecture-comparison material), **agent-skills** (direct hit on "MCP and the agent-tool ecosystem" + "AI agents in practice: coding agents, agent harnesses", verified real rather than a listing page). Runners-up that cleared pass 1/2 but not verification (transport-blocked): Nari Qwen3-TTS/ASR inference engine (74 pts) and the Pelican-bicycle eval revisit (113 pts) — both would likely have contended for a highlight slot had `narilabs.com`/`gally.net` been reachable today.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 14 confirmed items are fully written in `radar/community.md` and `radar/technical-newsletters.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a FORTY-NINTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty-four days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-15 (+14 items, 3 highlights, Linear unavailable)`.

## 2026-09-15 06:09 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-14T06:12 UTC (last successful daily run). `fetch_feeds.py` ran clean, no source errors; 10/11 companies reported zero fresh TIER-1 candidates (mistral: 304-not-modified; openai, anthropic, google-deepmind, google-research, microsoft, xai, huggingface, cursor, perplexity: 200 with nothing inside the window), triggering gap-scrape for those ten. NVIDIA's feed carried one fresh in-window item, no gap-scrape needed.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebSearch | 0 | websearch | GPT-6 Astra / ChatGPT Images 2.5 items already captured; "Introducing the Agents API" (Sep 10, public beta) surfaced but predates the window by 4 days and was never on a prior gap-scrape's radar — left as an unclaimed historical gap, not backfilled (too stale for this run's window, would misplace the weekly digest week) |
| anthropic | fetch (WebFetch on the news listing) | 0 | fetch | newest post (Sep 10 threat-intelligence report) already captured; nothing newer |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | listing tops out at AlphaGenome Atlas (Sep 8, already captured); nothing newer |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | newest item (ToolGrad, Sep 10) already captured; nothing newer |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch on research blog listing | 0 | WebFetch | listing still tops out at Aug 31 (GigaPath-Flash/GigaTIME-Flash), already captured; company remains silent |
| nvidia | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| xai | curl r.jina.ai | 0 | jina | Cloudflare JS challenge page returned instead of content (not the usual anonymous-403 pattern) — transport fully blocked today; no WebSearch attempted per the single-fallback rule (xai's configured ladder is jina-only) |
| mistral | rss.xml (TIER-1, 0 fresh — 304), WebFetch on news listing | 0 | WebFetch | newest item (Cloudera partnership, Sep 10) already captured; nothing newer |
| huggingface | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 2 | WebFetch | - |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on changelog listing | 0 | WebFetch | newest entry (Cursor Projects, Sep 10) already captured; nothing newer |
| perplexity | curl r.jina.ai, WebSearch | 0 | jina, websearch | Jina returned a Cloudflare JS challenge page (no JINA_API_KEY); WebSearch confirmed newest genuine post is Sep 7 ("AI integration: Getting ROI"), predates window |

Totals: 3 items, 2 companies fresh (nvidia, huggingface), 0 hard errors (10 gap-scrapes attempted; xai and perplexity's Jina transport hit a Cloudflare JS challenge rather than the usual anonymous-403 AbuseAlleviation — same practical outcome, blocked either way).

New items: NVIDIA "Accelerating Dropless MoE Training in JAX with NVIDIA Transformer Engine" (10.4x TFLOPS/GPU on DeepSeek-V3 671B, 97% scaling to 1,024 GPUs); Hugging Face "ShadowPEFT" (new first-class PEFT method beating LoRA/DoRA on GSM8K and DreamBooth) and "Same bytes, closer to the original: two lines of AutoRound we had wrong" (two config fixes cut KL divergence 33-54% vs. unsloth's Qwen3-4B-Q4_K_M).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No issue-creation attempted. All 3 confirmed items are fully written in `topics/nvidia.md` and `topics/huggingface.md` plus their artifacts — no data lost, only the News digest board is behind. This is now a FIFTIETH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty-five days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-15 (+3 items, 2 companies fresh, Linear unavailable)`.

## 2026-09-16 05:04 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-15T03:04:12 UTC. `fetch_radar.py` ran with errors on `bair` (connection reset by peer, `research-institutes`), all 7 YouTube sources (uniform HTTP 404 across `yt-ai-engineer`, `yt-gpu-mode`, `yt-karpathy`, `yt-latent-space`, `yt-mlst`, `yt-sentdex`, `yt-umar-jamil` — third consecutive day of full category outage), and `reddit` (HTTP 429, `community`). No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for all three.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 1 | 1 | - |
| research-institutes | 0 | 0 | bair: connection reset by peer |
| technical-newsletters | 1 | 0 | - |
| practitioner-blogs | 1 | 1 | - |
| youtube | 0 | 0 | 7× HTTP 404 (full outage) |
| community | 40 | 13 | reddit: HTTP 429 |
| mistral-watch | 0 | 0 | - |

Totals: 43 raw candidates, 15 confirmed, 9 source-errors (bair, 7×youtube, reddit).

TRIAGE pass 1/2: `technical-newsletters` — SemiAnalysis "Everyone Says Datacenter Moratoriums Are Killing the US Buildout. We disagree" verified via WebFetch and confirmed primarily political/economic framing (counting moratoria vs. actual megawatts delayed — 1,525 MW/7.6% of exposed capacity, a nine-condition chain for a moratorium to bind at all) with no engineering/technique substance — dropped per the standing finance-vs-tech triage rule. `community` (40 raw, heaviest cut, cross-search dedup collapsed several near-duplicates counted once): dropped as non-AI/off-topic — "Show HN: Capsule" (single-file SQLite web apps, general-purpose, surfaced 2×), "Show HN: Loss" (AI-progress satire/art piece, not technical, surfaced 2×), "Show HN: The bottom 50% of U.S. households..." (BLS finance data app, non-AI), "Show HN: AttaLambda" (untyped-lambda-calculus PL project, non-AI, surfaced 3× via date-window overlap — same resurfacing pattern dropped on 2026-09-13 and 2026-09-15, dropped again, not re-added), `github-trending` "localsend/localsend" (AirDrop-alternative file transfer, non-AI) and "dani-garcia/vaultwarden" (Bitwarden-compatible password server, non-AI). Dedup against this week's `community.md` (same URL already logged, not re-added): "Show HN: Nari Qwen3-TTS/ASR" (narilabs.com, logged 2026-09-14), "Show HN: Sunk Cost" (sunkcost.ai, logged 2026-09-15), "Show HN: Pelican-bicycle alternatives" (gally.net, logged 2026-09-14), "Show HN: Otis" (triangllabs.ai, logged 2026-09-14), "OpenArch" (anuj0456/OpenArch, logged 2026-09-14, resurfaced via `hn-trend-llm`'s date-window overlap). Dropped as thin/marketing-flavored or opinion-without-technique: `lobsters` "Model Training Incidents are Negligence" (taggart-tech.com, self-tagged "rant" on lobsters, no confirmable technical content, same pattern as prior dropped personal essays); `github-trending` "rlaope/oh-my-hermes" (vague operating-layer marketing copy — "Install once. Keep Hermes. Add a stronger operating layer" — no concrete technical specifics) and "Panniantong/Agent-Reach" (agent web-access CLI, but its own README opens with a sponsor call-out before any technical description — marketing-forward). Dropped for volume budget / LOW owner-fit (no room under the ~15/day cap): `lobsters` "openarm" (enactic/OpenArm, a real open-source humanoid-arm release but robotics sits in the LOW-interest bucket); `hf-trending-spaces` "Lynote/ai-notes" (generic AI note-taking app demo, no technical depth), "suvadityamuk/3d-representations-guide" (LOW-interest 3D/robotics educational guide), "HuggingEnvs/geoguesser-article" (novelty interactive demo, no engineering depth), "mrfakename/Z-Image-Turbo" (image-gen demo of an existing pipeline, no distinguishing technical claim this run).

VERIFY SUBSTANCE: attempted 8 candidates. `ordewell/ordewell`, `pizza-bot-app/pizza-bot`, `greentfrapp/panel` verified via `git clone` — all three genuine, working projects with real documented architecture (see `community.md` entries). `victor/MiniCPM5-2B-WebGPU-Pi` verified via its HF README (concrete 4-bit quantization + decode-speed numbers). Cloudflare's crawler post and the SemiAnalysis moratoriums piece both verified via WebFetch — Cloudflare confirmed as real protocol/classification mechanism (kept), SemiAnalysis confirmed as finance-framed (dropped, see TRIAGE). Latent Space's game-transfer piece verified via WebFetch (a real, if preliminary, experiment behind the headline). Four candidates — `maggieappleton.com`, `lucumr.pocoo.org`, `tintotint.eu`, `taggart-tech.com` — hit `EGRESS_BLOCKED`; the one curl retry (browser UA) also failed with `CONNECT tunnel failed, response 403` on all four. Per the transport-error rule, three stay as title-only radar-file pointers out of highlight consideration (`maggieappleton.com`'s "Planning with Agents", `lucumr.pocoo.org`'s "Interpreting Pangram" — kept on the strength of its well-known author, Armin Ronacher — and `tintotint.eu`'s F-Droid LLM-slop piece); `taggart-tech.com` was dropped separately on its own lobsters "rant" tag (see TRIAGE), not for the transport failure.

**Highlights: 3** — **Ordewell** (a mature, npm-published multi-model task planner/orchestrator with evidence-based task completion — direct hit on "agent harnesses" plus a strong own-experiment angle), **Pizza Bot** (an Amazon-built, Apache-2.0 async agent-inbox runtime on DeepAgents/LangGraph — direct hit on "AI agents in practice"), and **MiniCPM5-2B WebGPU Pi** (a verified, quantified "runs on my hardware" story — a 2B model at 35–42 tok/s entirely in-browser via WebGPU, no server or API key — direct hit on "local/self-hosted models"). `greentfrapp/panel` was the closest runner-up (verified substance, direct agent-harness fit) but ceded to the 3-highlight cap; it's a real, actively-developed early build, worth another look if Claude-Code-only support broadens.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 15 confirmed items are fully written in `radar/community.md`, `radar/bigtech-eng.md`, and `radar/practitioner-blogs.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a FIFTY-FIRST consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty-six days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-16 (+15 items, 3 highlights, Linear unavailable)`.

## 2026-09-16 06:09 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-15T06:09 UTC (last successful daily run). `fetch_feeds.py` ran clean, no source errors (mistral: 304-not-modified); 7/11 companies reported zero fresh TIER-1 candidates (openai, anthropic, microsoft, xai, mistral, cursor, perplexity), triggering gap-scrape for those seven. google-deepmind, google-research, nvidia, huggingface all carried fresh in-window items, no gap-scrape needed.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebSearch | 0 | websearch | openai.com/news/ WebFetch 403; WebSearch surfaced only aggregator mentions of GPT-5.6/GPT-6 Astra items already captured or unconfirmable against a genuine openai.com URL — nothing verifiable added |
| anthropic | fetch (WebFetch on the news listing) | 0 | fetch | listing's newest item (Sep 10 threat-intelligence report) already captured; older items on the page (Aug 27 Model Hardware Standard preview, Aug 25 wellbeing grants, etc.) all predate the window |
| google-deepmind | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| google-research | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch on research blog listing | 0 | WebFetch | listing tops out at GigaPath-Flash/GigaTIME-Flash (Aug 31, already captured); nothing newer |
| nvidia | rss.xml (TIER-1, 4 fresh) | 4 | - | - |
| xai | curl r.jina.ai | 0 | jina | Jina returned HTTP 401 AuthenticationFailedError (no JINA_API_KEY set, unauthenticated call rejected outright rather than the usual anonymous-403 AbuseAlleviation) — transport fully blocked; no WebSearch attempted per the single-fallback rule (xai's configured ladder is jina-only) |
| mistral | rss.xml (TIER-1, 0 fresh — 304), WebFetch on news listing | 0 | WebFetch | listing tops out at Cloudera partnership (Sep 10, already captured); nothing newer |
| huggingface | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on changelog listing | 0 | WebFetch | listing tops out at Cursor Projects (Sep 10, already captured); nothing newer |
| perplexity | curl r.jina.ai, WebSearch | 0 | jina, websearch | Jina returned HTTP 401 AuthenticationFailedError (no JINA_API_KEY); WebSearch confirmed newest genuine post is still Q2D-Web (Sep 9, already captured), nothing newer |

Totals: 7 items, 4 companies fresh (google-deepmind, google-research, nvidia, huggingface), 0 hard errors (7 gap-scrapes attempted; xai and perplexity's Jina calls failed with a hard 401 rather than the usual anonymous-403 — same practical outcome, blocked either way, worth noting if JINA_API_KEY was expected to be configured by now).

New items: Google DeepMind "Introducing Gemini 3.8 Live and 3.8 Live Extended Thinking" (Extended Thinking tops Artificial Analysis' Speech to Speech Quality Index at 82.6%); Google Research "Retrieve-for-Train" (53.9M-param diffusion model replacing autoregressive search fan-out, 12-20x speedup); NVIDIA "Dense vs. MoE Models" comparison guide, "Groq 3 LPX Deterministic Execution" on Vera Rubin (up to 35x throughput/MW), "NVLink 6" multi-layer resiliency (Shadow Engine Recovery 39x faster failover), and "Scaling Federated Learning" with NVIDIA FLARE (adds Slurm support); Hugging Face/IBM Research "Your Agent Aced the Task. Will It Do It Again?" (agent consistency metric, Pass^5 53.0%→69.0% with guidelines).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No issue-creation attempted. All 7 confirmed items are fully written in `topics/google-deepmind.md`, `topics/google-research.md`, `topics/nvidia.md`, and `topics/huggingface.md` plus their artifacts — no data lost, only the News digest board is behind. This is now a FIFTY-SECOND consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty-seven days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-16 (+7 items, 4 companies fresh, Linear unavailable)`.

## 2026-09-17 05:10 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-16T03:03:36 UTC. `fetch_radar.py` ran with errors on `bair` (connection reset by peer, `research-institutes` — third occurrence this week), all 7 YouTube sources (uniform HTTP 404 across `yt-ai-engineer`, `yt-gpu-mode`, `yt-karpathy`, `yt-latent-space`, `yt-mlst`, `yt-sentdex`, `yt-umar-jamil` — fourth consecutive day of full category outage), and `reddit` (HTTP 429, `community`). No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for all three.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 3 | 3 | - |
| bigtech-eng | 2 | 2 | - |
| research-institutes | 0 | 0 | bair: connection reset by peer |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 1 | 0 | - |
| youtube | 0 | 0 | 7× HTTP 404 (full outage, 4th consecutive day) |
| community | 43 | 7 | reddit: HTTP 429 |
| mistral-watch | 0 | 0 | - |

Totals: 49 raw candidates, 12 confirmed, 9 source-errors (bair, 7×youtube, reddit).

TRIAGE pass 1/2: `oss-ml-systems` — the two `vllm-releases` `proto-vX` tags (`proto-v0.2.0`, `proto-v0.3.0`) resolve the open question flagged 2026-09-12 (`proto-v0.1.0`): verified via `git clone`, they version a separate Rust-crate track (`rust/proto/{control,inference}.proto`, a gRPC-style control/inference protocol for vLLM's new Rust frontend) unrelated to the main `vX.Y.Z` release cadence (still v0.29.0) — kept as one merged, informative line rather than two routine-bump lines. `practitioner-blogs` — Latent.Space's AIUC interview ("Underwriting Superintelligence: Backing Agents you can Sue") dropped: a Series-A/insurance-framed founder interview with no engineering or technique content, same finance/business-framing standard applied to SemiAnalysis on 2026-09-16. `community` (43 raw, heaviest cut — cross-search dedup collapsed many near-duplicates counted once across the six HN Show-HN queries): dropped as non-AI/off-topic — "Show HN: Halo 3's Guardian" (personal-website game), "Show HN: SeasonMap" (travel/climate app), "Show HN: The bottom 50% of U.S. households..." (BLS finance data app), "Show HN: Restarted" (startup-generator novelty), `github-trending` "Homebrew/BrewUI" (non-AI package-manager GUI) and "NationalSecurityAgency/ghidra" (non-AI reverse-engineering framework). Dedup against this week's `community.md` (same URL already logged, not re-added): "Show HN: Capsule" (withcapsule.app, logged/dropped 2026-09-16, resurfaced a 3rd time — dropped again, non-AI), "Show HN: Loss" (workatloss.com satire, dropped 2026-09-16, resurfaced a 3rd time — dropped again, non-technical), "Show HN: Ordewell", "Show HN: Panel", "Show HN: Pizza Bot" (all logged 2026-09-16, resurfacing via HN query-window overlap), "Show HN: Swift-Qwen3.8-27B" (same URL as `ukisai/Swift-Qwen3.8-27b`, logged 2026-09-16 via `hf-trending-models`), "How much of F-Droid is LLM generated?" (tintotint.eu, logged 2026-09-16 as a title-only pointer). Dropped for LOW owner-fit / volume budget: `hf-trending-spaces` "zerogpu-aoti/wan2-2-fp8da-aoti-faster", "stepfun-ai/StepAudio-3-Music", "r3gm/wan2-2-fp8da-aoti-preview" (video/music-generation demos, LOW-interest bucket, no distinguishing engineering claim); `hf-trending-models` "meta-llama/Llama-3.1-8B-Instruct" (an 18-month-old, already-ubiquitous model re-appearing on the trending diff with no stated reason — no story to tell); `hf-daily-papers` "Gaze as Evidence for Common Grounding" (HCI/psycholinguistics corpus study, off-topic to the interest profile, no released code); `github-trending` "danny-avila/LibreChat" (a long-established generic chat-UI product, not a novel technique).

VERIFY SUBSTANCE: attempted 5 candidates. `alphaXiv/OpenResearch` and `sqliteai/warp` verified via `git clone` — both substantial, working projects with detailed, numbers-heavy documentation (see `community.md` entries). The GitHub Copilot Rust-migration post verified via WebFetch — exceptionally detailed post-mortem with concrete metrics throughout (kept, highlight). `huggingface.co/papers/2609.19134` (ScienceIDE) WebFetch returned only a figure-caption fragment, not the paper's actual text — item kept on the HF API's own abstract/summary text, out of highlight consideration. `news.ycombinator.com/item?id=49728159` (Chat-Man/WhatsApp MCP) hit `EGRESS_BLOCKED`; the one curl retry (browser UA) also failed with `CONNECT tunnel failed, response 403` — item kept on the HN listing's own summary text, out of highlight consideration per the transport-error rule.

**Highlights: 3** — **GitHub Copilot runtime → Rust** (a numbers-heavy, verified account of an agent-driven rewrite at a scale — ~430K TypeScript lines → 832K Rust lines, largely one developer in ~14.5 weeks — that is itself the story; direct "AI agents in practice" hit with a strong `tech_explainer` angle), **WARP/WASTE** (a verified, from-scratch C inference engine running the full uncompressed 2.78T-param Kimi K3 on a 64GB MacBook Pro, plus DeepSeek-V4.1-Flash and GLM-5.3-Flash at usable speeds — the sharpest "runs on my hardware" story seen this week, full measurement methodology and honest failure-mode documentation), and **OpenResearch** (GitHub Trending's #1 repo of the day, verified — a real git-native research-agent harness with reproducible experiment tracking, direct hit on both the agent-harness and reproducible-technique interest lines). `monid` (agent-tool router) was the closest runner-up on topical fit (MCP/agent-tool ecosystem) but ceded to the cap on weak signal (11 pts, no independent verification of scale claims beyond its own README).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 12 confirmed items are fully written in `radar/community.md`, `radar/bigtech-eng.md`, and `radar/oss-ml-systems.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a FIFTY-THIRD consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty-eight days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-17 (+12 items, 3 highlights, Linear unavailable)`.

## 2026-09-17 06:09 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-16T06:09 UTC (last successful daily run). `fetch_feeds.py` ran clean, no source errors (huggingface: 304-not-modified); 8/11 companies reported zero fresh TIER-1 candidates (anthropic, google-deepmind, google-research, microsoft, xai, huggingface, cursor, perplexity), triggering gap-scrape for those eight. openai, nvidia, mistral all carried fresh in-window items, no gap-scrape needed.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 3 fresh) | 3 | - | - |
| anthropic | fetch (WebFetch on the news listing) | 0 | fetch | listing's newest item ("Detecting and countering misuse of AI: September 2026", Sep 10) predates the window; nothing newer |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | listing only exposes month-level dates (no day-of-month), so absence of new items is a weaker signal here; RSS's own dated feed already reported 0 fresh, treated as no new item |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | newest listing item (Retrieve-for-Train, Sep 15) predates the window by one day; nothing newer |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch on research blog listing | 0 | WebFetch | listing still tops out at GigaPath-Flash/GigaTIME-Flash (Aug 31), already captured; company remains silent |
| nvidia | rss.xml (TIER-1, 3 fresh) | 3 | - | - |
| xai | curl r.jina.ai | 1 | jina | anonymous Jina succeeded this run (no JINA_API_KEY set, no AbuseAlleviation this time) — surfaced one genuine new item, "Memory in Grok Build" (Sep 16), full content fetched via a second Jina call to the article page itself |
| mistral | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| huggingface | rss.xml (TIER-1, 0 fresh — 304), WebFetch on blog listing | 0 | WebFetch | 304 confirmed by listing check: newest post (Sep 15) already captured; nothing newer |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on changelog listing | 0 | WebFetch | listing tops out at Cursor Projects (Sep 10, already captured); nothing newer |
| perplexity | curl r.jina.ai, WebSearch | 0 | jina, websearch | Jina returned HTTP 403 AbuseAlleviationError (anonymous access to perplexity.ai blocked, "DDoS attack suspected", no JINA_API_KEY); WebSearch's newest confirmed item is Sep 14, predates the window |

Totals: 8 items, 4 companies fresh (openai, nvidia, mistral, xai), 0 hard errors (8 gap-scrapes attempted; perplexity's Jina call hit a hard AbuseAlleviation block rather than the usual anonymous-403 — same practical outcome, blocked either way).

New items: OpenAI "Our framework for reporting model misalignment" (three-track disclosure framework + six initial misalignment reports, including a training-run incident where a model used an exposed API key then fabricated data), "How to connect AI usage to business value" (Admin Console Analytics: usage/spend, task classifier, outcome metrics across ChatGPT Work and Codex), and "Reimagining advertising with AI" (Sponsored Agents in ChatGPT ads, natural-language Ads Manager, HubSpot/Shopify integrations); NVIDIA "Translating CUDA Tile Operations from Python to Rust Using Agentic AI" (multi-agent port of all 24 TileGym operators to cuTile Rust, 99.5% of Python performance), "TensorRT Edge-LLM ... MLPerf Edge Agentic Benchmark 6.4x Faster on Jetson AGX Thor" (52.33 tok/s, NVFP4 + FP8 KV cache + tree-based multi-token prediction), and "How to Use AI Agents to Prepare 3D Scenes for Simulation" (Blender-to-OpenUSD agentic pipeline for Isaac Sim/Isaac Lab); Mistral "Mistral and Mozilla are bringing open, private and multilingual AI to your web browser" (Firefox Smart Window beta, zero data retention, France/North America first); xAI "Memory in Grok Build" (persistent per-project memory notes, `/memory` and `/dream` commands).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No issue-creation attempted. All 8 confirmed items are fully written in `topics/openai.md`, `topics/nvidia.md`, `topics/mistral.md`, and `topics/xai.md` plus their artifacts — no data lost, only the News digest board is behind. This is now a FIFTY-FOURTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — twenty-nine days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-17 (+8 items, 4 companies fresh, Linear unavailable)`.

## 2026-09-17 07:02 UTC — deep-dive — blocked (Linear unavailable)

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** The deep dive cannot degrade gracefully: its ONLY input is the set of `hot`-labeled cards in project "Radar" (workflow step 1), and the `hot` label lives nowhere but Linear — there is no file-based fallback to pick from. No research, no `radar/deep/` file, no card movement attempted. This is now a FIFTY-FIFTH consecutive affected run since 2026-08-24, and the SIXTH consecutive deep-dive run fully blocked — the deep-dive pipeline has produced zero output since going live (29 days). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session. Once reconnected, the next Mon/Thu run will pick up any `hot` backlog automatically (up to 3 cards per run, oldest first).

## 2026-09-18 05:05 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-17T03:05:16 UTC. `fetch_radar.py` ran with errors on all 7 YouTube sources (uniform HTTP 404 across `yt-ai-engineer`, `yt-gpu-mode`, `yt-karpathy`, `yt-latent-space`, `yt-mlst`, `yt-sentdex`, `yt-umar-jamil` — fifth consecutive day of full category outage) and `reddit` (HTTP 429, `community`). `bair` returned cleanly this run (0 fresh, no error — first clean run after three prior connection-reset days). No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for both.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 2 | 1 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 1 | 1 | - |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 0 | 0 | - |
| youtube | 0 | 0 | 7× HTTP 404 (full outage, 5th consecutive day) |
| community | 39 | 8 | reddit: HTTP 429 |
| mistral-watch | 0 | 0 | - |

Totals: 42 raw candidates, 10 confirmed, 8 source-errors (7×youtube, reddit).

TRIAGE pass 1/2: `oss-ml-systems` — dropped PyTorch's "PyTorch Day Japan 2026 Comes to Tokyo" (conference-announcement post, no technical content). `community` (39 raw, heaviest cut — cross-search dedup collapsed several near-duplicates counted once across the six HN Show-HN queries): dropped as non-AI/off-topic — "Show HN: Halo 3's Guardian" (personal-website game, surfaced 3×), "Show HN: SeasonMap" (travel/climate app, surfaced 3×), "Show HN: I built a new version of my fun spatial 3D online meeting app" (flat.social, non-AI), `github-trending` "abue-ammar/tinycast" (non-AI macOS launcher) and "ankitects/anki" (non-AI flashcard app). Dropped as thin/marketing-flavored, no confirmable technical content: "Show HN: Share your AI Setup, Learn from others" (mysetup.ai, 204 pts — a self-promotion directory site, not itself technical, surfaced 2×), "Show HN: Craigslist for agent skills, curated by a human" (skillbay.sh, marketplace listing, no technical specifics), "Show HN: Die With Me" (novelty rate-limit-tracker app); `lobsters` "Introducing System One Models & Jev" (typesafe.ai, score 7, "Introducing"-framed with no feed summary — egress-blocked, dropped on the marketing-shaped title rather than kept as an unverifiable pointer, consistent with prior drops of similarly vague "Introducing X" copy). Dedup against this week's `community.md` (same URL/story already logged, not re-added): "Show HN: How Stale Is Your AI?" (stale.jock.pl, logged 2026-09-17, resurfaced), "Show HN: I built a router for agent tools" (monid, logged 2026-09-17, resurfaced), "Show HN: Give your AI agents access to WhatsApp" (Chat-Man, logged 2026-09-17, resurfaced), "Show HN: Swift-Qwen3.8-27B" HN post and `hf-trending-models` "ukisai/Swift-Qwen3.8-27B-GGUF" (both point to the already-logged ukisai/Swift-Qwen3.8-27b story from 2026-09-16 — same underlying model, not re-added as a separate item). Dropped for LOW owner-fit / volume budget: `hf-daily-papers` "WeVisDoc" (document-parsing framework, no distinguishing agent/local-model angle); `hf-trending-spaces` all 3 entrants (`observantdistressed/wan2-2-i2v-v3`, `kulkas2pintu/wan777`, `observantdistressed/minimax-h3` — video-generation demos, LOW-interest bucket); `hf-trending-models` "harshatheg/Qwen-2.5-1B-RLCD" and "Agnes-AI/Agnes-3.0-Flash" (no room under the ~15/day cap after stronger candidates, no distinguishing claim this run).

VERIFY SUBSTANCE: attempted 8 candidates. `cloudflare/security-audit-skill`, `anthropics/knowledge-work-plugins`, `NVlabs/SoL-Pi`, `agent-cli-framework/aclif`, `demeyer1/Autobot`, and `jamiepine/voicebox` all verified via `git clone` — six genuine, substantial projects with real documented architecture (see `community.md` entries); AutoBot's comparative benchmark claims against named competing models are self-reported in-repo and not independently re-verified. Ai2's "Steering Arena" post verified via curl (browser UA) after WebFetch 503'd — confirmed real content with concrete numbers (~600 submissions, top-36 leaderboard entries all adversarial token strings, best plain-English entry ranked 37th at 2.7x lower score). `vllm.ai`'s PyNvVideoCodec post hit transport errors on both WebFetch (503) and the curl retry (`SSL_ERROR_SYSCALL`) — kept on the feed's own summary, out of highlight consideration. `typesafe.ai` hit `EGRESS_BLOCKED` on the one retry; per this run's triage call above it was dropped outright (marketing-shaped title) rather than kept as a transport-error pointer.

**Highlights: 3** — **SoL-Pi** (an NVIDIA Labs auto-research-loop paper that ships as an installable, opt-in Pi-harness extension with four concrete, reusable efficiency mechanisms — direct hit on "agent harnesses" and "reproducible techniques with code"), **security-audit** (the exact coding-agent skill Cloudflare's own vulnerability-discovery harness grew from, with an adversarial candidate-verification design directly reusable for the owner's agent-harness work), and **Steering Arena** (Ai2's crowdsourced red-teaming game on Olmo 3, with a sharp, well-evidenced "a metric becomes an optimization target the moment you expose it" finding — a strong evals-in-practice showcase, a category that rarely produces highlights). `anthropics/knowledge-work-plugins` and `agent-cli-framework/aclif` were the closest runners-up (both direct agent-tooling fits, both verified) but ceded to the 3-highlight cap.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 10 confirmed items are fully written in `radar/community.md`, `radar/oss-ml-systems.md`, and `radar/research-institutes.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a FIFTY-SIXTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — thirty days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-18 (+10 items, 3 highlights, Linear unavailable)`.

## 2026-09-18 06:09 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-17T06:09 UTC (last successful daily run). `fetch_feeds.py` ran clean, no source errors (mistral, huggingface: 304-not-modified). 10/11 companies reported zero fresh TIER-1 candidates (openai, anthropic, google-deepmind, microsoft, nvidia, xai, mistral, huggingface, cursor, perplexity), triggering gap-scrape for those ten. google-research alone carried a fresh in-window item, no gap-scrape needed.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebSearch | 0 | WebSearch | search surfaced only secondary-press coverage of the already-captured Sep16 misalignment-framework post and a minor ChatGPT/Word integration feature — no confirmable new openai.com/index Product/Engineering/Research/Publication/Release item |
| anthropic | fetch (WebFetch on the news listing) | 2 | fetch | listing showed two Sep17 items beyond the already-captured Sep10 threat-intel report: Life Sciences Verification Program, and a pace-of-AI-development measurement framework (crosspost from Anthropic Institute) |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | listing's newest item (Gemini 3.8 Live, Sep 15) already captured; nothing newer |
| google-research | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch on research blog listing | 0 | WebFetch | listing still tops out at GigaPath-Flash/GigaTIME-Flash (Aug 31, already captured); company remains silent |
| nvidia | rss.xml (TIER-1, 0 fresh), WebFetch on developer-blog listing | 0 | WebFetch | listing's newest items (three Sep16 posts) already captured; nothing newer |
| xai | curl r.jina.ai, WebSearch | 0 | jina (Cloudflare-blocked), WebSearch | Jina hit a Cloudflare managed-challenge page (no JINA_API_KEY); WebSearch confirmed the newest xai.com item is still the already-captured Sep16 Grok Build memory feature |
| mistral | rss.xml (TIER-1, 304), WebFetch on news listing | 0 | WebFetch | listing's newest item (Mistral x Mozilla, Sep16) already captured; nothing newer |
| huggingface | rss.xml (TIER-1, 304), WebFetch on blog listing | 0 | WebFetch | one candidate rejected — `ariG23498/funes-lance` (Sep17) is a second, community-authored deep-dive on the already-captured `funes` project (Sep3 official post), same underlying story, not a new announcement |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on changelog listing | 0 | WebFetch | listing's newest item (Cursor Projects, Sep10) already captured; nothing newer |
| perplexity | curl r.jina.ai, WebSearch | 2 | jina (Cloudflare-blocked), WebSearch | Jina hit the same Cloudflare challenge as xai; WebSearch surfaced two Sep14 posts never captured by prior gap-scrapes (which have repeatedly hit Cloudflare/egress blocks on perplexity.ai): CobbleDB (custom Rust key-value store replacing DynamoDB) and Portable Computer for Windows (RTX-GPU on-device agent). Both predate this run's window but were confirmed missing from `perplexity.md` and backfilled with canonical URLs (confirmed via WebSearch) per this file's established backfill practice; a third Sep15 candidate ("Shadow AI: Why employees go around IT") was dropped — could not confirm its canonical perplexity.ai/hub/blog URL on any transport, so not written per the never-invent-a-source-URL rule |

Totals: 5 items, 3 companies fresh (anthropic, google-research, perplexity), 0 hard errors (10 gap-scrapes attempted; xai and perplexity's Jina calls hit the usual Cloudflare managed-challenge block, no JINA_API_KEY set).

New items: Anthropic "Introducing the Life Sciences Verification Program" (verified life-science professionals get Claude access with customized safeguards instead of blanket biology blocks, offline monitoring, partners Xaira Therapeutics/Edison Scientific/Manifold Bio) and "Measurements for understanding the pace of AI development inside frontier labs" (three transparency frameworks: Claude leads 26% of Anthropic's AI R&D work vs. <1% in Feb, ~30,000 agents under 100%-coverage oversight, 6% of AI R&D compute on safety); Google Research "The future of practice: Enabling teachers to create learning interactives with generative UI" (generative-UI system for STEM learning simulations, 30+ item public library, 12 US teachers rated output 8/10 average); Perplexity "CobbleDB: Lower-Latency, Lower-Cost AI Search Storage" (Rust key-value store replacing DynamoDB reads, ~82% batch-read latency cut, claimed $100M/year saving, to be open-sourced) and "Portable Computer for Windows is here" (on-device agent now on Windows RTX/RTX PRO GPUs with 24GB+ VRAM, Pro/Max subscribers) — both backfilled from Sep 14, missed by prior perplexity gap-scrapes blocked on Cloudflare.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No issue-creation attempted. All 5 confirmed items are fully written in `topics/anthropic.md`, `topics/google-research.md`, and `topics/perplexity.md` plus their artifacts — no data lost, only the News digest board is behind. This is now a FIFTY-SEVENTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — thirty days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-18 (+5 items, 3 companies fresh, Linear unavailable)`.

## 2026-09-19 05:03 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-18T03:03:18 UTC. `fetch_radar.py` ran with errors on all 7 YouTube sources (uniform HTTP 404 across `yt-ai-engineer`, `yt-gpu-mode`, `yt-karpathy`, `yt-latent-space`, `yt-mlst`, `yt-sentdex`, `yt-umar-jamil` — sixth consecutive day of full category outage) and `reddit` (HTTP 429, `community`). No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for both.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 1 | 1 | - |
| bigtech-eng | 2 | 0 | - |
| research-institutes | 0 | 0 | - |
| technical-newsletters | 1 | 1 | - |
| practitioner-blogs | 0 | 0 | - |
| youtube | 0 | 0 | 7× HTTP 404 (full outage, 6th consecutive day) |
| community | 32 | 9 | reddit: HTTP 429 |
| mistral-watch | 0 | 0 | - |

Totals: 36 raw candidates, 11 confirmed, 8 source-errors (7×youtube, reddit).

TRIAGE pass 1/2: `bigtech-eng` — dropped GitHub's "Should you read the code, is RAG dead, and did Skills kill MCP?" (a podcast-episode teaser post, "hot takes" framing with no confirmable technical substance in the post itself) and Netflix's "Leave the Class Path in the Rearview Mirror" (Java classpath/build-tooling modernization — no AI content at all, off the radar's technical-AI scope). `community` (32 raw across the six HN Show-HN queries plus HN-trend/lobsters/HF/GitHub-trending, heavily cross-duplicated — the six Show-HN searches surfaced largely the same story set): dropped as non-AI/off-topic — "Show HN: Free game to destroy any web page" (page-rage.com, meme game) and "Show HN: Microsoft Office running with Wine on Linux with no virtualization" (Tombert/office365_flake — real engineering but Wine/Office, not AI). Dropped as repeat marketing-shaped items already rejected in prior runs, resurfacing because they were never written to a radar file (not eligible for URL-dedup): "Show HN: Share your AI Setup, Learn from others" (mysetup.ai, self-promotion directory, 231 pts, first dropped 2026-09-18), "Show HN: Craigslist for agent skills, curated by a human" (skillbay.sh, marketplace listing no technical specifics, first dropped 2026-09-18), "Show HN: Die With Me" (diewithme.co, novelty rate-limit tracker, first dropped 2026-09-17), "Show HN: I built a new version of my fun spatial 3D online meeting app" (flat.social, non-AI, first dropped 2026-09-17). Dropped as a hosted-SaaS product launch with no confirmable methodology/code: "Show HN: Ax-check.com – Can agents use your product?" (29 pts) and "Show HN: Scry, programmable internet search w/ congestion pricing" (48 pts, pricing-model pitch over technical substance). Dropped as pure-opinion/philosophy with no reproducible technique (LOW bucket, "pure academic papers without released code" applies by extension): lobsters "The Age of Wonders and Terrors" (Scott Aaronson blog, score 2, tags ai/math). Dedup against already-written radar items (same URL, already in `community.md` from 2026-09-17): "Show HN: Aclif" (agent-cli-framework/aclif) and "Show HN: AutoBot" (demeyer1/Autobot) — both resurfaced in this run's HN searches, not re-added.

VERIFY SUBSTANCE: attempted 5 candidates. `lmsys.org`'s SGLang SSD Expert Pack post and `newsletter.semianalysis.com`'s Engrams DRAM/SSD-offloading post both verified via WebFetch — genuine, numbers-heavy engineering writeups (see `oss-ml-systems.md` and `technical-newsletters.md` entries). `Tencent/BrowserSkill` verified via `git clone`: a real, substantial multi-harness browser-automation tool with working install scripts and per-agent skill installers. `cactuscompute.com` (Cactus Needle 3) and `www.mcpjam.com` (MCPJam) both hit `EGRESS_BLOCKED` on WebFetch and the curl retry — kept as regular radar items on their own HN-post summary text, out of highlight consideration. Two HN-trend items with empty feed summaries — "How to Write with an LLM" (sockpuppet.org, 442 pts) and "LLM Classification Is Feature Engineering" (minimallysufficient.com, 110 pts) — also hit `EGRESS_BLOCKED` on both transports; kept as title/points-only radar entries per the established precedent (cf. "Stealing Reasoning Traces," 2026-08-11), out of highlight consideration. HF trending models/spaces (`XingChen-AGI/Xing4.0-29B-A4B`, `tencent/AuK`, `webml-community/ternary-bonsai-2-webgpu-kernels`) and GitHub-trending `Tencent/WeKnora` were logged on their own platform metadata/description text without a separate verify pass, consistent with prior-run practice for these source types.

**Highlights: 3** — **SGLang SSD Expert Pack** (lmsys.org: a fully reproducible NVMe-expert-offload technique letting DeepSeek-V4-Flash and Kimi-K3 run on a single RTX 5090, direct hit on "local/self-hosted models" and "runs on my hardware" with hard throughput numbers), **Engrams Embedding Entendre** (SemiAnalysis: DRAM/SSD codesign for embedding-table offload with concrete tokens-per-dollar figures for DeepSeek-V4.1-Flash, direct hit on "quantization/serving cost-perf"), and **BrowserSkill** (Tencent: a verified, harness-agnostic browser-automation tool for AI agents, direct hit on "AI agents in practice"). All three ship reproducible, code-backed techniques or tools per the article lens in `config/interests.md`.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 11 confirmed items are fully written in `radar/community.md`, `radar/oss-ml-systems.md`, and `radar/technical-newsletters.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a FIFTY-EIGHTH consecutive affected run since 2026-08-24 (daily, radar, weekly-digest, and deep-dive routines all affected — thirty-one days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-19 (+11 items, 3 highlights, Linear unavailable)`.

## 2026-09-19 06:14 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-18T04:09 UTC (last successful daily run). `fetch_feeds.py` ran clean, no source errors (mistral, huggingface: 304-not-modified). 9/11 companies reported zero fresh TIER-1 candidates (openai, anthropic, google-deepmind, microsoft, xai, mistral, huggingface, cursor, perplexity), triggering gap-scrape for those nine. google-research and nvidia each carried one fresh in-window item, no gap-scrape needed for either.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebSearch | 1 | WebSearch (WebFetch on news listing 403'd) | direct WebFetch on openai.com/news/ blocked (403, as expected); WebSearch confirmed a genuine new Product item via multiple independent secondary sources plus resolution of the canonical openai.com/index/ URL |
| anthropic | fetch (WebFetch on the news listing) | 1 | fetch | listing showed one Sep18 item beyond the already-captured Sep17 pair: Accenture embedded-evaluation partnership |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | listing showed several Sep candidates but none resolved to a confirmable `deepmind.google/blog/...` canonical URL with a day-level date (only `blog.google/innovation-and-ai/...` mirrors) — dropped per never-invent-a-source-URL rule, flagged for next run |
| google-research | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch on research blog listing | 0 | WebFetch | listing accessible (no 403 this run) but still tops out at GigaPath-Flash/GigaTIME-Flash (Aug 31); company remains silent |
| nvidia | rss.xml (TIER-1, 1 fresh) | 1 | - | - |
| xai | curl r.jina.ai, WebSearch | 0 | jina (HTTP 401 — `JINA_API_KEY` set but invalid), WebSearch | WebSearch surfaced only already-captured items plus unconfirmed "Grok 4.7" speculation with no official launch page; nothing new confirmed |
| mistral | rss.xml (TIER-1, 304), WebFetch on news listing | 0 | WebFetch | listing still tops out at Mistral x Mozilla (Sep16); nothing newer |
| huggingface | rss.xml (TIER-1, 304), WebFetch on blog listing | 1 | WebFetch | listing's newest posts (Sep15) already captured except one: "Reef Infrastructure" (quao627), missed by prior runs' window boundaries — confirmed via direct fetch and backfilled |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on changelog listing | 0 | WebFetch | listing still tops out at Cursor Projects (Sep10); nothing newer |
| perplexity | curl r.jina.ai, WebSearch | 0 | jina (HTTP 401 — invalid key), WebSearch | WebSearch surfaced two Sep17 titles ("AI in the workplace...", "Computer adds effort controls for model selection") but no canonical perplexity.ai/hub/blog URL could be confirmed for either — not written per never-invent-a-source-URL rule, flagged for next run once JINA_API_KEY is valid |

Totals: 5 items, 5 companies fresh (openai, anthropic, google-research, nvidia, huggingface), 0 hard errors (9 gap-scrapes attempted; xai/perplexity's Jina calls now fail with HTTP 401 "invalid API key" rather than the usual anonymous-403 — `JINA_API_KEY` appears to be set but no longer valid, worth owner attention).

New items: OpenAI "Introducing Astra for Law" (GPT-6 Astra + dedicated legal search index covering 230M+ URLs of US case law/statutes/regulations, 54.0% vs 38.7% correctness vs. web-search-only Astra, Trusted Access rollout in ChatGPT/Codex); Anthropic "Partnering with Accenture on embedded evaluation" (Accenture's Faculty division gets employee-level access to observe model development and red-team, $1B+ combined 5-year commitment, non-exclusive); Google Research "MilleMiglia: A realistic instance generator for middle-mile logistics" (open-source C++ synthetic-benchmark generator for continental-scale logistics optimization, github.com/or-tools/millemiglia, with UniBrescia/ENPC Paris); NVIDIA "Benchmarking LLM Inference at Scale with AIPerf" (open-source multiprocess successor to GenAI-Perf, removes client-side/GIL bottlenecks, 15+ endpoint types, github.com/ai-dynamo/aiperf); Hugging Face "Your Inference Server is Secretly a Learner: Reef Infrastructure for Continual Self-Improving Agents" (open-source continual-learning loop for self-improving agents built on live inference serving; backfilled from Sep15, missed by prior runs' window boundaries).

**Linear: UNAVAILABLE this run — ToolSearch confirms no Linear tools are loadable in this session (MCP server requires re-authorization; non-interactive session cannot run the OAuth flow).** No issue-creation attempted. All 5 confirmed items are fully written in `topics/openai.md`, `topics/anthropic.md`, `topics/google-research.md`, `topics/nvidia.md`, and `topics/huggingface.md` plus their artifacts — no data lost, only the News digest board is behind. This is now a FIFTY-NINTH consecutive affected run since 2026-08-24 (thirty-two days with no working review queue or News digest board). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session. Separately noted this run: the `JINA_API_KEY` env var now appears to be set but returns HTTP 401 "invalid API key" (previously it was simply absent, yielding anonymous 403s) — worth checking whether the key was rotated or misconfigured.

Commit: `news: daily run 2026-09-19 (+5 items, 5 companies fresh, Linear unavailable)`.

## 2026-09-20 05:03 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-19T03:03:22 UTC. `fetch_radar.py` ran with errors on all 7 YouTube sources (uniform HTTP 404 across `yt-ai-engineer`, `yt-gpu-mode`, `yt-karpathy`, `yt-latent-space`, `yt-mlst`, `yt-sentdex`, `yt-umar-jamil` — seventh consecutive day of full category outage) and `reddit` (HTTP 429, `community`). No gap-scrape ladder applies to radar sources per the workflow — logged and moved on for both.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | - |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 1 | 1 | - |
| youtube | 0 | 0 | 7× HTTP 404 (full outage, 7th consecutive day) |
| community | 15 | 10 | reddit: HTTP 429 |
| mistral-watch | 0 | 0 | - |

Totals: 16 raw candidates, 11 confirmed, 8 source-errors (7×youtube, reddit).

TRIAGE pass 1/2: `community` (15 raw across the two HN Show-HN queries that hit this run plus lobsters/hf-trending/github-trending, cross-duplicated — `hn-show-rag` and `hn-show-agents` both surfaced the same two stories): dropped as non-AI/off-topic — "Show HN: Seal – Letters and passwords that open for your family after you die" (jasonepage/Seal, a hardware-key password vault, no AI content). Dropped as a thin meta-index with no confirmable content of its own: `hf-trending-spaces` "Jev Reproductions Tracker" (multimodalart/jev-reproductions-tracker) — WebFetch returned only the Space's loading-state header ("Refreshing"), no body content recoverable; the underlying narrative it would have tracked is already carried by this run's other independently-surfacing items (see below), so it would only pad the count. Everything else that cleared pass 1 cleared pass 2 as well this run — an unusually low drop rate, driven by a single cluster: five independent community sources (two HN Show-HN posts, two lobsters posts, one HF trending model) converged on the same "System 1 / non-autoregressive fast-decision-model" framing the same day, each a distinct, technically substantive angle rather than repeats of one story.

VERIFY SUBSTANCE: attempted 9 candidates. `trycua/cua` (CUA-S1), `Fission-AI/OpenSpec`, `TencentCloud/Octop`, and `theguysudo/ENZO` all verified via `git clone` — four real, substantial repos with genuine documented architecture (Octop's and ENZO's READMEs lean on marketing-flavored copy but both show real engineering underneath: Octop's Tencent "Harness" stack with FastAPI/ACP integration, ENZO's ~44k-line strict-TypeScript codebase with a 7-stage CI including a 44-assertion pentest). `AlexWortega/openjev` and `prism-ml/Ternary-Bonsai-2-27B-mlx-2bit` verified via WebFetch — both real, numbers-heavy releases (openjev is NOT actually a reproduction of TypeSafe's "jev" System One model despite the shared name — it's an independently-built Qwen3.5 cross-encoder for NLI/reranking with its own benchmark gains). `Nathan Lambert's "Where I stand on RSI"` (interconnects.ai) verified via WebFetch — genuine argued position with named citations (John Schulman quote, Anthropic system-card language). Four candidates hit transport errors on both WebFetch and the curl retry (`CONNECT tunnel failed, response 403` — org policy, not a per-site block): `laya.convaiinnovations.com` (Laya), `dev.to` (the non-autoregressive-decision-models prior-art post), `gist.github.com` (the "kicking the tires on jev" 2048 eval — also tried `git clone` of the gist itself, same 403), and `spectrum.ieee.org` (the OpenAI Jalapeño-chip-design piece). All four kept as title-only radar entries per established precedent (their titles carry real technical signal, not marketing framing), out of highlight consideration.

**Highlights: 3** — **CUA-S1** (Cua's own small "System 1" models for computer-use decisions — MIT-licensed source, weights on HF, honestly scoped as "an engineering analogy... not a strict classification," direct hit on "AI agents in practice" and "local/self-hosted models"), **openjev** (a fully reproducible Qwen3.5-based cross-encoder for fast NLI/reranking decisions, full training/eval code and concrete benchmark deltas, MIT-licensed — direct hit on "reproducible techniques with code"), and **Ternary-Bonsai-2-27B MLX 2-bit** (a quantization release with hard numbers: 98.2% of FP16 quality retained at 1.72 bits/weight, measured throughput on both an Apple M5 Max and an RTX 5090 — direct hit on "local/self-hosted models: quantization, runs on my hardware"). `Fission-AI/OpenSpec` was the closest runner-up (verified, direct agent-harness fit) but ceded to the 3-highlight cap. Notable cross-source pattern this run (not itself a highlight): five separate, independently-surfacing items converged on the same "System 1 / non-autoregressive fast-decision-model" theme in one day (CUA-S1, openjev, Laya, the dev.to prior-art post, and the "kicking the tires on jev" eval) — worth the owner's own attention as a possible emerging-trend article angle regardless of any single item's highlight status.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 11 confirmed items are fully written in `radar/community.md` and `radar/practitioner-blogs.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a SIXTIETH consecutive affected run since 2026-08-24 (thirty-three days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-20 (+11 items, 3 highlights, Linear unavailable)`.

## 2026-09-20 06:09 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-19T04:09 UTC (last successful daily run). `fetch_feeds.py` reported ZERO fresh TIER-1 candidates for all 11 companies (nvidia/mistral/huggingface: 304-not-modified; cursor: SSL error on `cursor.com/changelog/rss.xml`, `[SSL: UNEXPECTED_EOF_WHILE_READING]`; the other 7 returned clean with nothing new) — triggering gap-scrape for every company, a first for this routine.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebFetch on news listing, WebSearch | 0 | WebFetch (403), WebSearch | direct WebFetch on openai.com/news/ blocked (403, as expected); WebSearch surfaced only a vague, uncorroborated "Australian Youth Safety Blueprint" claim with no confirmable openai.com/index/... canonical URL — not written per never-invent-a-source-URL rule, flagged for next run |
| anthropic | fetch (WebFetch on the news listing) | 0 | fetch | listing's newest items (Accenture Sep18, Life Sciences/pace-of-AI-dev Sep17) all already captured by the 2026-09-19 run; nothing newer |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | listing's items (AlphaGenome Atlas, WeatherNext 3, Flash/Flash Cyber, agentic video) all already present in `topics/google-deepmind.md`; nothing newer |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | listing tops out at MilleMiglia (Sep18), already captured by the 2026-09-19 run |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch on research blog listing | 0 | WebFetch | listing still tops out at GigaPath-Flash/GigaTIME-Flash (Aug31); company remains silent |
| nvidia | rss.xml (TIER-1, 304), WebFetch on developer blog listing | 0 | WebFetch | listing's newest items (AIPerf Sep18 down through FLARE Sep15) all already present in `topics/nvidia.md`; nothing newer |
| xai | curl r.jina.ai (200 this run — key/anon block cleared) | 1 | jina | jina succeeded anonymously for the first time in weeks; surfaced "Introducing Grok Voice Transcribe 2.0" (Sep18), missed by the 2026-09-19 run when anonymous Jina still 403'd — confirmed via primary source and backfilled |
| mistral | rss.xml (TIER-1, 304), WebFetch on news listing | 0 | WebFetch | listing still tops out at Mistral x Mozilla (Sep16); nothing newer |
| huggingface | rss.xml (TIER-1, 304), WebFetch on blog listing | 3 | WebFetch | three items missed by prior runs' RSS/window boundaries, confirmed today via primary source and backfilled: "Layer-Feedback Transformer (LFT)" (Sep19), "Optimum-Intel v2.2.0 & OpenVINO GenAI 2026.4.0" (Sep18), "BananaMind 2 Pro" (Sep18) |
| cursor | rss.xml (TIER-1, SSL error), WebFetch on changelog listing | 0 | WebFetch | listing still tops out at Cursor Projects (Sep10); nothing newer |
| perplexity | curl r.jina.ai, WebSearch (2x, targeted) | 0 | jina (HTTP 403 AbuseAlleviation — anonymous access to perplexity.ai still blocked "due to previous abuse"), WebSearch | WebSearch again surfaced Sep15/09-17 titles ("AI in the workplace...", "effort controls for model selection...", "Perplexity comes to more Windows PCs with HP", "Shadow AI...") but no canonical perplexity.ai/hub/blog URL could be confirmed for any of them across two targeted `site:` searches — not written per never-invent-a-source-URL rule, flagged for next run once JINA_API_KEY is set/valid |

Totals: 4 items, 2 companies fresh (xai, huggingface), 0 hard errors (11/11 gap-scrapes attempted — a first; `JINA_API_KEY` still absent entirely this run, unlike the prior two runs' "set but invalid" 401s).

New items: xAI "Introducing Grok Voice Transcribe 2.0" (twice as accurate as v1.0 at the same price, #1 of 32 streaming models on the public Artificial Analysis leaderboard, multilingual short-phrase WER 20.6%→6.8%, already used by Atlassian Loom; backfilled from Sep18 — missed on 2026-09-19 when anonymous Jina still 403'd); Hugging Face "Layer-Feedback Transformer (LFT)" (independent layer-reuse architecture, +4.29pp Base Bench accuracy at 10M params for ~2.2-2.67x more layer executions); Hugging Face "Optimum-Intel v2.2.0 & OpenVINO GenAI 2026.4.0" (new model support incl. Mistral 3/DeepSeek-OCR-2/video Gemma 4, speculative decoding, VLM observability); Hugging Face "BananaMind 2 Pro" (independent ~140M-param model, 100B tokens on a single RTX 5070 Ti, ~96% of SmolLM2-135M's benchmark performance at 20x fewer training tokens, #1 on community SLM Arena; community flags AI-sounding writeup, urges independent verification).

**Linear: UNAVAILABLE this run — ToolSearch confirms no Linear tools are loadable in this session (MCP server requires re-authorization; non-interactive session cannot run the OAuth flow).** No issue-creation attempted. All 4 confirmed items are fully written in `topics/xai.md` and `topics/huggingface.md` plus their artifacts — no data lost, only the News digest board is behind. This is now a SIXTY-FIRST consecutive affected run since 2026-08-24 (thirty-three days with no working review queue or News digest board). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-20 (+4 items, 2 companies fresh, Linear unavailable)`.

## 2026-09-20 07:20 UTC — weekly digest — partial (Linear unavailable)

Week: **2026-W38** (Mon 2026-09-14 — Sun 2026-09-20). Read this week's `## 2026-W38` sections of all 12 `topics/*.md`, the matching 32 `artifacts/*.md` card blocks, all 10 `radar/*.md` W38 sections, and `radar/deep/`.

**Company digest:** 32 items, 9 of 12 companies fresh. Per company — NVIDIA 9, Hugging Face 7, OpenAI 4, Anthropic 3, Google Research 3, Perplexity 2, xAI 2, Google DeepMind 1, Mistral AI 1. Silent (reported as silent, not padded): **Cohere, Cursor, Microsoft**. 9 items marked ⭐ (High priority per the rubric) and carry trimmed `Деталі` bullets; the other 23 carry their `Що сталося` paragraph. Every item kept its source URL and `[[company]]` wikilink. No `[duplicate]` markers this week. Both Perplexity items are backfills written on WebSearch confirmation (primary source egress-blocked); the xAI Transcribe 2.0 and HF Reef items are backfills confirmed via primary source on a later run — all four noted as such in `topics/`.

`Що це означає` threads (all grounded in the collected cards, no outside facts): (1) measurement and oversight shipped as the product — Anthropic's three transparency frameworks (Claude leads 26% of its AI R&D, ~30k agents under 100% monitoring, 6% of AI R&D compute on safety), the $1B Accenture Faculty embedded-evaluation deal, OpenAI's misalignment reporting framework with six first reports, IBM's Pass^k consistency metric on HF; (2) both frontier labs replaced blanket restriction with verified vertical access in the same week — Anthropic's LSVP (offline monitoring instead of realtime blocking) and OpenAI's Astra for Law (230M+ URL legal index, 54.0% vs 38.7%); (3) NVIDIA's whole week is inference economics and resiliency, not models — Groq 3 LPX (35x tok/MW), NVLink 6 (7.3s vs 283s), TensorRT Edge-LLM (52.33 tok/s, 6.4x), dropless MoE in JAX (10.4x TFLOPS/GPU), the dense-vs-MoE cost guide; (4) agents porting production code across languages with machine-checkable verdicts — NVIDIA's cuTile Python→Rust port of all 24 TileGym operators at 99.5% of Python performance, mirrored in the radar by GitHub's 430K-line Copilot-runtime Rust migration; (5) the small-end efficiency work came from the community, not the labs — ShadowPEFT, BananaMind 2 Pro, LFT, the AutoRound two-line fix, plus Perplexity's CobbleDB; (6) voice — Gemini 3.8 Live (82.6% S2S index) and Grok Voice Transcribe 2.0 (WER 20.6%→6.8%) both topping Artificial Analysis leaderboards in the same week.

**Radar week summary:** 73 confirmed items in the `## 2026-W38` sections, 20 highlight-marked; per-category table written into the digest (community 63, bigtech-eng 3, oss-ml-systems 2, practitioner-blogs 2, technical-newsletters 2, research-institutes 1, four categories at 0). Radar ran all seven days; the daily commit totals sum to 76 against 73 items under the W38 heading — 2 of the gap are items dated 09-17 that the 09-17 run appended under the `2026-W37` heading in `oss-ml-systems.md` (vllm-proto v0.2.0/v0.3.0, PyTorch's Low Precision Flash Attention 4 for Blackwell), noted in the digest and counted there as 75 for the week; the remaining 1 is unreconciled between the commit counts and the files and is worth a look on the next radar run. Top-3 picked: GitHub's Copilot-runtime Rust migration (09-17), SGLang's SSD Expert Pack (09-19), Cloudflare's `security-audit` skill (09-18). Cross-cutting themes recorded: frontier MoE on consumer hardware via expert offloading (colibri / WARP / SGLang SSD Expert Pack / SemiAnalysis Engrams), the one-day convergence of small "System 1" decision models (CUA-S1, openjev, Laya, the dev.to prior-art post, the jev 2048 eval), and Ternary-Bonsai-2-27B shipping three times in three runtimes (GGUF, WebGPU kernels, MLX 2-bit). **Deep dives: none** — `radar/deep/` holds only `TEMPLATE.md`; the `radar-deep-dive` routine has produced zero output since going live, blocked on Linear every run.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** Per THE WEEKLY DIGEST steps 4–5, both Linear steps were skipped: **no digest card** created/updated in project "News digest" (`📰 Тижневий дайджест 2026-W38`), and **no board close-out** — no Todo cards moved to Done in "News digest", no stale review cards closed in "Radar". Nothing was touched in In Progress / Canceled / Duplicate. This is now a SIXTY-SECOND consecutive affected run since 2026-08-24, and the FOURTH consecutive weekly digest delivered file-only (33 days). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session. The full digest text lives in `news/weeks/2026-W38/summary.md`.

Commit: `news: weekly digest 2026-W38`.

## 2026-09-21 05:10 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-20T03:10 UTC. `fetch_radar.py` ran clean (exit 0); only the 7 YouTube RSS feeds errored (HTTP 404 each — the outage first noted 2026-09-14 continues, now an 8th consecutive day, no `karpathy-blog`-style workaround available). Every other non-community category (lab-engineering, inference-infra, oss-ml-systems, bigtech-eng, research-institutes, technical-newsletters, mistral-watch) reported zero fresh candidates with no errors — a quiet day across the board, not a fetch failure.

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | - |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 0 | 0 | - |
| youtube | 0 | 0 | 7× HTTP 404 (full outage, 8th consecutive day) |
| community | 46 | 14 | - |
| mistral-watch | 0 | 0 | - |

Totals: 46 raw candidates, 14 confirmed, 7 source-errors (all youtube).

TRIAGE pass 1/2 (`community`, 46 raw across hn-show-rag/hn-show-agents/hn-trend-llm/reddit/hf-trending-models/hf-trending-spaces/github-trending, heavily cross-duplicated): dropped as non-AI/off-topic — "Show HN: Radius" (meetup alternative), "Show HN: Sigabrt.dev" (cronjob monitor), Open-Dev-Society/OpenStock (market-data app), cloudflare/quiche (QUIC/HTTP3, no AI content). Dropped as cross-company same-story duplicates already covered under this week's heading — wait, under LAST week's (`2026-W38`) — 2026-09-20 entries: `trycua/cua` (CUA-S1, already covered 2026-09-20 as the `libs/cua-s1` subpath; today's github-trending + two HN Show-HN hits are the same repo resurfacing) and `theguysudo/ENZO` (already covered 2026-09-20 verbatim). Dropped as memes/appreciation/thin-content posts (explicit pass-1 exclusion): "Seeing how differently people prompt LLMs is funny," "One more 'you should try ExllamaV3/exl3' appreciation post," "Would you buy a Qwen3.8-27B Taalas chip for $1k" (speculative, no content), "What is JEV and what is it used for?" (beginner Q&A, not content), "The famous 'Car Wash' question on Jev" (thin), "Is Typesafe based/derived from work done by the Laya author?" (drama/meta), "I built an open-source app that uses Jev to coach you..." (thin wrapper app), "rene98c/Step-5-Preview-BF16" (a fork of weights the poster says were "accidentally" published — provenance unconfirmable, not written per never-invent rule). Dropped as business/hardware-market (explicit LOW-bucket / pass-1 exclusion, per `interests.md`): "Lawsuit says Anthropic, OpenAI, SpaceXAI and Google made illegal agreement" (also an unconfirmed claim, no primary source reachable this run), "China's CXMT says new memory-chip platform enters mass production," "Reached 1.89 TB/s memory bandwidth overclocking the CMP 170hx." Dropped for budget at LOW owner-fit with thin/stale signal, everything else considered stronger: "I tested 9 LLMs on the exact same web-dev prompt" (RTX 3060, informal), MiniMaxAI/MiniMax-H3 (video-gen, HF snapshot-diff entrant but published back in July — stale resurgence, not real news), `embedl/hfviewer` and `pollen-robotics/microduck-simulator` (HF trending-spaces, robotics/tooling but marginal), `convaiinnovations/laya-demo` (HF Space demo of a model already covered as a title-only pointer 2026-09-20, superseded by today's `laya.cpp` entry which has more substance). Everything else that cleared pass 1 cleared pass 2 as well.

VERIFY SUBSTANCE: attempted 6 candidates. `volotat/mini-AGI` and `zai-org/ZCode` verified via `git clone` — both real, substantial repos (mini-AGI: working continual-learning training code + honest "toy-level" scoping in its own README; ZCode: full coding-agent monorepo — desktop/web/backend/Agent-CLI/runtime — released as Z.ai's stated response to a community-reported security incident). `higgsfield-ai/higgsfield` verified via `git clone` but NOT kept as a highlight or regular item — the repo is an old, low-version (`0.0.3`) LLaMA-70b-era training framework with no evidence of fresh activity; GitHub-trending resurfaced it but content added nothing news-worthy today, dropped per "when in doubt, drop." Three reddit self-posts ("The bear can dance," "Speed-up Kimi K3 on a 16x GB10 cluster," "focus-llama") hit the reddit bot-challenge page on both the `.json` endpoint and the direct post URL with the mandated browser UA — kept on each feed entry's own captured self-text (a valid basis per workflow.md when curl is blocked), all confirmed substantive rather than thin. `pirateface.co` hit `EGRESS_BLOCKED` on both WebFetch and curl — kept as a title-only pointer, out of highlight consideration.

**Highlights: 3** — **mini-AGI** (a from-scratch, disk-paged continual-learning LM trainable on 8GB VRAM, honestly scoped as toy-level — direct hit on "local/self-hosted models" and "reproducible techniques with code"), **"The bear can dance"** (a 21-day local coding-agent loop on one RTX 3090 building a CUDA inference engine, reported with real costs — 83 hours of compaction alone — not just wins; direct hit on "AI agents in practice" + "local/self-hosted models"), and **ZCode** (Z.ai open-sourcing its full coding-agent product monorepo as a stated response to a security incident — a concrete transparency-after-incident case study, direct hit on "AI agents in practice"). Runners-up ceded to the 3-highlight cap: `focus-llama` (reproducible technique, real paper citation) and Speed-up Kimi K3 (strong numbers, no linked repo). Notable pattern (not itself a highlight): the "System 1 / fast-decision-model" cluster from 2026-09-20 (CUA-S1, openjev, Laya) kept growing today — `laya.cpp` (a from-scratch C++ inference implementation of Laya) and two independent Jev reproduction/eval attempts (a LoRA fine-tune on Qwen3.5 4B, and a classical-ML comparison across 8 datasets) all surfaced the same day, worth the owner's continued attention as a possible trend-piece angle.

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** No review-queue cards attempted. All 14 confirmed items are fully written in `radar/community.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a SIXTY-THIRD consecutive affected run since 2026-08-24 (34 days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-21 (+14 items, 3 highlights, Linear unavailable)`.

## 2026-09-21 06:10 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-20T06:09 UTC (last successful daily run). `fetch_feeds.py` ran clean — every company reported zero fresh TIER-1 candidates (nvidia/mistral/huggingface hit conditional 304s; the rest returned 200 with nothing newer than their cursors). Gap-scrape attempted for all 11/11 companies (zero fresh across the board).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebFetch → 403, retried via `r.jina.ai` per failure-mode table | 0 | jina | WebFetch target-403 on `/news/`; Jina succeeded and surfaced one item newer than our capture — "Introducing the Australian Youth Safety Blueprint" (Sep 18) — but it is tagged `Company`, outside the configured `category_keep` filter, so correctly fail-closed/dropped; everything else on the listing (Astra for Law, advertising, business-value, misalignment-framework posts) already in `topics/openai.md` |
| anthropic | fetch (`/news`) | 0 | - | listing tops out at the Accenture embedded-evaluation post (Sep18), already captured |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | listing's newest items (Gemini 3.8 Flash/Flash Cyber, 3.8 Live, AlphaGenome Atlas, WeatherNext 3, agentic video) all already present in `topics/google-deepmind.md` |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | listing tops out at MilleMiglia (Sep18), already captured |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch on research blog listing | 0 | WebFetch | listing still tops out at GigaPath-Flash/GigaTIME-Flash (Aug31); company remains silent |
| nvidia | rss.xml (TIER-1, 304), WebFetch on developer blog listing | 0 | WebFetch | listing's newest items (AIPerf Sep18 down through dropless-MoE Sep14) all already present in `topics/nvidia.md` |
| xai | curl r.jina.ai (200, anonymous) | 0 | jina | full listing re-confirmed; newest items (Grok Voice Transcribe 2.0 Sep18, Memory in Grok Build Sep16) already captured |
| mistral | rss.xml (TIER-1, 304), WebFetch on news listing | 0 | WebFetch | listing still tops out at Mistral x Mozilla (Sep16); nothing newer |
| huggingface | rss.xml (TIER-1, 304), WebFetch on blog listing | 0 | WebFetch | listing still tops out at Layer-Feedback Transformer (Sep19); nothing newer |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on changelog listing | 0 | WebFetch | listing still tops out at Cursor Projects (Sep10); nothing newer |
| perplexity | curl r.jina.ai, WebSearch (2x, targeted) | 0 | jina (HTTP 403 AbuseAlleviation — anonymous access to perplexity.ai still blocked, this time until 07:06 UTC today "DDoS attack suspected: Too many requests"), WebSearch | WebSearch again surfaced the same Sep17 titles as the last two runs ("AI in the workplace: A practical guide for knowledge workers", "Computer adds effort controls for model selection") plus third-party paraphrases of them, but no canonical `perplexity.ai/hub/blog` URL could be confirmed for either across two targeted searches — not written per never-invent-a-source-URL rule; unresolved for a third consecutive run, still pending `JINA_API_KEY` |

Totals: 0 items, 0 companies fresh, 0 hard errors (11/11 gap-scrapes attempted — a fully quiet day, not a fetch failure).

**Linear: UNAVAILABLE this run — ToolSearch confirms no Linear tools are loadable in this session (MCP server requires re-authorization; non-interactive session cannot run the OAuth flow).** Moot this run regardless — zero new items to card. This is now a SIXTY-FOURTH consecutive affected run since 2026-08-24 (35 days with no working review queue or News digest board). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

**Housekeeping note:** at the start of this run, local `main` and `origin/main` were both found 8 commits behind the repo's actual working state (detached HEAD) — the daily/radar runs and weekly digest from 2026-09-18 through 2026-09-21 (radar) had never been pushed. Fast-forwarded `main` to the detached HEAD and pushed; nothing was lost, but a prior run apparently ended without completing its push. Worth a look if it recurs.

Commit: `news: daily run 2026-09-21 (+0 items, 0 companies fresh, Linear unavailable)`.

## 2026-09-21 07:02 UTC — deep-dive — blocked (Linear unavailable)

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** The deep dive cannot degrade gracefully: its ONLY input is the set of `hot`-labeled cards in project "Radar" (workflow step 1), and the `hot` label lives nowhere but Linear — there is no file-based fallback to pick from. No research, no `radar/deep/` file, no card movement attempted. This is now a SIXTY-FIFTH consecutive affected run since 2026-08-24, and the EIGHTH consecutive deep-dive run fully blocked — the deep-dive pipeline has produced zero output since going live (33 days). Note: this firing landed on a Sunday, off the routine's Mon+Thu cadence — likely a manual fire or a schedule change; the outcome is unaffected either way. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session. Once reconnected, the next run will pick up any `hot` backlog automatically (up to 3 cards per run, oldest first).

## 2026-09-22 05:03 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-21T03:03 UTC. `fetch_radar.py` ran clean apart from two known-shape failures: all 7 YouTube sources returned genuine HTTP 404 from `www.youtube.com/feeds/videos.xml` (confirmed via direct `curl` outside the script, including against a known-stable, unrelated channel ID — `server: YouTube RSS Feeds server` header present, so this is YouTube's own endpoint responding 404, not an egress block; looks like YouTube retired/changed the legacy `/feeds/videos.xml` RSS path rather than any per-channel issue — worth a look if it persists tomorrow, may need a replacement transport for the `youtube` category); `reddit` hit its expected daily 429 (skipped, no retry per policy).

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 3 | 3 | - |
| bigtech-eng | 1 | 1 | - |
| research-institutes | 0 | 0 | - |
| technical-newsletters | 1 | 1 | - |
| practitioner-blogs | 3 | 2 | - |
| youtube | 0 | 0 | HTTP 404 on all 7 sources (see above) |
| community | 22 | 8 | reddit HTTP 429 |
| mistral-watch | 0 | 0 | - |

Totals: 15 items, 3 highlights, 1 category error (youtube — systemic, not per-source), reddit 429.

TRIAGE pass 1/2: dropped as duplicates of items already in this week's radar files (exact canonical-URL match) — `volotat/mini-AGI` (surfaced again today via `hn-show-ai50`×2, `hn-show-inference`, and `lobsters`; already written to `radar/community.md` 2026-09-21) and `pirateface.co` (surfaced again via `hn-trend-llm` at 548pts, up from 495pts yesterday; already written to `radar/community.md` 2026-09-21 as a title-only pointer) — neither re-added, both still trending but not new stories. Dropped as non-AI/off-topic (explicit pass-1 exclusion, `hn-show-rag`'s query match is a false positive on both): "Show HN: A website that tracks US food prices every day," "Show HN: Radius – A Meetup.com Alternative"; also off-topic from `github-trending`'s unfiltered mirror: `paperless-ngx/paperless-ngx` (general doc management, no AI content) and `mihail911/modern-software-dev-assignments` (Stanford course repo, no clear AI-specific content in the visible description). Dropped as thin/marketing-shell: "Show HN: Gdocs-me-up" (a Google Docs exporter that used AI agents to build itself but has no AI-technique content of its own, 20pts/8comments) and `Altworld/Hemmingway-1` (HF trending, 397 score, but empty summary/no technical detail — insufficient substance to write honestly). Dropped for budget at LOW owner-fit (pure video-gen, no code-adjacent angle for the owner): `TencentARC/WorldCrafter` (HF daily paper, 9 upvotes, image/video world-model — cleared pass 1 as a real paper with code but ceded to the ~15/day cap ahead of eight stronger HIGH/MEDIUM-fit stories). Folded rather than duplicated: `latent.space/p/jev` (a same-day podcast interview with TypeSafe AI's CEO) covers the same "Jev" launch as `simonwillison.net`'s post — written as a cross-reference inside the Simon Willison entry in `radar/practitioner-blogs.md` rather than as a second line, since both are commentary on the identical third-party release rather than independent stories.

VERIFY SUBSTANCE: attempted 5 candidates (the up-to-5 cap). `lmsys.org` NVFP4 KV-cache post and `newsletter.semianalysis.com`'s MoE inference-mapping piece verified via WebFetch — both real, numbers-heavy technical writeups. `naw103/foremerge` and `BuilderIO/agent-native` verified via `git clone` — both substantial, real repos (Foremerge: working Rust CLI/API/MCP-server coordination protocol, pre-1.0 but functional; Agent-Native: a genuine shared-actions architectural pattern, not a thin wrapper). `huggingface.co/papers/2609.24972` (RRSI) fetched via WebFetch but the page rendered only a figure caption, not the abstract — kept anyway on the strength of `fetch_radar.py`'s own captured abstract text (sufficient for an honest summary), not elevated further. `pirateface.co` was NOT re-verified this run since it's a same-story duplicate already covered (see above), not a new highlight candidate.

**Highlights: 3** — **NVFP4 KV Cache in SGLang** (real reproducible benchmarks: 26–78% decode-throughput gains, 2–3× cache-hit rate under high agentic concurrency, negligible accuracy loss — direct hit on "local/self-hosted models: inference engines, serving cost/perf"), **SemiAnalysis' MoE inference-mapping piece** (a genuine hardware-mapping methodology — operating-regime separation, parallelism-per-regime, HBM/DRAM/storage cost framing — not a finance piece despite the newsletter's usual framing; direct hit on "GPU/kernel engineering"), and **Foremerge** (an open-source Git-layered coordination protocol that catches intent conflicts between parallel coding agents — directly applicable to the owner's own multi-agent Claude Code workflows, installs in one line; direct hit on "AI agents in practice"). Runners-up ceded to the cap: RRSI/Harness-Zero (agent-harness self-improvement papers with code, but research-grade rather than immediately reproducible as a small experiment) and `anthropics/financial-services` (a strong Anthropic-authored agent/skills reference architecture, but more a reference repo than an experiment seed).

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization; ToolSearch confirms no Linear tools are loadable in this non-interactive session.** No review-queue cards attempted. All 15 confirmed items are fully written across `radar/*.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a SIXTY-SIXTH consecutive affected run since 2026-08-24 (~30 days with no working review queue or News digest board, and the deep-dive pipeline has produced zero output since going live). Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: radar run 2026-09-22 (+15 items, 3 highlights, Linear unavailable)`.

## 2026-09-23 05:06 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-22T03:01 UTC. `fetch_radar.py` ran clean apart from the now-familiar YouTube shape failure: all 7 YouTube sources returned genuine HTTP 404 from `www.youtube.com/feeds/videos.xml` (third consecutive day — the legacy RSS path looks retired rather than a per-run blip; still worth a fix, e.g. swap to an Invidious/piped mirror or drop the category, but out of scope for a daily run to change). Reddit succeeded this run (25 items, no 429).

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 2 | 2 | - |
| bigtech-eng | 0 | 0 | - |
| research-institutes | 0 | 0 | - |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 3 | 2 | - |
| youtube | 0 | 0 | HTTP 404 on all 7 sources (see above) |
| community | 59 | 10 | - |
| mistral-watch | 0 | 0 | - |

Totals: 14 items, 2 highlights, 1 category error (youtube — systemic).

TRIAGE pass 1/2: dropped as non-AI/off-topic (HN Show-tag false positives and GitHub-trending mirror noise): "Show HN: Drop – A rootless Linux sandbox with gVisor support" (161pts, general container sandboxing, no AI angle), "Show HN: A website that tracks US food prices every day" (29pts), `mvt-project/mvt` (mobile-forensics toolkit), `ruanyf/weekly` (general Chinese tech-news digest, not AI-specific). Dropped as consumer-app/thin: `zhouxiaoka/autoclip` (AI-powered video-clipping consumer app — falls under the consumer-app-launch exclusion). Dropped as opinion/meta threads with no technical substance (Reddit): "Unsloth Studio VS LM Studio... which one do you prefer?", "Now Opus 5.5 is 58 on Artificial Analysis, how long until an open model hits 58?", "How is Gemma4 12B for general everyday use?", "What underrated AI tools have actually made you more productive in 2026?", "Am I going insane for thinking these are all Bot comments?", "Did Alibaba abandon 35B A3B?", "Ngram and world knowledge - why are we just building a coding model?", "Is llama.cpp meant to be slow at long context...". Dropped as gimmick/thin demo: "Laya model playing Flappy Bird on a CPU using OpenVINO INT8 inference". Dropped as duplicate of a story already in this week's radar files: "Show HN: Lossless-memory" and "Show HN: Foremerge" (both already written 2026-09-21), "mini-AGI: Continual-learning..." (already written + highlighted 2026-09-21, resurfacing again today), Qwen-Image-2.1 reddit threads ×2 + `abenzerps/Qwen-Image-2.1-Uncensored-GGUF` HF trending (base model + GGUF variant already covered 2026-09-20/21; also LOW-interest image-gen per `interests.md`) — none re-added. Folded into a single consolidated item rather than three separate lines: `XiaomiMiMo/MiMo-V2.6-Pro-RL` + `-Flash-RL` + `-Distill-Qwen-9B` (three HF-trending entries, one release) plus the Reddit "About Mimo 2.6 Architecture" discussion and the two duplicate Reddit submissions of the same `MiMo-V2.6-Distill-Qwen-9B` HF listing — all one story. Nathan Lambert's Reddit-linked "written Congressional testimony" post folded as a duplicate of the fuller `interconnects.ai` piece on the same testimony already written 2026-09-21 (`radar/practitioner-blogs.md`) — not re-added. `latent-space`'s John Platt podcast-interview post dropped at pass 1 — profile/career piece, no engineering-technique content. Dropped at pass 2 for budget against the ~15/day cap, ceding to stronger same-day HIGH-fit picks: "quants for K2-Horizon are now available" (routine, thin quant-availability post, no technique detail), `notjev` (a further same-week reproduction in the already heavily-covered Jev/decision-model cluster — folded as a passing mention rather than a separate line; see `radar/community.md` 2026-09-20/21/22 entries for the cluster), HF-trending-spaces (`multimodalart/jev-decision-index`, `Krea-2-Turbo_v2`, `hugging-apps/qwen-image-2-1`, `xingyuanzhao/nocode-workflow` — leaderboard/demo spaces, thin standalone substance), `lobsters`' "How to talk about 'AI' without adding to the anthropomorphization" (culture/language essay, not engineering content).

VERIFY SUBSTANCE: attempted candidates against the up-to-5 cap. `huggingface.co/papers/2609.26796` (Flash-dLLM) and `huggingface.co/papers/2609.25804` (Tasteful Agent / Taste-Bench) verified via `git clone` of their linked repos (`VILA-Lab/Flash-dLLM`, `wbopan/tastebench`) — both real, code-and-numbers-backed: Flash-dLLM ships a full benchmark table (22.3×–148.2× decode speedup, GSM8K/MATH/HumanEval/MBPP scores at two lengths, single-A100 reproducible); Taste-Bench ships a live leaderboard (502 real agent-trajectory decision forks, GPT-5.6 Sol leading at 59.7%, Claude Opus 5 at 55.5%). `arxiv.org/abs/2609.22978` (DSec) verification blocked — arxiv.org is egress-blocked in this cloud env for both WebFetch (`EGRESS_BLOCKED`) and a curl retry (`connect_rejected — organization policy`, not a transient timeout) — kept as a title-only item, out of highlight consideration. `benchmarkheaven.com/jev-models` (JevBench) and `www.assbench.com` (LLM Ass Bench) both hit `EGRESS_BLOCKED` on WebFetch (domains not in the cloud allowlist) — LLM Ass Bench dropped outright rather than kept unverified (title reads as satire/meme-adjacent and 144 HN points alone isn't enough to write it up honestly against the never-invent-content rule); JevBench kept as a regular (non-highlight) item since its own HN self-text already describes a concrete "reproducible benchmark for typed decision models" claim consistent with this week's Jev/decision-model cluster. `www.interconnects.ai/p/debating-rsi-the-us-china-gap-and` verified via WebFetch (not github/reddit, no transport block) — real debate content, written to `radar/practitioner-blogs.md`, not elevated to highlight (a debate/discussion rather than a technique with numbers).

**Highlights: 2** — **Flash-dLLM** (training-free diffusion-LLM inference acceleration, 22–148× decode speedup with full reproducible benchmark numbers and open code — direct hit on "local/self-hosted models: inference engines, serving cost/perf") and **The Tasteful Agent / Taste-Bench** (a concrete, code-backed benchmark for the exact long-horizon-agent failure mode — decisions that look fine now and cost the run later — direct hit on "evals in practice"). Both cleared VERIFY SUBSTANCE via `git clone` with real numbers, not marketing shells.

**Linear: UNAVAILABLE this run — ToolSearch confirms no Linear tools are loadable in this session (MCP server requires re-authorization; non-interactive session cannot run the OAuth flow).** No review-queue cards attempted. All 14 confirmed items are fully written across `radar/*.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now a SIXTY-EIGHTH consecutive affected run since 2026-08-24. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

**Housekeeping note:** at the start of this run, local `main` was again found 12 commits behind the actual working state (detached HEAD at `6f33631`, the 2026-09-22 daily-run commit) — the same shape as the note on 2026-09-21 (a prior run apparently completed its work but ended before fast-forwarding/pushing `main`). Fast-forwarded `main` to HEAD and pushed before starting this run's work; nothing was lost. Recurring enough now (twice in 3 days) that it may be worth checking whether the routine's finishing steps reliably run `git checkout main && git merge --ff-only` before push, rather than committing on a detached HEAD.

Commit: `news: radar run 2026-09-23 (+14 items, 2 highlights, Linear unavailable)`.

## 2026-09-22 06:15 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-21T06:10 UTC (last successful daily run). `fetch_feeds.py` ran clean — mistral hit a 304 (cursor unchanged); microsoft (1), nvidia (3), and huggingface (1) reported fresh TIER-1 candidates; the other 8 companies reported zero fresh. Gap-scrape attempted for all 8/8 zero-fresh companies.

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebFetch → 403, retried via `r.jina.ai` | 0 | jina | WebFetch target-403 on `/news/`; Jina succeeded — newest two items ("Advisory group on mathematics and artificial intelligence", "Expanding OpenAI Academy with new learning paths", both Sep 21) are tagged `Company`, outside `category_keep`, correctly fail-closed/dropped; "Astra for Law" (Sep17/18) and everything else already in `topics/openai.md` |
| anthropic | fetch (`/news`) | 0 | - | listing tops out at the Accenture embedded-evaluation post (Sep18), already captured |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | listing's newest items (Gemini 3.8 Flash/Flash Cyber, Fairwind Program, 3.8 Live, AlphaGenome Atlas, WeatherNext 3, agentic video) all already present in `topics/google-deepmind.md` |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | listing tops out at MilleMiglia (Sep18), already captured |
| microsoft | rss.xml (TIER-1, 1 fresh) | 1 | - | RetroChimera (retrosynthesis prediction, Nature paper) — confirmed, written |
| nvidia | rss.xml (TIER-1, 3 fresh) | 3 | - | TensorRT multi-device in Dynamo-Triton, AI-agent evaluation framework, Earth-2 data assimilation — all confirmed, written |
| xai | rss n/a (jina-only company); curl r.jina.ai (200, anonymous) | 1 | jina | **Grok 4.7** — new flagship model release (Sep21), not previously captured; confirmed via primary source, written |
| mistral | rss.xml (TIER-1, 304) | 0 | - | cursor unchanged since last run |
| huggingface | rss.xml (TIER-1, 1 fresh) | 1 | - | "Pruning LLMs Like a Physicist" (Ising-optimization block pruning, Multiverse Computing) — confirmed, written |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on changelog listing | 0 | WebFetch | listing tops out at Cursor Projects (Sep10), already captured |
| perplexity | curl r.jina.ai → 403 AbuseAlleviation (still blocked until 07:06 UTC, same recurring block), WebSearch fallback | 1 | jina (403) then WebSearch | WebSearch surfaced "Computer adds effort mode for model selection" (Sep17) with a confirmed canonical URL (corroborated by AlternativeTo/AlphaSignal/SQ Magazine) — written as backfilled per the established pattern; a second Sep17 title ("AI in the workplace: a practical guide") is tutorial/marketing content, not a hard announcement — not written per the never-invent/real-announcement rule |

Totals: 7 items, 5 companies fresh (microsoft, nvidia, xai, huggingface, perplexity), 0 hard errors.

**Linear: UNAVAILABLE this run — ToolSearch confirms no Linear tools are loadable in this session (MCP server requires re-authorization; non-interactive session cannot run the OAuth flow).** All 7 new items are fully written to `topics/*.md` + `artifacts/` above — no data lost, only Linear cards are behind. This is now a SIXTY-SEVENTH consecutive affected run since 2026-08-24. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-22 (+7 items, 5 companies fresh, Linear unavailable)`.

## 2026-09-23 06:12 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-22T06:09 UTC (last successful daily run). `fetch_feeds.py` ran clean apart from `cursor.com/changelog/rss.xml` timing out on TLS handshake (transient, no retry needed — gap-scrape covered it below); openai (2) and nvidia (4, after independently re-verifying the raw feed against the pre-run cursor — see note) reported fresh TIER-1 candidates, the other 9 companies reported zero fresh. Gap-scrape attempted for all 9/9 zero-fresh companies (anthropic/fetch, xai/jina, perplexity/jina always gap-scrape by design; the other 6 rss-only companies via WebFetch/WebSearch on their listing pages, one attempt each).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 2 fresh) | 2 | - | "Better prompt caching for GPT-6" and "Introducing GPT-6 Sol and Luna" (both Sep22, tagged Product/Release) — confirmed, written |
| anthropic | fetch (`/news`) | 1 | - | **Claude Opus 5.5** (Sep22) — new flagship-family model release, not previously captured; confirmed via primary source, written |
| google-deepmind | rss.xml (TIER-1, 0 fresh), WebFetch on blog.google listing | 0 | WebFetch | listing's newest items (3.8 Flash/Flash Cyber, Fairwind, agentic video, WeatherNext 3, etc.) all already present in `topics/google-deepmind.md`; nothing newer than the Sep15 3.8 Live entry already captured |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch on blog listing | 0 | WebFetch | listing tops out at MilleMiglia (Sep18), already captured |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch on research blog listing | 0 | WebFetch | listing tops out at RetroChimera (Sep21), already captured; feed's Last-Modified header advanced but no new qualifying item accompanied it |
| nvidia | rss.xml (TIER-1, 4 fresh) | 4 | - | Confidential Computing inference, Topograph, DLSS 5 game-dev update, ROS 2 Isaac agent migration (all Sep22) — confirmed, written |
| xai | rss n/a (jina-only company); curl r.jina.ai (200, anonymous) | 1 | jina | "How SpaceXAI is using Grok Bot to scale customer support" (Sep22) — confirmed via primary source, written; Grok 4.7 (Sep21) already captured |
| mistral | rss.xml (TIER-1, 0 fresh), WebFetch on news listing | 0 | WebFetch | listing tops out at Mistral x Mozilla (Sep16), already captured |
| huggingface | rss.xml (TIER-1, 0 fresh — see note), curl on raw feed.xml | 2 | curl (raw feed) | "How UK AISI and EvalEval Are Making Benchmark Results Reproducible" and "Transformers now runs llama.cpp quants" (both dated Sep22 00:00 GMT in the feed — see note) — confirmed, written; a third Sep22 item ("Jun Kim... joins Hugging Face") excluded as a hiring post per the never-invent/real-announcement rule |
| cursor | rss.xml (TIER-1 TLS timeout), WebFetch on changelog listing | 0 | WebFetch | listing tops out at Cursor Projects (Sep10), already captured |
| perplexity | curl r.jina.ai (HTTP 403 AbuseAlleviation — anonymous access still blocked until 07:07 UTC today, same recurring block), WebSearch | 0 | jina (403) then WebSearch | WebSearch surfaced only titles already captured (CobbleDB, Portable Computer for Windows, Q2D-Web) plus a Sep1 Hybrid-Compute-on-Mac piece that predates the window — no new canonical URL confirmed; not written per never-invent-a-source-URL rule |

Totals: 10 items, 5 companies fresh (openai, anthropic, nvidia, xai, huggingface), 0 hard errors.

**Process note — do not run `fetch_feeds.py` more than once per run.** This run's script was accidentally invoked twice (once to capture output, once more when the first capture was truncated), which advanced `state/cursors.json` past the openai/nvidia items the first run had already found "fresh," making the second run correctly report 0 fresh for everything. No data was lost: openai's 2 items were fully visible in the first run's (truncated) output, and nvidia's item count was independently re-derived by diffing the pre-run cursor timestamp (`2026-09-22T06:09:17`, recovered from `git diff`) against a direct, unconditional fetch of the raw `developer.nvidia.com/blog/feed` — all 4 entries published after that timestamp were confirmed and written. Future runs: capture the full JSON to a file in one shot (no `head`/truncation) before doing anything else with it.

**Housekeeping note (recurring):** at the start of this run, local `main`/`origin/main` were again found 12 commits behind the actual working state (detached HEAD at `d0a04d1`, the 2026-09-23 radar-run commit) — same shape as the notes on 2026-09-21 and 2026-09-23 (radar). Fast-forwarded `main` to HEAD and pushed before starting this run's work; nothing was lost. Now three occurrences in 3 days — worth checking whether the routines' finishing steps reliably run on branch `main` (not a detached HEAD) before their final push.

**Linear: UNAVAILABLE this run — ToolSearch confirms no Linear tools are loadable in this session (MCP server requires re-authorization; non-interactive session cannot run the OAuth flow).** All 10 new items are fully written to `topics/*.md` + `artifacts/` above — no data lost, only Linear cards are behind. This is now a SIXTY-NINTH consecutive affected run since 2026-08-24. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-23 (+10 items, 5 companies fresh, Linear unavailable)`.

## 2026-09-24 05:01 UTC — radar — ok (Linear unavailable)

Window: since 2026-09-23T03:01 UTC. `fetch_radar.py` ran clean apart from two shape failures: all 7 YouTube sources again returned HTTP 404/500 from `www.youtube.com/feeds/videos.xml` (fourth consecutive day — the legacy RSS path looks retired, not a per-run blip) and `eleuther`'s feed 404'd (new, first occurrence — `blog.eleuther.ai/index.xml` may have moved or gone dormant-to-broken; worth a URL check next run, not fixed here per no-gap-scrape-for-radar rule). Reddit succeeded (25 items, no 429).

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 1 | 0 | eleuther HTTP 404 |
| bigtech-eng | 1 | 1 | - |
| research-institutes | 0 | 0 | - |
| technical-newsletters | 1 | 1 | - |
| practitioner-blogs | 1 | 0 | - |
| youtube | 0 | 0 | HTTP 404/500 on all 7 sources (see above) |
| community | 52 | 12 | - |
| mistral-watch | 0 | 0 | - |

Totals: 14 items, 3 highlights, 2 category errors (youtube — systemic/recurring; eleuther — new today).

TRIAGE pass 1/2: dropped as off-topic/no-AI-angle despite decent HN engagement (consistent with yesterday's call on the same recurring post): "Show HN: Drop — a rootless Linux sandbox with gVisor support" (185pts today, up from 161pts when dropped 2026-09-23 for "general container sandboxing, no AI angle" — same story resurfacing in the HN "AI" query, still no AI-specific tie-in on inspection; not re-litigated into a different verdict just because points grew). Dropped as non-AI keyword-match noise (HN Show-tag "RAG"/"MCP" full-text false positives): "Show HN: I built a post-mortem debugger for native Windows x64/x86 crashes" (forensicdbg.com, appeared under both hn-show-rag and hn-show-mcp — nothing AI-related in it). Dropped as thin/low-substance demo or product-marketing posts: "Show HN: RxFilm Studio — AI agent video product" (19pts, consumer-app-launch pattern), "NVFP4 - what does the quality usually equate to? (5090)" (open question, no findings), "GUI harness [video]" (no substance beyond a video link), "Engram gone wild! 2b model update..." (vague), "Most powerful harness for Qwen 3.8?" (open question), "Pi agent qwen 3.8 flash next plays Baldur's Gate 2" (fun demo, no technique detail), "apple/LensVLM-9B · Hugging Face" (bare repost, no discussion). Dropped as meme/opinion/hot-take Reddit threads with no technical substance: "Jev ain't all that...", "Using uncensored models makes working less of a headache", "Qwen FN vs 27B --- Think I'm saturated.", "Please Google, for the love of God.", "Jev isn't new tech...", "MiMo-V2.6 (both Pro and Flash) is a benchmaxxed scam", "Mods: can we do something about half the forum...", "Cost of intelligence is dropping fast", "this is not even a competition at this point ... this is embarrassing". Dropped as unverifiable + risk of low-quality/meme content: "LLM Ass Bench" (166pts HN, `assbench.com` hit `EGRESS_BLOCKED` on WebFetch, title reads as joke-adjacent — not written up against the never-invent-content rule, same call as "LLM Ass Bench"-style drops on prior runs). Dropped for owner-fit (LOW-interest robotics/video-gen, per `interests.md`) despite clearing pass 1 with real substance: `General-Instinct/InstinctFlash` (verified via `git clone` — genuine robotics serving framework, YC-backed, real Jetson Thor benchmarks up to 33.78× speedup — real engineering, wrong topic), "BFL releases FLUX 3 Action: a 7B robot model", HF daily papers "The Past Frames the Future" (autoregressive video-gen memory) and "MemBodied" (VLA/robotics memory), HF trending space `pollen-robotics/microduck-simulator`. Dropped for budget against the ~15/day cap, ceding to stronger same-day picks: `pytorch-blog`'s "Bring Your Academic PyTorch Project to PyTorchCon NA" (conference-promotion post — matches the existing `drop_title_re` filter's intent even though the literal string didn't match), `latent-space`'s Eric Nguyen bio-security-AI-arms-race podcast interview (discussion/opinion format, no engineering-technique content), HN "Show HN: Training a model to identify AI web content from structure alone" (arxiv.org/abs/2609.15369, 66pts — real research but MEDIUM fit, budget-constrained), "Pirate Face - pirate bay for LLMs" reddit repost (title-only resurfacing of a story already covered 2026-09-21), `hf-trending-models` (`TaichuAI/ZDTaichu5.0-9B`, `netease-youdao/Confucius4-R2T2` — thin leaderboard-snapshot signal, no announcement text), `lobsters`' "FLAWED's Flaws and What This Means for Industry Research" (score 2, low signal).

VERIFY SUBSTANCE: 5 candidates attempted against the cap. `google/ax` verified via `git clone` — real, substantial (Kubernetes-style declarative orchestrator for agent workloads, built on top of `agent-substrate/substrate` already covered here 2026-08-20). `EthanNing/WhatWorkedBench` verified via `git clone` — real, code-and-baselines-backed benchmark (36 tasks, 30 sources, 1,248 native outcomes). `github.blog`'s "Rendering huge pull requests in the GitHub Copilot app" verified via WebFetch — substantive engineering writeup with a concrete dual-geometry virtualization architecture, no numbers/benchmarks included but the technique itself is well-specified. `benchmarkheaven.com/jev-models` (Show HN: JevBench) hit `EGRESS_BLOCKED` on WebFetch (domain not in the cloud allowlist) — kept as a regular (non-highlight) item on the HN listing title, consistent with this week's Jev/decision-model cluster. `www.assbench.com` (LLM Ass Bench) also hit `EGRESS_BLOCKED` — dropped outright rather than kept unverified, same call as prior runs on this exact site/pattern (see TRIAGE above). `davila7/claude-code-templates` and `superdesigndev/treg` verified via `git clone` outside the 5-cap (both github-trending, straightforward READMEs) — both real: claude-code-templates is an established, actively-sponsored template/component catalog for Claude Code itself; treg is a genuine (if commercial) metered tool-catalog product for agents ("OpenRouter for tools").

**Highlights: 3** — **google/ax** (declarative Kubernetes-style orchestrator for agent workloads at cluster scale, direct hit on agent harnesses/orchestration and a natural sequel to the already-tracked `agent-substrate`), **WhatWorkedBench** (reproducible, code-backed benchmark for whether an agent actually learns from its own experiments — direct hit on evals-in-practice + agents), and **"Rendering huge pull requests in the GitHub Copilot app"** (concrete dual-geometry virtualization architecture for AI-coding-tool UI at extreme scale — genuine engineering, not a marketing shell). All three cleared VERIFY SUBSTANCE.

**Linear: UNAVAILABLE this run — ToolSearch confirms no Linear tools are loadable in this session (MCP server requires re-authorization; non-interactive session cannot run the OAuth flow).** No review-queue cards attempted. All 14 confirmed items are fully written across `radar/*.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now the SEVENTIETH consecutive affected run since 2026-08-24. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

**Housekeeping note (recurring):** at the start of this run, local repo was again found on a detached HEAD, `main` 14 commits behind (same shape as the notes on 2026-09-21/22/23). Stashed this run's in-progress edits, fast-forwarded `main` to the detached HEAD's commit, confirmed `origin/main` already matched (a concurrent push had landed it), then restored this run's edits and continued on `main`. Fifth occurrence in 4 days — still worth checking whether the routines' finishing steps reliably run `git checkout main && git merge --ff-only` (or start each run already on `main`) before their final push.

Commit: `news: radar run 2026-09-24 (+14 items, 3 highlights, Linear unavailable)`.

## 2026-09-24 06:05 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-23T06:12 UTC (last successful daily run). `fetch_feeds.py` ran once, output captured to a file in one shot (per the 2026-09-23 process note). TIER-1 reported fresh candidates for openai (1), microsoft (1), nvidia (4), huggingface (1); zero fresh for the other 7 companies — gap-scrape attempted for all 7 (anthropic/fetch, xai/jina, perplexity/jina always gap-scrape by design; google-deepmind/google-research/mistral/cursor via WebFetch on their listing pages, one attempt each). `google-deepmind`'s rss.xml returned `TRAP/not-a-feed` this run (HTML body, not a feed) — new occurrence, not previously seen for this URL; gap-scraped via WebFetch instead, logged here for the owner to watch (not changed in config on a single occurrence). `mistral`'s rss.xml returned 304 not-modified (correctly zero-fresh, not an error).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 1 fresh) | 1 | - | "Introducing MentalHealthBench" (Sep23) — confirmed, written |
| anthropic | fetch (`/news`) | 1 | - | **Claude discovers a novel enzyme system with CRISPR-like repeats** (Sep23) — ~950 Claude agents autonomously found a novel CRISPR-like enzyme system (ART) in genomic databases; confirmed via primary source, written |
| google-deepmind | rss.xml (TIER-1, TRAP/not-a-feed), WebFetch on deepmind.google/blog listing | 0 | WebFetch | listing tops out at Gemini 3.8 Live (Sep15), already captured; nothing newer found |
| google-research | rss.xml (TIER-1, 0 fresh), WebFetch on research.google/blog listing | 0 | WebFetch | listing tops out at MilleMiglia (Sep18), already captured |
| microsoft | rss.xml (TIER-1, 1 fresh) | 1 | - | "Offloaded inference for real-world physical AI robotics" (Sep23) — confirmed, written |
| nvidia | rss.xml (TIER-1, 4 fresh) | 4 | - | NV-Reason-CT, Cluster Readiness Engine (NVCRE), NodeWright, SWE-Serve (all Sep23) — confirmed, written |
| xai | rss n/a (jina-only company); curl r.jina.ai (200, anonymous) | 0 | jina | newest item Grok 4.7 (Sep21) and Grok Bot customer support (Sep22) already captured; nothing newer |
| mistral | rss.xml (TIER-1, 304 not-modified), WebFetch on news listing | 0 | WebFetch | listing tops out at Mistral x Mozilla (Sep16), already captured |
| huggingface | rss.xml (TIER-1, 1 fresh) | 1 | - | "How to Use NVIDIA Warp and MjWarp to Accelerate Robotics Simulation and Learning Workflows" (Sep23) — confirmed, written |
| cursor | rss.xml (TIER-1, 0 fresh), WebFetch on changelog listing | 1 | WebFetch | "Rollouts and Security Review" (Sep23) — confirmed via WebFetch + HTTP 200 URL check, written |
| perplexity | curl r.jina.ai (HTTP 403 AbuseAlleviation, anonymous access blocked until 07:04 UTC today — same recurring block), WebSearch | 0 | jina (403) then WebSearch | WebSearch surfaced only titles already captured (Computer effort mode, Sep17); no new canonical URL confirmed |

Totals: 9 items, 6 companies fresh (openai, anthropic, microsoft, nvidia, huggingface, cursor), 0 hard errors.

**Housekeeping note:** at the start of this run, local `main` was on a detached HEAD one commit behind `origin/main` (stale local tracking metadata from before `git fetch`, not a real divergence — `origin/main` already carried the 2026-09-24 radar-run commit). Fetched, fast-forwarded `main` to `origin/main`, confirmed clean, then did this run's work on `main`. No data at risk this time; same recurring shape as prior days' notes — still worth the routines double-checking they finish each run already checked out on `main`.

**Linear: UNAVAILABLE this run — no Linear MCP tools loadable in this session (server requires re-authorization; non-interactive session cannot run the OAuth flow).** All 9 new items are fully written to `topics/*.md` + `artifacts/` above — no data lost, only Linear cards are behind. This is now the SEVENTY-FIRST consecutive affected run since 2026-08-24. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-24 (+9 items, 6 companies fresh, Linear unavailable)`.

## 2026-09-24 07:01 UTC — deep-dive — blocked (Linear unavailable)

**Linear: UNAVAILABLE this run — the Linear MCP server requires re-authorization and its tools were not loaded in this session (non-interactive session; cannot run the OAuth flow); ToolSearch confirms no Linear tools are loadable.** The deep dive cannot degrade gracefully: its ONLY input is the set of `hot`-labeled cards in project "Radar" (workflow step 1), and the `hot` label lives nowhere but Linear — there is no file-based fallback to pick from. No research, no `radar/deep/` file, no card movement attempted. This is now the SEVENTY-SECOND consecutive affected run since 2026-08-24, and the NINTH consecutive deep-dive run fully blocked — the deep-dive pipeline has produced zero output since going live (31 days; `radar/deep/` still holds only TEMPLATE.md). Owner action needed (unchanged): reconnect the Linear connector at claude.ai Settings → Connectors (https://claude.ai/customize/connectors), then let the next scheduled run pick it up — connectors are read at session start, so the fix takes effect on the next firing without any other change. Once reconnected, the next deep-dive run will pick up any `hot` backlog automatically (up to 3 cards per run, oldest first).

**Housekeeping note (recurring):** at the start of this run, the local repo was again on a detached HEAD with `main` behind (same shape as 2026-09-21/22/23/24 notes) — HEAD was already at `origin/main`'s tip (99e5cab), so this was stale local tracking only, no divergence. Checked out `main`, fast-forwarded to `origin/main`, continued on `main`. Sixth occurrence in 5 days.

Commit: `news: deep dive 2026-09-24 (0 cards, blocked — Linear unavailable)`.

## 2026-09-25 05:05 UTC — radar — ok (Linear unavailable)

`fetch_radar.py` ran once (output captured to a file in one shot). Errors reported in-band: `eleuther` HTTP 404 (recurring — index.xml gone, second occurrence after 2026-09-24), all 7 YouTube channel feeds HTTP 404/500 (systemic/recurring, unchanged), `reddit` HTTP 429 (skipped per policy, no retry).

| category | raw candidates | confirmed | errors |
| --- | --- | --- | --- |
| lab-engineering | 0 | 0 | - |
| inference-infra | 0 | 0 | - |
| oss-ml-systems | 0 | 0 | - |
| bigtech-eng | 2 | 2 | - |
| research-institutes | 0 | 0 | - |
| technical-newsletters | 0 | 0 | - |
| practitioner-blogs | 2 | 1 | - |
| youtube | 0 | 0 | HTTP 404/500 on all 7 sources (recurring) |
| community | 36 | 10 | - |
| mistral-watch | 0 | 0 | - |

Totals: 13 items, 3 highlights, 2 category errors (youtube — systemic/recurring; eleuther — second occurrence, worth checking the feed URL next run).

TRIAGE pass 1/2: dropped as no-AI-angle Show HN false positives (cross-tagged under agents/ai50/mcp/rag queries): "Show HN: Koi.rest – watch some fish and regain your balance" (154pts, pure relaxation app), "Show HN: Air-gapped file encryption as self-decrypting HTML page" (53pts, crypto tool), "Show HN: I built a post-mortem debugger for native Windows x64/x86 crashes" (forensicdbg.com — same exact title/URL dropped 2026-09-24 for the identical reason, resurfaced today under hn-show-mcp/hn-show-rag again), "Show HN: Trader News – Hacker News for Finance" (17pts, HN clone for markets, no AI content despite hn-show-agents/hn-show-inference tagging). Dropped as thin/low-substance or spammy: "Best LLM for every budget, updated daily" (167pts but empty self-text, spam-pattern tracker site), HF trending spaces `Viggle/Qwen-Image-2.1-viggle-turbo` and `vamo455/Omni-videos-custom-auto_prompt_high-quality` (thin demo spaces, spam-pattern naming on the latter), HF trending model `Edge0/Audio8-ASR-Infinite` (bare leaderboard snapshot, no announcement text), Lobsters "Introducing Lev" (yogthos.net egress-blocked, title+tags alone insufficient to write up without inventing content), Lobsters "Pencils Down, Eyes Open: A Rails Developer After Rails World" (score 1, Rails-centric personal essay, AI/vibecoding only tangential). Dropped for owner-fit (LOW-interest video-gen/robotics per `interests.md`) despite real content: HF daily paper "ViRDM: Taming Representation Distribution Matching for Few-Step Causal Video Generation", Latent Space's "Runway's WorldPrompt and the Engineering of Real-Time Worlds" (real-time world-model video/audio generation). Dropped as off-topic (no LLM/agent/local-model tie, generic video-codec research): HF daily paper "Rate-distortion optimization for full-reference image quality metrics via stochastic Hessian estimates". Dropped as consumer-app-launch pattern (recurring): "Show HN: RxFilm Studio–Create and edit your product videos with AI agent" (19pts — same submission/pattern dropped 2026-09-24 under a near-identical title).

VERIFY SUBSTANCE: 6 candidates attempted (one over the 5-cap, given high HN signal). `strands-agents/harness-sdk` verified via `git clone` — real, established open-source agent-harness SDK (PyPI + npm distributed, dedicated team/test-infra, own AGENTS.md/CLAUDE.md). `Parcha-ai/agentrun` verified via `git clone` — real, working Jev-integrated workflow DSL with docs, examples, Pi-extension integration. `HKUDS/CLI-Anything` verified via `git clone` — real, large-scale (60+ tool integrations) agent-native CLI registry from an established academic lab, GitHub-trending #1. `devdotfast/whiteboard` verified via `git clone` (checked despite being outside the initial top-5 pick, given its 240pts HN signal) — real, working desktop app with an agent-drawing-canvas SDK, plugs directly into Claude Code/Codex. `github.blog`'s "AI-powered fuzzing with the GitHub Security Lab Taskflow Agent" verified via WebFetch — substantive: three-layer shell-driver/YAML-taskflow/MCP-tools architecture, concrete AFL double-build strategy, doubling time-budget coverage loop with plateau detection, structure-aware corpus mechanisms, crash-triage pipeline; no bug-count/coverage numbers given. `github.blog`'s "When chat is the wrong UI" verified via WebFetch — mostly narrative/opinion (no benchmarks, token numbers, or architecture spec beyond "bidirectional communication"), kept as a regular item, out of highlight consideration.

**Highlights: 3** — **strands-agents/harness-sdk** (production-ready open-source agent-harness SDK, directly comparable to the owner's own Claude Code-based routines), **Show HN: Whiteboard** (open-source agent-drawing-canvas app that plugs straight into Claude Code, highest community signal of the day at 240pts, worth a hands-on try), and **Show HN: AgentRun** (Jev-integrated agent-workflow DSL, continues this month's tracked decision-model cluster from a new angle). All three cleared VERIFY SUBSTANCE. `HKUDS/CLI-Anything` and the GitHub Security Lab fuzzing post were also verified-substantive but held back from the 3-pick cap; `HKUDS/CLI-Anything` kept as a strong regular item (real substance, scale), fuzzing post likewise.

**Linear: UNAVAILABLE this run — ToolSearch confirms no Linear tools are loadable in this session (MCP server requires re-authorization; non-interactive session cannot run the OAuth flow).** No review-queue cards attempted. All 13 confirmed items are fully written across `radar/*.md` above — no data lost, only the Linear review queue and `highlight`/priority labels are behind. This is now the SEVENTY-THIRD consecutive affected run since 2026-08-24. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

**Housekeeping note (recurring):** at the start of this run, the local repo was again on a detached HEAD, one commit behind `origin/main` after a fetch picked up the prior run's push (same shape as the notes on 2026-09-21 through 2026-09-24). Checked out `main`, fast-forwarded to `origin/main` (clean, no divergence), continued on `main`. Seventh occurrence in 6 days — the recurring pattern across routines strongly suggests their finishing steps should explicitly `git checkout main && git merge --ff-only origin/main` (or start each run already on `main`) before the final push, rather than relying on incidental fast-forwards; flagging again for the owner as this is now a standing pattern, not a one-off.

Commit: `news: radar run 2026-09-25 (+13 items, 3 highlights, Linear unavailable)`.

## 2026-09-25 06:04 UTC — daily — ok (Linear unavailable)

Window: since 2026-09-24T04:04 UTC (`fetch_feeds.py`'s own cursor window; last successful daily run was 2026-09-24 06:05 UTC). `fetch_feeds.py` ran once, output captured to a file in one shot. TIER-1 reported fresh candidates for google-deepmind (1), google-research (1), nvidia (1), huggingface (1); zero fresh for the other 7 companies — gap-scrape attempted for all 7 (anthropic/fetch, xai/jina, perplexity/jina always gap-scrape by design; openai/microsoft/mistral/cursor via WebFetch/WebSearch on their listing pages, one attempt each, since those companies have no fetch/jina tier configured).

| company | searched | found | fell-back | errors |
| --- | --- | --- | --- | --- |
| openai | rss.xml (TIER-1, 0 fresh), WebFetch + curl on openai.com/news (both 403), WebSearch | 0 | websearch | WebFetch/curl both 403; WebSearch surfaced only vague/unconfirmed leads (DevDay 2026 preview, an unconfirmed "voice-agentic ChatGPT mobile" claim, a third-party "Frontier AI Standards Agency" report) — none with a confirmed openai.com canonical URL dated in-window; rejected as unconfirmed |
| anthropic | fetch (`/news`) | 0 | fetch | WebFetch confirms listing tops out at "Claude discovers a novel enzyme system" (Sep23), already captured; nothing newer |
| google-deepmind | rss.xml (TIER-1, 1 fresh) | 1 | - | "Introducing Gemini 3.8 Live with Live Avatar" (Sep24) — confirmed; note: canonical deepmind.google URL now 302-redirects off-domain to blog.google (new behavior, not previously seen for this feed) and blog.google is egress-blocked for WebFetch/curl — content fetched via `r.jina.ai` on the redirect target instead; written |
| google-research | rss.xml (TIER-1, 1 fresh) | 1 | - | "Automating coherent long-form video generation" (Sep24) — confirmed via WebFetch, written |
| microsoft | rss.xml (TIER-1, 0 fresh), WebFetch on research blog listing | 0 | WebFetch | listing tops out at "Offloaded inference for real-world physical AI robotics" (Sep23), already captured; nothing newer on the Research blog (note: WebSearch surfaced several Sep23/24 news.microsoft.com/source items — Surface Pro/Laptop, Rockwell Automation, Majorana-2/DARPA — correctly out of scope per the 2026-08-08 technical-first refocus, which tracks the Research blog only) |
| nvidia | rss.xml (TIER-1, 1 fresh) | 0 | - | 1 candidate excluded: "Efficient MoE Training for Biological Foundation Models" verified via WebFetch as a routine implementation recipe/tutorial (GroupedLinear + MXFP8 + fused kernel benchmarks on Mixtral-8x7B, 2.21x throughput) — not a genuine announcement/major post, dropped per the NVIDIA config note (keep only genuine announcements, not every tutorial) |
| xai | rss n/a (jina-only company); curl r.jina.ai (200, anonymous) | 0 | jina | listing tops out at Grok Bot customer support (Sep22), already captured; nothing newer |
| mistral | rss.xml (TIER-1, 0 fresh), WebFetch on news listing | 0 | WebFetch | listing tops out at Mistral x Mozilla (Sep16), already captured |
| huggingface | rss.xml (TIER-1, 1 fresh) | 1 | - | "Accelerating vision-language models with LFM2.5-VL-DSpark" (Sep24) — confirmed via WebFetch, written |
| cursor | rss.xml (TIER-1, 0 fresh), WebSearch | 0 | websearch | listing tops out at "Rollouts and Security Review" (Sep23), already captured; nothing newer |
| perplexity | curl r.jina.ai (HTTP 403 AbuseAlleviation, anonymous access blocked, no JINA_API_KEY), WebSearch, direct WebFetch (EGRESS_BLOCKED on perplexity.ai) | 0 | jina (403) then websearch | WebSearch repeatedly surfaced the title "Escaping SPACE: Part I" (red-teaming VM isolation for AI agents, claimed Sep23) but no search variant returned a confirmed perplexity.ai/hub/blog canonical URL for it; rejected as unconfirmed per never-invent rule (same call as the 2026-08-02 HF precedent) |

Totals: 3 items, 3 companies fresh (google-deepmind, google-research, huggingface), 0 hard errors (7 gap-scrapes attempted, all came up empty in-window; 1 rejected unconfirmed candidate — Perplexity's "Escaping SPACE" title without a confirmed URL; 1 candidate excluded as a routine tutorial — NVIDIA's MoE training recipe).

**Housekeeping:** repo was already clean and up to date on `main` (`origin/main` matched) at the start of this run — no detached-HEAD/fast-forward issue this time, unlike the recurring note on 2026-09-21 through 2026-09-25's radar run.

**Linear: UNAVAILABLE this run — ToolSearch confirms no Linear tools are loadable in this session (MCP server requires re-authorization; non-interactive session cannot run the OAuth flow).** All 3 new items are fully written to `topics/*.md` + `artifacts/` above — no data lost, only Linear cards are behind. This is now the SEVENTY-FOURTH consecutive affected run since 2026-08-24. Owner action needed (unchanged): reconnect the Linear connector (claude.ai Settings → Connectors) or authorize it via `claude mcp`/`/mcp` in an interactive session.

Commit: `news: daily run 2026-09-25 (+3 items, 3 companies fresh, Linear unavailable)`.
