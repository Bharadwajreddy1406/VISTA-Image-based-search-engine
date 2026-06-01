from app.core.enums import ObjectStorageProviderChoices
from app.core.settings import settings

class ObjectStoreFactory:

    _provider = None

    @classmethod
    def get_provider(cls):
        if cls._provider is not None:
            return cls._provider
        provider_type = settings.OBJECT_STORAGE_PROVIDER

        match provider_type:
            case ObjectStorageProviderChoices.MINIO.value:
                from app.providers.object_storages.minio_provider import MinIOProvider
                cls._provider = MinIOProvider()
            case _:
                raise ValueError(f"Unsupported object storage provider: {provider_type}")
            
        return cls._provider