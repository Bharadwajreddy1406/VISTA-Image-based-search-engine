from datetime import datetime

from fastapi import UploadFile

from app.providers.embedding_provider import EmbeddingService,EmbeddingFactory
from app.providers.object_storages import ObjectStoreFactory , BaseObjectStorageProvider
from app.providers.vector_stores import VectorStoreFactory, BaseVectorStore
from app.models.image_registry import ImageRegistry
from app.core.enums import UserConsentTypes, ImageIngestionStates
from app.core.databases import SessionLocal
import uuid 
class ImageHandlerService:

    def __init__(self, object_store: BaseObjectStorageProvider = None, 
                 vector_store: BaseVectorStore = None,
                 embedding_service: EmbeddingService = None
                ):
        
        self.object_store = object_store or ObjectStoreFactory.get_provider()
        self.vector_store = vector_store or VectorStoreFactory.get_provider()
        self.embedding_service = embedding_service or EmbeddingFactory.get_provider()

    async def search(self, file: UploadFile, user_consent: bool = False):

        if not self.object_store.bucket_exists():
            raise ValueError("Storage service is down. Please try again later.")

        image_bytes = await file.read()
        file_name = f"{datetime.utcnow().strftime('%Y-%m-%d')}/{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        
        if user_consent:
            object_path = self.object_store.upload_file(
                file_data=image_bytes,
                object_name=file_name,
                content_type=file.content_type,
            )
            image_data = ImageRegistry(
                id=uuid.uuid4(),
                object_path=object_path,
                content_type=file.content_type or "application/octet-stream",
                status=ImageIngestionStates.PENDING.value,
                consent_type=UserConsentTypes.YES.value,
                created_at=datetime.utcnow(),
            )

            with SessionLocal() as db:
                try:
                    db.add(image_data)
                    db.commit()
                    db.refresh(image_data)
                except Exception:
                    db.rollback()
                    raise

        image_embedding = await self.embedding_service.get_embedding(image_bytes)
        search_results = await self.vector_store.search(image_embedding)

        image_urls = self.get_image_urls(search_results)

        return {"results": image_urls}