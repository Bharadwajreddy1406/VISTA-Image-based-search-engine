from pydantic import model_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from app.core.enums import (
    ObjectStorageProviderChoices,
    VectorStoreProviderChoices,
    EmbeddingProviderChoices,
)


class Settings(BaseSettings):

    # ==========================================================
    # region Database
    # ==========================================================

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # ==========================================================
    # region Object Storage
    # ==========================================================

    OBJECT_STORAGE_PROVIDER: ObjectStorageProviderChoices

    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str

    # ==========================================================
    # region Vector Store
    # ==========================================================

    VECTOR_STORE_PROVIDER: VectorStoreProviderChoices

    MILVUS_HOST: str
    MILVUS_PORT: int
    MILVUS_COLLECTION_NAME: str

    # ==========================================================
    # region Embeddings
    # ==========================================================

    EMBEDDING_PROVIDER: EmbeddingProviderChoices

    EMBEDDING_MODEL_NAME: str
    EMBEDDING_DEVICE: str = "cpu"

    # ==========================================================
    # region Application
    # ==========================================================

    TOP_K_SEARCH_RESULTS: int = 20
    MAX_UPLOAD_SIZE_MB: int = 25

    IMAGE_INGESTION_ENABLED: bool = True

    
    # ==========================================================
    # region Crons
    # ==========================================================
    CRONS: bool = False

    # ==========================================================
    # Computed Properties
    # ==========================================================

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    # ==========================================================
    # region Validators
    # ==========================================================

    @model_validator(mode="after")
    def validate_database(self):
        from app.core.validations import validate_database_settings

        validate_database_settings(
            {
                "POSTGRES_HOST": self.POSTGRES_HOST,
                "POSTGRES_PORT": self.POSTGRES_PORT,
                "POSTGRES_DB": self.POSTGRES_DB,
                "POSTGRES_USER": self.POSTGRES_USER,
                "POSTGRES_PASSWORD": self.POSTGRES_PASSWORD,
            }
        )

        return self

    @model_validator(mode="after")
    def validate_object_storage(self):
        from app.core.validations import validate_object_storage_settings

        validate_object_storage_settings(
            {
                "OBJECT_STORAGE_PROVIDER": self.OBJECT_STORAGE_PROVIDER,
                "MINIO_ENDPOINT": self.MINIO_ENDPOINT,
                "MINIO_ACCESS_KEY": self.MINIO_ACCESS_KEY,
                "MINIO_SECRET_KEY": self.MINIO_SECRET_KEY,
                "MINIO_BUCKET_NAME": self.MINIO_BUCKET_NAME,
            }
        )

        return self

    @model_validator(mode="after")
    def validate_vector_store(self):
        from app.core.validations import validate_vector_store_settings

        validate_vector_store_settings(
            {
                "VECTOR_STORE_PROVIDER": self.VECTOR_STORE_PROVIDER,
                "MILVUS_HOST": self.MILVUS_HOST,
                "MILVUS_PORT": self.MILVUS_PORT,
                "MILVUS_COLLECTION_NAME": self.MILVUS_COLLECTION_NAME,
            }
        )

        return self

    @model_validator(mode="after")
    def validate_embeddings(self):
        from app.core.validations import validate_embedding_settings

        validate_embedding_settings(
            {
                "EMBEDDING_PROVIDER": self.EMBEDDING_PROVIDER,
                "EMBEDDING_MODEL_NAME": self.EMBEDDING_MODEL_NAME,
                "EMBEDDING_DEVICE": self.EMBEDDING_DEVICE,
            }
        )

        return self

    # ==========================================================
    # region Pydantic Settings Config
    # ==========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()