import os

from pydantic import model_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):

    # region Database
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT: int = int(os.environ.get("POSTGRES_PORT"))
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")

    # region MinIO
    MINIO_ENDPOINT: str = os.environ.get("MINIO_ENDPOINT")
    MINIO_ROOT_USER: str = os.environ.get("MINIO_ROOT_USER")
    MINIO_ROOT_PASSWORD: str = os.environ.get("MINIO_ROOT_PASSWORD")
    MINIO_STORAGE_BUCKET_NAME: str = os.environ.get("MINIO_STORAGE_BUCKET_NAME")

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
    
    @model_validator(mode='after')
    def validate_database(self):
        from .validations import validate_database_settings
        
        database_dict = {
            "POSTGRES_HOST": self.POSTGRES_HOST,
            "POSTGRES_PORT": self.POSTGRES_PORT,
            "POSTGRES_DB": self.POSTGRES_DB,
            "POSTGRES_USER": self.POSTGRES_USER,
            "POSTGRES_PASSWORD": self.POSTGRES_PASSWORD,
        }
        validate_database_settings(database_dict)
        return self
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()