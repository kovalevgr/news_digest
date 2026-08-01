---
name: phase-check
description: Verify the current build phase's Done criteria before declaring a phase complete. Use when finishing a phase slice, when the owner asks whether a phase is done, or before starting the next phase.
---

# Phase Done verification

Source of truth: `docs/03_build_plan.md` (phases + Done criteria — re-read it, the list below is the executable digest). Determine the current phase from repo state, run that phase's checks, and report a pass/fail list with evidence. A phase is NOT done while any item fails.

DB checks run via: `docker compose exec db psql -U app -d content -c "..."`

## Phase 0 — Foundation
- `docker compose up -d --build` → all 5 services up (`docker compose ps`).
- `\dx` shows `vector`; `\dt` shows all 8 tables (`items`, `sightings`, `clusters`, `articles`, `article_clusters`, `edit_log`, `variants`, `cursors`).
- Trivial `generate` + `embed` round-trip works through `app/llm` roles (no hardcoded model anywhere).
- Config loads: `python3 .claude/skills/config-edit/validate_config.py config.yaml` → OK, and the app boots with it.
- Caddy fronts web with basic auth: `curl -s -o /dev/null -w '%{http_code}'` without creds → 401, with creds → 200.

## Phase 1 — Researcher
- Poller pulls real configured sources on cadence (logs show per-source polls).
- Items land; the same URL from two sources → **1 item, 2 sightings**:
  `SELECT item_id, count(*) FROM sightings GROUP BY item_id HAVING count(*) > 1 LIMIT 5;`
- Clusters form, carry a topic, get a blended score; cursors advance between two consecutive runs.

## Phase 2 — Triage (Gate 1)
- Top clusters get `triage_title`/`triage_summary` (written by the poller).
- Bot delivers each to the owner chat **exactly once** — restart both bot and poller, confirm nothing is re-sent (`status='sent'` flow).
- Approve → `approved` + pass-2 `full_text` fetched for the cluster's items; skip → `skipped`.
- Messages from any non-owner chat are ignored.

## Phase 3 — Editor: draft
- Approving a story yields a grounded canonical long-read in the web app.
- The assembled draft context demonstrably includes `content/style_guide.md` rules.
- Provenance links present in the draft; unverified claims flagged.

## Phase 4 — Editor: iterate + Gate 2
- A chat instruction edits the draft in place (no full regeneration); a manual hand-edit survives the next instruction.
- Every instruction lands in `edit_log`.
- Gate 2 → `articles.status = 'pre_publish'`.

## Phase 5 — Variants
- Per-platform variant generated on demand and stored in `variants`.
- Mark-as-published → `SELECT id, status, embedding IS NOT NULL FROM articles WHERE status='published';` → true.
- The published article is retrievable via `kb_search` when drafting the next piece.

## Phase 6 — Digest
- Digest delivered to Telegram per schedule; the `digest` article exists with clusters linked via `article_clusters`.
- Two consecutive runs over overlapping windows (e.g. 14d window, weekly) repeat **no** story.

## Phase 7 — Hardening & deploy
- See `/deploy` for the runbook. Verify: editor unreachable without auth; bot ignores strangers; nightly `pg_dump` exists and is < 24h old; reboot → all services return.
