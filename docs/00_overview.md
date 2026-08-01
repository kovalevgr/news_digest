# AI Content Engine — Overview

> Context document for the implementing agent. Read this first. It defines *what* we are building and the *principles* that must not be violated. The *how* lives in `01_technical.md`, `02_infra.md`, and `03_build_plan.md`.

## Purpose

A personal, non-commercial system that helps a single user (the **owner**) grow their AI/IT personal brand. It continuously researches top tech news, drafts commentary in the owner's voice grounded in the source material, and produces platform-ready variants for LinkedIn, Medium, and Reddit. The owner publishes **manually** — the system never posts on its own.

## Who it is for

A single user. This is not a product: no multi-tenancy, no other users, no SLA, no concurrency to speak of. Optimize every decision for **simplicity, low running cost, and owner-in-the-loop review** — not for scale, throughput, or fault tolerance. When two designs are equally correct, pick the simpler one.

## The pipeline at a glance

1. **Researcher** — polls configured sources on a schedule, normalizes each finding into an item, deduplicates items into clusters (one cluster = one story across many sources), and ranks the clusters.
2. **Gate 1 — triage** — the owner approves or skips a *story* in Telegram, shown as a title plus a short summary.
3. **Editor** — for an approved story, drafts a single canonical long-read in the owner's voice, grounded in the sources; the owner then iterates it through real-time chat in a web app.
4. **Gate 2 — final approval** — the owner approves the canonical draft.
5. **Variants** — per-platform versions are generated on demand from the canonical (LinkedIn / Medium / Reddit).
6. **Manual publish** — the owner copies the variant and posts it themselves.

## Architectural stance (this drives the implementation)

- **It is not a multi-agent system.** It is a staged pipeline whose stages coordinate through a single Postgres database. Stages never message each other directly; each writes its state and output to Postgres, and the next stage reads it.
- **Exactly one agentic component: the writer/editor** (the draft + iterate phases). It runs in a loop with a small set of on-demand tools (knowledge-base search, fetch a source, optional web search). Everything else is a single-shot model call: input → structured output, no loop, no tools. That includes triage summaries, topic classification, and variant formatting.
- **The researcher is deterministic code** that occasionally calls a model (embedding for dedup, an optional classifier for ambiguous items, a summary per top cluster). It is not an agent; its control flow is fixed in code.

A practical rule for the implementer when deciding how to build a step: use an **agent** only when the step needs a loop, tool use / fetching information, or reaction to a back-and-forth with the owner. Otherwise it is a **single model call**.

## Non-negotiables

- **Publishing is always manual.** The system produces text and per-platform formatting only. It must never post anywhere and must not integrate any auto-posting/publishing API. This eliminates account-ban and automation risk by design.
- **Grounded drafting.** The owner's name goes on the output. The drafter must stick to the source material, carry provenance links through to the draft, and explicitly flag any uncertain or unverifiable claim for the owner to check. It must not inject outside facts. Opinions and takes belong to the owner — the agent may *propose* a position, but the owner approves or edits it; the agent never puts judgements in the owner's mouth.
- **Postgres + pgvector is the single source of truth** and the coordination bus for the whole pipeline.
- **Configuration lives in a file.** Which people/sources/topics to follow, their cadences, and digest schedules are defined in a YAML file loaded at startup — *not* stored as database tables. The only mutable state persisted for polling is per-source cursors. Secrets (API keys, tokens) come from the environment, never from the config file.
- **The generative model is swappable** behind a thin abstraction. No step should hardcode a specific model; the step declares its needs and the model is configured.

## Hosting & cost (summary — see `02_infra.md`)

Everything runs in Docker Compose on a single small GCP VM in `europe-central2` (Warsaw). No GPU — the LLM is an external API (Anthropic API or Claude via Vertex). Expected total cost roughly **$25–50/month**: the VM is the main fixed cost, per-token model usage is the variable part, X API reads add a few dollars (pay-per-use), and embeddings are negligible.

## Out of scope / deferred (do not build in v1)

These are explicitly parked, not forgotten:

- Automatic publishing of any kind.
- A rich drag-and-drop "constructor" editor (the v1 editor is a lean chat + live preview).
- Image generation for posts.
- A Notion-based read-only library of finished pieces.
- YouTube and Bluesky source adapters.
- Distilling the edit log back into the style guide. The signal is captured in `edit_log` from day one; the periodic distillation step (manual, or a single-shot model call the owner triggers) comes later.

Deferred *technical* decisions (dedup similarity threshold, the topic-tagging classifier, paywall/JS-page extraction, exact feed-URL verification) are tracked in `03_build_plan.md` so the agent knows what is intentionally unspecified versus what is settled.

## Document map

- `00_overview.md` — this document: context and principles.
- `01_technical.md` — architecture, components, data model, and the LLM/agent specification.
- `02_infra.md` — hosting, Docker Compose, deployment, configuration, and secrets.
- `03_build_plan.md` — phased implementation plan and the open technical decisions.
- `config.yaml` (repo root, not in `docs/`) — the **authoritative** source/people/topic configuration: the runtime file itself, mounted read-only into the containers.
- `CLAUDE.md` — entry point for the implementing agent: conventions and pointers to the above.
