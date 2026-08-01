"""Morning-brief bot WIRING (app.bot.__main__) — Phase 9.

Drives _run_brief against a FAKE bot (no `import telegram` for the send path — the SDK is only
touched by _keyboard, which builds a real InlineKeyboardMarkup) and asserts:
  - one header then one card per selected cluster, each CLAIMED ('new' -> 'sent');
  - a second run over the same data sends nothing new (exactly-once: the cards are now 'sent');
  - a send failure on a card reverts THAT cluster to 'new' (nothing stranded at 'sent').

Plus pure assertions on _post_init's delivery mode and the scheduler's job set: with a brief the
drip is NOT started and a "brief" job IS registered; without a brief the drip starts and no brief
job is added.

DB isolation: _run_brief opens its OWN session via app.bot.__main__.get_session; we monkeypatch
that to hand back a session bound to the test's savepoint connection, so commits inside _run_brief
stay inside the rolled-back outer transaction. Guarded by RUN_PG_TESTS.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import pytest

import app.bot.__main__ as botmain
from app.config import Brief, Config

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"
pg_only = pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")


# --- a fake telegram.Bot + a fake App (only the attrs the wiring touches) -------------------


class _FakeBot:
    def __init__(self, *, fail_on=None):
        self.calls: list[dict] = []
        self.fail_on = fail_on  # a cluster text-substring to raise on, to simulate a send failure

    async def send_message(self, **kwargs):
        if self.fail_on is not None and self.fail_on in kwargs.get("text", ""):
            raise RuntimeError("simulated send failure")
        self.calls.append(kwargs)


class _FakeApp:
    def __init__(self, bot, cfg):
        self.bot = bot
        self.bot_data = {"cfg": cfg}


def _brief_cfg(*, schedule="08:00", window_s=86400, top_n=10):
    return Config(default_cadence_s=86400, brief=Brief(schedule=schedule, window_s=window_s, top_n=top_n))


# --- _post_init delivery-mode + scheduler job set (pure: a fake scheduler) ------------------


class _FakeScheduler:
    """Records add_job calls so the brief/digest job registration is inspectable without
    APScheduler driving anything."""

    def __init__(self):
        self.jobs: list[dict] = []
        self.started = False

    def add_job(self, func, **kwargs):
        self.jobs.append({"func": func, **kwargs})

    def start(self):
        self.started = True


@pytest.fixture()
def fake_scheduler(monkeypatch):
    """Patch AsyncIOScheduler + CronTrigger so _build_scheduler builds a recording fake."""
    import apscheduler.schedulers.asyncio as aio
    import apscheduler.triggers.cron as cron

    sched = _FakeScheduler()
    monkeypatch.setattr(aio, "AsyncIOScheduler", lambda *a, **k: sched)
    monkeypatch.setattr(cron, "CronTrigger", lambda *a, **k: ("cron", a, k))
    return sched


@pytest.mark.asyncio
async def test_post_init_with_brief_retires_drip_and_registers_brief_job(monkeypatch, fake_scheduler):
    # The owner must be configured for the brief to be scheduled at all.
    monkeypatch.setenv("TELEGRAM_OWNER_CHAT_ID", "42")
    created = {"drip": False}
    monkeypatch.setattr(botmain.asyncio, "create_task", lambda coro: created.__setitem__("drip", True) or coro)

    app = _FakeApp(_FakeBot(), _brief_cfg())
    await botmain._post_init(app)

    assert created["drip"] is False                      # the drip is RETIRED when a brief is set
    assert "delivery_task" not in app.bot_data
    job_ids = [j.get("id") for j in fake_scheduler.jobs]
    assert "brief" in job_ids                            # the brief job is registered


@pytest.mark.asyncio
async def test_post_init_without_brief_starts_drip_and_no_brief_job(monkeypatch, fake_scheduler):
    monkeypatch.setenv("TELEGRAM_OWNER_CHAT_ID", "42")
    created = {"drip": False}

    class _DummyTask:
        def cancel(self):
            pass

    def _fake_create_task(coro):
        created["drip"] = True
        coro.close()  # don't actually run the delivery loop in the test
        return _DummyTask()

    monkeypatch.setattr(botmain.asyncio, "create_task", _fake_create_task)

    app = _FakeApp(_FakeBot(), Config(default_cadence_s=86400))  # no brief
    await botmain._post_init(app)

    assert created["drip"] is True                       # the drip runs when no brief
    assert "delivery_task" in app.bot_data
    job_ids = [j.get("id") for j in fake_scheduler.jobs]
    assert "brief" not in job_ids                        # no brief job added


# --- _run_brief against the DB + a fake bot -------------------------------------------------


@pytest.fixture()
def pg_session(monkeypatch):
    """A savepoint-bound session, also patched in as app.bot.__main__.get_session so _run_brief's
    own get_session() shares this transaction (its commits land on the savepoint, rolled back at
    teardown)."""
    from app.db.session import engine, SessionLocal

    conn = engine.connect()
    outer = conn.begin()
    sess = SessionLocal(bind=conn, join_transaction_mode="create_savepoint")
    monkeypatch.setattr(botmain, "get_session", lambda: sess)
    try:
        yield sess
    finally:
        sess.close()
        outer.rollback()
        conn.close()


def _add_cluster(session, *, status="new", score=None, summary="A blurb", created_at=None, title="t"):
    from app.db.models import Cluster
    from app.researcher.cluster import new_cluster_id

    cid = new_cluster_id()
    cluster = Cluster(id=cid, status=status, score=score, triage_title=title, triage_summary=summary)
    if created_at is not None:
        cluster.created_at = created_at
    session.add(cluster)
    session.commit()
    return cid


@pg_only
@pytest.mark.asyncio
async def test_run_brief_sends_header_then_one_card_per_cluster_and_claims(monkeypatch, pg_session):
    from app.db.models import Cluster

    monkeypatch.setenv("TELEGRAM_OWNER_CHAT_ID", "42")
    now = datetime.now(timezone.utc)
    high = _add_cluster(pg_session, score=0.9, created_at=now, title="High")
    low = _add_cluster(pg_session, score=0.1, created_at=now, title="Low")

    bot = _FakeBot()
    app = _FakeApp(bot, _brief_cfg(window_s=86400, top_n=10))
    await botmain._run_brief(app)

    # 1 header + 2 cards, in order.
    assert len(bot.calls) == 3
    assert bot.calls[0]["text"] == "📰 Morning brief — 2 new stories"
    assert "parse_mode" not in bot.calls[0]              # header is plain text
    assert all(c["parse_mode"] == "HTML" for c in bot.calls[1:])  # cards are HTML
    assert all(c["chat_id"] == 42 for c in bot.calls)
    # Both clusters claimed (delivered) — now 'sent'.
    assert pg_session.get(Cluster, high).status == "sent"
    assert pg_session.get(Cluster, low).status == "sent"

    # Second run over the same data: the cards are 'sent', so nothing new -> not even a header.
    bot2 = _FakeBot()
    app2 = _FakeApp(bot2, _brief_cfg(window_s=86400, top_n=10))
    await botmain._run_brief(app2)
    assert bot2.calls == []                              # exactly-once: nothing re-sent


@pg_only
@pytest.mark.asyncio
async def test_run_brief_empty_window_sends_nothing(monkeypatch, pg_session):
    monkeypatch.setenv("TELEGRAM_OWNER_CHAT_ID", "42")
    now = datetime.now(timezone.utc)
    # The only summarized cluster is OUTSIDE the window -> empty selection -> no header.
    _add_cluster(pg_session, score=0.9, created_at=now - timedelta(days=2))

    bot = _FakeBot()
    await botmain._run_brief(_FakeApp(bot, _brief_cfg(window_s=86400, top_n=10)))
    assert bot.calls == []


@pg_only
@pytest.mark.asyncio
async def test_run_brief_send_failure_reverts_that_card_to_new(monkeypatch, pg_session):
    from app.db.models import Cluster

    monkeypatch.setenv("TELEGRAM_OWNER_CHAT_ID", "42")
    now = datetime.now(timezone.utc)
    good = _add_cluster(pg_session, score=0.9, created_at=now, title="Good")
    bad = _add_cluster(pg_session, score=0.5, created_at=now, title="WillFail")

    # The bot raises on the card whose rendered text contains "WillFail".
    bot = _FakeBot(fail_on="WillFail")
    await botmain._run_brief(_FakeApp(bot, _brief_cfg(window_s=86400, top_n=10)))

    # The failed card is reverted to 'new' (retried next run) — nothing stranded at 'sent'.
    assert pg_session.get(Cluster, bad).status == "new"
    # The good card was delivered and claimed.
    assert pg_session.get(Cluster, good).status == "sent"
    # The header plus the one successful card were sent (the failing send raised, so isn't recorded).
    sent_texts = [c["text"] for c in bot.calls]
    assert sent_texts[0].startswith("📰 Morning brief")
    assert any("Good" in t for t in sent_texts)
    assert all("WillFail" not in t for t in sent_texts)
