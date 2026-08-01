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
