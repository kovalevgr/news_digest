---
name: config-edit
description: Add or modify people, topics, or sources in config.yaml (the authoritative runtime config). Use whenever the owner wants to follow a new person, add/remove a source or topic, change cadences, or adjust digest schedules.
---

# Editing config.yaml

`config.yaml` (repo root) is the single static config: WHO/WHAT to poll and WHEN. It is **authoritative** — exactly six source types with exact field names (see the file header). Sources/people/topics live only here, never in the DB. Secrets never go here (env only).

## Procedure

1. Read the current `config.yaml` and its header (the header is the spec).
2. Make the minimal edit:
   - **New person** → entry under `people:`: `name`, optional `cadence` (their tempo; cascades to their sources), `sources` list.
   - **New topic source** → under `topics.<name>.sources`. New topic → a new mapping key under `topics:`.
   - **Allowed types & fields:** `x_user{handle}` · `github{user}` · `rss{url}` · `reddit_sub{id, listing: top|hot|new, window?: hour|day|week|month|year}` · `hn{listing: best|top|new, min_points?: int, match?: [keywords]}` · `arxiv{category}`. Any source may add `cadence` (e.g. `6h`, `12h`, `1d`, `2d`).
   - **Cadence** = how often we CHECK (freshness need + cost), not how often the author posts. Cascade: source → person → `defaults.cadence`.
   - **Topic digest:** `digest: { schedule: "sun 09:00", window: 7d, top_n: 10 }`.
3. Validate: `python3 .claude/skills/config-edit/validate_config.py config.yaml` — must print OK. (The same validator runs automatically as a PostToolUse hook on every edit of `config.yaml`.)
4. Tell the owner the cursor consequences: changing a source's **identity fields** resets its poll cursor (by design — safe, re-polling is idempotent); changing only `cadence` keeps the cursor.

## Never

- Invent a new source type or field. A new type is a feature, not a config edit: it needs an adapter module, the config header update, and a docs sync first.
- Put tokens/secrets/passwords in this file — env only.
- Add `x_user` sources under `topics` (X is people-only in v1).
