"""Prompt-caching regression lock (Phase 7 hardening).

The three generation paths that resend a LARGE STABLE system prefix across MULTIPLE calls each
carry exactly ONE `cache_control` breakpoint, placed on the last STABLE block so the whole stable
prefix is cached and any volatile trailing block stays uncached:

  - draft  (app.editor.context.build_system_blocks)         — the within-call agent tool loop
    resends header + grounding + piece brief + voice + SOURCE BUNDLE each turn.
  - iterate(app.editor.context.build_iterate_system_blocks) — same stable prefix, PLUS a volatile
    CURRENT DRAFT block that changes every owner turn and MUST be after the breakpoint (uncached).
  - variant(app.variants.format.build_variant_system_blocks)— the 3-4 platform calls reuse the
    same cached canonical.

These invariants are already asserted piecemeal in tests/test_editor.py, tests/test_iterate.py,
and tests/test_variants.py; this module consolidates them into one regression so the contract
can't silently regress (e.g. a refactor that moves the breakpoint, drops it, or marks a second
block). It also pins that the Anthropic provider forwards `system` blocks unchanged, so the
`cache_control` markers actually reach the API (no beta header needed for the configured recent
models — caching is GA on the standard Messages API for Sonnet 4.x / Opus 4.x / Haiku 4.x).

PURE + no network: the block assembly is string-in/list-out, and the provider forwarding is
checked with a fake SDK client (no real API call). No DB, no live LLM.
"""
from __future__ import annotations

from types import SimpleNamespace

from app.editor import context as ctx
from app.variants import format as vmod


# --- helpers -------------------------------------------------------------------------------


def _bundle(*items):
    """A SourceBundle of (title, url, full_text) tuples — same shape as the editor tests use."""
    return ctx.SourceBundle(
        cluster_id="c1",
        items=[ctx.SourceItem(title=t, url=u, full_text=x) for (t, u, x) in items],
    )


def _assert_single_breakpoint_on(blocks, idx):
    """Exactly ONE cache_control breakpoint, on block `idx` (idx may be negative), ephemeral."""
    marked = [i for i, b in enumerate(blocks) if "cache_control" in b]
    norm = [i % len(blocks) for i in marked]
    assert norm == [idx % len(blocks)], (
        f"expected exactly one cache_control breakpoint on block {idx}, got {marked}"
    )
    assert blocks[idx].get("cache_control") == {"type": "ephemeral"}


# --- draft: one breakpoint on the last (stable) block --------------------------------------


def test_draft_system_blocks_have_one_breakpoint_on_last_stable_block():
    blocks = ctx.build_system_blocks(
        voice=ctx.VoiceFiles(style_guide="VOICE"),
        bundle=_bundle(("H", "https://ex.com/p", "body text")),
    )
    # The SOURCE BUNDLE is the last (and only volatile-free) block in the draft prompt.
    assert "SOURCE BUNDLE" in blocks[-1]["text"]
    _assert_single_breakpoint_on(blocks, -1)


# --- iterate: one breakpoint on the last STABLE block; volatile draft block AFTER it, uncached


def test_iterate_system_blocks_breakpoint_on_bundle_not_volatile_draft():
    blocks = ctx.build_iterate_system_blocks(
        voice=ctx.VoiceFiles(style_guide="VOICE"),
        bundle=_bundle(("H", "https://ex.com/p", "body text")),
        current_draft="THE WORKING DRAFT",
    )
    # Last block is the volatile CURRENT DRAFT and must be UNcached (it changes every owner turn).
    assert "CURRENT DRAFT" in blocks[-1]["text"]
    assert "cache_control" not in blocks[-1]
    # The single breakpoint sits on the last STABLE block (the SOURCE BUNDLE) right above it.
    assert "SOURCE BUNDLE" in blocks[-2]["text"]
    _assert_single_breakpoint_on(blocks, -2)


def test_iterate_breakpoint_stays_on_bundle_when_draft_is_empty():
    # Even with an empty draft the volatile block is still appended uncached and the breakpoint
    # stays on the stable bundle — the placement must not depend on the draft's content.
    blocks = ctx.build_iterate_system_blocks(
        voice=ctx.VoiceFiles(),
        bundle=_bundle(("H", "https://ex.com/p", "t")),
        current_draft="",
    )
    assert "CURRENT DRAFT" in blocks[-1]["text"]
    assert "cache_control" not in blocks[-1]
    _assert_single_breakpoint_on(blocks, -2)


# --- variant: one breakpoint on the canonical block ----------------------------------------


def test_variant_system_blocks_have_one_breakpoint_on_canonical():
    blocks = vmod.build_variant_system_blocks("# Canonical\n\nApproved long-read body.")
    # The canonical is the last, largest, stable block — the 3-4 platform calls reuse it cached.
    assert "CANONICAL" in blocks[-1]["text"]
    _assert_single_breakpoint_on(blocks, -1)


# --- provider forwarding: cache_control on system blocks reaches the API --------------------


class _CapturingMessages:
    def __init__(self):
        self.captured_kwargs = None

    def create(self, **kwargs):
        self.captured_kwargs = kwargs
        # Shape the response like the Anthropic SDK: .content is a list of typed blocks.
        return SimpleNamespace(content=[SimpleNamespace(type="text", text="ok")])


class _FakeAnthropicClient:
    def __init__(self):
        self.messages = _CapturingMessages()


def test_anthropic_provider_forwards_system_blocks_verbatim(monkeypatch):
    """generate() must pass the `system` blocks (cache_control intact) straight to messages.create
    so the breakpoint reaches the API. Built with a fake SDK client — NO real network call."""
    from app.llm.providers.anthropic import AnthropicProvider

    provider = AnthropicProvider.__new__(AnthropicProvider)  # skip __init__ (no SDK/key needed)
    provider._client = _FakeAnthropicClient()

    system_blocks = ctx.build_system_blocks(
        voice=ctx.VoiceFiles(style_guide="VOICE"),
        bundle=_bundle(("H", "https://ex.com/p", "body")),
    )
    out = provider.generate(
        messages=[{"role": "user", "content": "draft it"}],
        model="test-model",  # a literal here is fine — role->model resolves upstream in app.llm
        system=system_blocks,
        max_tokens=64,
    )

    captured = provider._client.messages.captured_kwargs
    # The exact system object is forwarded unchanged — cache_control survives to the API.
    assert captured["system"] is system_blocks
    assert any("cache_control" in b for b in captured["system"])
    # No tools passed -> the provider flattens to text.
    assert out == "ok"


def test_anthropic_provider_omits_system_when_none(monkeypatch):
    """When no system is passed, the provider must not send a `system` kwarg at all (a None/empty
    system would otherwise be a different request shape)."""
    from app.llm.providers.anthropic import AnthropicProvider

    provider = AnthropicProvider.__new__(AnthropicProvider)
    provider._client = _FakeAnthropicClient()
    provider.generate(messages=[{"role": "user", "content": "hi"}], model="test-model")
    assert "system" not in provider._client.messages.captured_kwargs
