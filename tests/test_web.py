"""Editor web app (app.web) — NiceGUI page tests.

The UI is built on NiceGUI; these tests drive it HEADLESS via NiceGUI's `user` fixture
(nicegui.testing.user_plugin — registered in pytest.ini, which also sets asyncio_mode=auto and
points `main_file` at tests/nicegui_main.py). The fixture executes that main file, which imports
app.web.ui_pages and registers the `@ui.page('/')` dashboard and `@ui.page('/editor/{id}')`
editor on the global NiceGUI app; then `user.open(...)` renders a page and `user.should_see(...)`
/ `user.find(...)` assert against the rendered elements (each tagged with `.mark(...)`).

DB strategy: the pages open their own DB session via `app.db.session.get_session`. We monkeypatch
that to hand back ONE savepoint-wrapped Session (with a no-op close so the page closing it doesn't
end our transaction), seed exactly the rows a test needs, and roll the whole thing back at the
end. So these tests are deterministic and isolated from whatever demo data the DB holds — but they
DO need a live Postgres (the NiceGUI render path is real), so the file is guarded behind
RUN_PG_TESTS like the other DB-backed suites. The pure FastAPI bits (/healthz) and the chat seam
are covered without a DB.

The draft action path is exercised against a cluster seeded WITH an item carrying `full_text`
(the writer-agent refuses to draft a cluster with no fetched text — see tests/test_editor.py),
with `generate` scripted to return a final draft on the first turn (no real model call).
"""
from __future__ import annotations

import asyncio
import os
import uuid
from types import SimpleNamespace

import pytest

from app.web import chat as chat_seam

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"
pg_only = pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")


# --- Phase-5 backend-contract guards -------------------------------------------------------
#
# The Phase-5 backend slice (variants + mark-as-published) is built in PARALLEL against a frozen
# contract: `app.variants.generate_variant` / `list_latest_variants` / `VariantResult` and
# `app.editor.publish_article`. The UI here only CALLS those symbols. We detect whether each half
# has landed so the tests that exercise the REAL backend (or monkeypatch the variants seam the UI
# lazy-imports) run automatically once it's in, and SKIP (not fail) while it's still a stub — the
# UI's gating/render tests stay green either way.
import app.editor as editor_mod  # noqa: E402
import app.variants as variants_mod  # noqa: E402

_VARIANTS_READY = hasattr(variants_mod, "generate_variant") and hasattr(
    variants_mod, "VariantResult"
)
variants_ready = pytest.mark.skipif(
    not _VARIANTS_READY,
    reason="Phase-5 variants backend (app.variants.generate_variant + VariantResult) not landed yet",
)

# The hand-tune-save half of the variants slice is built in parallel too: the UI's "Save {Platform}"
# control lazy-imports `app.variants.save_variant_edit` (and the persistence test reads it back via
# `app.variants.latest_variant`). Guard so the persistence test SKIPS (not errors) until that symbol
# lands; the render/editable test below has no backend dependency and always runs.
_SAVE_VARIANT_READY = hasattr(variants_mod, "save_variant_edit") and hasattr(
    variants_mod, "latest_variant"
)
save_variant_ready = pytest.mark.skipif(
    not _SAVE_VARIANT_READY,
    reason="Phase-5 variants save backend (app.variants.save_variant_edit) not landed yet",
)

_PUBLISH_READY = hasattr(editor_mod, "publish_article")
publish_ready = pytest.mark.skipif(
    not _PUBLISH_READY,
    reason="Phase-5 mark-as-published backend (app.editor.publish_article) not landed yet",
)

# The SOURCES + VERSION HISTORY slice (this frontend addition) is built in PARALLEL against a frozen
# contract: `app.web.queries.load_article_sources` / `load_article_versions` (+ the ArticleSource /
# ArticleVersion dataclasses) and `app.editor.restore_article_version`. The editor page BUILDS both
# panels at render time, so the whole editor page render depends on the two read helpers. We detect
# whether each half has landed so these tests run automatically once the backend's half is in, and
# SKIP (not fail) while it's still absent — the module imports cleanly either way (the read helpers
# are called at render/runtime, not at import).
import app.web.queries as queries_mod  # noqa: E402

# The Phase-8 unified-Stories backend slice (the dashboard refactor) is built in PARALLEL against a
# frozen contract: `queries.load_stories` / `unified_status_counts` / `STATUS_SPECTRUM` and the
# `StoryRow` dataclass. The new dashboard CALLS those at render time, so the whole dashboard page
# render depends on them. We detect whether that half has landed so the new dashboard tests run
# automatically once it's in, and SKIP (not fail) while it's still absent — ui_pages imports cleanly
# either way (load_stories is called at render time, not at import).
_STORIES_READY = (
    hasattr(queries_mod, "load_stories")
    and hasattr(queries_mod, "unified_status_counts")
    and hasattr(queries_mod, "STATUS_SPECTRUM")
    and hasattr(queries_mod, "StoryRow")
)
stories_ready = pytest.mark.skipif(
    not _STORIES_READY,
    reason="Phase-8 unified-Stories backend (queries.load_stories + StoryRow) not landed yet",
)

_SOURCES_READY = hasattr(queries_mod, "load_article_sources") and hasattr(
    queries_mod, "ArticleSource"
)
_VERSIONS_READY = hasattr(queries_mod, "load_article_versions") and hasattr(
    queries_mod, "ArticleVersion"
)
_RESTORE_READY = hasattr(editor_mod, "restore_article_version")

# The panels render together (both in the preview pane), so both read helpers must be present for the
# editor page to render at all; gate the render/list tests on that pair.
history_render_ready = pytest.mark.skipif(
    not (_SOURCES_READY and _VERSIONS_READY),
    reason="Sources/version-history backend (queries.load_article_sources + load_article_versions) "
    "not landed yet",
)
restore_ready = pytest.mark.skipif(
    not (_SOURCES_READY and _VERSIONS_READY and _RESTORE_READY),
    reason="Restore backend (app.editor.restore_article_version) not landed yet",
)


# --- DB-free: /healthz + chat seam ---------------------------------------------------------


def test_healthz_ok():
    """The plain FastAPI liveness route still answers 200 with the NiceGUI mount in place."""
    from fastapi.testclient import TestClient

    from app.web import app

    resp = TestClient(app).get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_app_is_fastapi_with_nicegui_pages():
    """`from app.web import app` is the FastAPI instance, now serving the two NiceGUI pages."""
    import fastapi
    from nicegui import Client

    from app.web import app

    assert isinstance(app, fastapi.FastAPI)
    assert set(Client.page_routes.values()) >= {"/", "/editor/{article_id}"}


def test_storage_secret_env_and_fallback(monkeypatch):
    """WEB_STORAGE_SECRET wins; a blank/absent value falls back to the dev placeholder."""
    from app.web import routes

    monkeypatch.setenv("WEB_STORAGE_SECRET", "from-env")
    assert routes.storage_secret() == "from-env"
    monkeypatch.setenv("WEB_STORAGE_SECRET", "   ")
    assert routes.storage_secret() == routes._DEV_STORAGE_SECRET
    monkeypatch.delenv("WEB_STORAGE_SECRET", raising=False)
    assert routes.storage_secret() == routes._DEV_STORAGE_SECRET


# The Phase-4 iterate seam (app.web.chat) is a backend-owned slice built in parallel against the
# FROZEN CONTRACT: `handle_editor_message(article_id, instruction, *, base_draft=None,
# new_piece_type=None) -> IterateResult`, where IterateResult is re-exported from chat and the seam
# delegates to `iterate_article` (the symbol we monkeypatch). The UI here only CALLS the seam. We
# detect whether that contract has landed so this DB-free test goes green automatically once the
# backend's half is in (and is skipped — not failed — while the seam is still the Phase-3 stub).
_NEW_SEAM_READY = hasattr(chat_seam, "iterate_article") and hasattr(chat_seam, "IterateResult")
new_seam_only = pytest.mark.skipif(
    not _NEW_SEAM_READY,
    reason="Phase-4 iterate seam (app.web.chat.iterate_article + IterateResult) not landed yet",
)


@new_seam_only
def test_handle_editor_message_threads_args_and_returns_result(monkeypatch):
    """DB-free unit of the new iterate seam: handle_editor_message threads its args through to
    iterate_article and returns the IterateResult unchanged (we monkeypatch iterate_article so no
    model/DB is touched). This is the contract the UI builds against — base_draft (the owner's
    unsaved hand-edits) and new_piece_type (a mid-stream switch) must reach the agent."""
    IterateResult = chat_seam.IterateResult
    expected = IterateResult(
        reply="rewrote the intro",
        draft="# New\n\nrevised body",
        piece_type="hot_news",
        changed=True,
    )
    captured = {}

    def fake_iterate(*args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return expected

    monkeypatch.setattr(chat_seam, "iterate_article", fake_iterate)

    result = chat_seam.handle_editor_message(
        "a:1", "rewrite intro", base_draft="# Old\n\nbody", new_piece_type="digest"
    )
    assert result is expected
    # The instruction, the owner's base_draft, and the requested piece-type switch all reach the
    # agent (the exact positional/keyword shape is the backend's; assert presence by value).
    flat = list(captured["args"]) + list(captured["kwargs"].values())
    assert "a:1" in flat
    assert "rewrite intro" in flat
    assert "# Old\n\nbody" in flat
    assert "digest" in flat


@new_seam_only
def test_handle_editor_message_empty_instruction_is_noop(monkeypatch):
    """An empty/whitespace instruction is a no-op: the seam must NOT call the agent (nothing to
    edit-in-place from). The UI guards this too, but the seam stays safe on its own."""
    called = {"n": 0}

    def fake_iterate(*args, **kwargs):
        called["n"] += 1
        return chat_seam.IterateResult(reply="", draft="", piece_type="hot_news", changed=False)

    monkeypatch.setattr(chat_seam, "iterate_article", fake_iterate)
    result = chat_seam.handle_editor_message("a:1", "   ")
    assert called["n"] == 0
    # The seam returns a (non-crashing) IterateResult for the no-op; the draft is unchanged.
    assert result.changed is False


# --- DB-backed NiceGUI page tests ----------------------------------------------------------


@pytest.fixture
def pg_session():
    """One savepoint-wrapped Session, rolled back at the end. Yields the session so a test can
    seed rows; the page code under test will reuse the SAME session because we monkeypatch
    get_session to return it (see `wire_session`)."""
    from app.db.session import SessionLocal, engine

    conn = engine.connect()
    outer = conn.begin()
    sess = SessionLocal(bind=conn, join_transaction_mode="create_savepoint")
    try:
        yield sess
    finally:
        sess.close()
        outer.rollback()
        conn.close()


@pytest.fixture
def wire_session(pg_session, monkeypatch):
    """Make every `get_session()` the pages open return our one savepoint session, with a no-op
    close so the page's `finally: session.close()` doesn't end the transaction. The pages import
    get_session lazily from app.db.session, so patching there is enough."""
    import app.db.session as db

    class _NonClosing:
        """Proxy that forwards everything to the real session but swallows close()."""

        def __init__(self, real):
            self._real = real

        def __getattr__(self, name):
            return getattr(self._real, name)

        def close(self):  # the page closes its session each action; keep the txn open
            pass

    monkeypatch.setattr(db, "get_session", lambda: _NonClosing(pg_session))
    return pg_session


def _seed_cluster(sess, *, id, status="approved", topic="ai", score=0.9, title="A story"):
    from app.db.models import Cluster

    sess.add(
        Cluster(id=id, status=status, topic=topic, score=score,
                triage_title=title, triage_summary="s")
    )
    sess.flush()


def _seed_article(sess, *, id, piece_type="hot_news", status="drafting", draft=""):
    from app.db.models import Article

    sess.add(Article(id=id, piece_type=piece_type, status=status, current_draft=draft))
    sess.flush()


def _link_cluster(sess, *, article_id, cluster_id):
    """Link a cluster to an article (article_clusters) — the join the SOURCES panel walks to find
    the original items behind the draft."""
    from app.db.models import ArticleCluster

    sess.add(ArticleCluster(article_id=article_id, cluster_id=cluster_id))
    sess.flush()


def _seed_source_item(sess, *, cluster_id, title, source_key="rss:a"):
    """Seed one item in `cluster_id` with a sighting from `source_key` (e.g. "rss:a" → source type
    "rss"), via the real researcher upsert so the row shape matches production. Returns the URL."""
    from app.adapters.base import Item as AdapterItem, item_id
    from app.db.models import Item as ItemModel
    from app.researcher.store import upsert_item_and_sighting

    url = f"https://example.com/src/{uuid.uuid4().hex}"
    upsert_item_and_sighting(sess, AdapterItem(url=url, title=title), source_key)
    sess.flush()
    item = sess.get(ItemModel, item_id(url))
    item.cluster_id = cluster_id
    sess.flush()
    return url


def _seed_edit_log(sess, *, article_id, instruction, draft_snapshot):
    """Append one edit_log row (a draft version) for `article_id`. The version-history panel reads
    these oldest-first."""
    from app.db.models import EditLog

    sess.add(
        EditLog(
            article_id=article_id,
            instruction=instruction,
            draft_snapshot=draft_snapshot,
        )
    )
    sess.flush()


def _seed_owner_source(sess, *, article_id, kind="text", content="owner notes", title=None, url=None):
    """Seed one OwnerSource (Phase 10 flagship grounding) on `article_id`. The SOURCES panel + the
    dashboard surface these as owner material (source_types=["owner"])."""
    from app.db.models import OwnerSource

    row = OwnerSource(
        article_id=article_id, kind=kind, title=title, url=url, content=content
    )
    sess.add(row)
    sess.flush()
    return row.id


# --- dashboard: the unified Stories list + status & source filters --------------------------
#
# The dashboard is one paginated Stories list under TWO cross-filtered filters — a status filter and a
# SOURCE filter — rendered as a COMPACT row per story (no count cards, no ready-to-draft, no recent
# tables). Each row's action buttons are STATUS-AWARE (Change 1): article/digest → Open; cluster
# new/sent → Write → + Skip; cluster approved → Draft →; cluster skipped → none. These tests drive
# `queries.load_stories` / `unified_status_counts` / `source_counts` (the backend half built in
# parallel), so they SKIP until that lands. To stay deterministic regardless of whatever demo/PG rows
# exist, the list/filter + button-matrix tests monkeypatch load_stories + unified_status_counts (and,
# for the source-filter tests, source_counts) to a scripted set; the Write/Skip tests use the REAL
# load_stories + decide (and a scripted writer-agent `generate` for Write) so they assert the actual
# DB transition + draft. The two filters' COUNTS are CROSS-FILTERED (dynamic): picking a status
# re-labels the source toggle via source_counts(status=…), and picking a source re-labels the status
# toggle via unified_status_counts(source=…).


def _story_row(**kw):
    """Build a queries.StoryRow with sensible defaults, overridable per test. Mirrors the backend's
    frozen contract: key/kind/effective_status/title/topic/source_types/original_url/in_digest/
    cluster_id/article_id."""
    base = dict(
        key="cluster:cl:x",
        kind="cluster",
        effective_status="approved",
        title="A story",
        topic="ai",
        source_types=["rss"],
        original_url="https://example.com/x",
        in_digest=False,
        cluster_id="cl:x",
        article_id=None,
    )
    base.update(kw)
    return queries_mod.StoryRow(**base)


@pg_only
@stories_ready
async def test_dashboard_renders_stories_list(user, wire_session, monkeypatch):
    """The dashboard renders the status filter + the paginated Stories list. We script load_stories
    + the counts so the assertion is deterministic (independent of demo rows)."""
    from app.web import queries

    rows = [
        _story_row(key="cluster:cl:a", cluster_id="cl:a", title="Cluster story A",
                   effective_status="approved"),
        _story_row(key="article:a:b", kind="article", cluster_id=None, article_id="a:b",
                   title="Drafted article B", effective_status="drafting", original_url=None),
    ]
    monkeypatch.setattr(queries, "load_stories", lambda session, *, status=None, source=None: rows)
    monkeypatch.setattr(
        queries, "unified_status_counts", lambda session, *, source=None: {"approved": 1, "drafting": 1}
    )

    await user.open("/")
    await user.should_see(marker="status-filter")
    await user.should_see(marker="stories-list")
    await user.should_see("Cluster story A")
    await user.should_see("Drafted article B")


@pg_only
@stories_ready
async def test_dashboard_empty_shows_no_stories(user, wire_session, monkeypatch):
    """An empty filtered result renders the muted "No stories." note (defensive: a query hiccup
    degrades to [] too, so the page never blanks)."""
    from app.web import queries

    monkeypatch.setattr(queries, "load_stories", lambda session, *, status=None, source=None: [])
    monkeypatch.setattr(queries, "unified_status_counts", lambda session, *, source=None: {})

    await user.open("/")
    await user.should_see(marker="stories-empty")
    await user.should_see("No stories.")


@pg_only
@stories_ready
async def test_dashboard_paginates_large_list(user, wire_session, monkeypatch):
    """A list larger than one page renders the client-side paginator. We script load_stories to
    return more rows than _STORIES_PER_PAGE; the paginator control renders and page 1's rows show
    while a later-page row does not (it's sliced off the first page)."""
    from app.web import queries
    from app.web.ui_pages import _STORIES_PER_PAGE

    n = _STORIES_PER_PAGE + 5
    rows = [
        _story_row(
            key=f"cluster:cl:{i}", cluster_id=f"cl:{i}", title=f"Story number {i}",
            effective_status="new",
        )
        for i in range(n)
    ]
    monkeypatch.setattr(queries, "load_stories", lambda session, *, status=None, source=None: rows)
    monkeypatch.setattr(queries, "unified_status_counts", lambda session, *, source=None: {"new": n})

    await user.open("/")
    # The paginator renders (more than one page of rows).
    await user.should_see(marker="stories-pagination")
    # Page-1 rows are present; a row that only appears on page 2 is not in the initial DOM.
    await user.should_see("Story number 0")
    await user.should_see(marker=f"story-cluster:cl:{_STORIES_PER_PAGE - 1}")
    with pytest.raises(AssertionError):
        user.find(marker=f"story-cluster:cl:{_STORIES_PER_PAGE + 1}")


@pg_only
@stories_ready
async def test_dashboard_status_filter_narrows_list(user, wire_session, monkeypatch):
    """Changing the status filter re-queries load_stories(status=…) and rebuilds the list. We capture
    the status arg and return a different row set per status to prove the filter narrows the list."""
    from app.web import queries

    captured = {"status": "unset"}

    def fake_load(session, *, status=None, source=None):
        captured["status"] = status
        if status == "drafting":
            return [_story_row(key="article:a:d", kind="article", cluster_id=None,
                               article_id="a:d", title="Only drafting one",
                               effective_status="drafting", original_url=None)]
        return [
            _story_row(key="cluster:cl:a", cluster_id="cl:a", title="An approved one",
                       effective_status="approved"),
            _story_row(key="article:a:d", kind="article", cluster_id=None, article_id="a:d",
                       title="Only drafting one", effective_status="drafting", original_url=None),
        ]

    monkeypatch.setattr(queries, "load_stories", fake_load)
    monkeypatch.setattr(
        queries, "unified_status_counts", lambda session, *, source=None: {"approved": 1, "drafting": 1}
    )

    await user.open("/")
    await user.should_see("An approved one")
    await user.should_see("Only drafting one")

    # Drive the filter to "drafting" — setting the toggle value inside the client context fires its
    # bound on_value_change handler (the same path a real click takes).
    toggle = next(iter(user.find(marker="status-filter").elements))
    with user.client:
        toggle.set_value("drafting")

    # The list re-queried with status="drafting" and narrowed to just that row. should_see awaits the
    # async filter handler completing, so we assert the captured status AFTER that yield point.
    await user.should_see("Only drafting one")
    assert captured["status"] == "drafting"


@pg_only
@stories_ready
async def test_dashboard_renders_source_filter_with_counts(user, wire_session, monkeypatch):
    """The dashboard renders the SOURCE filter (alongside the status filter, in the slot the topic
    filter used to occupy), each option labelled with its count from `source_counts` — "All (N)" plus
    one per source type. We script source_counts + load_stories so the labels are deterministic. (The
    source filter's "All" is the STORY TOTAL — len(load_stories) — not the sum of the per-source
    counts, which are multi-valued.)"""
    from app.web import queries

    rows = [_story_row(key=f"cluster:cl:{i}", cluster_id=f"cl:{i}") for i in range(7)]
    monkeypatch.setattr(
        queries, "load_stories", lambda session, *, status=None, source=None: rows
    )
    monkeypatch.setattr(
        queries, "unified_status_counts", lambda session, *, source=None: {"new": 1}
    )
    monkeypatch.setattr(
        queries,
        "source_counts",
        lambda session, *, status=None: {
            "rss": 120, "hn": 40, "arxiv": 90, "x_user": 40, "github": 29
        },
    )

    await user.open("/")
    await user.should_see(marker="status-filter")
    await user.should_see(marker="source-filter")
    # The per-source counts are surfaced in the toggle labels, plus the "All (total)" option.
    await user.should_see("rss (120)")
    await user.should_see("hn (40)")
    await user.should_see("arxiv (90)")
    await user.should_see("x_user (40)")
    await user.should_see("github (29)")
    await user.should_see("All (7)")  # the STORY TOTAL (len load_stories), NOT 319 (the per-source sum)


@pg_only
@stories_ready
async def test_dashboard_source_filter_narrows_list(user, wire_session, monkeypatch):
    """Selecting a source re-queries load_stories(source=…) and rebuilds the list. We capture the
    source arg and return a different row set per source to prove the source filter narrows the list."""
    from app.web import queries

    captured = {"source": "unset"}

    def fake_load(session, *, status=None, source=None):
        captured["source"] = source
        if source == "arxiv":
            return [_story_row(key="cluster:cl:arx", cluster_id="cl:arx",
                               title="An arxiv story", source_types=["arxiv"],
                               effective_status="approved")]
        return [
            _story_row(key="cluster:cl:rss", cluster_id="cl:rss", title="An RSS story",
                       source_types=["rss"], effective_status="approved"),
            _story_row(key="cluster:cl:arx", cluster_id="cl:arx", title="An arxiv story",
                       source_types=["arxiv"], effective_status="approved"),
        ]

    monkeypatch.setattr(queries, "load_stories", fake_load)
    monkeypatch.setattr(
        queries, "unified_status_counts", lambda session, *, source=None: {"approved": 2}
    )
    monkeypatch.setattr(
        queries, "source_counts", lambda session, *, status=None: {"rss": 1, "arxiv": 1}
    )

    await user.open("/")
    await user.should_see("An RSS story")
    await user.should_see("An arxiv story")

    # Drive the source filter to "arxiv" — setting the toggle value inside the client context fires its
    # bound (sync) on_value_change handler, the same path a real click takes.
    toggle = next(iter(user.find(marker="source-filter").elements))
    with user.client:
        toggle.set_value("arxiv")

    # The list re-queried with source="arxiv" and narrowed to just that row.
    await user.should_see("An arxiv story")
    assert captured["source"] == "arxiv"


@pg_only
@stories_ready
async def test_dashboard_source_filter_dynamic_status_counts(user, wire_session, monkeypatch):
    """DYNAMIC counts (the key behavior): selecting a STATUS re-labels the SOURCE counts to that
    status's slice. We make source_counts cross-filter on the status it's called with — a status with
    no stories yields zero source counts. We capture the status source_counts is called with and assert
    the source toggle re-renders with the cross-filtered labels after a status pick."""
    from app.web import queries

    captured = {"source_counts_status": "unset"}

    monkeypatch.setattr(
        queries, "load_stories", lambda session, *, status=None, source=None: []
    )
    monkeypatch.setattr(
        queries, "unified_status_counts", lambda session, *, source=None: {"new": 5, "sent": 0}
    )

    def fake_source_counts(session, *, status=None):
        captured["source_counts_status"] = status
        # "new" has stories across sources; "sent" has none (so every source count goes to 0).
        if status == "sent":
            return {}
        return {"rss": 3, "hn": 2}

    monkeypatch.setattr(queries, "source_counts", fake_source_counts)

    await user.open("/")
    await user.should_see(marker="source-filter")
    # Initially (no status filter) the source counts are the unfiltered slice.
    await user.should_see("rss (3)")
    await user.should_see("hn (2)")

    # Pick status="sent" (a status with no stories). The source toggle must REBUILD with the
    # cross-filtered counts — every source count goes to (0) (source_counts({}) → All (0)).
    status_toggle = next(iter(user.find(marker="status-filter").elements))
    with user.client:
        status_toggle.set_value("sent")

    # source_counts was re-queried cross-filtered by the picked status, and the source toggle now
    # shows the empty (zero) slice — only "All (0)" remains, the per-source options are gone.
    await user.should_see("All (0)", marker="source-filter")
    assert captured["source_counts_status"] == "sent"
    with pytest.raises(AssertionError):
        await user.should_see("rss (3)")


@pg_only
@stories_ready
async def test_dashboard_status_and_source_filters_and_together(user, wire_session, monkeypatch):
    """Selecting BOTH a status and a source ANDs the two filters: the final load_stories call carries
    the status AND the source from the two toggles. We capture every (status, source) pair load_stories
    is called with and assert the last reflects both selections, and that only the doubly-matching row
    renders."""
    from app.web import queries

    calls: list[tuple] = []

    def fake_load(session, *, status=None, source=None):
        calls.append((status, source))
        rows = [
            _story_row(key="cluster:cl:rss_app", cluster_id="cl:rss_app",
                       title="RSS approved", source_types=["rss"],
                       effective_status="approved"),
            _story_row(key="article:a:rss_draft", kind="article", cluster_id=None,
                       article_id="a:rss_draft", title="RSS drafting",
                       source_types=["rss"], effective_status="drafting",
                       original_url=None),
            _story_row(key="cluster:cl:hn_app", cluster_id="cl:hn_app",
                       title="HN approved", source_types=["hn"],
                       effective_status="approved"),
        ]
        if status is not None:
            rows = [r for r in rows if r.effective_status == status]
        if source is not None:
            rows = [r for r in rows if source in r.source_types]
        return rows

    monkeypatch.setattr(queries, "load_stories", fake_load)
    monkeypatch.setattr(
        queries,
        "unified_status_counts",
        lambda session, *, source=None: {"approved": 2, "drafting": 1},
    )
    monkeypatch.setattr(
        queries, "source_counts", lambda session, *, status=None: {"rss": 2, "hn": 1}
    )

    await user.open("/")
    await user.should_see("RSS approved")
    await user.should_see("HN approved")

    # Pick status="approved" on the status filter…
    status_toggle = next(iter(user.find(marker="status-filter").elements))
    with user.client:
        status_toggle.set_value("approved")
    await user.should_see("HN approved")  # still both approved rows, RSS + HN

    # …then source="rss" on the source filter. The two filters AND: only the RSS+approved row survives.
    source_toggle = next(iter(user.find(marker="source-filter").elements))
    with user.client:
        source_toggle.set_value("rss")

    await user.should_see("RSS approved")
    # The HN-approved and the RSS-drafting rows are both filtered out (each fails one axis).
    with pytest.raises(AssertionError):
        user.find(marker="story-cluster:cl:hn_app")
    with pytest.raises(AssertionError):
        user.find(marker="story-article:a:rss_draft")
    # The final query carried BOTH the selected status AND the selected source.
    assert calls[-1] == ("approved", "rss")


@pg_only
@stories_ready
async def test_dashboard_approved_cluster_row_shows_draft_only(user, wire_session, monkeypatch):
    """Change 1 matrix: an APPROVED undrafted-cluster row shows ONLY "Draft →" (the cluster is
    already green-lit, so no Write and no Skip). It still renders source-type chips + the
    open-original link + the in-digest badge, and NO score/ratio anywhere."""
    from app.web import queries

    rows = [
        _story_row(
            key="cluster:cl:act", cluster_id="cl:act", title="Undrafted cluster",
            effective_status="approved", source_types=["hn", "rss"],
            original_url="https://example.com/orig", in_digest=True,
        )
    ]
    monkeypatch.setattr(queries, "load_stories", lambda session, *, status=None, source=None: rows)
    monkeypatch.setattr(queries, "unified_status_counts", lambda session, *, source=None: {"approved": 1})

    await user.open("/")
    await user.should_see("Undrafted cluster")
    # Approved cluster → Draft only; NOT Write, NOT Skip.
    await user.should_see(marker="draft-cl:act")
    with pytest.raises(AssertionError):
        user.find(marker="write-cl:act")
    with pytest.raises(AssertionError):
        user.find(marker="skip-cl:act")
    # Source-type chips render (one per source_type).
    await user.should_see(marker="src-cluster:cl:act-hn")
    await user.should_see(marker="src-cluster:cl:act-rss")
    # The open-original link is present (opens in a new tab) and the in-digest badge shows.
    await user.should_see(marker="open-original-cluster:cl:act")
    await user.should_see(marker="in-digest-cluster:cl:act")
    link = next(iter(user.find(marker="open-original-cluster:cl:act").elements))
    assert link._props.get("target") == "_blank"

    # NO score/ratio anywhere on the page (it is deliberately absent from the owner-facing list).
    rendered = " ".join(
        str(getattr(el, "text", "") or "") for el in user.client.layout.descendants()
    )
    assert "score" not in rendered.lower()
    assert "ratio" not in rendered.lower()


@pg_only
@stories_ready
async def test_dashboard_new_cluster_row_shows_write_and_skip(user, wire_session, monkeypatch):
    """Change 1 matrix: a NEW (or SENT) undrafted-cluster row shows "Write →" + "Skip", and NOT
    "Draft →" (drafting is only valid AFTER approve+fetch — the old always-on Draft would raise)."""
    from app.web import queries

    rows = [
        _story_row(
            key="cluster:cl:new", cluster_id="cl:new", title="A fresh cluster",
            effective_status="new",
        )
    ]
    monkeypatch.setattr(queries, "load_stories", lambda session, *, status=None, source=None: rows)
    monkeypatch.setattr(queries, "unified_status_counts", lambda session, *, source=None: {"new": 1})

    await user.open("/")
    await user.should_see("A fresh cluster")
    await user.should_see(marker="write-cl:new")
    await user.should_see(marker="skip-cl:new")
    with pytest.raises(AssertionError):
        user.find(marker="draft-cl:new")


@pg_only
@stories_ready
async def test_dashboard_skipped_cluster_row_has_no_actions(user, wire_session, monkeypatch):
    """Change 1 matrix: a SKIPPED undrafted-cluster row shows NO action buttons (just the status chip
    + the open-original link). None of Write / Draft / Skip render."""
    from app.web import queries

    rows = [
        _story_row(
            key="cluster:cl:skip", cluster_id="cl:skip", title="A skipped cluster",
            effective_status="skipped", original_url="https://example.com/skip",
        )
    ]
    monkeypatch.setattr(queries, "load_stories", lambda session, *, status=None, source=None: rows)
    monkeypatch.setattr(queries, "unified_status_counts", lambda session, *, source=None: {"skipped": 1})

    await user.open("/")
    await user.should_see("A skipped cluster")
    # The open-original link is still there (read-only convenience), but no action buttons.
    await user.should_see(marker="open-original-cluster:cl:skip")
    with pytest.raises(AssertionError):
        user.find(marker="write-cl:skip")
    with pytest.raises(AssertionError):
        user.find(marker="draft-cl:skip")
    with pytest.raises(AssertionError):
        user.find(marker="skip-cl:skip")


@pg_only
@stories_ready
async def test_dashboard_article_row_shows_open(user, wire_session, monkeypatch):
    """A drafted (article/digest) row shows an Open button (jump to its editor) and NOT the Gate-1
    Write/Draft/Skip controls."""
    from app.web import queries

    rows = [
        _story_row(
            key="article:a:open", kind="article", cluster_id=None, article_id="a:open",
            title="Drafted piece", effective_status="pre_publish", original_url=None,
        )
    ]
    monkeypatch.setattr(queries, "load_stories", lambda session, *, status=None, source=None: rows)
    monkeypatch.setattr(queries, "unified_status_counts", lambda session, *, source=None: {"pre_publish": 1})

    await user.open("/")
    await user.should_see("Drafted piece")
    await user.should_see(marker="open-article:a:open")


@pg_only
@stories_ready
async def test_dashboard_write_transitions_cluster_and_drafts(user, wire_session, monkeypatch):
    """Clicking "Write →" on a NEW cluster runs the REAL chain decide→fetch→create→draft and reaches
    the editor. We seed a `new` cluster WITH source full_text and script the writer-agent `generate`
    so no live model is hit (mirrors test_draft_button_runs_agent_and_opens_editor). After the click
    the DB row moved new → approved (decide's effect; Postgres is the source of truth) and the fresh
    draft renders in the editor we navigate to."""
    from app.adapters.base import Item as AdapterItem, item_id
    from app.db.models import Cluster, Item as ItemModel
    from app.editor import draft as draft_mod
    from app.researcher.store import upsert_item_and_sighting
    from app.web import queries

    sess = wire_session
    cid = "cl:ng_write"
    _seed_cluster(sess, id=cid, status="new", topic="ai", score=0.7, title="Write me")
    url = f"https://example.com/src/{uuid.uuid4().hex}"
    upsert_item_and_sighting(sess, AdapterItem(url=url, title="Source headline"), "rss:a")
    sess.flush()
    item = sess.get(ItemModel, item_id(url))
    item.cluster_id = cid
    item.full_text = "A grounded source fact for the draft."
    sess.flush()

    # Use the REAL load_stories so the seeded `new` cluster shows its Write button.
    monkeypatch.setattr(queries, "unified_status_counts", lambda session, *, source=None: {"new": 1})

    # Script generate: a final text draft on turn 1 (no tools, no model).
    def fake_generate(messages, role="generation", tools=None, system=None, **kwargs):
        return SimpleNamespace(content=[SimpleNamespace(type="text", text="# Written\n\nbody")])

    monkeypatch.setattr(draft_mod, "generate", fake_generate)

    await user.open("/")
    await user.should_see("Write me")
    await user.should_see(marker=f"write-{cid}")

    user.find(marker=f"write-{cid}").click()

    # The chain decides (new → approved) — assert the real DB transition. The chain runs in a worker
    # thread (run.io_bound) sharing this savepoint session, so poll briefly for visibility.
    final = None
    for _ in range(40):
        sess.expire_all()
        final = sess.get(Cluster, cid).status
        if final == "approved":
            break
        await asyncio.sleep(0.05)
    assert final == "approved"
    # …and it reaches the editor on the freshly-drafted article (scripted generate output renders).
    await user.should_see("Written")
    await user.should_see(marker="preview")


@pg_only
@stories_ready
async def test_dashboard_skip_transitions_cluster_and_refreshes(user, wire_session):
    """Clicking "Skip" on a NEW/SENT undrafted-cluster row runs the REAL Gate-1 write (decide →
    skipped) and refreshes the list. We seed a `sent` cluster, use the REAL load_stories so the row
    appears, click Skip, and assert the DB row moved to `skipped` (Postgres is the source of truth)."""
    from app.db.models import Cluster

    sess = wire_session
    cid = "cl:ng_dash_skip"
    _seed_cluster(sess, id=cid, status="sent", topic="ai", score=0.7, title="Skip me")

    await user.open("/")
    await user.should_see("Skip me")
    await user.should_see(marker=f"skip-{cid}")

    user.find(marker=f"skip-{cid}").click()

    # The DB row is actually moved to skipped (the real decide() transition). The Skip runs in a
    # worker thread (run.io_bound) sharing this savepoint session, so poll briefly for visibility.
    final = None
    for _ in range(20):
        sess.expire_all()
        final = sess.get(Cluster, cid).status
        if final == "skipped":
            break
        await asyncio.sleep(0.05)
    assert final == "skipped"


# --- editor ---------------------------------------------------------------------------------


@pg_only
async def test_editor_renders_existing_draft(user, wire_session):
    _seed_article(wire_session, id="a:ng_view", status="drafting",
                  draft="# Title\n\nbody text here.")
    await user.open("/editor/a:ng_view")
    await user.should_see(marker="editor")          # the two-pane splitter
    await user.should_see(marker="chat-input")       # chat composer
    await user.should_see(marker="preview")          # live markdown preview
    await user.should_see(marker="draft-textarea")   # raw hand-edit textarea
    await user.should_see(marker="save-edits")       # save control
    await user.should_see("body text here")          # the draft rendered in the preview


@pg_only
async def test_editor_unknown_article_shows_not_found(user, wire_session):
    await user.open("/editor/a:does-not-exist")
    await user.should_see(marker="not-found")
    await user.should_see("not found")


@pg_only
async def test_editor_empty_draft_renders_placeholder(user, wire_session):
    _seed_article(wire_session, id="a:ng_empty", status="drafting", draft="")
    await user.open("/editor/a:ng_empty")
    await user.should_see(marker="editor")
    await user.should_see("This draft is empty")


# --- the Draft action path (create + writer-agent draft) ------------------------------------


@pg_only
async def test_draft_button_runs_agent_and_opens_editor(user, wire_session, monkeypatch):
    """Click Draft on an approved cluster (seeded WITH source full_text) → the writer-agent runs
    (generate scripted to a final draft on turn 1) → the editor opens on the fresh draft."""
    from app.adapters.base import Item as AdapterItem, item_id
    from app.db.models import Item as ItemModel
    from app.editor import draft as draft_mod
    from app.researcher.store import upsert_item_and_sighting

    sess = wire_session
    cid = "cl:ng_draftable"
    _seed_cluster(sess, id=cid, status="approved", topic="ai", score=0.8, title="Draftable")
    url = f"https://example.com/src/{uuid.uuid4().hex}"
    upsert_item_and_sighting(sess, AdapterItem(url=url, title="Source headline"), "rss:a")
    sess.flush()
    item = sess.get(ItemModel, item_id(url))
    item.cluster_id = cid
    item.full_text = "A grounded source fact for the draft."
    sess.flush()

    # Script generate: a final text draft on turn 1 (no tools, no model).
    def fake_generate(messages, role="generation", tools=None, system=None, **kwargs):
        return SimpleNamespace(content=[SimpleNamespace(type="text", text="# NG Draft\n\nbody")])

    monkeypatch.setattr(draft_mod, "generate", fake_generate)

    await user.open("/")
    await user.should_see(marker=f"draft-{cid}")
    user.find(marker=f"draft-{cid}").click()
    # The action navigates to the new editor view, where the fresh draft renders.
    await user.should_see("NG Draft")
    await user.should_see(marker="preview")


@pg_only
async def test_draft_button_surfaces_no_text_refusal(user, wire_session):
    """An approved cluster with NO fetched source text → the writer-agent refuses (grounding has
    nothing to stand on); the UI shows the refusal as a notify and stays on the dashboard."""
    sess = wire_session
    cid = "cl:ng_notext"
    _seed_cluster(sess, id=cid, status="approved", topic="ai", score=0.7, title="No text yet")

    await user.open("/")
    user.find(marker=f"draft-{cid}").click()
    # The refusal message is surfaced (notify); we stay on the dashboard (no navigation).
    # (Phase 10 relaxed the guard to the empty-grounding-union case; the message now names the
    # missing grounding corpus.)
    await user.should_see("no grounding corpus")


# --- Phase-4 editor: chat iterate, piece-type switch, Gate-2 approve ------------------------
#
# These drive the editor page's new controls. They monkeypatch the iterate SEAM the UI calls
# (`app.web.chat.handle_editor_message`) to a scripted IterateResult — the frontend's contract is
# the seam boundary; the writer-agent itself (model + DB write + edit_log append) is the backend's
# slice and is unit-tested there. `approve_article` IS the real backend call (a small DB-only
# transition), so the Gate-2 test asserts the actual articles.status row.


def _fake_iterate_result(*, reply, draft, piece_type="hot_news", changed=True):
    """Build a scripted IterateResult (the seam's frozen return type) for the iterate-path tests."""
    return chat_seam.IterateResult(
        reply=reply, draft=draft, piece_type=piece_type, changed=changed
    )


@pg_only
@new_seam_only
async def test_editor_chat_iterate_refreshes_preview(user, wire_session, monkeypatch):
    """Sending a chat instruction on a NON-empty draft routes to the iterate seam and refreshes the
    live preview to the revised draft. We monkeypatch handle_editor_message to a scripted result and
    capture its kwargs to assert the owner's textarea value is passed as base_draft (manual edits
    are sacred — the agent must edit what the owner currently sees, even if unsaved)."""
    _seed_article(
        wire_session, id="a:ng_iter", status="drafting", draft="# Title\n\noriginal body."
    )

    captured = {}

    def fake_handle(article_id, instruction, *, base_draft=None, new_piece_type=None):
        captured["article_id"] = article_id
        captured["instruction"] = instruction
        captured["base_draft"] = base_draft
        captured["new_piece_type"] = new_piece_type
        return _fake_iterate_result(
            reply="tightened the intro",
            draft="# Title\n\nrevised body after iterate.",
        )

    monkeypatch.setattr(chat_seam, "handle_editor_message", fake_handle)

    await user.open("/editor/a:ng_iter")
    await user.should_see("original body")  # the starting draft renders in the preview

    user.find(marker="chat-input").type("tighten the intro")
    user.find(marker="chat-send").click()

    # The preview refreshes to the seam's revised draft (edit-in-place result rendered).
    await user.should_see("revised body after iterate")
    await user.should_see("tightened the intro")  # the agent's reply as a chat bubble

    # The seam received the article id, the instruction, and the current draft as base_draft
    # (manual-edit respect); no piece-type switch was requested.
    assert captured["article_id"] == "a:ng_iter"
    assert captured["instruction"] == "tighten the intro"
    assert "original body" in (captured["base_draft"] or "")
    assert captured["new_piece_type"] is None


@pg_only
@new_seam_only
async def test_editor_piece_type_switch_reformats_preview(user, wire_session, monkeypatch):
    """Changing the piece-type selector runs a structural reformat through the iterate seam with
    new_piece_type set, and refreshes the preview to the reformatted draft."""
    _seed_article(
        wire_session, id="a:ng_switch", piece_type="hot_news", status="drafting",
        draft="# Hot news\n\nbody.",
    )

    captured = {}

    def fake_handle(article_id, instruction, *, base_draft=None, new_piece_type=None):
        captured["new_piece_type"] = new_piece_type
        captured["base_draft"] = base_draft
        return _fake_iterate_result(
            reply="reformatted",
            draft="# Project post\n\nreformatted as a project post.",
            piece_type=new_piece_type or "hot_news",
        )

    monkeypatch.setattr(chat_seam, "handle_editor_message", fake_handle)

    await user.open("/editor/a:ng_switch")
    await user.should_see(marker="piece-type-select")

    # Drive the select to a new piece type. Setting `.value` inside the client context fires the
    # bound on_value_change handler (the same path a real selection takes), exactly as NiceGUI's
    # own `trigger`/`type` interactions run inside `user.client`.
    select = next(iter(user.find(marker="piece-type-select").elements))
    with user.client:
        select.set_value("project_post")

    # The reformat runs and the preview reflects the new structure.
    await user.should_see("reformatted as a project post")
    assert captured["new_piece_type"] == "project_post"
    assert "body" in (captured["base_draft"] or "")  # the current draft is the reformat base


@pg_only
async def test_editor_gate2_approve_moves_to_pre_publish(user, wire_session):
    """The Gate-2 Approve control moves a drafting article → pre_publish (the real backend call),
    and the header status chip reflects the new status. NOT publishing — pre_publish is the last
    status this UI sets."""
    from app.db.models import Article

    sess = wire_session
    _seed_article(sess, id="a:ng_gate2", status="drafting", draft="# Ready\n\nbody to approve.")

    await user.open("/editor/a:ng_gate2")
    await user.should_see(marker="approve-gate2")
    await user.should_see(marker="article-status")

    user.find(marker="approve-gate2").click()

    # The status chip reflects the Gate-2 transition…
    await user.should_see("pre_publish")
    # …and the DB row is actually moved (Postgres is the source of truth).
    sess.expire_all()
    assert sess.get(Article, "a:ng_gate2").status == "pre_publish"


# --- Phase-5 editor: variants + mark-as-published -------------------------------------------
#
# These drive the editor page's new Phase-5 controls. The variant-generation test monkeypatches the
# variants seam the UI lazy-imports (`app.variants.generate_variant`) to a scripted VariantResult —
# the frontend's contract is that seam boundary; the single model call itself is the backend's
# slice. The mark-as-published test uses the REAL `publish_article` (a small DB transition + KB
# embedding), monkeypatching only the embed provider so no live embedding backend is needed. Both
# are guarded so they SKIP (not fail) until the backend half lands.


@pg_only
async def test_editor_renders_variants_and_publish_controls(user, wire_session):
    """A pre_publish article's editor renders the Phase-5 controls: the Mark-as-published button,
    the variants section, and a per-platform Generate button. (No backend call — pure render.)"""
    _seed_article(
        wire_session, id="a:ng_p5render", status="pre_publish",
        draft="# Approved\n\nready to format.",
    )
    await user.open("/editor/a:ng_p5render")
    await user.should_see(marker="mark-published")
    await user.should_see(marker="variants-section")
    await user.should_see(marker="gen-variant-medium")
    await user.should_see(marker="variant-out-medium")


@pg_only
async def test_editor_drafting_disables_phase5_controls(user, wire_session):
    """Gating: a DRAFTING article (pre Gate 2) renders the Phase-5 controls but they are DISABLED —
    mark-published (must approve first) and the variant Generate buttons (variants are derived after
    Gate 2). The gate hint is shown."""
    _seed_article(
        wire_session, id="a:ng_p5gate", status="drafting", draft="# Draft\n\nstill drafting.",
    )
    await user.open("/editor/a:ng_p5gate")
    await user.should_see(marker="mark-published")
    await user.should_see(marker="gen-variant-medium")
    await user.should_see(marker="variants-gate-hint")

    # The rendered controls are disabled while the article is still drafting.
    publish_btn = next(iter(user.find(marker="mark-published").elements))
    assert publish_btn.enabled is False
    gen_btn = next(iter(user.find(marker="gen-variant-medium").elements))
    assert gen_btn.enabled is False


@pg_only
@variants_ready
async def test_editor_generate_variant_shows_output(user, wire_session, monkeypatch):
    """Clicking "Generate Medium" runs the variants seam off the event loop and shows the formatted
    text in the read-only output area. We monkeypatch the seam the UI lazy-imports
    (`app.variants.generate_variant`) to a scripted VariantResult, so no model/DB call is made — the
    frontend's contract is the seam boundary. Because the UI does `from app.variants import
    generate_variant` INSIDE the worker, we patch the attribute on the app.variants package."""
    import app.variants as variants_mod

    _seed_article(
        wire_session, id="a:ng_genvar", status="pre_publish",
        draft="# Canonical\n\nbody to format.",
    )

    def fake_generate(session, article_id, platform):
        return variants_mod.VariantResult(
            article_id=article_id,
            platform=platform,
            formatted_text="MEDIUM VARIANT TEXT for copy-out.",
            variant_id=1,
        )

    monkeypatch.setattr(variants_mod, "generate_variant", fake_generate)

    await user.open("/editor/a:ng_genvar")
    await user.should_see(marker="gen-variant-medium")
    user.find(marker="gen-variant-medium").click()
    await user.should_see("MEDIUM VARIANT TEXT for copy-out")


@pg_only
async def test_editor_variant_field_is_editable(user, wire_session):
    """The per-platform variant output field is now EDITABLE (the owner hand-tunes it inline), and a
    per-platform Save button is present. Pure render — no backend call. We assert the textarea element
    carries NO `readonly` prop and that the save-variant-medium button rendered."""
    _seed_article(
        wire_session, id="a:ng_vedit", status="pre_publish",
        draft="# Approved\n\nready to format.",
    )
    await user.open("/editor/a:ng_vedit")
    await user.should_see(marker="variant-out-medium")
    await user.should_see(marker="save-variant-medium")

    # The output textarea must NOT be readonly (hand-tunable). NiceGUI textarea props are a dict;
    # `readonly` would appear as a key when set — assert it is absent.
    out = next(iter(user.find(marker="variant-out-medium").elements))
    assert "readonly" not in out._props


@pg_only
@save_variant_ready
async def test_editor_save_variant_persists_edit(user, wire_session):
    """Typing into the (now editable) Medium variant field and clicking "Save Medium" persists the
    text via the REAL backend `save_variant_edit` (no model needed — it's a plain DB write). We read
    it back through `app.variants.latest_variant` to assert it landed. The save runs in a worker
    thread (run.io_bound) sharing this savepoint session, so its commit can become visible a beat
    after the notify — poll briefly rather than assert on the first read (mirrors the publish test)."""
    import app.variants as variants_mod

    sess = wire_session
    _seed_article(
        sess, id="a:ng_vsave", status="pre_publish", draft="# Canonical\n\nbody to format.",
    )

    await user.open("/editor/a:ng_vsave")
    await user.should_see(marker="variant-out-medium")

    edited = "Hand-tuned MEDIUM variant the owner edited inline."
    out = next(iter(user.find(marker="variant-out-medium").elements))
    with user.client:
        out.set_value(edited)
    user.find(marker="save-variant-medium").click()

    # The save handler echoes the saved text back into the field on success.
    await user.should_see("Hand-tuned MEDIUM variant")

    # …and the DB has it (Postgres is the source of truth). Poll briefly for cross-thread visibility.
    persisted = None
    for _ in range(20):
        sess.expire_all()
        latest = variants_mod.latest_variant(sess, "a:ng_vsave", "medium")
        if latest is not None:
            persisted = latest.formatted_text
            break
        await asyncio.sleep(0.05)
    assert persisted == edited


@pg_only
@publish_ready
async def test_editor_mark_published_flips_status(user, wire_session, monkeypatch):
    """The Mark-as-published control moves a pre_publish article → published via the REAL backend
    (`publish_article`), and the header status chip reflects it. This is BOOKKEEPING of an external
    manual publish — it flips status + builds the KB embedding; it never posts. We monkeypatch the
    embed provider (the module-level seam in app.editor.article) so the real publish_article runs
    without a live embedding backend."""
    from app.db.models import Article
    from app.editor import article as article_mod
    from app.llm.config import EMBEDDING_DIM

    sess = wire_session
    _seed_article(
        sess, id="a:ng_pub", status="pre_publish", draft="# Done\n\nposted manually elsewhere.",
    )

    # publish_article calls `embed(canonical)[0]` with the single canonical string. Return one
    # zero-vector of the right width so the real publish_article runs without a live embedding
    # provider (mirrors the Gate-2 test using the real backend).
    def fake_embed(text):
        texts = [text] if isinstance(text, str) else list(text)
        return [[0.0] * EMBEDDING_DIM for _ in texts]

    monkeypatch.setattr(article_mod, "embed", fake_embed)

    await user.open("/editor/a:ng_pub")
    await user.should_see(marker="mark-published")

    user.find(marker="mark-published").click()

    # The status chip reflects the published transition. We assert on the chip element specifically
    # (marker="article-status") rather than a bare "published" text match — the word appears in the
    # button tooltip too, and we wait for the async click handler to flip the chip.
    await user.should_see("published", marker="article-status")

    # …and the DB row is actually moved (Postgres is the source of truth). The publish runs in a
    # worker thread (run.io_bound) sharing this savepoint session, so its commit can become visible
    # a beat after the chip updates — poll briefly rather than assert on the first read.
    final = None
    for _ in range(20):
        sess.expire_all()
        final = sess.get(Article, "a:ng_pub").status
        if final == "published":
            break
        await asyncio.sleep(0.05)
    assert final == "published"


# --- editor: SOURCES panel + VERSION HISTORY panel ------------------------------------------
#
# These drive the two new right-column panels. Both depend on the read helpers the backend slice
# adds (`queries.load_article_sources` / `load_article_versions`), which the editor page calls at
# render time, and the restore test additionally on `app.editor.restore_article_version`. They are
# guarded so they SKIP (not fail) until those land; the module-import smoke test below has no backend
# dependency and always runs. Everything here is read/restore/inspect only — the system never posts.


def test_history_panel_module_imports_and_diff_is_python():
    """DB-free smoke: the frontend module imports cleanly (the panel builders + diff/restore helpers
    exist) regardless of whether the backend read helpers have landed, and the unified diff is
    computed IN PYTHON (added lines green, removed lines red)."""
    import app.web.ui_pages as ui_pages

    assert hasattr(ui_pages, "_build_sources_panel")
    assert hasattr(ui_pages, "_build_history_panel")
    assert hasattr(ui_pages, "_on_restore_click")

    diff_html = ui_pages._unified_diff_html(
        "alpha\nbeta\n", "alpha\ngamma\n", from_label="#1", to_label="#2"
    )
    # Added line carries the green colour; removed line carries the red colour (Python difflib).
    assert "#15803d" in diff_html  # green-700 for the added "gamma"
    assert "#b91c1c" in diff_html  # red-700 for the removed "beta"
    assert "gamma" in diff_html and "beta" in diff_html

    # Identical drafts → no changes message (still in-Python, no crash).
    same = ui_pages._unified_diff_html("x\n", "x\n", from_label="#1", to_label="#2")
    assert "No changes" in same


@pg_only
@history_render_ready
async def test_editor_sources_panel_renders_links(user, wire_session):
    """An article whose linked cluster has source items renders the SOURCES panel with a clickable
    link per original article (opened in a new tab) and a source-type chip. The link text is the
    item title; the URL is the original article (read-only — the system never posts)."""
    sess = wire_session
    _seed_cluster(sess, id="cl:ng_src", status="approved", topic="ai", title="Sourced story")
    _seed_article(sess, id="a:ng_src", status="drafting", draft="# Draft\n\nbody.")
    _link_cluster(sess, article_id="a:ng_src", cluster_id="cl:ng_src")
    _seed_source_item(
        sess, cluster_id="cl:ng_src", title="The original headline", source_key="rss:a"
    )

    await user.open("/editor/a:ng_src")
    await user.should_see(marker="sources-panel")
    await user.should_see("The original headline")  # the source link text

    # The link opens in a NEW TAB (the owner re-reads the source without leaving the editor).
    link = next(iter(user.find("The original headline").elements))
    assert link._props.get("target") == "_blank"


@pg_only
@history_render_ready
async def test_editor_sources_panel_empty_when_no_links(user, wire_session):
    """An article with no linked clusters/items renders the SOURCES panel with the muted empty
    placeholder (load_article_sources returns [])."""
    _seed_article(wire_session, id="a:ng_nosrc", status="drafting", draft="# Draft\n\nbody.")
    await user.open("/editor/a:ng_nosrc")
    await user.should_see(marker="sources-panel")
    await user.should_see(marker="sources-empty")
    await user.should_see("No source links for this article")


@pg_only
@history_render_ready
async def test_editor_history_panel_lists_versions(user, wire_session):
    """The VERSION HISTORY panel lists the article's draft versions (the edit_log entries) with their
    instructions, plus a per-version View-diff and Restore button (the latter for non-only versions)."""
    sess = wire_session
    _seed_article(
        sess, id="a:ng_hist", status="drafting", draft="# v2\n\nsecond version body."
    )
    _seed_edit_log(
        sess, article_id="a:ng_hist", instruction="draft the canonical",
        draft_snapshot="# v1\n\nfirst version body.",
    )
    _seed_edit_log(
        sess, article_id="a:ng_hist", instruction="tighten the intro",
        draft_snapshot="# v2\n\nsecond version body.",
    )

    await user.open("/editor/a:ng_hist")
    await user.should_see(marker="history-panel")
    await user.should_see("tighten the intro")  # the latest instruction shows in a row
    await user.should_see("draft the canonical")  # the earlier instruction shows too
    # Per-version diff buttons render (seq-marked so tests can target a specific version).
    await user.should_see(marker="diff-2")


@pg_only
@restore_ready
async def test_editor_restore_changes_draft_and_refreshes_preview(user, wire_session):
    """Clicking Restore on an earlier version calls the REAL `restore_article_version` (a draft
    mutation that also logs the restore to edit_log), which flips current_draft back to that version;
    the live preview refreshes to the restored text and the DB row reflects it (source of truth)."""
    from app.db.models import Article

    sess = wire_session
    _seed_article(
        sess, id="a:ng_restore", status="drafting", draft="# v2\n\nlatest body to undo.",
    )
    _seed_edit_log(
        sess, article_id="a:ng_restore", instruction="draft the canonical",
        draft_snapshot="# v1\n\nthe earlier body to restore.",
    )
    _seed_edit_log(
        sess, article_id="a:ng_restore", instruction="rewrite body",
        draft_snapshot="# v2\n\nlatest body to undo.",
    )

    await user.open("/editor/a:ng_restore")
    await user.should_see(marker="history-panel")
    await user.should_see("latest body to undo")  # the current draft renders in the preview

    # Restore the FIRST (genesis-ish / seq 1) version — the earlier body.
    await user.should_see(marker="restore-1")
    user.find(marker="restore-1").click()

    # The preview refreshes to the restored (earlier) text — edit-in-place, never a new generation.
    await user.should_see("the earlier body to restore")

    # …and the DB row is actually moved back (Postgres is the source of truth). The restore runs in a
    # worker thread (run.io_bound) sharing this savepoint session, so poll briefly for visibility.
    restored = None
    for _ in range(20):
        sess.expire_all()
        restored = sess.get(Article, "a:ng_restore").current_draft
        if restored and "earlier body to restore" in restored:
            break
        await asyncio.sleep(0.05)
    assert restored is not None and "the earlier body to restore" in restored


# --- Phase 10: flagship intake (own-material → canonical draft) -----------------------------
#
# The dashboard's "New piece from my material" button mints a cluster-less FLAGSHIP article from the
# owner's OWN material (pasted text / an uploaded file / a URL), drafts it, and opens its editor; the
# editor's "Attach material" control adds more owner material to the currently-open article (the
# fusion / add-more path). Owner material renders with a distinct "owner" chip on both surfaces. These
# drive the Phase-10 backend (`app.editor.create_flagship_article` + the attach helpers), which the UI
# CALLS; they SKIP (not fail) until that backend lands. The new-piece flow uses the REAL flagship
# chain with a SCRIPTED `app.editor.draft.generate` (a final draft on turn 1, no live model), so it
# asserts the actual flagship article + draft landed and the page navigated into its editor.

_FLAGSHIP_READY = (
    hasattr(editor_mod, "create_flagship_article")
    and hasattr(editor_mod, "attach_owner_source")
    and hasattr(editor_mod, "parse_uploaded_file")
)
flagship_ready = pytest.mark.skipif(
    not _FLAGSHIP_READY,
    reason="Phase-10 flagship intake backend (app.editor.create_flagship_article + attach helpers) "
    "not landed yet",
)


def test_intake_helpers_exist_and_owner_chip_is_distinct():
    """DB-free smoke: the Phase-10 frontend pieces exist (the intake builders + submit cores) and the
    owner source-type chip is a DISTINCT colour from the neutral pipeline-source chip — so a flagship
    piece's own-material provenance stands out at a glance on both the dashboard and the Sources panel."""
    import app.web.ui_pages as ui_pages

    assert hasattr(ui_pages, "_build_new_piece_entry")
    assert hasattr(ui_pages, "_build_attach_material_control")
    assert hasattr(ui_pages, "_build_intake_dialog")
    assert hasattr(ui_pages, "_create_flagship_and_draft")
    assert hasattr(ui_pages, "_attach_owner_material")

    owner_color = ui_pages._source_chip_color("owner")
    pipeline_color = ui_pages._source_chip_color("rss")
    assert owner_color != pipeline_color  # owner material reads distinctly


@pg_only
async def test_dashboard_renders_new_piece_button(user, wire_session, monkeypatch):
    """The dashboard surfaces the "New piece from my material" entry point near the filter bar. We
    script load_stories/counts so the render is deterministic regardless of demo rows."""
    from app.web import queries

    monkeypatch.setattr(queries, "load_stories", lambda session, *, status=None, source=None: [])
    monkeypatch.setattr(queries, "unified_status_counts", lambda session, *, source=None: {})

    await user.open("/")
    await user.should_see(marker="new-piece-button")


@pg_only
@stories_ready
async def test_dashboard_flagship_row_shows_owner_chip(user, wire_session, monkeypatch):
    """A flagship article surfaces on the dashboard as an article row carrying source_types=["owner"];
    the row's source chips render an "owner" chip (distinct from the pipeline-source chips). We script
    load_stories to return one such row so the assertion is deterministic."""
    from app.web import queries

    rows = [
        _story_row(
            key="article:a:flag", kind="article", cluster_id=None, article_id="a:flag",
            title="My flagship explainer", effective_status="drafting", topic="—",
            source_types=["owner"], original_url=None,
        )
    ]
    monkeypatch.setattr(queries, "load_stories", lambda session, *, status=None, source=None: rows)
    monkeypatch.setattr(queries, "unified_status_counts", lambda session, *, source=None: {"drafting": 1})

    await user.open("/")
    await user.should_see("My flagship explainer")
    # The "owner" source chip renders for the flagship row (marked src-<key>-owner like any chip).
    await user.should_see(marker="src-article:a:flag-owner")


@pg_only
async def test_new_piece_dialog_validates_empty_inputs(user, wire_session, monkeypatch):
    """Opening the dialog and submitting with NO material → a negative notify and NO article created.
    We patch create_flagship_article so we can assert it was never called (the validation guards it)."""
    from app.editor import sources as sources_mod

    called = {"n": 0}

    def fake_create(session, *, piece_type="tech_explainer"):
        called["n"] += 1
        return "a:should-not-happen"

    # The submit core does `from app.editor import create_flagship_article`, which resolves to the
    # function object on app.editor (re-exported from app.editor.sources). Patch both so neither path
    # mints an article.
    monkeypatch.setattr(editor_mod, "create_flagship_article", fake_create)
    monkeypatch.setattr(sources_mod, "create_flagship_article", fake_create)

    await user.open("/")
    await user.should_see(marker="new-piece-button")
    user.find(marker="new-piece-button").click()
    # The dialog opens with its inputs.
    await user.should_see(marker="new-piece-text")
    await user.should_see(marker="new-piece-submit")

    # Submit with nothing filled → validation refuses, no article minted.
    user.find(marker="new-piece-submit").click()
    await user.should_see("Add at least one of")
    assert called["n"] == 0


@pg_only
@flagship_ready
async def test_new_piece_creates_flagship_drafts_and_navigates(
    user, wire_session, monkeypatch
):
    """The end-to-end new-piece flow: open the dialog, paste text, submit → the REAL flagship chain
    runs (create_flagship_article → attach_owner_source → draft_article) with a SCRIPTED
    `app.editor.draft.generate` so no live model is hit, and the page navigates into the new editor on
    the fresh draft. We then read the DB back to assert a flagship article exists with a draft and is
    surfaced as a kind='article' / source_types=['owner'] story (load_stories) — the flagship contract."""
    from app.editor import draft as draft_mod
    from app.web import queries

    sess = wire_session

    # Script generate: a final text draft on turn 1 (no tools, no model) — same seam the Write/Draft
    # tests use. The flagship draft_article grounds on the attached owner material.
    def fake_generate(messages, role="generation", tools=None, system=None, **kwargs):
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text="# Flagship\n\ndrafted from my material.")]
        )

    monkeypatch.setattr(draft_mod, "generate", fake_generate)

    await user.open("/")
    await user.should_see(marker="new-piece-button")
    user.find(marker="new-piece-button").click()
    await user.should_see(marker="new-piece-text")

    # Paste owner notes and submit.
    user.find(marker="new-piece-text").type("These are my own notes about the new release.")
    user.find(marker="new-piece-submit").click()

    # The flagship chain runs and navigates into the editor on the fresh draft (scripted output).
    await user.should_see("drafted from my material")
    await user.should_see(marker="preview")

    # A flagship article now exists with a draft and is surfaced as an owner-material story. The chain
    # ran in a worker thread (run.io_bound) sharing this savepoint session, so poll for visibility.
    flagship = None
    for _ in range(40):
        sess.expire_all()
        stories = queries.load_stories(sess)
        for s in stories:
            if (
                s.kind == "article"
                and s.source_types == ["owner"]
                and s.article_id is not None
            ):
                view = queries.load_article(sess, s.article_id)
                if view is not None and "drafted from my material" in (view.current_draft or ""):
                    flagship = view
                    break
        if flagship is not None:
            break
        await asyncio.sleep(0.05)
    assert flagship is not None
    assert flagship.piece_type == "tech_explainer"  # the flagship default


@pg_only
@flagship_ready
async def test_editor_attach_material_adds_owner_source(user, wire_session):
    """On a flagship article's editor, the "Attach material" control adds a text owner source and the
    Sources panel refreshes to show it. We open the editor, use the attach dialog to paste text, and
    assert the new owner row appears in the Sources panel (with its "owner" chip)."""
    from app.db.models import OwnerSource
    from sqlalchemy import select

    sess = wire_session
    # A flagship-shaped article: cluster-less, already drafting, with one seed owner source so the
    # panel has prior content (the attach adds a SECOND, distinct one).
    _seed_article(sess, id="a:ng_attach", piece_type="tech_explainer", status="drafting",
                  draft="# Flagship\n\nbody.")
    _seed_owner_source(sess, article_id="a:ng_attach", kind="text",
                       title="Existing note", content="existing owner material")

    await user.open("/editor/a:ng_attach")
    await user.should_see(marker="sources-panel")
    await user.should_see(marker="attach-material-button")

    # Open the attach dialog, paste new material, submit.
    user.find(marker="attach-material-button").click()
    await user.should_see(marker="attach-text")
    await user.should_see(marker="attach-submit")
    user.find(marker="attach-text").type("A freshly attached owner note for fusion.")
    user.find(marker="attach-submit").click()

    # The Sources panel refreshes in place to surface the new owner material (title shows). should_see
    # awaits the async submit handler completing (attach off the event loop, then the panel rebuild).
    await user.should_see("A freshly attached owner note")

    # …and it landed in the DB (the new OwnerSource row; Postgres is the source of truth).
    attached = None
    for _ in range(20):
        sess.expire_all()
        rows = sess.execute(
            select(OwnerSource.content).where(OwnerSource.article_id == "a:ng_attach")
        ).scalars().all()
        if any("freshly attached owner note" in (c or "") for c in rows):
            attached = rows
            break
        await asyncio.sleep(0.05)
    assert attached is not None


@pg_only
@history_render_ready
async def test_editor_sources_panel_shows_owner_chip(user, wire_session):
    """A flagship article (owner material, no URL) renders the Sources panel with an "owner" chip and
    the material's title — and an owner row with NO url renders as plain text (no broken empty link)."""
    sess = wire_session
    _seed_article(sess, id="a:ng_ownerchip", piece_type="tech_explainer", status="drafting",
                  draft="# Flagship\n\nbody.")
    _seed_owner_source(sess, article_id="a:ng_ownerchip", kind="text",
                       title="My pasted note", content="some owner notes", url=None)

    await user.open("/editor/a:ng_ownerchip")
    await user.should_see(marker="sources-panel")
    # The owner row renders its title and a distinct "owner" chip (marked source-chip-owner).
    await user.should_see("My pasted note")
    await user.should_see(marker="source-chip-owner")


# --- Phase 10a: the X / Twitter variant card -----------------------------------------------
#
# The variants section ITERATES `app.variants.PLATFORMS` (it does not hardcode three platforms), so
# "x" gets a card automatically with the standard variant-card-x / gen-variant-x / variant-out-x /
# save-variant-x marks and the same Gate-2 gating as the others. These tests assert the X card
# renders on a pre_publish article and that Generate (scripted seam) populates its output area.


def test_variants_section_iterates_platforms_and_labels_x():
    """DB-free smoke: the variant block uses the PLATFORMS tuple's labels — "x" reads as "X / Twitter"
    (not the bare capitalised "X") and gets its own chip colour distinct from the pipeline default."""
    import app.web.ui_pages as ui_pages
    from app.variants import PLATFORMS

    assert "x" in PLATFORMS  # the backend exposes the X platform
    assert ui_pages._platform_label("x") == "X / Twitter"
    # An unmapped platform still gets a sensible fallback label.
    assert ui_pages._platform_label("medium") == "Medium"
    # The X chip colour is a real (non-fallback) colour.
    assert ui_pages._platform_chip_color("x") != "grey-6"


@pg_only
async def test_editor_renders_x_variant_card(user, wire_session):
    """A pre_publish article's editor renders the X / Twitter variant card with the standard marks —
    variant-card-x / gen-variant-x / variant-out-x / save-variant-x — proving the section iterates
    PLATFORMS (so "x" gets a card without any hardcoding). Pure render — no backend call."""
    _seed_article(
        wire_session, id="a:ng_xcard", status="pre_publish",
        draft="# Approved\n\nready to format.",
    )
    await user.open("/editor/a:ng_xcard")
    await user.should_see(marker="variant-card-x")
    await user.should_see(marker="gen-variant-x")
    await user.should_see(marker="variant-out-x")
    await user.should_see(marker="save-variant-x")


@pg_only
@variants_ready
async def test_editor_generate_x_variant_shows_output(user, wire_session, monkeypatch):
    """Clicking "Generate X / Twitter" runs the variants seam off the event loop (scripted to a
    VariantResult, no model/DB) and shows the formatted text in the X output area — the X card wires
    to generate_variant exactly like the other platforms."""
    import app.variants as variants_mod

    _seed_article(
        wire_session, id="a:ng_genx", status="pre_publish",
        draft="# Canonical\n\nbody to format.",
    )

    def fake_generate(session, article_id, platform):
        assert platform == "x"
        return variants_mod.VariantResult(
            article_id=article_id,
            platform=platform,
            formatted_text="X THREAD HOOK for copy-out.",
            variant_id=1,
        )

    monkeypatch.setattr(variants_mod, "generate_variant", fake_generate)

    await user.open("/editor/a:ng_genx")
    await user.should_see(marker="gen-variant-x")
    user.find(marker="gen-variant-x").click()
    await user.should_see("X THREAD HOOK for copy-out")


# --- Phase 10b: fusion discovery ("Find related news") -------------------------------------
#
# The intake dialogs carry a "Find related news" control over the pasted text. On the dashboard
# new-piece dialog it is READ-ONLY discovery (the article doesn't exist yet) — results list related
# news with open-original links and no attach button. On the editor attach-material dialog it is the
# FUSION path — each result gets an "Attach as source" button that pulls the cluster's URL into the
# open article via `attach_owner_url` (no article_clusters link) and refreshes the Sources panel. We
# monkeypatch find_related_clusters (and, for the attach test, attach_owner_url) so no embedding /
# fetch backend is hit — the frontend's contract is those seam boundaries.


def _related_cluster(**kw):
    """Build an app.editor.RelatedCluster with sensible defaults, overridable per test (mirrors the
    frozen contract: cluster_id/title/topic/url/distance/source_types)."""
    base = dict(
        cluster_id="cl:rel",
        title="A related story",
        topic="ai",
        url="https://example.com/related",
        distance=0.12,
        source_types=["rss"],
    )
    base.update(kw)
    return editor_mod.RelatedCluster(**base)


@pg_only
async def test_new_piece_find_related_renders_results(user, wire_session, monkeypatch):
    """On the dashboard new-piece dialog, "Find related news" over pasted text lists related clusters
    (titles + topic/source chips + open-original links) — READ-ONLY discovery (no attach button). We
    monkeypatch find_related_clusters to a fixed list so the render is deterministic (no embedding)."""
    from app.web import queries

    monkeypatch.setattr(queries, "load_stories", lambda session, *, status=None, source=None: [])
    monkeypatch.setattr(queries, "unified_status_counts", lambda session, *, source=None: {})

    fixed = [
        _related_cluster(cluster_id="cl:r1", title="Related news one",
                         url="https://example.com/one", source_types=["rss"]),
        _related_cluster(cluster_id="cl:r2", title="Related news two",
                         url=None, source_types=["hn"]),
    ]
    # _find_related does `from app.editor import find_related_clusters`, resolving the name on the
    # app.editor package — patch it there.
    monkeypatch.setattr(editor_mod, "find_related_clusters", lambda session, text, **kw: fixed)

    await user.open("/")
    await user.should_see(marker="new-piece-button")
    user.find(marker="new-piece-button").click()
    await user.should_see(marker="new-piece-text")
    await user.should_see(marker="new-piece-find-related")

    # Paste material, then find related news.
    user.find(marker="new-piece-text").type("My notes about the latest model release.")
    user.find(marker="new-piece-find-related").click()

    # Results render: both titles + the open-original link for the URL-bearing one.
    await user.should_see(marker="related-results")
    await user.should_see("Related news one")
    await user.should_see("Related news two")
    await user.should_see(marker="related-open-0")  # the first result has a URL → open-original link
    # The read-only discovery path has NO "Attach as source" button.
    await user.should_not_see(marker="attach-related-0")


@pg_only
async def test_find_related_empty_input_no_call(user, wire_session, monkeypatch):
    """Clicking "Find related news" with NO pasted text → a notify and NO backend call (nothing to
    embed). We patch find_related_clusters to assert it is never reached."""
    from app.web import queries

    monkeypatch.setattr(queries, "load_stories", lambda session, *, status=None, source=None: [])
    monkeypatch.setattr(queries, "unified_status_counts", lambda session, *, source=None: {})

    called = {"n": 0}

    def fake_find(session, text, **kw):
        called["n"] += 1
        return []

    monkeypatch.setattr(editor_mod, "find_related_clusters", fake_find)

    await user.open("/")
    await user.should_see(marker="new-piece-button")
    user.find(marker="new-piece-button").click()
    await user.should_see(marker="new-piece-find-related")
    user.find(marker="new-piece-find-related").click()
    await user.should_see("Paste some text first")
    assert called["n"] == 0


@pg_only
async def test_find_related_empty_results_shows_note(user, wire_session, monkeypatch):
    """When the fusion query returns nothing, the results container shows a "No related news found."
    line rather than an empty box."""
    from app.web import queries

    monkeypatch.setattr(queries, "load_stories", lambda session, *, status=None, source=None: [])
    monkeypatch.setattr(queries, "unified_status_counts", lambda session, *, source=None: {})
    monkeypatch.setattr(editor_mod, "find_related_clusters", lambda session, text, **kw: [])

    await user.open("/")
    user.find(marker="new-piece-button").click()
    await user.should_see(marker="new-piece-text")
    user.find(marker="new-piece-text").type("Something with no matches in the store.")
    user.find(marker="new-piece-find-related").click()
    await user.should_see(marker="related-empty")
    await user.should_see("No related news found")


@pg_only
async def test_editor_attach_find_related_attaches_source(user, wire_session, monkeypatch):
    """On the editor attach-material dialog, "Find related news" lists results WITH an "Attach as
    source" button (the fusion path). Clicking it calls `attach_owner_url(session, article_id, url)`
    (NO article_clusters link) and refreshes the Sources panel. We monkeypatch find_related_clusters
    (fixed list) and attach_owner_url (records the call) so no embedding/fetch backend is hit."""
    sess = wire_session
    _seed_article(sess, id="a:ng_fuse", piece_type="tech_explainer", status="drafting",
                  draft="# Flagship\n\nbody.")

    fixed = [
        _related_cluster(cluster_id="cl:fuse", title="Fusion-worthy news",
                         url="https://example.com/fuse", source_types=["rss"]),
    ]
    monkeypatch.setattr(editor_mod, "find_related_clusters", lambda session, text, **kw: fixed)

    attached = {"calls": []}

    def fake_attach(session, article_id, url, **kw):
        attached["calls"].append((article_id, url))
        # Mirror the real backend: persist an owner source so the Sources panel refresh shows it.
        from app.db.models import OwnerSource

        row = OwnerSource(
            article_id=article_id, kind="url", title="Fusion-worthy news",
            url=url, content="fetched related text",
        )
        session.add(row)
        session.flush()
        return row.id

    monkeypatch.setattr(editor_mod, "attach_owner_url", fake_attach)

    await user.open("/editor/a:ng_fuse")
    await user.should_see(marker="attach-material-button")
    user.find(marker="attach-material-button").click()
    await user.should_see(marker="attach-text")
    await user.should_see(marker="attach-find-related")

    user.find(marker="attach-text").type("My take on this; what news connects to it?")
    user.find(marker="attach-find-related").click()
    await user.should_see("Fusion-worthy news")
    await user.should_see(marker="attach-related-0")  # the editor path renders the attach button

    # Attach the related cluster as a source → attach_owner_url is called and the Sources panel
    # refreshes to show the new owner material. The attach runs in a worker thread (run.io_bound)
    # sharing this savepoint session, so its effect can land a beat after the click — poll briefly.
    user.find(marker="attach-related-0").click()
    for _ in range(40):
        if attached["calls"]:
            break
        await asyncio.sleep(0.05)

    # The fusion attach called attach_owner_url with THIS article + the cluster's URL (no
    # article_clusters link — the covered-marker stays untouched).
    assert attached["calls"] == [("a:ng_fuse", "https://example.com/fuse")]

    # …and the Sources panel refreshed to surface the newly-attached owner material.
    await user.should_see(marker="sources-panel")
    await user.should_see("Fusion-worthy news", marker="sources-panel")


@pg_only
async def test_attach_related_disabled_without_url(user, wire_session, monkeypatch):
    """A related result with NO url renders its "Attach as source" button DISABLED — there is nothing
    to fetch and attach as a grounding source."""
    sess = wire_session
    _seed_article(sess, id="a:ng_nourl", piece_type="tech_explainer", status="drafting",
                  draft="# Flagship\n\nbody.")

    fixed = [_related_cluster(cluster_id="cl:nourl", title="No-URL related", url=None,
                              source_types=["x_user"])]
    monkeypatch.setattr(editor_mod, "find_related_clusters", lambda session, text, **kw: fixed)

    await user.open("/editor/a:ng_nourl")
    user.find(marker="attach-material-button").click()
    await user.should_see(marker="attach-text")
    user.find(marker="attach-text").type("Looking for related news.")
    user.find(marker="attach-find-related").click()
    await user.should_see("No-URL related")

    attach_btn = next(iter(user.find(marker="attach-related-0").elements))
    assert attach_btn.enabled is False


# --- Phase 10c: rich draft preview (highlighted code + mermaid diagrams) --------------------
#
# The draft preview renders markdown with syntax-highlighted fenced code (NiceGUI's default
# `fenced-code-blocks` extra → Pygments) and routes ```mermaid fenced blocks to `ui.mermaid`. A
# malformed mermaid block must NOT crash the preview (it falls back to a plain code block). The
# splitter is a pure helper, so its routing is also covered DB-free.


def test_split_mermaid_segments_routes_correctly():
    """DB-free: the segment splitter routes ```mermaid fences to mermaid segments and everything else
    to markdown segments (including a non-mermaid fenced code block, which stays one markdown chunk so
    ui.markdown highlights it)."""
    import app.web.ui_pages as ui_pages

    # Plain markdown → one markdown segment.
    assert ui_pages._split_mermaid_segments("hello **world**") == [("markdown", "hello **world**")]

    # A mermaid fence is isolated; the surrounding text is markdown.
    segs = ui_pages._split_mermaid_segments("Intro.\n\n```mermaid\ngraph TD; A-->B;\n```\n\nOutro.")
    kinds = [k for k, _ in segs]
    assert kinds == ["markdown", "mermaid", "markdown"]
    assert "graph TD" in dict((k, v) for k, v in segs if k == "mermaid")["mermaid"]

    # A python fenced block is NOT a mermaid block — it stays a single markdown segment (highlighted
    # by ui.markdown's fenced-code-blocks extra).
    py = ui_pages._split_mermaid_segments("```python\nx = 1\n```")
    assert py == [("markdown", "```python\nx = 1\n```")]


@pg_only
async def test_editor_preview_highlights_fenced_code(user, wire_session):
    """A draft with a ```python fenced block renders the preview markdown with Pygments highlight
    wiring (the `codehilite` container + token spans NiceGUI's default fenced-code-blocks extra
    emits). We assert on the rendered markdown element's innerHTML under the preview container."""
    from nicegui import ui as nicegui_ui

    _seed_article(
        wire_session, id="a:ng_code", status="drafting",
        draft="# Title\n\nSome prose.\n\n```python\nx = 1\nprint(x)\n```\n",
    )
    await user.open("/editor/a:ng_code")
    await user.should_see(marker="preview")

    # The preview container holds one ui.markdown whose innerHTML carries the codehilite highlight
    # wiring for the python block.
    markdowns = list(user.find(kind=nicegui_ui.markdown).elements)
    highlighted = any(
        "codehilite" in (md._props.get("innerHTML") or "") for md in markdowns
    )
    assert highlighted


@pg_only
async def test_editor_preview_renders_mermaid_diagram(user, wire_session):
    """A draft containing a ```mermaid block routes that segment to a `ui.mermaid` element (the
    diagram), while the surrounding prose still renders as markdown. We assert a mermaid element was
    created under the preview (marked preview-mermaid) carrying the diagram source."""
    from nicegui import ui as nicegui_ui

    _seed_article(
        wire_session, id="a:ng_mermaid", status="drafting",
        draft="# Title\n\nA diagram:\n\n```mermaid\ngraph TD; A-->B;\n```\n\nAfter.",
    )
    await user.open("/editor/a:ng_mermaid")
    await user.should_see(marker="preview")
    # A ui.mermaid element renders the diagram segment.
    await user.should_see(marker="preview-mermaid")
    mermaids = list(user.find(kind=nicegui_ui.mermaid).elements)
    assert mermaids
    assert any("graph TD" in (m._props.get("content") or "") for m in mermaids)
    # The surrounding prose still renders as markdown (the "After." tail).
    await user.should_see("After.")


@pg_only
async def test_editor_plain_draft_still_renders(user, wire_session):
    """A normal draft (no fenced blocks at all) still renders in the preview as markdown — the rich
    renderer is a superset, not a regression."""
    _seed_article(
        wire_session, id="a:ng_plain", status="drafting",
        draft="# Heading\n\nJust ordinary **prose** with no code or diagrams.",
    )
    await user.open("/editor/a:ng_plain")
    await user.should_see(marker="preview")
    await user.should_see("Just ordinary")


@pg_only
async def test_editor_malformed_mermaid_does_not_crash(user, wire_session, monkeypatch, caplog):
    """A malformed mermaid block must NOT take down the preview — if constructing `ui.mermaid` raises,
    the renderer falls back to a plain code block. We force ui.mermaid to raise and assert the page
    still renders (the preview + the markdown fallback) without crashing.

    The fallback logs the failure at ERROR (the production signal that a diagram couldn't render); the
    NiceGUI `user` fixture fails on ANY captured ERROR log, so we clear that one EXPECTED record before
    teardown (asserting it was the mermaid-fallback log we provoked)."""
    import app.web.ui_pages as ui_pages

    def boom(*a, **kw):
        raise RuntimeError("mermaid construction blew up")

    # Patch the symbol the renderer calls (ui.mermaid via the module's `ui` import).
    monkeypatch.setattr(ui_pages.ui, "mermaid", boom)

    _seed_article(
        wire_session, id="a:ng_badmermaid", status="drafting",
        draft="Intro.\n\n```mermaid\nnot a real diagram %%%\n```\n\nTail.",
    )
    await user.open("/editor/a:ng_badmermaid")
    # The page renders the preview despite the mermaid failure (the segment fell back to a code block).
    await user.should_see(marker="preview")
    await user.should_see("Tail.")

    # The fallback path emitted exactly the expected ERROR log; clear it so the user-fixture's
    # "no unexpected ERROR logs" teardown check passes (this ERROR is the intended fallback signal).
    fallback_logs = [r for r in caplog.get_records("call") if r.levelname == "ERROR"]
    assert any("mermaid render failed" in r.getMessage() for r in fallback_logs)
    caplog.clear()
