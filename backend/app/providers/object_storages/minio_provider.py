from .base_object_storage_provider import BaseObjectStorageProvider
from minio import Minio
from app.core.settings import settings

class MinIOProvider(BaseObjectStorageProvider):

    def __init__(
        self,
        endpoint: str = settings.MINIO_ENDPOINT,
        access_key: str = settings.MINIO_ROOT_USER,
        secret_key: str = settings.MINIO_ROOT_PASSWORD,
        bucket_name: str = settings.MINIO_STORAGE_BUCKET_NAME,
        secure: bool = False,
    ):
        """
        Initialize MinIO provider with settings or custom values.
        
        Args:
            endpoint: MinIO endpoint (default: from settings.MINIO_ENDPOINT)
            access_key: MinIO access key (default: from settings.MINIO_ROOT_USER)
            secret_key: MinIO secret key (default: from settings.MINIO_ROOT_PASSWORD)
            bucket_name: Bucket name (default: from settings.MINIO_STORAGE_BUCKET_NAME)
            secure: Use HTTPS (default: False)
        """
        self.endpoint = endpoint or settings.MINIO_ENDPOINT
        self.access_key = access_key or settings.MINIO_ROOT_USER
        self.secret_key = secret_key or settings.MINIO_ROOT_PASSWORD
        self.bucket_name = bucket_name or settings.MINIO_STORAGE_BUCKET_NAME
        
        # Initialize MinIO client
        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=secure
        )
        
        # Create bucket if it doesn't exist
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
    
    def build_minio_connection_url(self, object_name: str) -> str:
        """Build a presigned URL for accessing the object."""
        protocol = "https" if self.endpoint.endswith(":443") else "http"
        url = f"{protocol}://{self.endpoint}/{self.bucket_name}/{object_name}"
        return url

    def upload_file(self, file_path: str, object_name: str) -> str:
        """Upload file to MinIO and return object path."""
        self.client.fput_object(self.bucket_name, object_name, file_path)
        return f"{self.bucket_name}/{object_name}"

    def download_file(self, object_name: str, destination_path: str) -> None:
        """Download file from MinIO."""
        self.client.fget_object(self.bucket_name, object_name, destination_path)

    def delete_file(self, object_name: str) -> None:
        """Delete file from MinIO."""
        self.client.remove_object(self.bucket_name, object_name)