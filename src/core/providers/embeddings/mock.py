import hashlib

from .base import BaseEmbeddingProvider


class MockEmbeddingProvider(BaseEmbeddingProvider):
    """
    Deterministic SHA256 embedding provider.

    Suitable only for development and automated testing.
    """

    def __init__(self, dimensions: int = 768):
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    @property
    def provider_name(self) -> str:
        return "mock"

    def generate_embedding(self, text: str) -> list[float]:
        if not text:
            return [0.0] * self._dimensions

        digest = hashlib.sha256(text.encode("utf-8")).digest()

        vector = []

        for i in range(self._dimensions):
            value = digest[i % len(digest)]
            vector.append((value / 127.5) - 1.0)

        return vector

    def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts using deterministic SHA256."""
        return [self.generate_embedding(text) for text in texts]
