"""Gate-1 bot core — SDK-free logic (docs/01_technical.md §2.2; build plan Phase 2).

This is the deterministic heart of the Telegram triage bot: callback_data encode/parse,
message rendering, and the cluster-status transitions that make delivery exactly-once. It is
kept FREE of `python-telegram-bot` (no `import telegram` anywhere) so it is unit-testable
without the SDK or a running bot — the async wiring lives in app/bot/__main__.py and calls
into here. The bot coordinates with the poller purely through `clusters.status` /
`clusters.triage_*` in Postgres; it never calls another stage. It makes ZERO model calls — it
only reads what the researcher wrote and writes a status (it never publishes anything).

The exactly-once guarantee (Phase 2 Done: "the owner receives each top story exactly once —
restarting the bot or the poller resends nothing") rests on the cluster status machine, all of
it conditional UPDATEs that key on the CLUSTER (clusters are first-class — no per-item state):

    new --claim_for_send--> sent --decide--> approved / skipped
     ^                        |
     +------revert_to_new-----+   (only ever from 'sent', on a send FAILURE)

  - claim_for_send is a guarded `new -> sent`: exactly one caller can win it, so a cluster is
    delivered at most once even if two sweeps (or a restarted bot/poller) race. Claiming BEFORE
    the Telegram send is what survives a restart — a crash after claim leaves the card 'sent'
    and it is simply never re-selected.
  - revert_to_new is a guarded `sent -> new`, used ONLY when the send itself fails, to put the
    card back in the queue. Guarded on 'sent' so it can never resurrect a decided story.
  - decide is a guarded `(sent|new) -> approved/skipped`: idempotent, so a double-tap on the
    inline buttons is a no-op (returns None once terminal).

callback_data is bounded: a cluster id is "cl:" + a 64-hex sha256 body (67 chars), which blows
past Telegram's 64-BYTE callback_data limit. So the button carries only an action + a 16-hex
PREFIX of the id body (the token); resolve_by_token maps that prefix back to the unique cluster
at tap time, treating an ambiguous or missing prefix as a safe no-op.
"""
from __future__ import annotations

import html
import logging

from sqlalchemy import select, update

from app.db.models import Cluster

log = logging.getLogger("bot.triage")

# Callback actions, kept to single chars so encoded callback_data stays well under Telegram's
# 64-byte limit. The id prefix in app.researcher.cluster.new_cluster_id() is "cl:".
ACTION_APPROVE = "a"
ACTION_SKIP = "s"
_ACTIONS = (ACTION_APPROVE, ACTION_SKIP)

_CLUSTER_PREFIX = "cl:"
# Length of the id-body prefix used as the callback token. The body is 64 hex chars; 16 hex =
# 64 bits of the sha256, collision-vanishingly-unlikely for a single user's cluster set, and
# small enough that "<action>:<token>" (e.g. "a:0123456789abcdef") is ~18 bytes — far under 64.
_TOKEN_LEN = 16


# --- pure: callback_data + rendering -------------------------------------------------------


def cluster_token(cluster_id: str) -> str:
    """The first 16 chars of a cluster id's BODY (the hex after the "cl:" prefix).

    We strip the "cl:" prefix before slicing so the token is purely the discriminating hex;
    resolve_by_token re-adds the prefix when matching (`LIKE 'cl:'||token||'%'`). If the id has
    no "cl:" prefix (defensive — all real ids do), we slice the whole string."""
    body = cluster_id[len(_CLUSTER_PREFIX):] if cluster_id.startswith(_CLUSTER_PREFIX) else cluster_id
    return body[:_TOKEN_LEN]


def encode_callback(action: str, cluster_id: str) -> str:
    """Encode a button's callback_data as `<action>:<token>`. Raises ValueError on an unknown
    action (a programming error — only the module's two actions are valid). The result is well
    under Telegram's 64-byte callback_data limit (action is 1 char, token is 16)."""
    if action not in _ACTIONS:
        raise ValueError(f"unknown triage action {action!r}; expected one of {_ACTIONS}")
    return f"{action}:{cluster_token(cluster_id)}"


def parse_callback(data: str | None) -> tuple[str, str] | None:
    """Decode callback_data back to (action, token), or None for anything malformed.

    Tolerant by design — junk callback_data must be a safe no-op, never an exception: None,
    empty, no colon, an unknown action, or an empty token all return None. A valid result is
    (action in _ACTIONS, non-empty token)."""
    if not data or ":" not in data:
        return None
    action, _, token = data.partition(":")
    if action not in _ACTIONS or not token:
        return None
    return action, token


def format_message(cluster) -> str:
    """Render a cluster as the Telegram triage card (HTML parse mode).

    Layout: bold title, blank line, summary, blank line, an italic meta line with topic and
    score. EVERY dynamic field is html.escape'd so a title containing `<`, `>`, or `&` can't
    break the HTML or inject markup (the test pins this). Missing topic/score degrade to
    readable placeholders rather than 'None'/a format error."""
    title = html.escape(cluster.triage_title or "(untitled)")
    summary = html.escape(cluster.triage_summary or "")
    topic = html.escape(cluster.topic or "—")
    score = cluster.score
    score_str = f"{score:.2f}" if isinstance(score, (int, float)) else "—"
    return (
        f"<b>{title}</b>\n\n"
        f"{summary}\n\n"
        f"<i>topic: {topic} · score: {score_str}</i>"
    )


def owner_chat_id() -> int | None:
    """The owner's Telegram chat id from env TELEGRAM_OWNER_CHAT_ID, or None if unset/garbage.

    Lives here (not just in __main__) because the callback handler authorizes against it. A
    secret/identity from the ENVIRONMENT only — never config.yaml or git (hard rule 3)."""
    import os

    raw = os.environ.get("TELEGRAM_OWNER_CHAT_ID")
    if raw is None or not raw.strip():
        return None
    try:
        return int(raw.strip())
    except ValueError:
        log.warning("bad TELEGRAM_OWNER_CHAT_ID=%r — treating as unset", raw)
        return None


# --- DB: resolve / select / claim / revert / decide ----------------------------------------


def resolve_by_token(session, token: str) -> str | None:
    """Resolve a 16-hex callback token back to its full cluster id, or None.

    A UNIQUE prefix match: `Cluster.id LIKE 'cl:'||token||'%'`, limited to 2 rows. Returns the
    id only when EXACTLY ONE cluster matches; an ambiguous token (two clusters share the
    prefix) or a missing one both return None — a safe no-op rather than acting on the wrong
    story. (16 hex = 64 bits, so a real collision is vanishingly unlikely; this is correctness
    insurance, and it also guards a malformed/forged token.)"""
    if not token:
        return None
    pattern = _CLUSTER_PREFIX + token + "%"
    rows = session.execute(
        select(Cluster.id).where(Cluster.id.like(pattern)).limit(2)
    ).scalars().all()
    if len(rows) == 1:
        return rows[0]
    return None


def select_deliverable(session, *, limit: int) -> list[Cluster]:
    """The NEW clusters that have a triage summary and are ready to deliver, best first.

    Predicate: status=='new' AND triage_summary IS NOT NULL — i.e. the researcher has
    summarized it and the bot hasn't sent it yet. Ordered score DESC (NULLs last), created_at
    ASC, id, capped at `limit`. Returns full Cluster rows so the caller can render the card and
    then claim each one. (Selection alone delivers nothing — claim_for_send is the guard.)"""
    from sqlalchemy import nullslast

    return list(
        session.execute(
            select(Cluster)
            .where(Cluster.status == "new")
            .where(Cluster.triage_summary.is_not(None))
            .order_by(
                nullslast(Cluster.score.desc()),
                Cluster.created_at.asc(),
                Cluster.id.asc(),
            )
            .limit(limit)
        ).scalars().all()
    )


def claim_for_send(session, cluster_id: str) -> bool:
    """Atomically claim a cluster for delivery: conditional UPDATE status 'new' -> 'sent'.

    THIS is the exactly-once guard. The UPDATE matches only WHERE status=='new', so exactly one
    caller can transition a given cluster; a second claim (a racing sweep, or a re-selection
    after a restart) matches 0 rows. Returns True and COMMITS iff this call won (rowcount==1);
    otherwise ROLLS BACK and returns False. Claiming BEFORE the Telegram send means a crash
    between claim and send leaves the card 'sent' and simply never resends — at-most-once
    delivery that survives a bot/poller restart."""
    result = session.execute(
        update(Cluster)
        .where(Cluster.id == cluster_id)
        .where(Cluster.status == "new")
        .values(status="sent")
    )
    if result.rowcount == 1:
        session.commit()
        return True
    session.rollback()
    return False


def revert_to_new(session, cluster_id: str) -> None:
    """Put a claimed-but-not-delivered cluster back in the queue: conditional UPDATE 'sent' ->
    'new'. Used ONLY when the Telegram send FAILS after a successful claim, so the next sweep
    retries it. Guarded on status=='sent', so it can NEVER resurrect a story the owner already
    decided (approved/skipped) — those stay terminal. Commits."""
    session.execute(
        update(Cluster)
        .where(Cluster.id == cluster_id)
        .where(Cluster.status == "sent")
        .values(status="new")
    )
    session.commit()


def decide(session, cluster_id: str, *, approve: bool) -> str | None:
    """Record the owner's Gate-1 decision: conditional UPDATE status IN ('sent','new') ->
    'approved' / 'skipped'. Returns the new status, or None if the cluster is already terminal.

    Idempotent and safe against a double-tap: once a cluster is 'approved'/'skipped' the WHERE
    matches 0 rows, so a second tap (or tapping the other button on an already-decided card)
    returns None and changes nothing. 'new' is accepted alongside 'sent' defensively — a tap
    can arrive for a card whose claim hasn't committed yet (or after a revert); deciding it
    directly is harmless (it just means no further delivery) and avoids a stuck story. Commits
    on a real transition; rolls back on a no-op."""
    new_status = "approved" if approve else "skipped"
    result = session.execute(
        update(Cluster)
        .where(Cluster.id == cluster_id)
        .where(Cluster.status.in_(("sent", "new")))
        .values(status=new_status)
    )
    if result.rowcount == 1:
        session.commit()
        return new_status
    session.rollback()
    return None


__all__ = [
    "ACTION_APPROVE",
    "ACTION_SKIP",
    "cluster_token",
    "encode_callback",
    "parse_callback",
    "format_message",
    "owner_chat_id",
    "resolve_by_token",
    "select_deliverable",
    "claim_for_send",
    "revert_to_new",
    "decide",
]
