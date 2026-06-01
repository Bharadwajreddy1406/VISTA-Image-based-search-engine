from abc import ABC, abstractmethod

class BaseObjectStorageProvider(ABC):
    
    @abstractmethod
    def upload_file(self, file_path: str | None, object_name: str, file_data: bytes | None) -> str:
        """Uploads a file to the object storage and returns the URL."""
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
    def generate_access_url(self, object_name: str) -> str:
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