"""Triage summaries — the researcher's last step before Gate 1 (docs/01_technical.md §2.1;
build plan Phase 2).

After dedup/classify/rank have produced ranked clusters, this stage gives the highest-ranked
NEW clusters a phone-sized headline + blurb so the bot can deliver an at-a-glance triage card.
It is a SINGLE-SHOT model call per cluster — NOT an agent (docs: "Triage summaries ... are
single-shot model calls"; the one agent is the future writer). The model gets only the
cluster's own item headlines and is told to stay strictly grounded in them; it writes
`clusters.triage_title` / `triage_summary` and nothing else — it never advances status (the
bot does that at Gate 1).

Pipeline position: this is stage 4 of run_process (embed_and_cluster -> classify -> rank ->
TRIAGE). It coordinates with the bot purely through Postgres: the poller writes triage_*, the
bot polls for summarized-but-unsent clusters. The stages never call each other.

Two layers, split so the model boundary is unit-testable without a DB or network:

  - build_triage_prompt / parse_triage_reply — PURE. Prompt assembly and a tolerant parse of
    the model's `TITLE:` / `SUMMARY:` reply. Tested directly (tests/test_triage.py).
  - select_triage_candidates / summarize_pending_triage — the DB path: pick the top NEW,
    un-summarized clusters by score and write each one's summary, idempotently and without
    ever overwriting or touching a cluster the bot has already moved on.

Grounding contract (HARD RULE — docs: "Triage summary grounded ONLY in the cluster's own item
titles — never invent facts/opinions"): the ONLY input to the model is the cluster's pass-1
item titles (never full_text — that is pass-2, post-approval). The prompt forbids inventing
facts or opinions; the parser carries the model's words through verbatim (capped), inventing
nothing of its own.

Determinism / safety contract:
  - NEW + un-summarized ONLY: selection requires status=='new' AND triage_summary IS NULL, so
    a sent/approved/skipped cluster is never reconsidered, and an existing summary is never
    re-generated.
  - WRITE-GUARDED: persisting is a single guarded conditional UPDATE that re-confirms
    status=='new' AND triage_summary IS NULL atomically in SQL (the WHERE clause) — so a bot
    decision that landed mid-pass matches 0 rows and is never clobbered, even inside the
    poller's long-lived session where a Python read would hit the stale identity-map cache.
  - IDEMPOTENT: a run that summarizes a cluster removes it from the next run's candidate set;
    a second pass over unchanged data summarizes nothing new.
  - MODEL SWAPPABLE: the one generate() call uses a logical ROLE via triage_role() (default
    "generation") — never a hardcoded model id.

Selection knobs (top-N / min-score / per-pass cap) are an intentionally-OPEN decision
(docs/03_build_plan.md "Triage selection & delivery rule"): they live here as env-overridable
accessors with inline justification, so tuning the gate never means touching the DB path.
"""
from __future__ import annotations

import logging
import os

from sqlalchemy import nullslast, select, update

from app.db.models import Cluster, Item as ItemModel
from app.llm import generate

log = logging.getLogger("researcher.triage")

# --- Selection / formatting knobs (an intentionally-open decision — one place to tune) -----
#
# How many clusters get a triage summary per pass. A single user can only act on a handful of
# stories at a time, and each summary is a model call, so we cap the highest-ranked NEW
# clusters rather than summarizing the whole backlog every pass. Default 8 — a comfortable
# phone-screen batch that keeps a steady trickle of the best stories flowing to Gate 1.
DEFAULT_TRIAGE_TOP_N = 8

# Optional score floor: skip clusters whose blended score is below this (and any NULL-score
# cluster — an unranked cluster has no business jumping the triage queue). Default OFF (None):
# with a small single-user store we'd rather summarize a thin story than silently drop it; the
# floor exists for when real data shows the long tail isn't worth a card.
DEFAULT_TRIAGE_MIN_SCORE: float | None = None

# The logical role for the triage call. "generation" (not "cheap"): the triage blurb is the
# owner's first-glance signal for whether to spend effort on a story, so it's worth the better
# model. A logical role only — NEVER a model id (the role->model map lives in config).
DEFAULT_TRIAGE_ROLE = "generation"

# How many of a cluster's item titles to feed the model. A cluster is one story; a few of its
# headlines give plenty of grounding without ballooning the prompt. Oldest-first so the
# representative set is stable run-to-run.
DEFAULT_TRIAGE_TITLE_LIMIT = 6

# Output caps so a runaway reply can't bloat a row or a Telegram card. Generous vs a real
# headline/blurb; they bound the worst case, not the normal case.
_TITLE_CAP = 200
_SUMMARY_CAP = 1500

# Reply markers the model is asked to use and the parser prefers. Case-insensitive on parse.
_TITLE_MARKER = "TITLE:"
_SUMMARY_MARKER = "SUMMARY:"


def triage_top_n() -> int:
    """Max clusters summarized per pass (env TRIAGE_TOP_N). Falls back to the default on
    absence/garbage/non-positive — a 0/negative cap would silently stall triage."""
    raw = os.environ.get("TRIAGE_TOP_N")
    if raw is None:
        return DEFAULT_TRIAGE_TOP_N
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad TRIAGE_TOP_N=%r — falling back to %s", raw, DEFAULT_TRIAGE_TOP_N)
        return DEFAULT_TRIAGE_TOP_N
    return val if val > 0 else DEFAULT_TRIAGE_TOP_N


def triage_min_score() -> float | None:
    """Optional score floor for triage candidates (env TRIAGE_MIN_SCORE). Returns None when
    unset (the default — no floor) or on garbage, so a typo never silently filters the queue."""
    raw = os.environ.get("TRIAGE_MIN_SCORE")
    if raw is None:
        return DEFAULT_TRIAGE_MIN_SCORE
    try:
        return float(raw)
    except ValueError:
        log.warning("bad TRIAGE_MIN_SCORE=%r — falling back to %s", raw, DEFAULT_TRIAGE_MIN_SCORE)
        return DEFAULT_TRIAGE_MIN_SCORE


def triage_role() -> str:
    """The logical role for the triage call (env TRIAGE_ROLE). A blank override falls back to
    the default so we never pass an empty role into the role->model map. NEVER a model id."""
    raw = os.environ.get("TRIAGE_ROLE")
    if raw is None or not raw.strip():
        return DEFAULT_TRIAGE_ROLE
    return raw.strip()


def triage_title_limit() -> int:
    """Max item titles fed to the model per cluster (env TRIAGE_TITLE_LIMIT). Falls back on
    absence/garbage/non-positive — we always feed at least the default number of headlines."""
    raw = os.environ.get("TRIAGE_TITLE_LIMIT")
    if raw is None:
        return DEFAULT_TRIAGE_TITLE_LIMIT
    try:
        val = int(raw)
    except ValueError:
        log.warning("bad TRIAGE_TITLE_LIMIT=%r — falling back to %s", raw, DEFAULT_TRIAGE_TITLE_LIMIT)
        return DEFAULT_TRIAGE_TITLE_LIMIT
    return val if val > 0 else DEFAULT_TRIAGE_TITLE_LIMIT


# --- pure: prompt + parse ------------------------------------------------------------------


def build_triage_prompt(titles: list[str]) -> str:
    """Assemble the single-shot triage prompt (PURE — no DB, no network).

    The model sees ONLY the cluster's item headlines (the grounding set) and is asked for a
    crisp title and a 1-2 sentence summary in a strict `TITLE:` / `SUMMARY:` shape so
    parse_triage_reply has the easiest possible job. The instruction is explicit about the hard
    grounding rule — stay within the headlines, invent no facts and assert no opinions — because
    this blurb is the owner's first-glance signal and must not editorialize."""
    title_block = "\n".join(f"- {t}" for t in titles) if titles else "- (no title available)"
    return (
        "You are a triage assistant for a personal tech-news pipeline. The owner skims your "
        "summary on their phone to decide whether a story is worth drafting about.\n\n"
        "Below are the headlines a cluster of sources used for ONE story. Using ONLY these "
        "headlines, write:\n"
        f"  {_TITLE_MARKER} a single crisp headline for the story (<= 15 words)\n"
        f"  {_SUMMARY_MARKER} 1-2 plain sentences on what the story is\n\n"
        "Hard rules: stay strictly grounded in the headlines below. Do NOT invent facts, "
        "numbers, names, or details that are not in them, and do NOT add opinions or takes — "
        "the owner forms the opinion. If the headlines are thin, keep the summary short rather "
        "than padding it.\n\n"
        "Headlines:\n"
        f"{title_block}\n\n"
        f"Reply with exactly two lines, starting with {_TITLE_MARKER} and {_SUMMARY_MARKER}."
    )


def _clean_field(value: str) -> str:
    """Strip surrounding whitespace and a single leading list dash from a parsed field.
    Models sometimes echo the prompt's `- ` bullet style into the value; we drop one leading
    dash + space so 'TITLE: - Foo' yields 'Foo', not '- Foo'."""
    value = value.strip()
    if value.startswith("-"):
        value = value[1:].strip()
    return value


def parse_triage_reply(text: str | None, titles: list[str]) -> tuple[str, str] | None:
    """Parse a model reply into (title, summary). PURE and deliberately TOLERANT.

    Precedence:
      1. If the reply carries `TITLE:` / `SUMMARY:` markers (case-insensitive), use them. A
         leading dash + whitespace is stripped from each. Missing TITLE but present SUMMARY ->
         the title falls back to titles[0] (the cluster's seed headline).
      2. No markers at all -> treat the whole reply as the summary and fall back to titles[0]
         for the title (the model just wrote prose; don't lose it).

    Returns None ONLY when there is genuinely nothing to record: an empty/whitespace reply AND
    no titles to fall back to. (An empty reply WITH titles still yields a usable card from the
    seed headline.) Title is capped at ~200 chars and summary at ~1500 so a runaway reply can't
    bloat the row or the Telegram card. Invents nothing — every field is the model's words or a
    real cluster headline."""
    fallback_title = titles[0] if titles else None
    raw = (text or "").strip()

    if not raw:
        if fallback_title is None:
            return None
        # Empty reply but we have a seed headline: a usable, if bare, card.
        return _cap(fallback_title, _TITLE_CAP), ""

    title_val: str | None = None
    summary_val: str | None = None

    # Scan lines for the markers (case-insensitive); everything after a SUMMARY: marker (incl.
    # any wrapped continuation lines the model emits) belongs to the summary.
    lines = raw.splitlines()
    in_summary = False
    summary_parts: list[str] = []
    for line in lines:
        stripped = line.strip()
        upper = stripped.upper()
        if upper.startswith(_TITLE_MARKER):
            title_val = _clean_field(stripped[len(_TITLE_MARKER):])
            in_summary = False
        elif upper.startswith(_SUMMARY_MARKER):
            summary_parts = [_clean_field(stripped[len(_SUMMARY_MARKER):])]
            in_summary = True
        elif in_summary and stripped:
            summary_parts.append(stripped)

    if summary_parts:
        summary_val = " ".join(p for p in summary_parts if p).strip()

    has_marker = title_val is not None or summary_val is not None
    if not has_marker:
        # No markers: the whole reply is the summary; title falls back to the seed headline.
        title = fallback_title if fallback_title is not None else raw
        return _cap(title, _TITLE_CAP), _cap(raw, _SUMMARY_CAP)

    # Markers present (at least one). Fill any missing side from the seed headline / empty.
    title = title_val if title_val else (fallback_title or "")
    summary = summary_val or ""
    return _cap(title, _TITLE_CAP), _cap(summary, _SUMMARY_CAP)


def _cap(text: str, limit: int) -> str:
    """Truncate to `limit` chars (no ellipsis — the cap is a safety bound, not a display rule)."""
    return text if len(text) <= limit else text[:limit]


def summarize_titles(titles: list[str]) -> tuple[str, str] | None:
    """The ONE model call: build the prompt, call generate(role=triage_role()), parse it.

    Factored out (titles in, (title, summary)-or-None out) so the model boundary is a single
    seam shared by the DB loop and any future caller, and so tests can monkeypatch the
    module-level `generate`. Returns None when there are no titles (nothing to ground a summary
    in — we never call the model on an empty cluster). The role is logical (triage_role()),
    never a model id."""
    if not titles:
        return None
    reply = generate(
        messages=[{"role": "user", "content": build_triage_prompt(titles)}],
        role=triage_role(),
    )
    return parse_triage_reply(reply, titles)


# --- DB path -------------------------------------------------------------------------------


def select_triage_candidates(
    session, *, top_n: int, min_score: float | None = None
) -> list[str]:
    """The highest-ranked NEW, un-summarized cluster ids, best first, capped at `top_n`.

    Predicate: status=='new' AND triage_summary IS NULL — a cluster the bot has already
    delivered/decided, or one already summarized, is never a candidate. Ordering: score DESC
    with NULLs last (an unranked cluster sorts after every ranked one rather than jumping the
    queue), then created_at ASC, then id, so equal-score clusters order deterministically.

    `min_score` (when set) excludes clusters scoring below it AND any NULL-score cluster — a
    floor implies "must be ranked at least this high", so an unranked cluster can't pass it."""
    stmt = (
        select(Cluster.id)
        .where(Cluster.status == "new")
        .where(Cluster.triage_summary.is_(None))
    )
    if min_score is not None:
        # NULL-score rows are excluded automatically: NULL >= min_score is not true in SQL.
        stmt = stmt.where(Cluster.score >= min_score)
    stmt = stmt.order_by(
        nullslast(Cluster.score.desc()),
        Cluster.created_at.asc(),
        Cluster.id.asc(),
    ).limit(top_n)
    return list(session.execute(stmt).scalars().all())


def _cluster_titles(session, cluster_id: str, *, limit: int) -> list[str]:
    """Up to `limit` non-empty item titles for a cluster, oldest-first (a stable representative
    set). PASS-1 metadata only — `title`, never `full_text` (full_text is post-approval pass-2
    and is not the triage grounding set)."""
    rows = session.execute(
        select(ItemModel.title)
        .where(ItemModel.cluster_id == cluster_id)
        .where(ItemModel.title.is_not(None))
        .order_by(ItemModel.fetched_at.asc(), ItemModel.id.asc())
        .limit(limit)
    ).scalars().all()
    return [t.strip() for t in rows if t and t.strip()]


def summarize_pending_triage(session, cfg=None) -> dict:
    """Summarize the top NEW, un-summarized clusters; write triage_title / triage_summary.

    For each candidate (select_triage_candidates with the env-resolved knobs): gather its
    pass-1 item titles, run the single model call, and persist the result via a single GUARDED
    CONDITIONAL UPDATE that re-confirms status=='new' AND triage_summary IS NULL atomically in
    SQL (the WHERE clause), mirroring the bot's claim_for_send/decide pattern. Doing the
    re-confirm in SQL — not a Python read-then-write — is what makes this safe to run on a timer
    alongside the bot inside the poller's long-lived session: a session.get would return the
    identity-map-cached row and miss a status the bot committed after this session last read it,
    so the guard could pass on stale state. The UPDATE re-checks live row state, so if a Gate-1
    decision (or another pass's summary) landed between selection and write, the UPDATE matches
    0 rows and the decided/summarized cluster is left untouched (never overwrite, never
    resurrect). Commits per cluster so a long batch makes incremental, crash-safe progress.

    Idempotent: writing a summary drops the cluster from the next pass's candidate set, so a
    re-run over unchanged data summarizes nothing new.

    `cfg` is accepted for signature symmetry with the other run_process stages but is UNUSED:
    triage needs no config (its grounding is the DB titles, its knobs are env), so this never
    reads config.yaml on a pass. Returns {"selected", "summarized"}.
    """
    top_n = triage_top_n()
    min_score = triage_min_score()
    title_limit = triage_title_limit()

    candidate_ids = select_triage_candidates(session, top_n=top_n, min_score=min_score)
    stats = {"selected": len(candidate_ids), "summarized": 0}

    for cluster_id in candidate_ids:
        titles = _cluster_titles(session, cluster_id, limit=title_limit)
        result = summarize_titles(titles)
        if result is None:
            # No titles to ground a summary -> nothing to write (an empty/untitled cluster).
            continue
        title, summary = result

        # Re-confirm-in-SQL before writing: a single guarded conditional UPDATE keyed on
        # status=='new' AND triage_summary IS NULL. Doing the re-confirm in the WHERE (not a
        # Python read-then-write) is what makes it airtight inside the poller's long-lived
        # session: session.get would return the identity-map-cached row and miss a status the
        # bot committed after this session last read it. The UPDATE re-checks against live row
        # state, so a Gate-1 decision that landed mid-pass matches 0 rows and we leave the
        # decided cluster untouched (never overwrite, never resurrect); an already-summarized
        # cluster likewise no-ops. synchronize_session defaults to "auto", which keeps any
        # in-identity-map Cluster object in sync with the values written here.
        result = session.execute(
            update(Cluster)
            .where(Cluster.id == cluster_id)
            .where(Cluster.status == "new")
            .where(Cluster.triage_summary.is_(None))
            .values(triage_title=title, triage_summary=summary)
        )
        if result.rowcount == 1:
            stats["summarized"] += 1
        session.commit()  # commit per cluster: incremental progress, crash-safe

    if stats["selected"]:
        log.info(
            "triage: selected %d cluster(s), summarized %d",
            stats["selected"], stats["summarized"],
        )
    return stats


__all__ = [
    "DEFAULT_TRIAGE_TOP_N",
    "DEFAULT_TRIAGE_MIN_SCORE",
    "DEFAULT_TRIAGE_ROLE",
    "DEFAULT_TRIAGE_TITLE_LIMIT",
    "triage_top_n",
    "triage_min_score",
    "triage_role",
    "triage_title_limit",
    "build_triage_prompt",
    "parse_triage_reply",
    "summarize_titles",
    "select_triage_candidates",
    "summarize_pending_triage",
]
