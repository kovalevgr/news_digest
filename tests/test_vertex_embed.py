"""Vertex embeddings transport (app.llm.providers.vertex.VertexProvider.embed) — Phase 7.

Behavior-preserving swap off the removed `vertexai.language_models` SDK to the Google
Gen AI SDK (`google-genai`). DB-light and fully OFFLINE: we inject a fake `google.genai`
(+ `google.genai.types`) into sys.modules so the lazy import inside embed() resolves to a
recording double — no client is ever constructed against a real endpoint, no network call.

We assert the new call shape (client kwargs, embed_content args incl. output_dimensionality
== EMBEDDING_DIM) and the unchanged return contract (list[list[float]], one per input,
order preserved), plus the clear RuntimeError when the package is absent.
"""
from __future__ import annotations

import sys
import types

import pytest

from app.llm.config import EMBEDDING_DIM
from app.llm.providers.vertex import VertexProvider


class _FakeEmbedding:
    def __init__(self, values):
        self.values = values


class _FakeEmbedResponse:
    def __init__(self, embeddings):
        self.embeddings = embeddings


class _FakeModels:
    def __init__(self, recorder):
        self._rec = recorder

    def embed_content(self, *, model, contents, config):
        # Record exactly what the provider passed so the test can assert the call shape.
        self._rec["model"] = model
        self._rec["contents"] = contents
        self._rec["config"] = config
        # One embedding per input text, order preserved; each a length-EMBEDDING_DIM vector.
        embeddings = [
            _FakeEmbedding([float(i)] * EMBEDDING_DIM) for i, _ in enumerate(contents)
        ]
        return _FakeEmbedResponse(embeddings)


class _FakeClient:
    def __init__(self, recorder, **kwargs):
        recorder["client_kwargs"] = kwargs
        self.models = _FakeModels(recorder)


class _FakeEmbedContentConfig:
    """Stand-in for google.genai.types.EmbedContentConfig: records the kwargs it's built with."""

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.output_dimensionality = kwargs.get("output_dimensionality")


def _install_fake_genai(monkeypatch, recorder):
    """Inject fake `google.genai` and `google.genai.types` modules into sys.modules so the
    lazy `from google import genai` / `from google.genai.types import EmbedContentConfig`
    inside embed() resolve to our doubles. Uses monkeypatch.setitem so it's auto-undone."""
    # Ensure a `google` namespace package exists without clobbering a real one's attrs.
    google_mod = sys.modules.get("google")
    if google_mod is None:
        google_mod = types.ModuleType("google")
        monkeypatch.setitem(sys.modules, "google", google_mod)

    genai_mod = types.ModuleType("google.genai")
    genai_mod.Client = lambda **kwargs: _FakeClient(recorder, **kwargs)

    types_mod = types.ModuleType("google.genai.types")
    types_mod.EmbedContentConfig = _FakeEmbedContentConfig
    genai_mod.types = types_mod

    monkeypatch.setitem(sys.modules, "google.genai", genai_mod)
    monkeypatch.setitem(sys.modules, "google.genai.types", types_mod)
    # `from google import genai` reads the attribute off the google package object.
    monkeypatch.setattr(google_mod, "genai", genai_mod, raising=False)


def test_embed_call_shape_and_return(monkeypatch):
    rec: dict = {}
    _install_fake_genai(monkeypatch, rec)

    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "proj-x")
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "europe-central2")
    provider = VertexProvider()

    out = provider.embed(["a", "b"], "gemini-embedding-001")

    # Client constructed against Vertex with the configured project/location.
    assert rec["client_kwargs"] == {
        "vertexai": True,
        "project": "proj-x",
        "location": "europe-central2",
    }

    # embed_content received the role-supplied model (NOT hardcoded), the contents verbatim,
    # and output_dimensionality pinned to EMBEDDING_DIM for parity with stored vectors.
    assert rec["model"] == "gemini-embedding-001"
    assert rec["contents"] == ["a", "b"]
    assert rec["config"].output_dimensionality == EMBEDDING_DIM
    # No task_type set — raw-value parity with the old call.
    assert "task_type" not in rec["config"].kwargs

    # Return contract: list[list[float]], one per input, order preserved (the .values lists).
    assert out == [[0.0] * EMBEDDING_DIM, [1.0] * EMBEDDING_DIM]
    assert len(out) == 2
    assert all(len(v) == EMBEDDING_DIM for v in out)


def test_embed_missing_package_raises_clear_runtimeerror(monkeypatch):
    # Robustly simulate google-genai NOT installed — regardless of whether an earlier test or
    # import in the same session already cached the real module. `from google import genai` reads
    # the `genai` attribute off the already-imported `google` package when present (bypassing
    # sys.modules), so poisoning sys.modules alone is order-fragile: also drop the cached attribute
    # and the cached submodule, so the import genuinely fails with ImportError -> RuntimeError.
    google_mod = sys.modules.get("google")
    if google_mod is not None:
        monkeypatch.delattr(google_mod, "genai", raising=False)
    monkeypatch.delitem(sys.modules, "google.genai.types", raising=False)
    monkeypatch.setitem(sys.modules, "google.genai", None)

    provider = VertexProvider()
    with pytest.raises(RuntimeError, match="install google-genai for Vertex embeddings"):
        provider.embed(["a"], "gemini-embedding-001")
