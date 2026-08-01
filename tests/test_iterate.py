"""Writer-agent ITERATE slice (app.editor.iterate) + Gate 2 + the web chat seam (Phase 4).

DB-LIGHT by default (build plan testing note: the default suite needs no live Postgres). The
iterate agent loop, the edit-in-place + edit_log behaviour, the piece-type switch, the empty
no-op, Gate-2 approve, and the web seam are exercised without a DB by scripting the model boundary
(monkeypatching `app.editor.iterate.generate`) and using a tiny stub session — exactly like
tests/test_editor.py scripts `app.editor.draft.generate`. The DB-backed pieces (end-to-end draft
→ iterate → approve over real pgvector) are guarded behind RUN_PG_TESTS.

The model boundary is the crux: the fake provider returns a string and CANNOT emit tool_use, so
the default suite scripts `generate` directly — turn 1 may emit a tool_use block, turn 2 the full
revised draft — via the module-level `app.editor.iterate.generate` import seam. No
ANTHROPIC_API_KEY is needed; the loop never touches a real API.
"""
from __future__ import annotations

import os
import uuid
from types import SimpleNamespace

import pytest

from app.editor import context as ctx
from app.editor import iterate as iterate_mod
from app.editor import tools as editor_tools

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"
pg_only = pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")


# --- helpers: scripted model responses (real-SDK-shaped fakes) ------------------------------


def _text_block(text):
    return SimpleNamespace(type="text", text=text)


def _tool_use_block(*, id, name, input):
    return SimpleNamespace(type="tool_use", id=id, name=name, input=input)


def _response(*blocks):
    """A fake provider response shaped like the Anthropic object: a `.content` list of blocks."""
    return SimpleNamespace(content=list(blocks))


def _scripted_generate(*responses):
    """Return a generate() stand-in that yields the given responses in order, one per call.
    Records the calls so a test can assert what the loop sent (system, tools, messages)."""
    calls = []
    seq = list(responses)

    def fake_generate(messages, role="generation", tools=None, system=None, **kwargs):
        calls.append(SimpleNamespace(messages=messages, role=role, tools=tools, system=system, kwargs=kwargs))
        return seq[len(calls) - 1]

    fake_generate.calls = calls
    return fake_generate


def _bundle(*items):
    return ctx.SourceBundle(
        cluster_id="cl:x",
        items=[ctx.SourceItem(title=t, url=u, full_text=ft) for (t, u, ft) in items],
    )


# --- stub session + article (DB-light loop, mirrors test_editor._LoopSession/_LoopArticle) ---


class _LoopArticle:
    """Minimal article stand-in the iterate loop reads/writes."""
    def __init__(self, *, current_draft="# Draft\n\noriginal body", piece_type="hot_news",
                 status="drafting"):
        self.id = "a:loop"
        self.piece_type = piece_type
        self.status = status
        self.current_draft = current_draft


class _LoopSession:
    """A stub session sufficient for iterate_article's reads/writes:
    session.get(Article, id) → the article; the cluster-link + bundle reads are monkeypatched;
    session.add captures EditLog rows; session.commit records commits.

    `_ensure_genesis` (Feature A) issues a COUNT(*) of edit_log rows for the article via
    session.execute(...).scalar_one(); the stub answers it from the EditLog rows captured so far so
    the genesis safety-net behaves as it would against Postgres (zero rows → genesis added once)."""
    def __init__(self, article):
        self._article = article
        self.added = []
        self.commits = 0

    def get(self, model, ident):
        return self._article

    def execute(self, stmt):
        from app.db.models import EditLog
        edit_log_count = sum(1 for o in self.added if isinstance(o, EditLog))

        class _R:
            def all(self_inner):
                return []
            def scalar_one_or_none(self_inner):
                return None
            def scalar_one(self_inner):
                # The only scalar_one() the iterate path issues is the edit_log COUNT(*) in
                # _ensure_genesis; answer it from the captured rows.
                return edit_log_count
        return _R()

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.commits += 1


def _wire_context(monkeypatch, *, bundle=None, voice=None):
    """Stub the DB-touching context reads so the iterate loop runs without Postgres. Iterate now
    grounds via the combined load_grounding_bundle (cluster items + owner material)."""
    monkeypatch.setattr(
        iterate_mod,
        "load_grounding_bundle",
        lambda s, aid: bundle if bundle is not None else _bundle(
            ("Source headline", "https://ex.com/s", "A grounded fact.")
        ),
    )
    monkeypatch.setattr(
        iterate_mod, "load_voice_files",
        lambda: voice if voice is not None else ctx.VoiceFiles(style_guide="be clear"),
    )


def _edit_log_rows(session):
    """The EditLog rows captured by the stub session (added via session.add)."""
    from app.db.models import EditLog
    return [o for o in session.added if isinstance(o, EditLog)]


# --- iterate context assembly (PURE) --------------------------------------------------------


def test_iterate_system_blocks_carry_draft_rules_and_grounding():
    b = _bundle(("Headline", "https://ex.com/p", "Body fact from the source."))
    blocks = ctx.build_iterate_system_blocks(
        voice=ctx.VoiceFiles(style_guide="VOICE_MARKER"),
        bundle=b,
        current_draft="THE_WORKING_DRAFT_TEXT",
        piece_type="hot_news",
    )
    flat = ctx.system_blocks_to_text(blocks)
    # The current draft to edit is present (the thing iterate adds over draft).
    assert "THE_WORKING_DRAFT_TEXT" in flat
    assert "CURRENT DRAFT" in flat
    # Edit-in-place rules present (the iterate contract).
    assert "EDITING AN EXISTING DRAFT IN PLACE" in flat
    assert "NEVER regenerate" in flat
    # Grounding + voice + bundle still carried (same as draft).
    assert "GROUNDING RULES" in flat
    assert "VOICE_MARKER" in flat
    assert "Body fact from the source." in flat


def test_iterate_blocks_cache_breakpoint_on_last_stable_block_not_the_draft():
    # The volatile current-draft block is LAST and must NOT carry the cache breakpoint; the
    # breakpoint sits on the last stable block (the source bundle) above it.
    b = _bundle(("H", "https://ex.com/p", "text"))
    blocks = ctx.build_iterate_system_blocks(
        voice=ctx.VoiceFiles(), bundle=b, current_draft="draft text"
    )
    assert "CURRENT DRAFT" in blocks[-1]["text"]
    assert "cache_control" not in blocks[-1]  # the draft block is uncached (it changes every turn)
    assert blocks[-2].get("cache_control") == {"type": "ephemeral"}  # last stable block cached


def test_iterate_blocks_include_switch_directive_on_piece_switch():
    b = _bundle(("H", "https://ex.com/p", "t"))
    flat = ctx.system_blocks_to_text(
        ctx.build_iterate_system_blocks(
            voice=ctx.VoiceFiles(), bundle=b, current_draft="d",
            piece_type="digest", is_piece_switch=True,
        )
    )
    assert "STRUCTURAL REFORMAT" in flat
    assert "digest" in flat


def test_iterate_message_carries_the_instruction():
    msg = ctx.build_iterate_message("cut the intro paragraph")
    assert "cut the intro paragraph" in msg
    assert "edit" in msg.lower()


# --- iterate_article: edit in place, persist, log -------------------------------------------


def test_iterate_edits_in_place_persists_and_logs(monkeypatch):
    """The model returns the full revised draft on turn 1 (no tools): iterate persists it to
    current_draft, commits, and appends exactly one edit_log row carrying the instruction +
    the resulting snapshot."""
    article = _LoopArticle(current_draft="# Draft\n\noriginal body")
    session = _LoopSession(article)
    _wire_context(monkeypatch)
    fake = _scripted_generate(_response(_text_block("# Draft\n\nrevised body with a sharper intro")))
    monkeypatch.setattr(iterate_mod, "generate", fake)

    result = iterate_mod.iterate_article(session, "a:loop", "sharpen the intro")

    assert result.changed is True
    assert "revised body" in result.draft
    assert article.current_draft == result.draft  # persisted
    assert session.commits >= 1
    assert len(fake.calls) == 1
    # Feature A safety net: a FRESH article (no prior edit_log) edited for the first time ends with
    # TWO rows — the genesis pre-image first, then the edit. The genesis snapshots the PRE-edit text.
    rows = _edit_log_rows(session)
    assert len(rows) == 2
    assert rows[0].instruction == "[genesis draft]"
    assert rows[0].draft_snapshot == "# Draft\n\noriginal body"  # the pre-edit text
    # The edit row carries the owner's instruction + the resulting snapshot.
    assert rows[1].instruction == "sharpen the intro"
    assert rows[1].draft_snapshot == article.current_draft
    assert rows[1].article_id == "a:loop"
    # A terse confirmation, not the draft body, in the reply.
    assert "review" in result.reply.lower()


def test_iterate_dispatches_tool_then_persists(monkeypatch):
    """Turn 1: the model requests a tool (kb_search); the loop dispatches it and feeds the result
    back. Turn 2: the model returns the full revised draft, which is persisted. The iterate loop
    must work exactly like the draft loop here."""
    article = _LoopArticle(current_draft="# Draft\n\nbody")
    session = _LoopSession(article)
    _wire_context(monkeypatch)

    dispatched = []
    real_dispatch = iterate_mod.dispatch_tool

    def tracking_dispatch(s, call):
        dispatched.append(call.name)
        return real_dispatch(s, call)

    monkeypatch.setattr(iterate_mod, "dispatch_tool", tracking_dispatch)

    fake = _scripted_generate(
        _response(
            _text_block("checking past pieces for continuity"),
            _tool_use_block(id="tu_kb", name=editor_tools.TOOL_KB_SEARCH, input={"query": "rag"}),
        ),
        _response(_text_block("# Draft\n\nrevised with continuity in mind")),
    )
    monkeypatch.setattr(iterate_mod, "generate", fake)

    result = iterate_mod.iterate_article(session, "a:loop", "make it consistent with past posts")

    assert dispatched == [editor_tools.TOOL_KB_SEARCH]
    assert "revised with continuity" in result.draft
    assert article.current_draft == result.draft
    assert len(fake.calls) == 2
    # The second call's history carries the tool_result fed back.
    flat = str(fake.calls[1].messages)
    assert "tu_kb" in flat and "tool_result" in flat
    # The system context offered the iterate edit-in-place rules + tools.
    assert fake.calls[0].tools
    assert any("EDITING AN EXISTING DRAFT IN PLACE" in b.get("text", "")
               for b in fake.calls[0].system)


def test_iterate_respects_base_draft_as_the_edit_base(monkeypatch):
    """When base_draft is passed (the owner's unsaved hand-edits), it is persisted FIRST and is the
    base the agent edits — the agent sees the hand-edited text in its CURRENT DRAFT context, not the
    stale persisted draft."""
    article = _LoopArticle(current_draft="STALE persisted draft")
    session = _LoopSession(article)
    _wire_context(monkeypatch)

    # The model echoes back what it was given so we can prove which text it edited.
    def echo_generate(messages, role="generation", tools=None, system=None, **kwargs):
        # Pull the CURRENT DRAFT block out of the system context to prove it carried base_draft.
        flat = ctx.system_blocks_to_text(system)
        assert "HANDEDITED working text" in flat
        assert "STALE persisted draft" not in flat
        return _response(_text_block("HANDEDITED working text, now revised"))

    monkeypatch.setattr(iterate_mod, "generate", echo_generate)

    result = iterate_mod.iterate_article(
        session, "a:loop", "tweak it", base_draft="HANDEDITED working text"
    )
    assert "now revised" in result.draft
    assert article.current_draft == result.draft


def test_iterate_piece_switch_updates_type_and_reformats(monkeypatch):
    """A new_piece_type switches articles.piece_type, instructs a structural reformat, and the
    result + edit_log reflect the switch."""
    article = _LoopArticle(current_draft="# Long read\n\nbody", piece_type="hot_news")
    session = _LoopSession(article)
    _wire_context(monkeypatch)

    captured_system = {}

    def fake_generate(messages, role="generation", tools=None, system=None, **kwargs):
        captured_system["flat"] = ctx.system_blocks_to_text(system)
        return _response(_text_block("## Digest\n\n- story one\n- story two"))

    monkeypatch.setattr(iterate_mod, "generate", fake_generate)

    result = iterate_mod.iterate_article(
        session, "a:loop", "", new_piece_type="digest"
    )
    # The article's piece type changed and the result reports it.
    assert article.piece_type == "digest"
    assert result.piece_type == "digest"
    assert "Digest" in result.draft
    # The reformat directive was in the prompt.
    assert "STRUCTURAL REFORMAT" in captured_system["flat"]
    # The reply names the new type.
    assert "digest" in result.reply.lower()
    # edit_log records the switch with a synthesized instruction. A fresh article also gets the
    # genesis pre-image first (Feature A safety net) → two rows: genesis, then the switch.
    rows = _edit_log_rows(session)
    assert len(rows) == 2
    assert rows[0].instruction == "[genesis draft]"
    assert "digest" in rows[1].instruction


def test_iterate_piece_switch_rejects_unknown_type(monkeypatch):
    article = _LoopArticle()
    session = _LoopSession(article)
    _wire_context(monkeypatch)
    monkeypatch.setattr(iterate_mod, "generate", _scripted_generate())  # must not be called
    with pytest.raises(ValueError, match="unknown piece_type"):
        iterate_mod.iterate_article(session, "a:loop", "x", new_piece_type="bogus")


def test_iterate_empty_instruction_is_noop(monkeypatch):
    """An empty/whitespace instruction with no switch is a no-op: the model is NOT called and NO
    edit_log row is written."""
    article = _LoopArticle(current_draft="# Draft\n\nbody")
    session = _LoopSession(article)
    _wire_context(monkeypatch)
    fake = _scripted_generate()  # any call would IndexError → proves generate isn't called
    monkeypatch.setattr(iterate_mod, "generate", fake)

    result = iterate_mod.iterate_article(session, "a:loop", "   ")
    assert result.changed is False
    assert "nothing to do" in result.reply.lower()
    assert article.current_draft == "# Draft\n\nbody"  # untouched
    assert len(fake.calls) == 0
    assert _edit_log_rows(session) == []  # no edit_log row for a no-op


def test_iterate_empty_instruction_with_base_draft_persists_handedit_no_log(monkeypatch):
    """An empty instruction is still a no-op for the AGENT, but a supplied base_draft (the owner's
    hand-edit) is persisted — and crucially NOT logged as an instruction (it isn't one)."""
    article = _LoopArticle(current_draft="old")
    session = _LoopSession(article)
    _wire_context(monkeypatch)
    fake = _scripted_generate()
    monkeypatch.setattr(iterate_mod, "generate", fake)

    result = iterate_mod.iterate_article(session, "a:loop", "  ", base_draft="hand-edited text")
    assert article.current_draft == "hand-edited text"  # persisted
    assert result.draft == "hand-edited text"
    assert result.changed is False
    assert len(fake.calls) == 0
    assert _edit_log_rows(session) == []  # a hand-edit is not an instruction → not logged
    assert session.commits >= 1  # but the hand-edit IS committed


def test_iterate_missing_article_raises(monkeypatch):
    class _NoneSession:
        def get(self, model, ident):
            return None
    monkeypatch.setattr(iterate_mod, "generate", _scripted_generate())
    with pytest.raises(ValueError, match="not found"):
        iterate_mod.iterate_article(_NoneSession(), "a:nope", "do something")


def test_iterate_no_linked_cluster_still_edits(monkeypatch):
    """A zero-source article (no cluster, no owner material → empty grounding bundle) can still be
    edited — iterate must NOT refuse like draft does; the bundle is grounding for NEW facts only."""
    article = _LoopArticle(current_draft="# Draft\n\nbody")
    session = _LoopSession(article)
    # Empty grounding bundle (no cluster items, no owner material).
    monkeypatch.setattr(
        iterate_mod, "load_grounding_bundle",
        lambda s, aid: ctx.SourceBundle(cluster_id=None, items=[]),
    )
    monkeypatch.setattr(iterate_mod, "load_voice_files", lambda: ctx.VoiceFiles())
    fake = _scripted_generate(_response(_text_block("# Draft\n\nrevised body")))
    monkeypatch.setattr(iterate_mod, "generate", fake)

    result = iterate_mod.iterate_article(session, "a:loop", "tighten it")
    assert "revised body" in result.draft
    assert len(fake.calls) == 1


def test_iterate_flagship_article_owner_bundle(monkeypatch):
    """Iterate works on a FLAGSHIP article (grounded in the owner's own material): the owner bundle
    reaches the prompt, the edit is applied in place, and an edit_log row is appended."""
    article = _LoopArticle(current_draft="# Explainer\n\noriginal body", piece_type="tech_explainer")
    session = _LoopSession(article)
    owner_bundle = ctx.SourceBundle(
        cluster_id=None,
        items=[ctx.SourceItem(title="My result", url="", full_text="5000 rps measured", kind="owner")],
    )
    _wire_context(monkeypatch, bundle=owner_bundle)
    fake = _scripted_generate(_response(_text_block("# Explainer\n\nrevised, sharper body")))
    monkeypatch.setattr(iterate_mod, "generate", fake)

    result = iterate_mod.iterate_article(session, "a:loop", "sharpen the example")
    assert "sharper body" in result.draft
    assert article.current_draft == result.draft
    # The owner material reached the prompt (labelled as an OWNER ARTIFACT).
    flat = ctx.system_blocks_to_text(fake.calls[0].system)
    assert "OWNER ARTIFACT" in flat
    assert "5000 rps measured" in flat
    # The instruction was appended to edit_log (the voice signal).
    edit_rows = [r for r in _edit_log_rows(session) if r.instruction == "sharpen the example"]
    assert len(edit_rows) == 1


def test_iterate_respects_turn_cap(monkeypatch):
    """A model that keeps requesting tools must not loop forever — the cap stops it and the best
    text seen is persisted (never blanks the draft)."""
    monkeypatch.setenv("MAX_TOOL_TURNS", "3")
    article = _LoopArticle(current_draft="# Draft\n\nbody")
    session = _LoopSession(article)
    _wire_context(monkeypatch)

    calls = {"n": 0}

    def always_tool(messages, role="generation", tools=None, system=None, **kwargs):
        calls["n"] += 1
        return _response(
            _text_block("partial revision so far"),
            _tool_use_block(id="tu", name=editor_tools.TOOL_FETCH_SOURCE,
                            input={"url": "https://ex.com/s"}),
        )

    monkeypatch.setattr(iterate_mod, "generate", always_tool)
    monkeypatch.setattr(iterate_mod, "dispatch_tool", lambda s, c: "fetch_source: ...")

    result = iterate_mod.iterate_article(session, "a:loop", "expand section 2")
    assert calls["n"] == 3
    assert "partial revision so far" in result.draft


def test_iterate_role_is_logical_default(monkeypatch):
    monkeypatch.delenv("ITERATE_ROLE", raising=False)
    assert iterate_mod.iterate_role() == iterate_mod.DEFAULT_ITERATE_ROLE == "generation"
    monkeypatch.setenv("ITERATE_ROLE", "generation_high")
    assert iterate_mod.iterate_role() == "generation_high"
    monkeypatch.setenv("ITERATE_ROLE", "   ")
    assert iterate_mod.iterate_role() == "generation"  # blank falls back


# --- Gate 2: approve_article ----------------------------------------------------------------


class _ApproveArticle:
    def __init__(self, status):
        self.id = "a:g2"
        self.status = status


class _ApproveSession:
    def __init__(self, article):
        self._article = article
        self.commits = 0

    def get(self, model, ident):
        return self._article

    def commit(self):
        self.commits += 1


def test_approve_drafting_to_pre_publish():
    from app.editor import approve_article
    art = _ApproveArticle("drafting")
    sess = _ApproveSession(art)
    assert approve_article(sess, "a:g2") == "pre_publish"
    assert art.status == "pre_publish"
    assert sess.commits == 1


def test_approve_pre_publish_is_idempotent():
    from app.editor import approve_article
    art = _ApproveArticle("pre_publish")
    sess = _ApproveSession(art)
    assert approve_article(sess, "a:g2") == "pre_publish"
    assert art.status == "pre_publish"
    assert sess.commits == 0  # idempotent → no write


def test_approve_published_refuses():
    from app.editor import approve_article
    art = _ApproveArticle("published")
    sess = _ApproveSession(art)
    with pytest.raises(ValueError, match="already 'published'"):
        approve_article(sess, "a:g2")
    assert art.status == "published"  # unchanged
    assert sess.commits == 0


def test_approve_missing_article_raises():
    from app.editor import approve_article

    class _NoneSession:
        def get(self, model, ident):
            return None
    with pytest.raises(ValueError, match="not found"):
        approve_article(_NoneSession(), "a:nope")


# --- the web chat seam (app.web.chat.handle_editor_message) ---------------------------------


def test_chat_seam_returns_iterate_result(monkeypatch):
    """handle_editor_message delegates to iterate_article and returns the IterateResult whose
    .draft is the revised text. iterate_article is monkeypatched so no DB/model is touched."""
    from app.web import chat as chat_seam

    expected = chat_seam.IterateResult(
        reply="Applied your edit — review the updated draft on the right.",
        draft="# Revised\n\nbody",
        piece_type="hot_news",
        changed=True,
    )
    captured = {}

    def fake_iterate(session, article_id, instruction, *, base_draft=None, new_piece_type=None):
        captured["article_id"] = article_id
        captured["instruction"] = instruction
        captured["base_draft"] = base_draft
        captured["new_piece_type"] = new_piece_type
        return expected

    monkeypatch.setattr(chat_seam, "iterate_article", fake_iterate)

    result = chat_seam.handle_editor_message(
        "a:1", "rewrite intro", base_draft="# Old\n\nbody", new_piece_type="digest"
    )
    assert result is expected
    assert result.draft == "# Revised\n\nbody"
    assert captured["article_id"] == "a:1"
    assert captured["instruction"] == "rewrite intro"
    assert captured["base_draft"] == "# Old\n\nbody"
    assert captured["new_piece_type"] == "digest"


def test_chat_seam_empty_instruction_is_noop(monkeypatch):
    """An empty/whitespace instruction with no switch short-circuits in the seam: iterate_article
    is NOT called (no DB session opened), and a no-op IterateResult is returned."""
    from app.web import chat as chat_seam

    called = {"n": 0}

    def fake_iterate(*args, **kwargs):
        called["n"] += 1
        return chat_seam.IterateResult(reply="x", draft="x", piece_type="hot_news", changed=True)

    monkeypatch.setattr(chat_seam, "iterate_article", fake_iterate)
    result = chat_seam.handle_editor_message("a:1", "   ")
    assert called["n"] == 0
    assert result.changed is False
    assert "nothing to do" in result.reply.lower()


def test_chat_seam_piece_switch_with_empty_text_still_delegates(monkeypatch):
    """A pure piece-switch (empty text, new_piece_type set) is NOT a seam no-op — it must reach
    iterate_article so the agent reformats."""
    from app.web import chat as chat_seam

    called = {"n": 0}

    def fake_iterate(session, article_id, instruction, *, base_draft=None, new_piece_type=None):
        called["n"] += 1
        return chat_seam.IterateResult(
            reply="Reformatted as digest — review on the right.",
            draft="## Digest", piece_type="digest", changed=True,
        )

    monkeypatch.setattr(chat_seam, "iterate_article", fake_iterate)
    result = chat_seam.handle_editor_message("a:1", "", new_piece_type="digest")
    assert called["n"] == 1
    assert result.piece_type == "digest"


# --- DB-backed (guarded): end-to-end draft → iterate → approve ------------------------------


@pytest.fixture()
def session():
    from app.db.session import engine, SessionLocal

    conn = engine.connect()
    outer = conn.begin()
    sess = SessionLocal(bind=conn, join_transaction_mode="create_savepoint")
    try:
        yield sess
    finally:
        sess.close()
        outer.rollback()
        conn.close()


def _approved_cluster_with_item(session, *, full_text="A grounded source fact."):
    """Create an approved cluster with one item carrying pass-2 full_text. Returns the cluster id.
    Mirrors tests/test_editor.py's helper."""
    from app.adapters.base import Item as AdapterItem, item_id
    from app.db.models import Cluster, Item as ItemModel
    from app.researcher.cluster import new_cluster_id
    from app.researcher.store import upsert_item_and_sighting

    cid = new_cluster_id()
    session.add(Cluster(id=cid, status="approved", topic="ai", score=0.5,
                        triage_title="Approved", triage_summary="s"))
    session.flush()
    url = f"https://example.com/src/{uuid.uuid4().hex}"
    upsert_item_and_sighting(session, AdapterItem(url=url, title="Source headline"), "rss:a")
    session.flush()
    item = session.get(ItemModel, item_id(url))
    item.cluster_id = cid
    item.full_text = full_text
    session.flush()
    session.commit()
    return cid


@pg_only
def test_draft_then_iterate_then_approve_end_to_end(session, monkeypatch):
    """Full DB path: create the article from an approved cluster, draft it, then iterate (asserting
    current_draft changes + an edit_log row lands in Postgres), then approve (Gate 2 → pre_publish)."""
    from app.db.models import Article, EditLog
    from app.editor import draft as draft_mod
    from app.editor import iterate as it_mod
    from app.editor import approve_article, create_article_for_cluster

    cid = _approved_cluster_with_item(session)
    aid = create_article_for_cluster(session, cid)

    # Draft.
    draft_fake = _scripted_generate(
        _response(_text_block("# Original Draft\n\nGrounded long-read body.")),
    )
    monkeypatch.setattr(draft_mod, "generate", draft_fake)
    original = draft_mod.draft_article(session, aid)
    assert "Original Draft" in original

    # Iterate (edit-in-place): the model returns a revised full draft.
    it_fake = _scripted_generate(
        _response(_text_block("# Original Draft\n\nGrounded long-read body, now with a sharper close.")),
    )
    monkeypatch.setattr(it_mod, "generate", it_fake)
    result = it_mod.iterate_article(session, aid, "sharpen the closing line")
    assert result.changed is True
    assert "sharper close" in result.draft

    session.expire_all()
    persisted = session.get(Article, aid).current_draft
    assert "sharper close" in persisted

    # The instruction landed in edit_log in Postgres. Feature A: draft anchored a genesis row, so
    # after one iterate there are TWO rows — genesis (from draft) then the edit. Ordered by id.
    rows = session.execute(
        EditLog.__table__.select()
        .where(EditLog.article_id == aid)
        .order_by(EditLog.id.asc())
    ).all()
    assert len(rows) == 2
    assert rows[0].instruction == "[genesis draft]"
    assert "Original Draft" in (rows[0].draft_snapshot or "")  # the first-draft snapshot
    assert rows[1].instruction == "sharpen the closing line"
    assert "sharper close" in (rows[1].draft_snapshot or "")

    # Gate 2: approve → pre_publish.
    assert approve_article(session, aid) == "pre_publish"
    session.expire_all()
    assert session.get(Article, aid).status == "pre_publish"
    # Idempotent re-approve.
    assert approve_article(session, aid) == "pre_publish"


@pg_only
def test_iterate_piece_switch_persists_in_postgres(session, monkeypatch):
    """A piece-type switch updates articles.piece_type in Postgres and logs the switch."""
    from app.db.models import Article, EditLog
    from app.editor import draft as draft_mod
    from app.editor import iterate as it_mod
    from app.editor import create_article_for_cluster

    cid = _approved_cluster_with_item(session)
    aid = create_article_for_cluster(session, cid)  # defaults to hot_news

    monkeypatch.setattr(draft_mod, "generate",
                        _scripted_generate(_response(_text_block("# Hot News\n\nbody"))))
    draft_mod.draft_article(session, aid)

    monkeypatch.setattr(it_mod, "generate",
                        _scripted_generate(_response(_text_block("## Digest\n\n- a\n- b"))))
    result = it_mod.iterate_article(session, aid, "", new_piece_type="digest")
    assert result.piece_type == "digest"

    session.expire_all()
    assert session.get(Article, aid).piece_type == "digest"
    rows = session.execute(
        EditLog.__table__.select().where(EditLog.article_id == aid)
    ).all()
    assert any("digest" in (r.instruction or "") for r in rows)
