import hashlib

from src.core.logging import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    def __init__(self, dimensions: int = 768):
        self.dimensions = dimensions

    def generate_embedding(self, text: str) -> list[float]:
        """Generate a pseudo-embedding for testing."""
        if not text:
            return [0.0] * self.dimensions
        hash_obj = hashlib.sha256(text.encode("utf-8"))
        hash_bytes = hash_obj.digest()
        vector = []
        for i in range(self.dimensions):
            byte_val = hash_bytes[i % len(hash_bytes)]
            normalized = (byte_val / 127.5) - 1.0
            vector.append(normalized)
        return vector
