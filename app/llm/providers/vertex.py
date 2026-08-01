"""Vertex AI transport: Claude via Model Garden + gemini embeddings, billed to one
GCP account via ADC (no API key). Requires extra installs:
    pip install "anthropic[vertex]" google-genai
(Claude generation uses anthropic[vertex]; embeddings use the Google Gen AI SDK,
google-genai — the old vertexai.language_models embedding SDK was removed 2026-06-24.)
and GOOGLE_CLOUD_PROJECT / GOOGLE_CLOUD_LOCATION (+ ADC).

Note: Claude model ids on Vertex use the publisher form; set LLM_MODEL_<ROLE> to the
Vertex-style id if it differs from the default Anthropic id.
"""
import os

from app.llm.config import EMBEDDING_DIM


class VertexProvider:
    def __init__(self):
        self._project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        self._location = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-central2")

    def _claude(self):
        try:
            from anthropic import AnthropicVertex
        except ImportError as e:  # pragma: no cover
            raise RuntimeError('install "anthropic[vertex]" for Vertex Claude transport') from e
        return AnthropicVertex(project_id=self._project, region=self._location)

    def generate(self, messages, model, tools=None, max_tokens=4096, system=None, **kwargs):
        client = self._claude()
        kw = dict(model=model, max_tokens=max_tokens, messages=messages)
        if tools:
            kw["tools"] = tools
        if system:
            kw["system"] = system
        resp = client.messages.create(**kw)
        if tools:
            return resp
        return "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")

    def embed(self, texts, model):
        try:
            from google import genai
            from google.genai.types import EmbedContentConfig
        except ImportError as e:  # pragma: no cover
            raise RuntimeError("install google-genai for Vertex embeddings") from e
        client = genai.Client(vertexai=True, project=self._project, location=self._location)
        resp = client.models.embed_content(
            model=model,
            contents=texts,
            config=EmbedContentConfig(output_dimensionality=EMBEDDING_DIM),
        )
        return [e.values for e in resp.embeddings]
