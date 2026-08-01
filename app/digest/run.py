"""The weekly digest — a scheduled QUERY over the rolling store + ONE single-shot summarize
(docs/01_technical.md §2.5, §3; build plan Phase 6).

This is deterministic code plus exactly ONE model call. It is NOT an agent and NOT a fresh poll
(hard rule: "Digest is a scheduled query over the rolling store run by the bot ... not a fresh
poll", "One agent only: the writer/editor"). The job runs in the bot process at each topic's
configured `digest.schedule`; it reads clusters/items the researcher already built incrementally
during polling, picks the window's top-N still-uncovered stories, and asks the model once for a
dense awareness rollup.

Stage coordination is Postgres-only: this reads `clusters`/`items` and writes one `digest`
`articles` row plus its `article_clusters` links. It calls no other stage (poller/bot/researcher)
and it NEVER publishes (hard rule 1) — the rollup is text the owner reads in Telegram and can take
through the editor; nothing is posted anywhere.

The dual-purpose digest article (docs §2.5): `run_digest` creates the `digest` article UP FRONT
and links EVERY selected cluster via `article_clusters`. That linkage is the persistent
"covered" marker — the very thing a future run filters on (see `select_digest_clusters`) — so the
article + links are created even if the owner never drafts the post. From that single artifact:
(a) the bot delivers the dense `current_draft` to the owner for awareness, and (b) the owner can
take the same article through the editor like any other piece (it is created at status
`'drafting'` for exactly that reason).

Why the linkage is the repeat-preventer: a topic's window is typically longer than its schedule
interval (e.g. a 14d window on a weekly schedule), so consecutive runs re-scan the overlap. If
"already covered" weren't filtered out, the overlap would resurface the same stories every run.
Excluding any cluster already linked to ANY article — a hot-news piece OR a previous digest —
means each story appears in at most one rollup. A Gate-1 `skipped` cluster STAYS eligible: skip
means "no standalone post", not "omit from the weekly awareness rollup" (docs §2.5).

Two layers, split so the model boundary is unit-testable without a DB or network (mirrors
app.researcher.triage):

  - parse_digest_schedule / build_digest_prompt / summarize_digest — PURE prompt + schedule
    work and the ONE model call (with a module-level `generate` monkeypatch seam).
  - select_digest_clusters / run_digest — the DB path: the windowed, covered-marker-filtered,
    score-ranked query, and the create-article-+-link transaction.

Grounding contract (HARD RULE 2 — mirrors triage's posture): the rollup summarizes each story
strictly from that cluster's PASS-1 metadata — its `triage_title`/`triage_summary` if present,
else its item titles — and carries each story's provenance URL. No pass-2 `full_text` is assumed
(digest clusters needn't be Gate-1 approved). The prompt forbids inventing facts, numbers, or
opinions; nothing here fabricates content of its own.

Model swappable: the one summarize call uses a logical ROLE via digest_role() (default
"generation") — NEVER a hardcoded model id (the role->model map lives in config).

Config is a file: the window / top_n / schedule come from the passed `app.config.Digest` object
(loaded from config.yaml); nothing config-shaped is read from or written to the DB. The per-run
formatting knobs (role, max chars, title limit) are env-overridable accessors with inline
justification — one place to tune without touching the DB path.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy import nullslast, select

from app.db.models import Article, ArticleCluster, Cluster, Item as ItemModel
from app.editor.article import _ensure_genesis, new_article_id
from app.llm import generate  # module-level import = the summarize monkeypatch seam

log = logging.getLogger("digest.run")

# --- Formatting / model knobs (env-overridable; one place to tune the rollup) ---------------
#
# The logical role for the summarize call. "generation" (not "cheap"): the rollup is the owner's
# weekly awareness artifact AND the seed draft they may take through the editor, so it is worth
# the better model. A logical role only — NEVER a model id (the role->model map lives in config).
DEFAULT_DIGEST_ROLE = "generation"

# Hard cap on the rollup length. A digest covers top-N stories at a line or two each; 20k chars
# is generous vs that and bounds the worst case (a runaway reply can't bloat the row or the
# Telegram delivery). A safety bound, not a display rule — no ellipsis on truncation.
DEFAULT_DIGEST_MAX_CHARS = 20000

# How many of a cluster's item titles to feed the model when it has no triage summary. A few
# headlines give plenty of grounding without ballooning the prompt; oldest-first so the
# representative set is stable run-to-run (mirrors triage's title limit).
DEFAULT_DIGEST_TITLE_LIMIT = 5

# Per-field display caps inside the prompt so one pathological cluster can't dominate the prompt.
# Generous vs a real headline / blurb; they bound the worst case, not the normal case.
_PROMPT_TITLE_CAP = 300
_PROMPT_SUMMARY_CAP = 1500


def digest_role() -> str:
    """The logical role for the summarize call (env DIGEST_ROLE). A blank override falls back to
    the default so we never pass an empty role into the role->model map. NEVER a model id."""
    raw = os.environ.get("DIGEST_ROLE")
    if raw is None or not raw.strip():
        return DEFAULT_DIGEST_ROLE
    return raw.strip()


def digest_max_chars() -> int:
    """Max chars of the rollup we keep (env DIGEST_MAX_CHARS). Falls back on
    absence/garbage/non-positive — a 0/negative cap would discard the whole rollup."""
    raw = os.environ.get("DIGEST_MAX_CHARS")
    if raw is None:
        return DEFAULT_DIGEST_MAX_CHARS
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad DIGEST_MAX_CHARS=%r — falling back to %s", raw, DEFAULT_DIGEST_MAX_CHARS)
        return DEFAULT_DIGEST_MAX_CHARS
    return val if val > 0 else DEFAULT_DIGEST_MAX_CHARS


def digest_title_limit() -> int:
    """Max item titles fed per cluster as the grounding fallback (env DIGEST_TITLE_LIMIT). Falls
    back on absence/garbage/non-positive — we always feed at least the default number."""
    raw = os.environ.get("DIGEST_TITLE_LIMIT")
    if raw is None:
        return DEFAULT_DIGEST_TITLE_LIMIT
    try:
        val = int(raw)
    except ValueError:
        log.warning(
            "bad DIGEST_TITLE_LIMIT=%r — falling back to %s", raw, DEFAULT_DIGEST_TITLE_LIMIT
        )
        return DEFAULT_DIGEST_TITLE_LIMIT
    return val if val > 0 else DEFAULT_DIGEST_TITLE_LIMIT


# --- detached result shapes (primitives only — safe to return past the session) -------------


@dataclass
class DigestCluster:
    """One selected story's pass-1 metadata + provenance, detached from the ORM so the pure
    summarize layer (and any caller) never touches a live session. `summary` is "" when the
    cluster has no triage summary; the prompt then leans on `title` (a real headline)."""
    cluster_id: str
    title: str
    summary: str
    url: str
    score: float | None


@dataclass
class DigestResult:
    """The outcome of a digest run, primitives only (detached from the ORM) so it survives past
    the session and across the Postgres-only seam to the bot. `cluster_ids` is exactly the set
    linked via article_clusters this run — the covered-marker the next run filters on."""
    topic: str
    article_id: str
    cluster_ids: list
    rollup: str


# --- pure: schedule + prompt ----------------------------------------------------------------


def parse_digest_schedule(schedule: str) -> dict:
    """Parse a config `digest.schedule` ("sun 09:00") into APScheduler CronTrigger kwargs.

    PURE — no DB, no network. Returns the day/hour/minute shape a CronTrigger takes:
    `"sun 09:00"` -> `{"day_of_week": "sun", "hour": 9, "minute": 0}`. Tolerant of a single-digit
    hour (`"mon 9:05"` -> hour 9, minute 5) and surrounding whitespace.

    config.yaml already validates the schedule shape (app.config.SCHEDULE_RE + range checks), so
    this is a defensive guard, not the primary validator: it raises ValueError on a clearly
    malformed string (bad day, missing time, out-of-range hour/minute) rather than silently
    handing APScheduler garbage. The day-of-week tokens match config's lowercase set."""
    if not isinstance(schedule, str):
        raise ValueError(f"digest schedule must be a string, got {schedule!r}")
    parts = schedule.strip().split()
    if len(parts) != 2:
        raise ValueError(f"bad digest schedule {schedule!r} (expected like 'sun 09:00')")
    day, hhmm = parts[0].lower(), parts[1]
    if day not in {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}:
        raise ValueError(f"bad digest schedule {schedule!r}: unknown day-of-week {day!r}")
    if ":" not in hhmm:
        raise ValueError(f"bad digest schedule {schedule!r}: time must look like '09:00'")
    h_str, m_str = hhmm.split(":", 1)
    try:
        hour, minute = int(h_str), int(m_str)
    except ValueError:
        raise ValueError(f"bad digest schedule {schedule!r}: non-numeric time")
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"bad digest schedule {schedule!r}: hour/minute out of range")
    return {"day_of_week": day, "hour": hour, "minute": minute}


def _cap(text: str, limit: int) -> str:
    """Truncate to `limit` chars (no ellipsis — the cap is a safety bound, not a display rule)."""
    return text if len(text) <= limit else text[:limit]


def build_digest_prompt(topic: str, clusters: list) -> str:
    """Assemble the single-shot digest prompt (PURE — no DB, no network).

    The model sees ONLY each story's pass-1 metadata (title, optional triage summary, provenance
    URL) and is asked for a dense, scannable markdown rollup: one short entry per story — its
    title, a one-line grounded "what it is", and its source link. The grounding rules are explicit
    and mirror triage's posture (hard rule 2): use ONLY the provided per-cluster metadata, invent
    no facts/numbers/opinions, keep each entry short. The header names the topic's weekly digest
    so the rollup reads as a coherent artifact."""
    title_topic = topic.strip() or "Tech"
    lines: list[str] = []
    for i, c in enumerate(clusters, start=1):
        title = _cap((c.title or "").strip() or "(untitled)", _PROMPT_TITLE_CAP)
        summary = _cap((c.summary or "").strip(), _PROMPT_SUMMARY_CAP)
        url = (c.url or "").strip() or "(no link)"
        lines.append(f"{i}. TITLE: {title}")
        if summary:
            lines.append(f"   SUMMARY: {summary}")
        lines.append(f"   SOURCE: {url}")
    story_block = "\n".join(lines) if lines else "(no stories)"
    return (
        "You are writing a weekly awareness digest for a personal tech-news pipeline. The owner "
        f"reads it to catch up on the week's {title_topic} stories at a glance.\n\n"
        f"Write a dense, scannable markdown rollup titled as the weekly {title_topic} digest. "
        "Produce ONE short entry per story below, in the given order. Each entry is:\n"
        "  - the story's title as a bullet heading,\n"
        "  - a single plain sentence on what it is, grounded in the provided title/summary,\n"
        "  - the provenance link (its SOURCE url) so the owner can read more.\n\n"
        "Hard grounding rules: use ONLY the per-story metadata provided below. Do NOT invent "
        "facts, numbers, names, or details that are not in it, and do NOT add opinions or takes — "
        "the owner forms the opinion. If a story's metadata is thin, keep its entry to one short "
        "line rather than padding it. Carry every story's SOURCE link through into the rollup.\n\n"
        "Stories (pass-1 metadata only):\n"
        f"{story_block}\n"
    )


def summarize_digest(topic: str, clusters: list) -> str:
    """The ONE model call: build the prompt, call generate(role=digest_role()), cap the reply.

    Factored out (topic + detached clusters in, capped markdown out) so the model boundary is a
    single seam shared by run_digest and any future caller, and so tests can monkeypatch the
    module-level `generate`. Returns "" when there are no clusters (nothing to ground a rollup in
    — we never call the model on an empty set; run_digest short-circuits before reaching here, so
    this guard is belt-and-suspenders). The role is logical (digest_role()), never a model id; the
    output is capped at digest_max_chars() so a runaway reply can't bloat the article row or the
    Telegram delivery."""
    if not clusters:
        return ""
    reply = generate(
        messages=[{"role": "user", "content": build_digest_prompt(topic, clusters)}],
        role=digest_role(),
    )
    return _cap((reply or "").strip(), digest_max_chars())


# --- DB path --------------------------------------------------------------------------------


def _cluster_provenance(session, cluster_id: str, *, limit: int) -> tuple[list[str], str]:
    """A cluster's pass-1 item titles (oldest-first, capped at `limit`) and a representative URL.

    PASS-1 metadata only — `title`/`url`, never `full_text` (full_text is post-approval pass-2 and
    is not the digest grounding set; digest clusters needn't be Gate-1 approved). The first item's
    url is the provenance link for the story. Mirrors triage._cluster_titles' stable oldest-first
    ordering so the representative set is deterministic run-to-run."""
    rows = session.execute(
        select(ItemModel.title, ItemModel.url)
        .where(ItemModel.cluster_id == cluster_id)
        .order_by(ItemModel.fetched_at.asc(), ItemModel.id.asc())
        .limit(limit)
    ).all()
    titles = [t.strip() for (t, _u) in rows if t and t.strip()]
    url = next((u.strip() for (_t, u) in rows if u and u.strip()), "")
    return titles, url


def select_digest_clusters(
    session, topic: str, *, window_days: int, top_n: int, now=None
) -> list:
    """The window's top-N still-uncovered clusters for `topic`, best first (docs §2.5).

    Filters, in order:
      - Rolling window: created_at >= (now or utcnow()) - window_days days. A topic's window is
        typically longer than its schedule interval, so consecutive runs deliberately re-scan the
        overlap; the covered-marker (below) is what stops repeats.
      - Topic match: Cluster.topic == topic.
      - COVERED-MARKER exclusion: drop any cluster already linked to ANY article via
        article_clusters — covered by a hot-news piece OR a previous digest. This is THE
        repeat-preventer (docs §2.5): NOT IN (SELECT cluster_id FROM article_clusters). With an
        overlapping window, "already covered" must be filtered out, not merely re-ranked.

    NO status filter beyond the covered-marker: new/sent/approved AND skipped are all eligible. A
    Gate-1 `skipped` cluster stays in the rollup — skip means "no standalone post", not "omit from
    the weekly awareness rollup" (docs §2.5). Only the article_clusters linkage excludes.

    Ordering: score DESC with NULLs last (an unranked cluster sorts after every ranked one rather
    than jumping the queue), then created_at ASC, then id ASC, so equal-score clusters order
    deterministically; LIMIT top_n.

    For each selected cluster gathers its pass-1 metadata into a detached DigestCluster: `title`
    = triage_title else the first item title else "(untitled)"; `summary` = triage_summary else
    ""; `url` = the first item's url (provenance); `score`. One extra query per cluster for the
    titles/url (oldest-first, capped at digest_title_limit()) — mirrors triage's per-cluster
    title gather. Reads only; writes nothing."""
    cutoff = (now or datetime.now(timezone.utc)) - timedelta(days=window_days)
    title_limit = digest_title_limit()

    covered = select(ArticleCluster.cluster_id)
    rows = session.execute(
        select(
            Cluster.id,
            Cluster.triage_title,
            Cluster.triage_summary,
            Cluster.score,
        )
        .where(Cluster.topic == topic)
        .where(Cluster.created_at >= cutoff)
        .where(Cluster.id.notin_(covered))
        .order_by(
            nullslast(Cluster.score.desc()),
            Cluster.created_at.asc(),
            Cluster.id.asc(),
        )
        .limit(top_n)
    ).all()

    selected: list[DigestCluster] = []
    for cid, triage_title, triage_summary, score in rows:
        titles, url = _cluster_provenance(session, cid, limit=title_limit)
        title = (triage_title or "").strip() or (titles[0] if titles else "") or "(untitled)"
        summary = (triage_summary or "").strip()
        selected.append(
            DigestCluster(cluster_id=cid, title=title, summary=summary, url=url, score=score)
        )
    return selected


def run_digest(session, topic: str, digest_cfg) -> DigestResult | None:
    """Run one topic's digest: select → summarize → create the digest article + cluster links.

    `digest_cfg` is an app.config.Digest (its `.window_days`/`.top_n`/`.schedule` come from
    config.yaml — config is a file, not the DB). Steps:

      1. select_digest_clusters with the config window/top_n (the windowed, covered-marker-
         filtered, score-ranked query).
      2. If NO eligible clusters → log + return None. We never create an empty digest article: an
         empty article would be a covered-marker for nothing and clutter the editor's queue.
      3. summarize_digest — the ONE model call — into the dense rollup markdown.
      4. Create one `articles` row: id=new_article_id() (reusing the editor's opaque `a:` id mint),
         piece_type="digest", status="drafting", current_draft=rollup. Status `'drafting'` (not
         `approved`) so the owner can take it through the editor like any article (docs §2.5).
      5. Link EVERY selected cluster via article_clusters. THIS linkage is the persistent
         "covered" marker — the exact thing the NEXT run's select_digest_clusters filters out — so
         a story summarized this week never resurfaces in next week's overlapping window. The
         article + links are created UP FRONT (before any drafting), so the covered-marker exists
         even if the owner never drafts the post.
      6. Commit and return a DigestResult (primitives only, detached from the ORM) so the result
         survives past the session and crosses the Postgres-only seam to the bot, which delivers
         the dense `rollup` to Telegram.

    Coordinates only through Postgres: reads clusters/items, writes the article + join rows. Calls
    no other stage (poller/bot/researcher) and NEVER publishes (hard rule 1) — the rollup is text
    for the owner to read and optionally draft; nothing is posted anywhere.
    """
    clusters = select_digest_clusters(
        session, topic, window_days=digest_cfg.window_days, top_n=digest_cfg.top_n
    )
    if not clusters:
        log.info("digest[%s]: no eligible clusters in the window — no digest article created", topic)
        return None

    rollup = summarize_digest(topic, clusters)

    article_id = new_article_id()
    session.add(
        Article(
            id=article_id,
            piece_type="digest",
            status="drafting",
            current_draft=rollup,
        )
    )
    cluster_ids = [c.cluster_id for c in clusters]
    for cid in cluster_ids:
        session.add(ArticleCluster(article_id=article_id, cluster_id=cid))
    session.commit()

    # Anchor the digest article's version trail (Feature A): record the rollup as the genesis
    # edit_log row so the digest piece has the same version history any drafted piece does (the
    # owner can take it through the editor). IFF no edit_log rows yet — idempotent on a re-run.
    if _ensure_genesis(session, article_id, rollup):
        session.commit()

    log.info(
        "digest[%s]: created article %s covering %d cluster(s) (linked as the covered-marker)",
        topic, article_id, len(cluster_ids),
    )
    return DigestResult(
        topic=topic, article_id=article_id, cluster_ids=cluster_ids, rollup=rollup
    )


__all__ = [
    "DEFAULT_DIGEST_ROLE",
    "DEFAULT_DIGEST_MAX_CHARS",
    "DEFAULT_DIGEST_TITLE_LIMIT",
    "digest_role",
    "digest_max_chars",
    "digest_title_limit",
    "DigestCluster",
    "DigestResult",
    "parse_digest_schedule",
    "build_digest_prompt",
    "summarize_digest",
    "select_digest_clusters",
    "run_digest",
]
