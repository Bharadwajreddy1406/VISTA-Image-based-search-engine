from .base_vector_store import BaseVectorStoreProvider
from app.core.settings import settings

class MilvusVectorStoreProvider(BaseVectorStoreProvider):
    def __init__(self,):
        self.host = settings.MILVUS_HOST
        self.port = settings.MILVUS_PORT
        self.collection_name = settings.MILVUS_COLLECTION_NAME
        
        # connect_to_milvus(self.host, self.port)  # TODO: Implement connection logic to Milvus server

    def insert(self, image_id: str, embedding: list[float]):
        # Code to add vectors to Milvus collection
        pass

    def search(self, embedding: list[float], top_k: int) -> list:
        # Code to search for similar vectors in Milvus collection
        pass

    def delete_vectors(self, ids: list):
        # Code to delete vectors from Milvus collection by IDs
        pass
    