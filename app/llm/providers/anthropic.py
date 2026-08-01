"""Anthropic API transport for generate(). Embeddings are not an Anthropic product —
embed() routes to Vertex/Voyage/fake instead."""
import os


class AnthropicProvider:
    def __init__(self):
        try:
            import anthropic
        except ImportError as e:  # pragma: no cover
            raise RuntimeError("anthropic SDK not installed (pip install anthropic)") from e
        self._client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def generate(self, messages, model, tools=None, max_tokens=4096, system=None, **kwargs):
        kw = dict(model=model, max_tokens=max_tokens, messages=messages)
        if tools:
            kw["tools"] = tools
        if system:
            kw["system"] = system
        resp = self._client.messages.create(**kw)
        if tools:
            return resp  # the agent loop inspects tool_use blocks
        return "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")

    def embed(self, texts, model):
        raise NotImplementedError(
            "Anthropic has no embedding API; set EMBEDDING_PROVIDER=vertex|voyage|fake"
        )
