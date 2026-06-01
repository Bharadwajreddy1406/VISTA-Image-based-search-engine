from fastapi import File

from backend.app.providers.embedding_provider import EmbeddingService,EmbeddingFactory
from backend.app.providers.object_storages import ObjectStoreFactory , BaseObjectStorageProvider
from backend.app.providers.vector_stores import VectorStoreFactory, BaseVectorStore

class ImageHandlerService:

    def __init__(self, object_store: BaseObjectStorageProvider = None, 
                 vector_store: BaseVectorStore = None,
                 embedding_service: EmbeddingService = None
                ):
        
        self.object_store = object_store or ObjectStoreFactory.get_provider()
        self.vector_store = vector_store or VectorStoreFactory.get_provider()
        self.embedding_service = embedding_service or EmbeddingFactory.get_provider()

    def search(self,file: File, user_consent: bool = False):

        pass