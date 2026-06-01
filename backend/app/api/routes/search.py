from fastapi import APIRouter, File, UploadFile

from backend.app.providers.object_storages import ObjectStoreFactory
from backend.app.providers.vector_stores import VectorStoreFactory
from backend.app.services.image_handler_service import ImageHandlerService
from backend.app.providers.embedding_provider import EmbeddingFactory

router = APIRouter()
object_store = ObjectStoreFactory.get_provider()
vector_store = VectorStoreFactory.get_provider()
embedding_service = EmbeddingFactory.get_provider()

image_handler_service = ImageHandlerService(object_store=object_store,
                                            vector_store=vector_store, 
                                            embedding_service=embedding_service
                                            )


@router.get("/search-test")
def search_test():
    return {"message": "Search API is working!"}

@router.get("/search")
def search():
    return {"message": "Search API is working!"}