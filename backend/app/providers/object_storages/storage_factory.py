from app.core.enums import ObjectStorageProviderChoices
from app.core.settings import settings

class ObjectStoreFactory:

    @staticmethod
    def get_provider():

        provider_type = settings.OBJECT_STORAGE_PROVIDER

        match provider_type:
            case ObjectStorageProviderChoices.MINIO.value:
                from app.providers.object_storages.minio_provider import MinIOProvider
                return MinIOProvider()
            case _:
                raise ValueError(f"Unsupported object storage provider: {provider_type}")