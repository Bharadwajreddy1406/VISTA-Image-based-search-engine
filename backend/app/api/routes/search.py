from fastapi import APIRouter, File, UploadFile

from app.providers.object_storages import ObjectStoreFactory
from app.providers.vector_stores import VectorStoreFactory
from app.services.image_handler_service import ImageHandlerService
from app.providers.embedding_provider import EmbeddingFactory

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

@router.post("/search")
async def search(file: UploadFile = File(...), user_consent: bool = False):
    return await image_handler_service.search(file=file, user_consent=user_consent)