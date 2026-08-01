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
