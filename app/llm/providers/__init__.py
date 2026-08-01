"""Provider factories. Backends are lazy-imported so optional heavy SDKs
(Vertex, Voyage) are only required when actually selected."""


def get_generation_provider(name: str):
    if name == "fake":
        from app.llm.providers.fake import FakeProvider
        return FakeProvider()
    if name == "anthropic":
        from app.llm.providers.anthropic import AnthropicProvider
        return AnthropicProvider()
    if name == "vertex":
        from app.llm.providers.vertex import VertexProvider
        return VertexProvider()
    raise ValueError(f"unknown LLM_PROVIDER {name!r} (anthropic | vertex | fake)")


def get_embedding_provider(name: str):
    if name == "fake":
        from app.llm.providers.fake import FakeProvider
        return FakeProvider()
    if name == "vertex":
        from app.llm.providers.vertex import VertexProvider
        return VertexProvider()
    if name == "voyage":
        raise NotImplementedError(
            "voyage embedding provider is a documented seam, not implemented yet; "
            "use EMBEDDING_PROVIDER=vertex or fake"
        )
    raise ValueError(f"unknown EMBEDDING_PROVIDER {name!r} (vertex | voyage | fake)")
