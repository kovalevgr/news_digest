"""Thin, swappable LLM interface (docs/01_technical.md §4).

    generate(messages, role="generation", tools=None) -> str | provider response
    embed(texts) -> list[list[float]]

Steps pass a logical role, never a model id. Transport is selected by env
(LLM_PROVIDER / EMBEDDING_PROVIDER) behind a provider seam, so the model and the
embedding backend stay swappable.
"""
from app.llm.config import (
    EMBEDDING_DIM,
    embedding_provider,
    generation_provider,
    model_for,
)
from app.llm import providers


def generate(messages, role: str = "generation", tools=None, **kwargs):
    """Run a generation. Returns plain text when no tools are passed; returns the
    raw provider response when tools are passed (the agent loop inspects tool_use)."""
    model = model_for(role)
    provider = providers.get_generation_provider(generation_provider())
    return provider.generate(messages=messages, model=model, tools=tools, **kwargs)


def embed(texts):
    """Embed one string or a list of strings -> list of vectors (length EMBEDDING_DIM)."""
    if isinstance(texts, str):
        texts = [texts]
    provider_name = embedding_provider()
    model = model_for("embedding")
    provider = providers.get_embedding_provider(provider_name)
    vectors = provider.embed(texts=texts, model=model)

    # Guard the provider->DB boundary: fail loudly here, with a precise message, instead of as
    # an opaque pgvector insert error if a region/model/provider misconfig returns the wrong
    # count or dimension (e.g. a Vertex model defaulting to 3072 instead of EMBEDDING_DIM).
    if len(vectors) != len(texts):
        raise ValueError(
            f"embedding provider {provider_name!r} (role 'embedding', model {model!r}) "
            f"returned {len(vectors)} vector(s) for {len(texts)} input(s)"
        )
    for i, v in enumerate(vectors):
        if len(v) != EMBEDDING_DIM:
            raise ValueError(
                f"embedding provider {provider_name!r} (role 'embedding', model {model!r}) "
                f"returned dim {len(v)} for input #{i}, expected EMBEDDING_DIM={EMBEDDING_DIM}"
            )
    return vectors


__all__ = ["generate", "embed", "model_for", "EMBEDDING_DIM"]
