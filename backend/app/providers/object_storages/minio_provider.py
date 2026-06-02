import io

from .base_object_storage_provider import BaseObjectStorageProvider
from minio import Minio
from app.core.settings import settings

class MinIOProvider(BaseObjectStorageProvider):

    def __init__(
        self,
        endpoint: str = settings.MINIO_ENDPOINT,
        access_key: str = settings.MINIO_ACCESS_KEY,
        secret_key: str = settings.MINIO_SECRET_KEY,
        bucket_name: str = settings.MINIO_BUCKET_NAME,
        secure: bool = False,
    ):
        """
        Initialize MinIO provider with settings or custom values.
        
        Args:
            endpoint: MinIO endpoint (default: from settings.MINIO_ENDPOINT)
            access_key: MinIO access key (default: from settings.MINIO_ACCESS_KEY)
            secret_key: MinIO secret key (default: from settings.MINIO_SECRET_KEY)
            bucket_name: Bucket name (default: from settings.MINIO_BUCKET_NAME)
            secure: Use HTTPS (default: False)
        """

        self.endpoint = endpoint or settings.MINIO_ENDPOINT
        self.access_key = access_key or settings.MINIO_ACCESS_KEY
        self.secret_key = secret_key or settings.MINIO_SECRET_KEY
        self.bucket_name = bucket_name or settings.MINIO_BUCKET_NAME
        
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
        """Build a URL for accessing the object."""
        object_name = self._strip_bucket_prefix(object_name)
        protocol = "https" if self.endpoint.endswith(":443") else "http"
        url = f"{protocol}://{self.endpoint}/{self.bucket_name}/{object_name}"
        return url

    def _strip_bucket_prefix(self, object_path: str) -> str:
        """Normalize an object path to the MinIO object name."""
        prefix = f"{self.bucket_name}/"
        if object_path.startswith(prefix):
            return object_path[len(prefix) :]
        return object_path

    def upload_file(
        self,
        file_data: bytes,
        object_name: str,
        content_type: str | None = None,
    ) -> str:
        """Upload raw bytes to MinIO and return the object path."""

        self.client.put_object(
            self.bucket_name,
            object_name,
            io.BytesIO(file_data),
            length=len(file_data),
            content_type=content_type,
        )
        return object_name

    def download_file(self, object_name: str, destination_path: str) -> None:
        """Download file from MinIO."""
        object_name = self._strip_bucket_prefix(object_name)
        self.client.fget_object(self.bucket_name, object_name, destination_path)

    def object_exists(self, object_name: str) -> bool:
        """Check if object exists in MinIO."""
        object_name = self._strip_bucket_prefix(object_name)
        try:
            self.client.stat_object(self.bucket_name, object_name)
            return True
        except Exception:
            return False

    def generate_obj_url(self, object_path: str) -> str:
        """Generate a presigned URL using the normalized object key."""
        object_name = self._strip_bucket_prefix(object_path)
        return self.client.get_presigned_url(
            "GET",
            self.bucket_name,
            object_name,
        )

    def delete_file(self, object_name: str) -> None:
        """Delete file from MinIO."""
        object_name = self._strip_bucket_prefix(object_name)
        self.client.remove_object(self.bucket_name, object_name)
    
    def bucket_exists(self) -> bool:
        """Check if the bucket exists in MinIO."""
        return self.client.bucket_exists(self.bucket_name)
    

    
    @staticmethod
    def create_bucket_if_not_exists() -> bool:
        """Create bucket if it doesn't exist. only used in initialization, before yeild in lifespan.
        usage is seen in backend/app/main.py
        """
        client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )
        if not client.bucket_exists(settings.MINIO_BUCKET_NAME):
            client.make_bucket(settings.MINIO_BUCKET_NAME)
            return True
        return False