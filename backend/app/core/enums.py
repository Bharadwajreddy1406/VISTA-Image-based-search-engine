from enum import Enum

class ImageIngestionStates(Enum):
    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

class UserConsentTypes(Enum):
    DEFAULT = "DEFAULT_CONSENT"
    YES = "USER_CONSENTED"
    NO = "USER_DENIED"

class ObjectStorageProviderChoices(Enum):
    MINIO = "MINIO"
    S3 = "S3"
    AZURE_BLOB = "AZURE_BLOB"
    GOOGLE_CLOUD_STORAGE = "GOOGLE_CLOUD_STORAGE"


class VectorStoreProviderChoices(Enum):
    FAISS = "FAISS"
    MILVUS = "MILVUS"
    QDRANT = "QDRANT"
    PINECONE = "PINECONE"

class EmbeddingProviderChoices(str, Enum):
    CLIP = "CLIP"
    OPEN_CLIP = "OPEN_CLIP"
    SIGLIP = "SIGLIP"