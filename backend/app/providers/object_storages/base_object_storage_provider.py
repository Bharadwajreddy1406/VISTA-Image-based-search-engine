from abc import ABC, abstractmethod

class BaseObjectStorageProvider(ABC):
    
    @abstractmethod
    def upload_file(self, file_data: bytes, object_name: str, content_type: str | None = None) -> str:
        """Uploads raw file bytes to object storage and returns the object path."""
        pass

    @abstractmethod
    def download_file(self, object_name: str, destination_path: str) -> None:
        """Downloads a file from the object storage to the specified destination."""
        pass

    @abstractmethod
    def delete_file(self, object_name: str) -> None:
        """Deletes a file from the object storage."""
        # TODO: this implements HARD DELETE, so not now
        pass 

    @abstractmethod
    def generate_obj_url(self, object_name: str) -> str:
        """Generates a URL for accessing the file in the object storage."""
        pass

    @abstractmethod
    def object_exists(self, object_name: str) -> bool:
        """Checks if a file exists in the object storage."""
        try:
            self.download_file(object_name, "/tmp/temp_file")
            return True
        except Exception:
            return False

    @abstractmethod
    def bucket_exists(self) -> bool:
        """Checks if the bucket exists in the object storage."""
        pass

    @abstractmethod
    def create_bucket_if_not_exists(self) -> bool:
        """Creates the bucket if it does not exist."""
        pass
