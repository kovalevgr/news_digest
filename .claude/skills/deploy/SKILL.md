---
name: deploy
description: Owner-run runbook for deploying and updating the system on the GCP VM — provisioning, first deploy, updates, backup and reboot checks. Side-effectful; invoked manually.
disable-model-invocation: true
---

# Deploy runbook (GCP VM + Docker Compose) — see docs/02_infra.md §8

## First deploy

1. **VM:** Ubuntu LTS on `e2-small`, `europe-central2`, reserved static IP, firewall: 80/443 open, 22 source-restricted. Install Docker + compose plugin. Point the domain at the IP.
2. **Clone the repo.** Create `.env` with: `DB_PASSWORD`, `TELEGRAM_TOKEN`, `TELEGRAM_OWNER_CHAT_ID`, `WEB_AUTH_USER`, `WEB_AUTH_HASH` (generate: `docker run --rm caddy:2 caddy hash-password --plaintext '...'`; double every `$` to `$$` in `.env`, and never leave it empty or Caddy refuses to start), `X_BEARER_TOKEN`, `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, model credentials (skip if using Vertex ADC via the VM service account — then grant it Vertex AI permissions instead). Confirm `Caddyfile` domain matches.
3. `docker compose up -d --build` — the one-shot `migrate` service applies `CREATE EXTENSION vector` + Alembic migrations before `web`/`bot`/`poller` start.
4. **Verify:**
   - `https://<domain>` without creds → 401; with creds → editor loads.
   - Bot answers the owner chat; a message from another account is ignored.
   - Poller logs show per-source polls; `docker compose ps` → all 5 services up.

## Update

```
git pull && docker compose up -d --build
```
Poller and bot restart cleanly; nothing else needed.

## Backups

- Nightly `pg_dump` via host cron → local file + GCS bucket.
- Check: newest dump < 24h old. Quarterly: test-restore into a scratch database.
- The DB is the only stateful piece (item history, clusters, the published-article KB) — losing it loses the knowledge base.

## Reboot test

`sudo reboot` → after boot, all services return via `restart: unless-stopped`; re-run the Verify list above.
