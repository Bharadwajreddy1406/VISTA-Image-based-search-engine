from datetime import datetime

from fastapi import UploadFile

from app.providers.embedding_provider import EmbeddingService, EmbeddingFactory
from app.providers.object_storages import ObjectStoreFactory, BaseObjectStorageProvider
from app.providers.vector_stores import VectorStoreFactory, BaseVectorStore
from app.models.image_registry import ImageRegistry, ImageMetadata
from app.core.enums import UserConsentTypes, ImageIngestionStates
import os
import uuid
import hashlib

from PIL import Image
import imagehash

from app.core.databases import SessionLocal
from app.core.settings import settings

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
            if not settings.CRONS:
                await ImageHandlerService.ingest_images()


        image_embedding = await self.embedding_service.get_embedding(image_bytes)
        search_results = await self.vector_store.search(image_embedding)

        image_urls = await get_image_urls(search_results)

        return {"results": image_urls}

    def handle_user_consent(self, image_bytes: bytes, file_name: str, file: UploadFile):

        """
        when user consent is given, we upload the image to object storage and store 
        the metadata in the database with pending status for ingestion. 
        
        """
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
    async def ingest_images():
        # we get the images with pending status, embedding, and insert those embeddings into vector store
        with SessionLocal() as db:
            pending_images = db.query(ImageRegistry).filter(ImageRegistry.status == ImageIngestionStates.PENDING.value).all()

            object_store = ObjectStoreFactory.get_provider()
            embedding_service = EmbeddingFactory.get_provider()
            vector_store = VectorStoreFactory.get_provider()

            for image in pending_images:
                try:
                    # download image from object storage
                    temp_path = f"/tmp/{image.id}"
                    object_store.download_file(image.object_path, temp_path)

                    await ImageHandlerService.extract_and_store_metadata(temp_path, image.id)

                    with open(temp_path, "rb") as f:
                        image_bytes = f.read()

                    embedding = await embedding_service.get_embedding(image_bytes)

                    # insert into vector store
                    vector_store.insert(image_id=image.id, embedding=embedding)

                    # update status to ingested
                    image.status = ImageIngestionStates.PROCESSED.value
                    db.commit()
                except Exception as e:
                    print(f"Error ingesting image {image.id}: {e}")
                    db.rollback()

    @staticmethod
    async def extract_and_store_metadata(
        image_path: str,
        image_id: uuid.UUID
    ):
        """
        Extract metadata required for:
        - exact duplicate detection (SHA256)
        - near duplicate detection (pHash)
        - image dimensions
        - storage statistics
        """

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        sha256_hash = hashlib.sha256(image_bytes).hexdigest()

        image = Image.open(image_path)

        metadata = ImageMetadata(
            image_registry_id=image_id,

            file_name=os.path.basename(image_path),

            mime_type=Image.MIME.get(
                image.format,
                "application/octet-stream"
            ),

            file_size_bytes=os.path.getsize(image_path),

            sha256_hash=sha256_hash,

            perceptual_hash=str(
                imagehash.phash(image)
            ),

            image_width=image.width,

            image_height=image.height,
        )

        with SessionLocal() as db:
            try:
                existing = (
                    db.query(ImageMetadata)
                    .filter(
                        ImageMetadata.image_registry_id == image_id
                    )
                    .first()
                )

                if existing:
                    return

                db.add(metadata)
                db.commit()

            except Exception:
                db.rollback()
                raise

# region helpers

async def get_image_urls(search_results: list[str]) -> list[str]:
    if len(search_results) == 0:
        return []

    image_ids = [str(result) for result in search_results]
    object_store = ObjectStoreFactory.get_provider()

    with SessionLocal() as db:
        images = db.query(ImageRegistry).filter(ImageRegistry.id.in_(image_ids)).all()

    return [object_store.generate_obj_url(image.object_path) for image in images]