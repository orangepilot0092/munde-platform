from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingProvider(ABC):
    """
    Abstract interface for all embedding providers.
    """

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def dimensions(self) -> int:
        """
        Embedding dimension.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Provider name.
        """
        raise NotImplementedError
