from abc import ABC, abstractmethod

class BaseEmbeddingProvider(ABC):

    @abstractmethod
    def get_embedding(self, image_data):
        """Get the embedding for a given image data."""
        pass