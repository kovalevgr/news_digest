"""Per-platform variant formatting (app.variants) — Phase 5 (docs/01_technical.md §2.4, §4).

DB-LIGHT by default (build plan testing note: the default suite needs no live Postgres). The
single-call model boundary is the crux and is exercised PURELY (prompt/brief assembly) and with a
monkeypatched module-level `generate` (script a return string). The status/empty guards run on a
tiny stub session; the full DB round-trip (append history, latest read) is guarded behind
RUN_PG_TESTS like the other PG tests.

Variants are a SINGLE model call per platform — NOT an agent (hard rule 5) — so `format_variant`
passes NO tools and the provider returns plain text; the tests script that text directly.
"""
from __future__ import annotations

import os
from types import SimpleNamespace

import pytest

from app.variants import format as vmod
from app.variants import (
    PLATFORMS,
    VariantResult,
    format_variant,
    generate_variant,
    latest_variant,
    list_latest_variants,
    save_variant_edit,
)

RUN_PG = os.environ.get("RUN_PG_TESTS") == "1"
pg_only = pytest.mark.skipif(not RUN_PG, reason="set RUN_PG_TESTS=1 to run DB tests")

CANONICAL = (
    "# RAG goes mainstream\n\n"
    "Retrieval-augmented generation shipped widely this week. "
    "See https://ex.com/a for the announcement and https://ex.com/b for reactions. "
    "[proposed take: this changes how teams ground LLMs]"
)


# --- contract: PLATFORMS exact tuple -------------------------------------------------------


def test_platforms_exact_tuple():
    assert PLATFORMS == ("medium", "reddit", "linkedin", "x")


def test_x_in_platforms():
    assert "x" in PLATFORMS


# --- pure: per-platform briefs carry the right markers + grounding -------------------------


def _flat(blocks):
    return "\n\n".join(b["text"] for b in blocks)


def test_medium_prompt_includes_canonical_and_markdown_markers():
    flat = _flat(vmod.build_variant_system_blocks(CANONICAL))
    # The canonical is carried into the system context verbatim.
    assert "RAG goes mainstream" in flat
    assert "https://ex.com/a" in flat

    prompt = vmod.build_variant_prompt("medium")
    assert "Medium" in prompt
    assert "Markdown" in prompt or "markdown" in prompt
    # Roughly passthrough — must NOT condense.
    assert "PASSTHROUGH" in prompt or "passthrough" in prompt.lower()
    assert "format" in prompt.lower()


def test_reddit_prompt_includes_tone_adjustment():
    prompt = vmod.build_variant_prompt("reddit")
    assert "Reddit" in prompt
    assert "tone" in prompt.lower()
    assert "subreddit" in prompt.lower()
    # Markdown, not a condense.
    assert "Markdown" in prompt or "markdown" in prompt


def test_linkedin_prompt_condenses_to_short_plain_text():
    prompt = vmod.build_variant_prompt("linkedin")
    assert "LinkedIn" in prompt
    assert "CONDENSE" in prompt or "condense" in prompt.lower()
    assert "hook" in prompt.lower()
    assert "short" in prompt.lower()
    # Plain text — no markdown headers.
    assert "PLAIN-TEXT" in prompt or "plain-text" in prompt.lower() or "plain text" in prompt.lower()


def test_x_prompt_is_hook_thread_plain_text():
    prompt = vmod.build_variant_prompt("x")
    # Targets X / Twitter.
    assert "X / Twitter" in prompt or "Twitter" in prompt
    # A hook post + a numbered thread, condensed.
    assert "hook" in prompt.lower()
    assert "thread" in prompt.lower()
    assert "CONDENSE" in prompt or "condense" in prompt.lower()
    # Numbered-thread + per-tweet length markers.
    assert "1/" in prompt
    assert "280" in prompt
    # Plain text — no markdown headings.
    assert "PLAIN TEXT" in prompt or "plain text" in prompt.lower()
    # The link rides in the final tweet; no hashtag spam / engagement-bait.
    assert "link" in prompt.lower()
    assert "hashtag" in prompt.lower()
    assert "engagement-bait" in prompt.lower() or "clickbait" in prompt.lower()


def test_every_brief_carries_grounding_language():
    # The grounding constraint lives in the system blocks (shared across platforms).
    flat = "\n\n".join(b["text"] for b in vmod.build_variant_system_blocks(CANONICAL))
    assert "no new facts" in flat.lower() or "do not introduce any new facts" in flat.lower()
    assert "provenance" in flat.lower()
    assert "REFORMATTING" in flat or "reformat" in flat.lower()
    # Opinions stay the owner's; never publish.
    assert "OWNER" in flat
    assert "never publish" in flat.lower() or "you never publish" in flat.lower()


def test_unknown_platform_brief_raises():
    with pytest.raises(ValueError, match="unknown platform"):
        vmod.platform_brief("twitter")
    with pytest.raises(ValueError, match="unknown platform"):
        vmod.build_variant_prompt("twitter")


def test_system_blocks_mark_last_block_cacheable():
    blocks = vmod.build_variant_system_blocks(CANONICAL)
    assert blocks[-1].get("cache_control") == {"type": "ephemeral"}
    assert all("cache_control" not in b for b in blocks[:-1])


def test_piece_type_folds_into_prompt():
    prompt = vmod.build_variant_prompt("medium", piece_type="project_post")
    assert "project_post" in prompt


# --- format_variant: monkeypatched module-level generate -----------------------------------


def _scripted_generate(return_text):
    """A generate() stand-in returning a fixed string; records the calls so a test can assert the
    role / system / max_tokens the single call passed."""
    calls = []

    def fake_generate(messages, role="generation", tools=None, system=None, **kwargs):
        calls.append(SimpleNamespace(messages=messages, role=role, tools=tools, system=system, kwargs=kwargs))
        return return_text

    fake_generate.calls = calls
    return fake_generate


def test_format_variant_returns_model_text_and_passes_role(monkeypatch):
    fake = _scripted_generate("# Formatted for Medium\n\nbody https://ex.com/a")
    monkeypatch.setattr(vmod, "generate", fake)

    out = format_variant("medium", CANONICAL)
    assert out == "# Formatted for Medium\n\nbody https://ex.com/a"
    # Exactly one single-shot call, role 'generation', NO tools (not an agent), system blocks set.
    assert len(fake.calls) == 1
    call = fake.calls[0]
    assert call.role == "generation"
    assert call.tools is None
    assert call.system  # canonical carried in system blocks
    assert call.kwargs.get("max_tokens") == vmod.variant_max_tokens()


def test_format_variant_caps_text(monkeypatch):
    monkeypatch.setenv("VARIANT_MAX_CHARS", "50")
    monkeypatch.setattr(vmod, "generate", _scripted_generate("z" * 5000))
    out = format_variant("reddit", CANONICAL)
    assert len(out) == 50


def test_format_variant_unknown_platform_raises(monkeypatch):
    # Must reject before ever calling generate.
    monkeypatch.setattr(vmod, "generate", _scripted_generate("should not be returned"))
    with pytest.raises(ValueError, match="unknown platform"):
        format_variant("mastodon", CANONICAL)


def test_format_variant_respects_role_env(monkeypatch):
    monkeypatch.setenv("VARIANT_ROLE", "generation_high")
    fake = _scripted_generate("out")
    monkeypatch.setattr(vmod, "generate", fake)
    format_variant("linkedin", CANONICAL)
    assert fake.calls[0].role == "generation_high"


def test_format_variant_x_returns_text_and_uses_x_brief(monkeypatch):
    # The X variant goes through the same single-call seam: returns the model text and the X brief
    # reaches the model (the user turn carries the brief built by build_variant_prompt).
    fake = _scripted_generate("Hook tweet about RAG\n\n1/ detail https://ex.com/a")
    monkeypatch.setattr(vmod, "generate", fake)

    out = format_variant("x", CANONICAL)
    assert out == "Hook tweet about RAG\n\n1/ detail https://ex.com/a"
    assert len(fake.calls) == 1
    call = fake.calls[0]
    assert call.role == "generation"
    assert call.tools is None  # single-shot, not an agent
    # The X brief's guidance rode into the single call's user turn.
    user_turn = call.messages[0]["content"]
    assert "X / Twitter" in user_turn or "Twitter" in user_turn
    assert "thread" in user_turn.lower()
    assert "280" in user_turn
    # The shared grounding still rides in the system blocks (not weakened by the new platform).
    flat = "\n\n".join(b["text"] for b in call.system)
    assert "provenance" in flat.lower()


# --- DB-light: generate_variant status/empty guards (stub session) -------------------------


class _StubArticle:
    def __init__(self, *, status="pre_publish", current_draft=CANONICAL, piece_type="hot_news"):
        self.id = "a:stub"
        self.status = status
        self.current_draft = current_draft
        self.piece_type = piece_type


class _StubSession:
    """Tiny stub: session.get(Article, id) → the article; commit() records; add() captures the row.
    Sufficient for generate_variant's guard paths (which return before/at the insert)."""
    def __init__(self, article):
        self._article = article
        self.added = []
        self.committed = False

    def get(self, model, ident):
        return self._article

    def add(self, obj):
        # Mimic the autoincrement PK so VariantResult.variant_id is an int (real DB assigns it).
        obj.id = 1
        self.added.append(obj)

    def commit(self):
        self.committed = True


def test_generate_variant_unknown_platform_raises():
    sess = _StubSession(_StubArticle())
    with pytest.raises(ValueError, match="unknown platform"):
        generate_variant(sess, "a:stub", "twitter")


def test_generate_variant_missing_article_raises():
    class _Empty:
        def get(self, model, ident):
            return None
    with pytest.raises(ValueError, match="not found"):
        generate_variant(_Empty(), "a:missing", "medium")


def test_generate_variant_refuses_drafting_article(monkeypatch):
    monkeypatch.setattr(vmod, "format_variant", lambda *a, **k: "should not run")
    sess = _StubSession(_StubArticle(status="drafting"))
    with pytest.raises(ValueError, match="Gate 2"):
        generate_variant(sess, "a:stub", "medium")
    assert not sess.committed


def test_generate_variant_refuses_empty_draft(monkeypatch):
    monkeypatch.setattr(vmod, "format_variant", lambda *a, **k: "should not run")
    sess = _StubSession(_StubArticle(current_draft="   "))
    with pytest.raises(ValueError, match="empty"):
        generate_variant(sess, "a:stub", "medium")


def test_generate_variant_persists_via_stub(monkeypatch):
    # pre_publish + non-empty draft → format_variant runs, a Variant row is added + committed.
    monkeypatch.setattr(vmod, "format_variant", lambda platform, canonical, *, piece_type=None: f"VAR[{platform}]")
    sess = _StubSession(_StubArticle(status="pre_publish"))
    res = generate_variant(sess, "a:stub", "medium")
    assert isinstance(res, VariantResult)
    assert res.platform == "medium"
    assert res.formatted_text == "VAR[medium]"
    assert res.article_id == "a:stub"
    assert sess.committed
    assert len(sess.added) == 1


def test_generate_variant_allows_published_article(monkeypatch):
    # A re-derive after publishing is still allowed (status published is a valid source).
    monkeypatch.setattr(vmod, "format_variant", lambda *a, **k: "ok")
    sess = _StubSession(_StubArticle(status="published"))
    res = generate_variant(sess, "a:stub", "reddit")
    assert res.formatted_text == "ok"
    assert sess.committed


# --- DB-light: save_variant_edit guards (stub session, NO model call) ----------------------

# A module-level generate() that explodes if called — save_variant_edit is a plain DB write and
# must NEVER reach the model. Installed in the tests below so any accidental call fails loudly.
def _exploding_generate(*a, **k):
    raise AssertionError("save_variant_edit must NOT call the model")


def test_save_variant_edit_unknown_platform_raises(monkeypatch):
    monkeypatch.setattr(vmod, "generate", _exploding_generate)
    sess = _StubSession(_StubArticle())
    with pytest.raises(ValueError, match="unknown platform"):
        save_variant_edit(sess, "a:stub", "twitter", "hand-tuned")
    assert not sess.committed


def test_save_variant_edit_missing_article_raises(monkeypatch):
    monkeypatch.setattr(vmod, "generate", _exploding_generate)

    class _Empty:
        def get(self, model, ident):
            return None

    with pytest.raises(ValueError, match="not found"):
        save_variant_edit(_Empty(), "a:missing", "medium", "hand-tuned")


def test_save_variant_edit_empty_text_raises(monkeypatch):
    monkeypatch.setattr(vmod, "generate", _exploding_generate)
    sess = _StubSession(_StubArticle())
    with pytest.raises(ValueError, match="empty"):
        save_variant_edit(sess, "a:stub", "medium", "")
    with pytest.raises(ValueError, match="empty"):
        save_variant_edit(sess, "a:stub", "medium", "   \n\t  ")
    with pytest.raises(ValueError, match="empty"):
        save_variant_edit(sess, "a:stub", "medium", None)
    assert not sess.committed


def test_save_variant_edit_persists_without_model_call(monkeypatch):
    # The happy path on a stub session: NO model call, a Variant row is added + committed,
    # the text is stripped and stored verbatim. _StubSession.latest read is None (no prior row),
    # so the no-op guard does not fire.
    monkeypatch.setattr(vmod, "generate", _exploding_generate)
    monkeypatch.setattr(vmod, "latest_variant", lambda *a, **k: None)
    sess = _StubSession(_StubArticle())
    res = save_variant_edit(sess, "a:stub", "medium", "  hand-tuned variant text  ")
    assert isinstance(res, VariantResult)
    assert res.platform == "medium"
    assert res.formatted_text == "hand-tuned variant text"
    assert res.article_id == "a:stub"
    assert sess.committed
    assert len(sess.added) == 1


def test_save_variant_edit_noop_when_text_unchanged(monkeypatch):
    # If the latest stored text already equals the (stripped) input, return it without appending.
    monkeypatch.setattr(vmod, "generate", _exploding_generate)
    same = VariantResult(article_id="a:stub", platform="medium", formatted_text="kept text", variant_id=7)
    monkeypatch.setattr(vmod, "latest_variant", lambda *a, **k: same)
    sess = _StubSession(_StubArticle())
    res = save_variant_edit(sess, "a:stub", "medium", "  kept text  ")
    assert res is same
    assert res.variant_id == 7
    assert not sess.committed
    assert sess.added == []


def test_save_variant_edit_ignores_article_status(monkeypatch):
    # Unlike generate_variant, save_variant_edit does NOT gate on Gate-2 status: the owner can save
    # a hand-tuned variant regardless of the canonical's lifecycle stage.
    monkeypatch.setattr(vmod, "generate", _exploding_generate)
    monkeypatch.setattr(vmod, "latest_variant", lambda *a, **k: None)
    sess = _StubSession(_StubArticle(status="drafting"))
    res = save_variant_edit(sess, "a:stub", "reddit", "owner text")
    assert res.formatted_text == "owner text"
    assert sess.committed


# --- DB-backed (guarded): append history + latest reads ------------------------------------


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


def _pre_publish_article(session, *, status="pre_publish", draft=CANONICAL):
    from app.db.models import Article
    from app.editor.article import new_article_id

    aid = new_article_id()
    session.add(Article(id=aid, piece_type="hot_news", status=status, current_draft=draft))
    session.commit()
    return aid


@pg_only
def test_generate_variant_stores_and_appends(session, monkeypatch):
    # Script the single call so no API is needed; each call returns a distinct text.
    seq = iter(["FIRST medium variant", "SECOND medium variant"])
    monkeypatch.setattr(vmod, "format_variant", lambda *a, **k: next(seq))

    aid = _pre_publish_article(session)
    r1 = generate_variant(session, aid, "medium")
    assert r1.formatted_text == "FIRST medium variant"
    assert isinstance(r1.variant_id, int)

    # A second call APPENDS a new row (no overwrite — variant history is preserved).
    r2 = generate_variant(session, aid, "medium")
    assert r2.formatted_text == "SECOND medium variant"
    assert r2.variant_id != r1.variant_id

    # latest_variant returns the NEWEST (highest id) row.
    latest = latest_variant(session, aid, "medium")
    assert latest is not None
    assert latest.variant_id == r2.variant_id
    assert latest.formatted_text == "SECOND medium variant"


@pg_only
def test_generate_variant_stores_and_reads_x_variant(session, monkeypatch):
    # The X platform persists + reads back exactly like the other platforms.
    monkeypatch.setattr(vmod, "format_variant", lambda *a, **k: "Hook\n\n1/ point https://ex.com/a")
    aid = _pre_publish_article(session)

    res = generate_variant(session, aid, "x")
    assert res.platform == "x"
    assert isinstance(res.variant_id, int)
    assert res.formatted_text == "Hook\n\n1/ point https://ex.com/a"

    latest = latest_variant(session, aid, "x")
    assert latest is not None
    assert latest.variant_id == res.variant_id
    assert latest.platform == "x"
    assert latest.formatted_text == "Hook\n\n1/ point https://ex.com/a"


@pg_only
def test_list_latest_variants_one_per_platform(session, monkeypatch):
    monkeypatch.setattr(vmod, "format_variant", lambda platform, canonical, *, piece_type=None: f"{platform}-text")
    aid = _pre_publish_article(session)
    generate_variant(session, aid, "medium")
    generate_variant(session, aid, "reddit")
    # Regenerate medium so there are two medium rows; only the latest should appear.
    monkeypatch.setattr(vmod, "format_variant", lambda *a, **k: "medium-text-v2")
    generate_variant(session, aid, "medium")

    latest = list_latest_variants(session, aid)
    assert set(latest.keys()) == {"medium", "reddit"}  # linkedin never generated → absent
    assert latest["medium"].formatted_text == "medium-text-v2"
    assert latest["reddit"].formatted_text == "reddit-text"


@pg_only
def test_latest_variant_none_when_never_generated(session):
    aid = _pre_publish_article(session)
    assert latest_variant(session, aid, "linkedin") is None
    assert list_latest_variants(session, aid) == {}


@pg_only
def test_generate_variant_refuses_drafting_in_db(session, monkeypatch):
    monkeypatch.setattr(vmod, "format_variant", lambda *a, **k: "should not run")
    aid = _pre_publish_article(session, status="drafting")
    with pytest.raises(ValueError, match="Gate 2"):
        generate_variant(session, aid, "medium")


@pg_only
def test_generate_variant_refuses_empty_draft_in_db(session, monkeypatch):
    monkeypatch.setattr(vmod, "format_variant", lambda *a, **k: "should not run")
    aid = _pre_publish_article(session, draft="")
    with pytest.raises(ValueError, match="empty"):
        generate_variant(session, aid, "medium")


# --- DB-backed (guarded): save_variant_edit round-trip + no-op + append ---------------------


def _count_variants(session, article_id, platform):
    from sqlalchemy import func, select as _select
    from app.db.models import Variant

    return session.execute(
        _select(func.count())
        .select_from(Variant)
        .where(Variant.article_id == article_id)
        .where(Variant.platform == platform)
    ).scalar_one()


@pg_only
def test_save_variant_edit_round_trip(session):
    # No model monkeypatch needed: save_variant_edit makes no model call.
    aid = _pre_publish_article(session)
    res = save_variant_edit(session, aid, "medium", "hand-tuned text")
    assert isinstance(res.variant_id, int)
    assert res.formatted_text == "hand-tuned text"

    latest = latest_variant(session, aid, "medium")
    assert latest is not None
    assert latest.variant_id == res.variant_id
    assert latest.formatted_text == "hand-tuned text"
    assert _count_variants(session, aid, "medium") == 1


@pg_only
def test_save_variant_edit_same_text_is_noop(session):
    aid = _pre_publish_article(session)
    r1 = save_variant_edit(session, aid, "medium", "hand-tuned text")
    assert _count_variants(session, aid, "medium") == 1

    # Saving the SAME text again (even with surrounding whitespace) does NOT append a row.
    r2 = save_variant_edit(session, aid, "medium", "  hand-tuned text  ")
    assert r2.variant_id == r1.variant_id
    assert _count_variants(session, aid, "medium") == 1


@pg_only
def test_save_variant_edit_different_text_appends(session):
    aid = _pre_publish_article(session)
    r1 = save_variant_edit(session, aid, "medium", "first edit")
    assert _count_variants(session, aid, "medium") == 1

    r2 = save_variant_edit(session, aid, "medium", "second edit")
    assert r2.variant_id != r1.variant_id
    assert _count_variants(session, aid, "medium") == 2

    latest = latest_variant(session, aid, "medium")
    assert latest.variant_id == r2.variant_id
    assert latest.formatted_text == "second edit"


@pg_only
def test_save_variant_edit_empty_text_in_db_raises(session):
    aid = _pre_publish_article(session)
    with pytest.raises(ValueError, match="empty"):
        save_variant_edit(session, aid, "medium", "   ")
    assert _count_variants(session, aid, "medium") == 0
