"""Role -> model mapping and provider selection. No pipeline step ever hardcodes a
model; it passes a logical role and this module resolves it (overridable via env).

EMBEDDING_DIM is the single source of truth for the pgvector column width — kept at
1536 because gemini-embedding-001's default 3072 exceeds pgvector's ~2000-dim index
limit. The DB schema imports it from here, so dimension and embedder never drift.
"""
import os

EMBEDDING_DIM = int(os.environ.get("EMBEDDING_DIM", "1536"))

# Logical role -> default model. Override any role with env LLM_MODEL_<ROLE>.
_DEFAULT_MODELS = {
    "generation": "claude-sonnet-4-6",            # workhorse: triage, drafting, iteration, variants
    "generation_high": "claude-opus-4-8",         # optional higher-quality draft tier
    "cheap": "claude-haiku-4-5-20251001",         # classification, optional triage summaries
    "embedding": "gemini-embedding-001",          # dedup + KB retrieval vectors
}

GENERATION_ROLES = {"generation", "generation_high", "cheap"}


def model_for(role: str) -> str:
    if role not in _DEFAULT_MODELS:
        raise ValueError(f"unknown LLM role {role!r}; known: {sorted(_DEFAULT_MODELS)}")
    return os.environ.get(f"LLM_MODEL_{role.upper()}", _DEFAULT_MODELS[role])


def generation_provider() -> str:
    """Backend for generate(): anthropic (default) | vertex | fake."""
    return os.environ.get("LLM_PROVIDER", "anthropic").lower()


def embedding_provider() -> str:
    """Backend for embed(): vertex (default) | voyage | fake."""
    return os.environ.get("EMBEDDING_PROVIDER", "vertex").lower()
