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

# region Retreival

    async def search(self, file: UploadFile, user_consent: bool = False):

        if not self.object_store.bucket_exists():
            raise ValueError("Storage service is down. Please try again later.")

        image_bytes = await file.read()
        file_name = f"{datetime.utcnow().strftime('%Y-%m-%d')}/{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        
        if user_consent:
            self.handle_user_consent(image_bytes, file_name, file)


        image_embedding = await self.embedding_service.get_embedding(image_bytes)
        search_results = await self.vector_store.search(image_embedding)

        image_urls = await get_image_urls(search_results)

        return {"results": image_urls}

    def handle_user_consent(self, image_bytes: bytes, file_name: str, file: UploadFile):
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

# region Ingestion

    @staticmethod
    def ingest_images():
        # we get the images with pending status, embedding, and insert those embeddings into vector store
        with SessionLocal() as db:
            pending_images = db.query(ImageRegistry).filter(ImageRegistry.status == ImageIngestionStates.PENDING.value).all()
            for image in pending_images:
                try:
                    # download image from object storage
                    temp_path = f"/tmp/{image.id}"
                    ObjectStoreFactory.get_provider().download_file(image.object_path, temp_path)

                    # TODO Hashing and Perceptual Hashing and metadata_storing implementation here
                    ImageHandlerService.extract_and_store_metadata(temp_path, image.id)
                    # get embedding
                    with open(temp_path, "rb") as f:
                        image_bytes = f.read()
                    embedding = EmbeddingFactory.get_provider().get_embedding(image_bytes)

                    # insert into vector store
                    VectorStoreFactory.get_provider().insert(image_id=image.id, embedding=embedding)

                    # update status to ingested
                    image.status = ImageIngestionStates.INGESTED.value
                    db.commit()
                except Exception as e:
                    print(f"Error ingesting image {image.id}: {e}")
                    db.rollback()

    @staticmethod
    def extract_and_store_metadata(image_path: str, image_id: uuid.UUID):
        # Placeholder for metadata extraction logic (e.g., hashing, perceptual hashing)
        # For now, we just print the action
        print(f"Extracting metadata for image {image_id} at {image_path}")


# region helpers

async def get_image_urls(search_results: list[str]) -> list[str]:
    if len(search_results) == 0:
        return []
    image_ids = [result.id for result in search_results]

    with SessionLocal() as db:
        images = db.query(ImageRegistry).filter(ImageRegistry.id.in_(image_ids)).all()

    return [image.object_path for image in images]