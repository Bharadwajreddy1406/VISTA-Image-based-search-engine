from .base_embedding_provider import BaseEmbeddingProvider
from app.core.settings import settings
class CLIPEmbeddingProvider(BaseEmbeddingProvider):

    def __init__(self):
        self.model = settings.EMBEDDING_MODEL

    def get_embedding(self, image_data):
        """Get the CLIP embedding for a given image data."""
        return self.model.encode(image_data)