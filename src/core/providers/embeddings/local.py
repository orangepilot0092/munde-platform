"""Local sentence-transformer embedding provider for DGX Spark AI Node."""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any

from .base import BaseEmbeddingProvider

logger = logging.getLogger(__name__)

# Default model optimized for multilingual (Marathi/Hindi/English) government text
DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@lru_cache(maxsize=1)
def _load_model(model_name: str) -> Any:
    """Load and cache the sentence-transformer model.

    Uses lru_cache to ensure the model is loaded only once per process,
    which is critical for batch embedding generation performance.
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        raise ImportError(
            "sentence-transformers is required for LocalEmbeddingProvider. "
            "Install with: pip install sentence-transformers"
        ) from e

    logger.info("Loading embedding model: %s", model_name)
    model = SentenceTransformer(model_name)
    logger.info(
        "Model loaded: %s (dimensions=%d)",
        model_name,
        model.get_sentence_embedding_dimension(),
    )
    return model


class LocalEmbeddingProvider(BaseEmbeddingProvider):
    """Production embedding provider using local sentence-transformers.

    Designed to run on the DGX Spark AI Node for batch embedding generation.
    Supports multilingual text (Marathi, Hindi, English) for Maharashtra
    government datasets.

    Args:
        model_name: HuggingFace model identifier. Defaults to a multilingual
            model optimized for Indic languages.
        batch_size: Batch size for encoding. Larger values improve throughput
            on GPU but use more memory.
    """

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        batch_size: int = 64,
    ) -> None:
        self._model_name = model_name
        self._batch_size = batch_size
        self._model = _load_model(model_name)
        self._dimensions: int = self._model.get_sentence_embedding_dimension()

    @property
    def dimensions(self) -> int:
        return self._dimensions

    @property
    def provider_name(self) -> str:
        return f"local:{self._model_name}"

    def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding vector for a single text string.

        For batch processing, use generate_embeddings_batch() instead
        to leverage GPU parallelism.
        """
        if not text or not text.strip():
            return [0.0] * self._dimensions

        embedding = self._model.encode(text, normalize_embeddings=True)
        result: list[float] = embedding.tolist()
        return result

    def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts.

        Leverages GPU parallelism for significantly higher throughput
        compared to calling generate_embedding() in a loop.

        Args:
            texts: List of text strings to embed.

        Returns:
            List of embedding vectors in the same order as input texts.
        """
        if not texts:
            return []

        # Replace empty strings with placeholder to avoid zero-length issues
        processed = [t if t and t.strip() else "" for t in texts]

        embeddings = self._model.encode(
            processed,
            batch_size=self._batch_size,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        result: list[list[float]] = embeddings.tolist()
        return result
