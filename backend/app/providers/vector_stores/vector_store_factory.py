from app.core.settings import settings
from app.core.enums import VectorStoreProviderChoices
class VectorStoreFactory:
    _provider = None

    @classmethod
    def get_provider(cls):
        if cls._provider is not None:
            return cls._provider

        provider_type = settings.VECTOR_STORE_PROVIDER

        match provider_type:
            case VectorStoreProviderChoices.MILVUS:
                from .milvus_provider import MilvusVectorStoreProvider
                cls._provider = MilvusVectorStoreProvider()
            case _:
                raise ValueError(f"Unsupported vector store provider: {provider_type}")

        return cls._provider
