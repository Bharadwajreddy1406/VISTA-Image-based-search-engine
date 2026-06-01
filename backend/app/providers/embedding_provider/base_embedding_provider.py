from abc import ABC, abstractmethod

class BaseEmbeddingProvider(ABC):

    @abstractmethod
    async def get_embedding(
        self,
        image_bytes: bytes
    ) -> list[float]:
        pass

    @abstractmethod
    def initialize_model_connection(self):
        """Initialize connection to the embedding model if necessary."""
        pass

    @abstractmethod
    def close_model_connection(self):
        """Close connection to the embedding model if necessary."""
        pass