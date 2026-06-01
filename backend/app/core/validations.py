
from typing import Dict
from .exceptions import DatabaseCredentialsNotFound

def validate_database_settings(DATABASE_SETTINGS: Dict[str, str]):
    required_keys = ["POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD"]
    missing_keys = [key for key in required_keys if key not in DATABASE_SETTINGS or not DATABASE_SETTINGS[key]]

    if missing_keys:
        raise DatabaseCredentialsNotFound(f"Missing database credentials: {', '.join(missing_keys)}")
    
def validate_object_storage_settings(OBJECT_STORAGE_SETTINGS: Dict[str, str]):
    pass
    # required_keys = ["OBJECT_STORAGE_PROVIDER", "MINIO_ENDPOINT", "MINIO_ACCESS_KEY", "MINIO_SECRET_KEY", "MINIO_BUCKET_NAME"]
    # missing_keys = [key for key in required_keys if key not in OBJECT_STORAGE_SETTINGS or not OBJECT_STORAGE_SETTINGS[key]]     

    # if missing_keys:
    #     raise ValueError(f"Missing object storage settings: {', '.join(missing_keys)}")
    
def validate_vector_store_settings(VECTOR_STORE_SETTINGS: Dict[str, str]):
    pass

def validate_embedding_settings(EMBEDDING_SETTINGS: Dict[str, str]):
    pass