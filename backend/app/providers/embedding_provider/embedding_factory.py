from app.core.settings import settings
from app.core.enums import EmbeddingProviderChoices
class EmbeddingFactory:

    _provider = None

    @classmethod
    def get_provider(cls):

        if cls._provider is None:
            match settings.EMBEDDING_PROVIDER:
                case EmbeddingProviderChoices.CLIP:
                    from .clip_embedding_provider import CLIPEmbeddingProvider
                    cls._provider = CLIPEmbeddingProvider()
                case _:
                    raise ValueError(
                        f"Unsupported embedding provider: {settings.EMBEDDING_PROVIDER}"
                    )

        return cls._provider