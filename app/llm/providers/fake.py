"""Deterministic, dependency-free provider for offline dev, Phase-0 round-trip
verification, and tests. NOT for production — it invents no facts, it just echoes."""
import hashlib
import math

from app.llm.config import EMBEDDING_DIM


class FakeProvider:
    def generate(self, messages, model, tools=None, **kwargs):
        last_user = ""
        for m in messages:
            if m.get("role") == "user":
                last_user = m.get("content", "")
        return f"[fake:{model}] {last_user[:280]}"

    def embed(self, texts, model):
        return [self._vec(t) for t in texts]

    @staticmethod
    def _vec(text: str):
        """Deterministic, L2-normalized pseudo-embedding of fixed dimension.
        Same text -> same vector (no randomness), so dedup/tests are reproducible."""
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        raw = []
        counter = 0
        while len(raw) < EMBEDDING_DIM:
            digest = hashlib.sha256(digest + counter.to_bytes(2, "big")).digest()
            for byte in digest:
                raw.append((byte / 255.0) * 2.0 - 1.0)
                if len(raw) >= EMBEDDING_DIM:
                    break
            counter += 1
        norm = math.sqrt(sum(x * x for x in raw)) or 1.0
        return [x / norm for x in raw]
