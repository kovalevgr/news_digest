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
