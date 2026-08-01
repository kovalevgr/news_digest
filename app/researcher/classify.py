"""Cheap topic classifier for ambiguous clusters (Phase 1 slice 3b).

slice 3a (cluster.py) fills `clusters.topic` only when the cluster's seed item has an
UNAMBIGUOUS source-default topic (exactly one `topic:<name>` owner). Two cases are left
NULL on purpose: a *person-only* item (its source carries no inherent topic) and an item
genuinely owned by several distinct topics. This stage resolves those leftover NULLs.

It is the researcher's ONE single-shot model call (docs/01_technical.md: triage/topic
classification are single-shot model calls, NOT agents). For each cluster with topic IS
NULL we assemble a tiny prompt from its items' titles (pass-1 metadata only — no full_text)
and ask `app.llm.generate(role="cheap")` to pick one of the CONFIGURED topic names or the
explicit "other" escape. We set `clusters.topic` only when the reply maps to a configured
topic; "other"/unparseable leaves it NULL. The model stays swappable: role "cheap" only,
never a hardcoded model id.

Determinism / safety contract:
  - NULL-ONLY: the SQL predicate selects `topic IS NULL` clusters, so a non-null
    source-default topic from slice 3a is NEVER reconsidered or overwritten.
  - NEVER INVENT: parse_label returns a label only if it is in the configured set (+"other");
    anything else (declined, garbage, hallucinated topic) -> None -> topic stays NULL.
  - IDEMPOTENT: re-running only touches still-NULL clusters; a run that sets a topic shrinks
    the next run's candidate set, and an "other" verdict simply leaves the cluster for a
    later (possibly better-informed) pass.

Label set + prompt are an intentionally-OPEN decision (docs/03_build_plan.md). They live in
ONE place here (`build_prompt`, `OTHER_LABEL`, `classify_titles_for_cluster`) so tuning the
wording or the candidate labels never means hunting through the DB path.
"""
from __future__ import annotations

import logging
import os

from sqlalchemy import select

from app.config import Config, load_config
from app.db.models import Cluster, Item as ItemModel
from app.llm import generate

log = logging.getLogger("researcher.classify")

# The explicit escape hatch: the classifier must be able to DECLINE rather than be forced to
# pick a wrong topic. "other" is reserved — it is appended to the candidate labels offered to
# the model but is NOT a configured topic, so a verdict of "other" maps to None (topic stays
# NULL). Keeping it a module constant means the reserved word is defined once.
OTHER_LABEL = "other"

# How many item titles to feed the model per cluster. A cluster is one story; a few of its
# titles give the classifier enough signal without ballooning the (cheap-role) prompt. Tunable
# via env without touching code. Oldest-first so the representative set is stable run-to-run.
DEFAULT_CLASSIFY_TITLE_LIMIT = int(os.environ.get("CLASSIFY_TITLE_LIMIT", "5"))


def configured_topics(cfg: Config) -> list[str]:
    """The configured topic names, in config order, as the candidate label set.

    Source of truth is config, never a hardcoded list: the topic keys under
    `topics:` in config.yaml (exposed as cfg.raw["topics"]). Non-string / blank keys are
    skipped defensively; "other" is the reserved escape and is excluded here (added only when
    we build the offered label list)."""
    raw_topics = (cfg.raw or {}).get("topics") or {}
    names: list[str] = []
    for name in raw_topics.keys():
        if isinstance(name, str) and name.strip() and name != OTHER_LABEL:
            names.append(name)
    return names


def build_prompt(titles: list[str], labels: list[str]) -> str:
    """Assemble the single-shot classification prompt (pure — no DB, no network).

    `labels` are the configured topic names; we offer them plus the OTHER_LABEL escape and ask
    for exactly one, lowercased, on its own. Titles are the pass-1 signal (one per line). The
    instruction is deliberately strict about replying with a single bare label so parse_label
    has the easiest possible job — but parse_label stays tolerant in case the model adds
    chatter."""
    offered = labels + [OTHER_LABEL]
    label_line = ", ".join(offered)
    title_block = "\n".join(f"- {t}" for t in titles) if titles else "- (no title available)"
    return (
        "You are a strict topic classifier for a tech-news pipeline.\n"
        f"Choose the SINGLE best topic for the story below from this exact list: {label_line}.\n"
        f"Reply with exactly one label from the list, lowercase, and nothing else. "
        f"If none clearly fits, reply {OTHER_LABEL!r}.\n\n"
        "Story headlines:\n"
        f"{title_block}\n\n"
        "Topic:"
    )


def parse_label(model_text: str | None, labels: list[str]) -> str | None:
    """Map a model reply to a configured label, or None.

    Tolerance rules (case-insensitive throughout):
      - exact match (after strip) to a configured label wins;
      - otherwise a whole-word, case-insensitive occurrence of a configured label anywhere in
        the reply is accepted (so "Topic: ai" or "I'd say dotnet." resolve) — matched as a
        bounded token, not a substring, so 'ai' does not spuriously fire inside 'maintain';
      - the OTHER_LABEL escape and any reply that contains no configured label -> None
        (the cluster stays NULL — we never invent a topic);
      - to avoid silently picking the wrong one when a reply names several configured topics,
        an ambiguous reply (two or more DISTINCT configured labels mentioned) -> None.

    Returns a label guaranteed to be in `labels`, or None. Never returns OTHER_LABEL."""
    if not model_text:
        return None
    text = model_text.strip().lower()
    if not text:
        return None

    # 1) Clean single-label reply (the asked-for shape).
    for label in labels:
        if text == label.lower():
            return label

    # 2) Whole-word scan, tolerant of surrounding chatter. Collect DISTINCT configured labels
    #    that appear as bounded tokens; require exactly one to avoid guessing on ambiguity.
    tokens = _tokenize(text)
    hits = [label for label in labels if label.lower() in tokens]
    # de-dup while preserving order (a label mentioned twice is still one distinct hit)
    distinct: list[str] = []
    for h in hits:
        if h not in distinct:
            distinct.append(h)
    if len(distinct) == 1:
        return distinct[0]
    return None


def _tokenize(text: str) -> set[str]:
    """Lowercase word tokens of `text` for whole-word matching. We split on any run of
    non-alphanumeric characters, which keeps multi-word topic names out of scope for the
    token path (they would only match via the exact-match branch) but reliably isolates the
    common single-word topics ('ai', 'dotnet') from surrounding punctuation/words."""
    token = []
    out: set[str] = set()
    for ch in text.lower():
        if ch.isalnum():
            token.append(ch)
        elif token:
            out.add("".join(token))
            token = []
    if token:
        out.add("".join(token))
    return out


def _cluster_titles(session, cluster_id: str, *, limit: int) -> list[str]:
    """Up to `limit` non-empty item titles for a cluster, oldest-first (stable representative
    set). Pass-1 metadata only — title, never full_text."""
    rows = session.execute(
        select(ItemModel.title)
        .where(ItemModel.cluster_id == cluster_id)
        .where(ItemModel.title.is_not(None))
        .order_by(ItemModel.fetched_at.asc(), ItemModel.id.asc())
        .limit(limit)
    ).scalars().all()
    return [t.strip() for t in rows if t and t.strip()]


def classify_titles_for_cluster(titles: list[str], labels: list[str]) -> str | None:
    """The ONE model call: build the prompt, call generate(role='cheap'), parse the reply.

    Factored out (titles in, label-or-None out) so the model boundary is a single seam: the DB
    loop below and any future caller share this, and tests can drive it with a monkeypatched
    `generate`. If the candidate label set is empty (no topics configured) there is nothing to
    classify into, so we decline without calling the model. role is always 'cheap' — no model
    id is named here."""
    if not labels:
        return None
    prompt = build_prompt(titles, labels)
    reply = generate(messages=[{"role": "user", "content": prompt}], role="cheap")
    return parse_label(reply, labels)


def classify_pending_topics(session, cfg: Config | None = None, now=None) -> dict[str, int]:
    """Fill `clusters.topic` for clusters where it is still NULL, via the cheap classifier.

    For each cluster WHERE topic IS NULL (oldest-first for stable ordering): gather its item
    titles, ask the classifier for a configured topic or "other", and set `clusters.topic` only
    when the verdict maps to a configured topic. "other"/unparseable leaves it NULL. Commits per
    cluster so a long backlog makes incremental progress and a crash strands nothing.

    NULL-only by construction (the predicate never selects a non-null topic) — a source-default
    topic is never overwritten. Idempotent: a re-run only revisits clusters still NULL.

    `now` is accepted for signature symmetry with the other researcher stages (and future
    time-windowing) but is unused here. Returns {"considered": n, "labeled": k}.
    """
    cfg = cfg or load_config()
    labels = configured_topics(cfg)
    stats = {"considered": 0, "labeled": 0}

    if not labels:
        # No topics configured -> nothing to classify into. Don't call the model at all.
        log.info("classify: no configured topics; nothing to do")
        return stats

    cluster_ids = session.execute(
        select(Cluster.id)
        .where(Cluster.topic.is_(None))
        .order_by(Cluster.created_at.asc(), Cluster.id.asc())
    ).scalars().all()

    for cluster_id in cluster_ids:
        stats["considered"] += 1
        titles = _cluster_titles(cluster_id=cluster_id, session=session, limit=DEFAULT_CLASSIFY_TITLE_LIMIT)
        label = classify_titles_for_cluster(titles, labels)
        if label is not None:
            # Re-read inside the same session and re-check NULL before writing: never clobber a
            # topic another path may have set; honours the no-overwrite contract even if this
            # ever runs alongside slice-3a re-clustering.
            cluster = session.get(Cluster, cluster_id)
            if cluster is not None and cluster.topic is None:
                cluster.topic = label
                stats["labeled"] += 1
        session.commit()  # commit per cluster: incremental progress, crash-safe

    if stats["considered"]:
        log.info(
            "classify: considered %d NULL-topic cluster(s), labeled %d",
            stats["considered"], stats["labeled"],
        )
    return stats


__all__ = [
    "OTHER_LABEL",
    "DEFAULT_CLASSIFY_TITLE_LIMIT",
    "configured_topics",
    "build_prompt",
    "parse_label",
    "classify_titles_for_cluster",
    "classify_pending_topics",
]
