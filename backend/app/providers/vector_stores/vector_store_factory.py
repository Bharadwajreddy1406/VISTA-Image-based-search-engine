from app.core.settings import settings
from app.core.enums import VectorStoreProviderChoices
class VectorStoreFactory:

    @staticmethod
    def get_provider():
        provider_type = settings.VECTOR_STORE_PROVIDER

        match provider_type:
            case VectorStoreProviderChoices.MILVUS.value:
                from .milvus_provider import MilvusVectorStoreProvider
                return MilvusVectorStoreProvider()
            case _:
                raise ValueError(f"Unsupported vector store provider: {provider_type}")
