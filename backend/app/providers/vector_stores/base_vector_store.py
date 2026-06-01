from abc import ABC, abstractmethod

class BaseVectorStoreProvider(ABC):

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        top_k: int = None
    ):
        pass

    @abstractmethod
    def insert(
        self,
        image_id: str,
        embedding: list[float]
    ):
        pass