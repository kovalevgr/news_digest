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
