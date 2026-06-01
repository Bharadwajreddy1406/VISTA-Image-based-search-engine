from app.core.settings import settings
from app.core.enums import EmbeddingProviderChoices
class EmbeddingFactory:

    _provider = None

    @classmethod
    def get_provider(cls):

        if cls._provider is None:
            if settings.EMBEDDING_MODEL_TYPE == EmbeddingProviderChoices.CLIP.value:
                from .clip_embedding_provider import CLIPEmbeddingProvider
                cls._provider = CLIPEmbeddingProvider()
            else:
                raise ValueError(f"Unsupported embedding model type: {settings.EMBEDDING_MODEL_TYPE}")
        
        return cls._provider