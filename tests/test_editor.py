"""Writer-agent DRAFT slice (app.editor) — the one agentic component (build plan Phase 3).

DB-LIGHT by default (build plan testing note: the default suite needs no live Postgres). The
agent loop, context assembly, response parsing, and the web trigger are exercised without a DB
by scripting the model boundary and using a tiny stub session; the DB-backed pieces
(create_article_for_cluster, kb_search over real pgvector, draft_article end-to-end) are guarded
behind RUN_PG_TESTS like the other PG tests.

The model boundary is the crux: the fake provider returns a string and CANNOT emit tool_use, so
the default suite scripts `generate` directly — turn 1 emits a tool_use block, turn 2 a final
text draft — by monkeypatching `app.editor.draft.generate` (the module-level import seam). No
ANTHROPIC_API_KEY is needed; the loop never touches a real API.
"""
from __future__ import annotations

import os
import uuid
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest

from app.editor import context as ctx
from app.editor import tools as editor_tools
from app.editor.tools import ToolCall, _parse_response

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


# --- _parse_response (works on real-SDK-shaped objects AND dict fakes) -----------------------


def test_parse_response_plain_string():
    parsed = _parse_response("just text")
    assert parsed.text == "just text"
    assert parsed.tool_calls == []
    assert not parsed.wants_tools


def test_parse_response_text_blocks():
    parsed = _parse_response(_response(_text_block("hello "), _text_block("world")))
    assert parsed.text == "hello world"
    assert not parsed.wants_tools


def test_parse_response_tool_use_attr_objects():
    resp = _response(
        _text_block("let me look"),
        _tool_use_block(id="tu_1", name="kb_search", input={"query": "rag"}),
    )
    parsed = _parse_response(resp)
    assert parsed.wants_tools
    assert parsed.text == "let me look"
    (call,) = parsed.tool_calls
    assert call.id == "tu_1" and call.name == "kb_search" and call.input == {"query": "rag"}


def test_parse_response_dict_blocks():
    # The parser must also accept plain-dict blocks (a simpler fake the tests might build).
    resp = {"content": [{"type": "tool_use", "id": "x", "name": "fetch_source", "input": {"url": "u"}}]}
    parsed = _parse_response(resp)
    assert parsed.wants_tools
    assert parsed.tool_calls[0].name == "fetch_source"


def test_parse_response_none_is_empty():
    parsed = _parse_response(None)
    assert parsed.text == "" and parsed.tool_calls == []


# --- context assembly (the quality crux) ----------------------------------------------------


def _bundle(*items):
    return ctx.SourceBundle(
        cluster_id="cl:x",
        items=[ctx.SourceItem(title=t, url=u, full_text=ft) for (t, u, ft) in items],
    )


def test_build_source_bundle_text_includes_titles_urls_and_text():
    b = _bundle(
        ("RAG goes mainstream", "https://ex.com/a", "Retrieval augmented generation is..."),
        ("A second take", "https://ex.com/b", ""),
    )
    text = ctx.build_source_bundle_text(b)
    assert "RAG goes mainstream" in text
    assert "https://ex.com/a" in text
    assert "Retrieval augmented generation is" in text
    # An item with no fetched text is marked so the agent fetches rather than inventing.
    assert "no full text fetched" in text
    assert "https://ex.com/b" in text


def test_build_source_bundle_text_caps_item_text():
    b = _bundle(("Long", "https://ex.com/x", "y" * 5000))
    text = ctx.build_source_bundle_text(b, item_chars=100)
    assert "truncated" in text
    # The capped body is far shorter than the raw 5000 chars.
    assert text.count("y") <= 200


def test_system_blocks_include_style_guide_bundle_and_grounding(tmp_path):
    # Real voice files on a temp content dir → loaded verbatim into the system context.
    (tmp_path / "style_guide.md").write_text("VOICE_MARKER_hybrid_deep_accessible", encoding="utf-8")
    (tmp_path / "anti_patterns.md").write_text("ANTIPAT_MARKER_no_delve", encoding="utf-8")
    voice = ctx.load_voice_files(directory=tmp_path)

    b = _bundle(("Headline", "https://ex.com/p", "Body fact from the source."))
    blocks = ctx.build_system_blocks(voice=voice, bundle=b, piece_type="hot_news")
    flat = ctx.system_blocks_to_text(blocks)

    # (a) voice files present
    assert "VOICE_MARKER_hybrid_deep_accessible" in flat
    assert "ANTIPAT_MARKER_no_delve" in flat
    # (b) source bundle present
    assert "Body fact from the source." in flat
    assert "https://ex.com/p" in flat
    # (c) grounding rules enforced in the system prompt (hard rule 2)
    assert "GROUNDING RULES" in flat
    assert "ONLY facts" in flat
    assert "PROVENANCE" in flat
    assert "FLAG" in flat
    assert "never invent" in flat.lower()
    assert "Opinions and takes are the OWNER" in flat
    # piece-type brief
    assert "hot_news" in flat


def test_system_blocks_mark_last_block_cacheable():
    b = _bundle(("H", "https://ex.com/p", "text"))
    blocks = ctx.build_system_blocks(voice=ctx.VoiceFiles(), bundle=b)
    assert blocks[-1].get("cache_control") == {"type": "ephemeral"}
    # Earlier blocks are not marked (only the final stable block carries the cache breakpoint).
    assert all("cache_control" not in blk for blk in blocks[:-1])


def test_system_blocks_grounding_present_even_without_voice_files():
    # Missing voice files must not drop the grounding rules (hard rule).
    b = _bundle(("H", "https://ex.com/p", "t"))
    flat = ctx.system_blocks_to_text(ctx.build_system_blocks(voice=ctx.VoiceFiles(), bundle=b))
    assert "GROUNDING RULES" in flat


# --- Phase 10: owner-material rendering + tech_explainer + grounding bundle ------------------


def _owner_bundle(*items):
    """A bundle of OWNER items (kind='owner') — the flagship grounding shape."""
    return ctx.SourceBundle(
        cluster_id=None,
        items=[ctx.SourceItem(title=t, url=u, full_text=ft, kind="owner") for (t, u, ft) in items],
    )


def test_build_source_bundle_text_labels_owner_artifacts_and_adds_note():
    b = ctx.SourceBundle(
        cluster_id=None,
        items=[
            ctx.SourceItem(title="My benchmark", url="", full_text="5000 rps measured", kind="owner"),
            ctx.SourceItem(title="A news item", url="https://ex.com/n", full_text="reported", kind="source"),
        ],
    )
    text = ctx.build_source_bundle_text(b)
    assert "[OWNER ARTIFACT 1]" in text
    assert "[SOURCE 2]" in text
    # The authoritative-source note is prepended exactly once when ANY owner item is present.
    assert "authoritative source facts" in text
    assert "do not flag the owner's own numbers as unverified" in text


def test_build_source_bundle_text_no_owner_note_when_only_sources():
    text = ctx.build_source_bundle_text(_bundle(("H", "https://ex.com/p", "body")))
    assert "OWNER ARTIFACT" not in text
    assert "authoritative source facts" not in text


def test_bundle_has_full_text_from_owner_content_alone():
    # An owner-only bundle (no cluster items) is grounded iff an owner item carries content.
    assert _owner_bundle(("note", "", "real content")).has_full_text is True
    assert _owner_bundle(("note", "", "")).has_full_text is False


def test_tech_explainer_brief_present_and_teach_down():
    brief = ctx.piece_type_brief("tech_explainer")
    assert "tech_explainer" in brief
    # The teach-down structure markers.
    for marker in ("motivation", "mechanism", "example", "caveat"):
        assert marker in brief.lower()


def test_load_grounding_bundle_combines_cluster_and_owner(monkeypatch):
    """load_grounding_bundle unions the cluster's items + the owner's material; cluster_id carries
    through. Stubs the two I/O seams so it runs without Postgres."""
    monkeypatch.setattr(ctx, "_linked_cluster_id", lambda s, aid: "cl:x")
    monkeypatch.setattr(
        ctx, "load_source_bundle",
        lambda s, cid: _bundle(("Cluster src", "https://ex.com/c", "cluster fact")),
    )
    # load_owner_sources is imported lazily inside load_grounding_bundle from app.editor.sources.
    import app.editor.sources as sources_mod
    monkeypatch.setattr(
        sources_mod, "load_owner_sources",
        lambda s, aid: [ctx.SourceItem(title="Owner note", url="", full_text="owner fact", kind="owner")],
    )

    bundle = ctx.load_grounding_bundle(session=None, article_id="a:x")
    assert bundle.cluster_id == "cl:x"
    kinds = [it.kind for it in bundle.items]
    assert kinds == ["source", "owner"]
    flat = ctx.build_source_bundle_text(bundle)
    assert "cluster fact" in flat and "owner fact" in flat


def test_load_grounding_bundle_flagship_no_cluster(monkeypatch):
    """A flagship article (no cluster) → cluster_id None, items are the owner material only."""
    monkeypatch.setattr(ctx, "_linked_cluster_id", lambda s, aid: None)
    import app.editor.sources as sources_mod
    monkeypatch.setattr(
        sources_mod, "load_owner_sources",
        lambda s, aid: [ctx.SourceItem(title="Owner note", url="", full_text="owner fact", kind="owner")],
    )
    bundle = ctx.load_grounding_bundle(session=None, article_id="a:flagship")
    assert bundle.cluster_id is None
    assert len(bundle.items) == 1 and bundle.items[0].kind == "owner"
    assert bundle.has_full_text is True


def test_loads_repo_voice_files_by_default():
    # The actual content/ files in the repo load and carry their real content (build plan Done:
    # "the assembled draft context demonstrably includes the style-guide rules").
    repo_content = Path(__file__).resolve().parent.parent / "content"
    voice = ctx.load_voice_files(directory=repo_content)
    assert voice.style_guide.strip()
    assert "Grounded" in voice.style_guide or "grounded" in voice.style_guide.lower()


def test_load_voice_files_missing_dir_degrades():
    voice = ctx.load_voice_files(directory=Path("/no/such/dir/exists"))
    assert voice.style_guide == "" and voice.anti_patterns == ""
    assert not voice.present


# --- tool dispatch: fetch_source over MockTransport, kb_search empty, web_search disabled ----

FIXTURE = (Path(__file__).parent / "fixtures" / "article.html").read_text(encoding="utf-8")


def test_fetch_source_tool_via_mock_transport(monkeypatch):
    # Drive fetch_full_text's network through an injected MockTransport (no network).
    def handler(request):
        return httpx.Response(200, text=FIXTURE)

    client = httpx.Client(transport=httpx.MockTransport(handler))

    # The tool calls app.fetcher.fetch_full_text WITHOUT a client; patch it to use ours.
    from app.editor import tools as t

    real = t.fetch_full_text
    monkeypatch.setattr(t, "fetch_full_text", lambda url: real(url, client=client))

    call = ToolCall(id="t1", name=editor_tools.TOOL_FETCH_SOURCE, input={"url": "https://ex.com/rag"})
    out = editor_tools.dispatch_tool(session=None, call=call)
    assert "full text of https://ex.com/rag" in out
    assert "relevance head" in out.lower()
    client.close()


def test_fetch_source_tool_empty_returns_clear_result(monkeypatch):
    from app.editor import tools as t

    monkeypatch.setattr(t, "fetch_full_text", lambda url: None)
    call = ToolCall(id="t1", name=editor_tools.TOOL_FETCH_SOURCE, input={"url": "https://ex.com/x"})
    out = editor_tools.dispatch_tool(session=None, call=call)
    assert "no extractable text" in out
    assert "invent" in out.lower()


def test_fetch_source_tool_catches_transport_error(monkeypatch):
    from app.editor import tools as t

    def boom(url):
        raise httpx.ConnectError("down", request=httpx.Request("GET", url))

    monkeypatch.setattr(t, "fetch_full_text", boom)
    call = ToolCall(id="t1", name=editor_tools.TOOL_FETCH_SOURCE, input={"url": "https://ex.com/x"})
    out = editor_tools.dispatch_tool(session=None, call=call)
    # Caught, not propagated — the loop gets a usable tool_result.
    assert "could not fetch" in out


def test_unknown_tool_is_safe_noop():
    out = editor_tools.dispatch_tool(session=None, call=ToolCall(id="t", name="nope", input={}))
    assert "unknown tool" in out


def test_web_search_disabled_by_default(monkeypatch):
    monkeypatch.delenv("EDITOR_WEB_SEARCH", raising=False)
    assert not editor_tools.web_search_enabled()
    # Not offered to the model.
    names = {s["name"] for s in editor_tools.tool_schemas()}
    assert editor_tools.TOOL_WEB_SEARCH not in names
    assert editor_tools.TOOL_KB_SEARCH in names and editor_tools.TOOL_FETCH_SOURCE in names
    # Invoked while disabled → a clear "disabled" result, never a fabrication.
    out = editor_tools.dispatch_tool(session=None, call=ToolCall(id="t", name=editor_tools.TOOL_WEB_SEARCH, input={"query": "x"}))
    assert "disabled" in out


def test_web_search_offered_when_enabled(monkeypatch):
    monkeypatch.setenv("EDITOR_WEB_SEARCH", "1")
    assert editor_tools.web_search_enabled()
    names = {s["name"] for s in editor_tools.tool_schemas()}
    assert editor_tools.TOOL_WEB_SEARCH in names


def test_kb_search_tool_empty_kb_message():
    # A stub session that returns no rows → the empty-KB graceful message.
    class _EmptyResult:
        def all(self):
            return []

    class _StubSession:
        def execute(self, stmt):
            return _EmptyResult()

    call = ToolCall(id="t", name=editor_tools.TOOL_KB_SEARCH, input={"query": "anything"})
    out = editor_tools.dispatch_tool(session=_StubSession(), call=call)
    assert "no past published articles matched" in out


# --- the agent loop (scripted generate → tool dispatched → final draft persisted) ------------


class _LoopArticle:
    """Minimal article stand-in the loop writes current_draft onto."""
    def __init__(self):
        self.id = "a:loop"
        self.piece_type = "hot_news"
        self.current_draft = None


class _LoopSession:
    """A stub session sufficient for draft_article's reads + the kb_search tool call:
    session.get(Article, id) → the article; the cluster-link + bundle reads are monkeypatched.

    `_ensure_genesis` (Feature A) runs after the draft is persisted: it issues a COUNT(*) of the
    article's edit_log rows via execute(...).scalar_one() and, on zero, session.add(EditLog(...)).
    The stub answers the count from the EditLog rows captured so far (0 then 1) and captures the
    genesis row so the draft loop records its version anchor exactly once."""
    def __init__(self, article):
        self._article = article
        self.committed = False
        self.added = []

    def get(self, model, ident):
        return self._article

    def execute(self, stmt):
        from app.db.models import EditLog
        edit_log_count = sum(1 for o in self.added if isinstance(o, EditLog))

        # kb_search (if the scripted tool is kb_search) hits this; return no rows.
        class _R:
            def all(self_inner):
                return []
            def scalar_one(self_inner):
                # The only scalar_one() the draft path issues is the edit_log COUNT(*) in
                # _ensure_genesis; answer it from the captured rows.
                return edit_log_count
        return _R()

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.committed = True


def test_draft_loop_dispatches_tool_then_persists(monkeypatch):
    """Turn 1: the model requests kb_search. The loop must dispatch it, feed the result back,
    and Turn 2: the model returns the final draft, which is persisted to current_draft. No real
    API key, no fake-provider tool_use limitation — generate is scripted directly."""
    from app.editor import draft as draft_mod

    article = _LoopArticle()
    session = _LoopSession(article)

    # Stub the DB-touching context read so the loop runs without Postgres. draft now grounds via
    # the combined load_grounding_bundle (cluster items + owner material), so we stub that.
    monkeypatch.setattr(
        draft_mod,
        "load_grounding_bundle",
        lambda s, aid: _bundle(("Source headline", "https://ex.com/s", "A grounded fact.")),
    )
    monkeypatch.setattr(draft_mod, "load_voice_files", lambda: ctx.VoiceFiles(style_guide="be clear"))

    # Track tool dispatch.
    dispatched = []
    real_dispatch = draft_mod.dispatch_tool

    def tracking_dispatch(s, call):
        dispatched.append(call.name)
        return real_dispatch(s, call)

    monkeypatch.setattr(draft_mod, "dispatch_tool", tracking_dispatch)

    fake = _scripted_generate(
        _response(
            _text_block("checking past pieces"),
            _tool_use_block(id="tu_kb", name=editor_tools.TOOL_KB_SEARCH, input={"query": "rag"}),
        ),
        _response(_text_block("# The Final Draft\n\nGrounded body. https://ex.com/s")),
    )
    monkeypatch.setattr(draft_mod, "generate", fake)

    out = draft_mod.draft_article(session, "a:loop")

    # The tool was dispatched, the draft persisted, generate called exactly twice.
    assert dispatched == [editor_tools.TOOL_KB_SEARCH]
    assert "The Final Draft" in out
    assert article.current_draft == out
    assert session.committed
    assert len(fake.calls) == 2

    # The loop passed tools + the assembled system context to generate, and the second call's
    # message history carries the tool_result the loop fed back.
    first_call = fake.calls[0]
    assert first_call.tools  # tools offered
    assert first_call.system  # system blocks assembled
    second_msgs = fake.calls[1].messages
    # The tool_result for tu_kb must be present in the history sent on turn 2.
    flat = str(second_msgs)
    assert "tu_kb" in flat
    assert "tool_result" in flat


def test_draft_loop_final_text_first_turn(monkeypatch):
    """If the model returns final text immediately (no tools), that text is the draft."""
    from app.editor import draft as draft_mod

    article = _LoopArticle()
    session = _LoopSession(article)
    monkeypatch.setattr(
        draft_mod, "load_grounding_bundle",
        lambda s, aid: _bundle(("H", "https://ex.com/s", "fact")),
    )
    monkeypatch.setattr(draft_mod, "load_voice_files", lambda: ctx.VoiceFiles())
    fake = _scripted_generate(_response(_text_block("# Done\n\nbody")))
    monkeypatch.setattr(draft_mod, "generate", fake)

    out = draft_mod.draft_article(session, "a:loop")
    assert "# Done" in out
    assert len(fake.calls) == 1


def test_draft_flagship_article_owner_bundle_uses_tech_explainer(monkeypatch):
    """A FLAGSHIP article (no cluster, ≥1 owner source, tech_explainer) drafts from the owner's
    material: the grounding bundle is owner-only, the tech_explainer brief reaches the prompt, and
    the draft is persisted. The fake provider is not needed — generate is scripted directly."""
    from app.editor import draft as draft_mod

    article = _LoopArticle()
    article.piece_type = "tech_explainer"
    session = _LoopSession(article)
    # Owner-only grounding bundle (no cluster) — has_full_text true from owner content alone.
    monkeypatch.setattr(
        draft_mod, "load_grounding_bundle",
        lambda s, aid: _owner_bundle(("My result", "", "throughput was 5000 rps")),
    )
    monkeypatch.setattr(draft_mod, "load_voice_files", lambda: ctx.VoiceFiles())

    fake = _scripted_generate(_response(_text_block("# Explainer\n\nGrounded teach-down body.")))
    monkeypatch.setattr(draft_mod, "generate", fake)

    out = draft_mod.draft_article(session, "a:loop")
    assert "Explainer" in out
    assert article.current_draft == out
    assert session.committed
    # The tech_explainer brief + the OWNER ARTIFACT note reached the system prompt.
    flat = ctx.system_blocks_to_text(fake.calls[0].system)
    assert "tech_explainer" in flat
    assert "OWNER ARTIFACT" in flat
    assert "authoritative source facts" in flat


def test_draft_refuses_when_no_grounding_corpus(monkeypatch):
    """An article whose grounding union is empty (no cluster full_text AND no owner material) → a
    clear refusal (grounding has nothing to stand on), not an ungrounded draft (hard rule 2)."""
    from app.editor import draft as draft_mod

    article = _LoopArticle()
    session = _LoopSession(article)
    monkeypatch.setattr(
        draft_mod, "load_grounding_bundle",
        lambda s, aid: _bundle(("H", "https://ex.com/s", "")),  # no full_text, no owner material
    )
    monkeypatch.setattr(draft_mod, "load_voice_files", lambda: ctx.VoiceFiles())
    monkeypatch.setattr(draft_mod, "generate", _scripted_generate())  # must never be called

    with pytest.raises(ValueError, match="no grounding corpus"):
        draft_mod.draft_article(session, "a:loop")


def test_draft_loop_respects_turn_cap(monkeypatch):
    """A model that keeps requesting tools must not loop forever — the cap stops it and the best
    text seen is persisted."""
    from app.editor import draft as draft_mod

    monkeypatch.setenv("MAX_TOOL_TURNS", "3")
    article = _LoopArticle()
    session = _LoopSession(article)
    monkeypatch.setattr(
        draft_mod, "load_grounding_bundle",
        lambda s, aid: _bundle(("H", "https://ex.com/s", "fact")),
    )
    monkeypatch.setattr(draft_mod, "load_voice_files", lambda: ctx.VoiceFiles())

    # Every response requests a tool again (never a clean final answer).
    def always_tool():
        return _response(
            _text_block("partial draft so far"),
            _tool_use_block(id="tu", name=editor_tools.TOOL_FETCH_SOURCE, input={"url": "https://ex.com/s"}),
        )

    calls = {"n": 0}

    def fake_generate(messages, role="generation", tools=None, system=None, **kwargs):
        calls["n"] += 1
        return always_tool()

    monkeypatch.setattr(draft_mod, "generate", fake_generate)
    # fetch_source tool returns something harmless.
    monkeypatch.setattr(draft_mod, "dispatch_tool", lambda s, c: "fetch_source: ...")

    out = draft_mod.draft_article(session, "a:loop")
    # Capped at 3 generate calls; the best partial text is persisted (never an empty crash).
    assert calls["n"] == 3
    assert "partial draft so far" in out


# --- DB-backed (guarded): article creation, kb_search, end-to-end draft ----------------------


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
    """Create an approved cluster with one item carrying pass-2 full_text. Returns the cluster id."""
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
def test_create_article_for_cluster_links_and_is_idempotent(session):
    from app.db.models import Article, ArticleCluster
    from app.editor.article import create_article_for_cluster

    cid = _approved_cluster_with_item(session)
    aid = create_article_for_cluster(session, cid)

    art = session.get(Article, aid)
    assert art is not None
    assert art.status == "drafting"
    assert art.piece_type == "hot_news"
    # Linked via article_clusters (the digest "covered" marker).
    link = session.execute(
        ArticleCluster.__table__.select().where(ArticleCluster.article_id == aid)
    ).first()
    assert link is not None

    # Idempotent-ish: a second call returns the SAME article id, no duplicate.
    aid2 = create_article_for_cluster(session, cid)
    assert aid2 == aid
    count = session.execute(
        ArticleCluster.__table__.select().where(ArticleCluster.cluster_id == cid)
    ).all()
    assert len(count) == 1


@pg_only
def test_create_article_rejects_non_approved_cluster(session):
    from app.db.models import Cluster
    from app.editor.article import create_article_for_cluster
    from app.researcher.cluster import new_cluster_id

    cid = new_cluster_id()
    session.add(Cluster(id=cid, status="new"))
    session.commit()
    with pytest.raises(ValueError, match="not 'approved'"):
        create_article_for_cluster(session, cid)


@pg_only
def test_kb_search_empty_then_nonempty(session):
    from app.db.models import Article
    from app.editor.kb import kb_search
    from app.editor.article import new_article_id
    from app.llm import embed

    # Empty KB → [].
    assert kb_search(session, "anything") == []

    # Seed a PUBLISHED, embedded article → it becomes retrievable.
    aid = new_article_id()
    text = "A published piece about retrieval augmented generation and vector search."
    session.add(Article(id=aid, piece_type="hot_news", status="published",
                        current_draft=text, embedding=embed(text)[0]))
    session.commit()

    hits = kb_search(session, "retrieval augmented generation")
    assert len(hits) >= 1
    assert hits[0].article_id == aid
    assert "retrieval" in hits[0].excerpt.lower()

    # A draft (un-published) article is NOT in the KB.
    draft_id = new_article_id()
    session.add(Article(id=draft_id, piece_type="hot_news", status="drafting",
                        current_draft="draft only", embedding=embed("draft only")[0]))
    session.commit()
    hit_ids = {h.article_id for h in kb_search(session, "draft only", top_k=10)}
    assert draft_id not in hit_ids


@pg_only
def test_draft_article_end_to_end_scripted(session, monkeypatch):
    """Full DB path: create the article from an approved cluster, then run draft_article with a
    scripted generate (tool then final draft). Asserts current_draft is persisted in Postgres."""
    from app.db.models import Article
    from app.editor import draft as draft_mod
    from app.editor.article import create_article_for_cluster

    cid = _approved_cluster_with_item(session)
    aid = create_article_for_cluster(session, cid)

    fake = _scripted_generate(
        _response(
            _text_block("checking sources"),
            _tool_use_block(id="tu_kb", name=editor_tools.TOOL_KB_SEARCH, input={"query": "topic"}),
        ),
        _response(_text_block("# Persisted Draft\n\nGrounded long-read body.")),
    )
    monkeypatch.setattr(draft_mod, "generate", fake)

    out = draft_mod.draft_article(session, aid)
    assert "Persisted Draft" in out
    session.expire_all()
    assert "Persisted Draft" in session.get(Article, aid).current_draft
    assert len(fake.calls) == 2
