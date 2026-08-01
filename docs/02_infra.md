# AI Content Engine — Infrastructure

> Hosting, deployment, configuration, and cost. Assumes `00_overview.md` and `01_technical.md` have been read. This describes a single-user deployment optimized for low cost and simplicity.

## 1. Hosting model

Everything runs in **Docker Compose on one small GCP VM** in `europe-central2` (Warsaw — low latency for the owner and EU data residency). There is **no GPU**: the LLM is an external API call, so the host only runs light Python glue plus a small Postgres. Serverless and managed Postgres (Cloud SQL) are deliberately avoided — for a single user they add moving parts and Cloud SQL cannot scale to zero, so a single always-on VM is both cheaper and simpler.

## 2. The VM

- **Machine type:** start with `e2-small` (2 GB RAM); use `e2-medium` (4 GB) if Postgres + the app want more headroom. No GPU.
- **Region/zone:** `europe-central2` (Warsaw).
- **OS:** Ubuntu LTS, with Docker and the Compose plugin installed.
- **Static external IP:** reserve one (needed for a domain and the Telegram webhook).
- **Firewall:** allow inbound `80` and `443` (Caddy / web) and `22` (SSH, ideally source-restricted). **Do not expose Postgres** — it stays on the internal Compose network only.
- **Disk:** the boot persistent disk holds the Postgres volume; ~20–30 GB is plenty at this scale.

## 3. Containers (Docker Compose)

The web app, the Telegram bot, and the poller are **the same Python image run as three processes** (different commands), plus Postgres and a reverse proxy. Skeleton:

```yaml
services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: content
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - dbdata:/var/lib/postgresql/data
    restart: unless-stopped

  web:                      # editor + admin/status (the one always-on HTTP surface)
    build: .
    command: uvicorn app.web:app --host 0.0.0.0 --port 8000
    env_file: .env
    volumes:
      - ./config.yaml:/app/config.yaml:ro
      - ./content:/app/content:ro
    depends_on: [db]
    restart: unless-stopped

  bot:                      # Telegram triage (Gate 1) + the scheduled digest job and its delivery
    build: .
    command: python -m app.bot
    env_file: .env
    volumes:
      - ./config.yaml:/app/config.yaml:ro
    depends_on: [db]
    restart: unless-stopped

  poller:                   # the researcher, driven by an in-process scheduler
    build: .
    command: python -m app.poller
    env_file: .env
    volumes:
      - ./config.yaml:/app/config.yaml:ro
    depends_on: [db]
    restart: unless-stopped

  proxy:                    # TLS termination + basic auth in front of web
    image: caddy:2
    ports: ["80:80", "443:443"]
    env_file: .env          # WEB_AUTH_USER / WEB_AUTH_HASH for basic_auth
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddydata:/data
    depends_on: [web]
    restart: unless-stopped

volumes:
  dbdata:
  caddydata:
```

- `config.yaml` is mounted **read-only** into the app containers (it is set once and edited by hand). `content/` — the owner-authored voice files (`style_guide.md`, `anti_patterns.md`, `projects/`) — is mounted read-only into `web`, where the editor consumes it; hand-edits land via `git pull`, no rebuild needed.
- The **poller** runs a long-lived process with an in-process scheduler (e.g. APScheduler) firing each source's poll on its cadence. This is simpler than a separate cron container and keeps all logic in one codebase.
- Postgres uses the `pgvector/pgvector` image; on first boot run `CREATE EXTENSION IF NOT EXISTS vector;` and the schema migrations.

## 4. Configuration & secrets

**Configuration** is a single YAML file — `config.yaml` at the repo root, mounted read-only into the app containers — loaded at startup and seeded once (no admin UI — it is static). That file is **authoritative** for the shape: exactly the source types `x_user` / `github` / `rss` / `reddit_sub` / `hn` / `arxiv` and the field names defined in its header — do not invent new ones. Illustrative excerpt (see the real file for the full shape):

```yaml
defaults:
  cadence: 1d                       # fallback if a source sets none

people:                             # followed authors — span X, blog/RSS, GitHub (not just X)
  - name: Simon Willison
    cadence: 1d                     # person's tempo; cascades to their sources
    sources:
      - { type: x_user, handle: simonw }
      - { type: rss,    url: "https://simonwillison.net/atom/everything/" }
      - { type: github, user: simonw }

topics:                             # named groups of sources
  ai:
    sources:
      - { type: reddit_sub, id: LocalLLaMA, listing: hot, cadence: 12h }
      - { type: hn,    listing: best, min_points: 100, match: ["LLM","AI"], cadence: 6h }
      - { type: arxiv, category: cs.LG, cadence: 1d }
    digest: { schedule: "sun 09:00", window: 7d, top_n: 10 }
```

Notes: `cadence` is per-source with a source → person → `defaults.cadence` cascade; X appears only under `people` (topic search via X is not used in v1); a topic's `digest` schedule is a separate dimension from its sources' polling cadence. Exact feed URLs are illustrative — verify at build time.

**Secrets** never go in the YAML or in git. They come from the environment via the Compose `.env` file: `DB_PASSWORD`, the model credentials (see §6), `TELEGRAM_TOKEN`, `TELEGRAM_OWNER_CHAT_ID` (the single allowed chat: the bot accepts commands/callbacks only from it and uses it as the destination for pushed triage and digests), `WEB_AUTH_USER` / `WEB_AUTH_HASH` (basic-auth credentials for the web editor, see §5), `X_BEARER_TOKEN` (X read access is pay-per-use — a developer account with prepaid credits, see §9), `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET` (the OAuth app for the Reddit API; free non-commercial tier), and any other source tokens. The poll **cursors** are *not* config — they persist in the `cursors` table.

## 5. External access & TLS

- The **web editor** is the only inbound HTTP surface. Front it with **Caddy**, which auto-provisions and renews TLS for a domain pointing at the VM's static IP. The editor hosts Gate 2 and the drafts published under the owner's name, so it is **never exposed without auth** — a single basic-auth credential pair is enough for one user:

  ```
  yourdomain.example {
    basic_auth {
      {$WEB_AUTH_USER} {$WEB_AUTH_HASH}
    }
    reverse_proxy web:8000
  }
  ```

  Generate the hash with `caddy hash-password` (e.g. `docker run --rm caddy:2 caddy hash-password --plaintext '...'`) and put both values in `.env` — the Caddyfile stays free of secrets and can live in git. Compose interpolates `.env`, so **double every `$` in the hash to `$$`** when pasting it (Caddy receives the correct single-`$` value); an empty `WEB_AUTH_HASH` makes Caddy refuse to start.

- The **Telegram bot** can use either webhook (requires the public HTTPS endpoint above) or long-polling (no inbound needed). Long-polling is the simpler default for a single user; switch to a webhook only if desired. Either way the bot must ignore updates from any chat other than `TELEGRAM_OWNER_CHAT_ID` — bots are discoverable by username, and Gate 1 approve/skip must not be pressable by strangers.
- If exposing the web app publicly is unwanted, a **Cloudflare Tunnel** or **Tailscale** can reach it privately instead of opening 80/443; then the bot uses long-polling. Either approach is fine.

## 6. Model & embedding transport

Two equivalent options for reaching Claude and the embedding model:

- **Vertex AI (recommended given the GCP host):** run Claude via Vertex Model Garden and use Vertex embeddings (`gemini-embedding-001`, `dim=1536`). Auth via the VM's service account (Application Default Credentials) — **no API key in `.env`**, and everything bills to the one GCP account. Grant the service account Vertex AI permissions. The embedder (poller now; web later) needs ADC at the container's default path: **on the prod VM the attached service account supplies it automatically**; for **local** runs `docker-compose.yml` mounts `~/.config/gcloud` read-only into the poller (after `gcloud auth application-default login`). Set `EMBEDDING_PROVIDER=vertex` + `GOOGLE_CLOUD_PROJECT`/`GOOGLE_CLOUD_LOCATION` in `.env`.
- **Anthropic API directly** for Claude + a separate embedding provider (Vertex or Voyage). Then `ANTHROPIC_API_KEY` (and any embedding key) live in `.env`.

Either way, enable **prompt caching** on the repeated context (style guide, retrieved context, the working draft during iteration) to cut input cost.

## 7. Persistence & backups

- Postgres data lives in the `dbdata` Docker volume on the VM's persistent disk. This is the only stateful piece (config and the style guide are files in the repo / mounted; everything else is reproducible).
- Add a **nightly `pg_dump`** (a small cron on the host or a tiny scheduled job) writing a dump locally and, ideally, to a GCS bucket. Losing the DB means losing the item history, clusters, and the published-article knowledge base, so back it up.

## 8. Deploy & update

1. Provision the VM (Ubuntu + Docker + Compose), reserve the static IP, set firewall rules, point the domain at the IP.
2. Clone the repo, create `.env` (secrets) and `config.yaml` (sources), create the `Caddyfile`.
3. `docker compose up -d --build`. On first run, ensure the `vector` extension and migrations are applied (an entrypoint/migration step in the image).
4. Updates: `git pull && docker compose up -d --build`. The poller and bot restart cleanly; `restart: unless-stopped` brings everything back after a reboot.

## 9. Cost (summary)

- **VM (fixed):** small e2 in Warsaw ≈ $15–25/month on-demand; a 1-year committed-use discount cuts it substantially (closer to $8–12). Plus a small disk (~$3).
- **Models (variable):** depends on writing/iteration volume; roughly $10–20/month on Sonnet 4.6 at expected usage, less with prompt caching, a bit more if drafting on Opus.
- **X API (variable):** read access is pay-per-use only (prepaid credits; the free read tier closed in early 2026) — roughly $2–5/month for ~4 followed accounts at a 1–3d cadence with `since_id` cursors. Reddit's API tier is free for non-commercial use.
- **Embeddings:** negligible (~$1/month).
- **Total:** roughly **$25–50/month**, dominated by the VM and writing volume. Verify exact VM pricing in the GCP calculator for the chosen machine and region.
