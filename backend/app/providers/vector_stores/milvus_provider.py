from pymilvus import (
    MilvusClient,
    DataType
)

from app.core.settings import settings
from .base_vector_store import BaseVectorStoreProvider


class MilvusVectorStoreProvider(
    BaseVectorStoreProvider
):

    EMBEDDING_DIMENSION = 512

    def __init__(self):

        self.host = settings.MILVUS_HOST
        self.port = settings.MILVUS_PORT
        self.collection_name = (
            settings.MILVUS_COLLECTION_NAME
        )
        self.top_k = settings.TOP_K_SEARCH_RESULTS

        self.connect_to_milvus()

        self.create_collection_if_not_exists()

    def connect_to_milvus(self):

        self.milvus_url = (
            f"http://{self.host}:{self.port}"
        )

        root_token = "root:Milvus"

        self.client = MilvusClient(
            uri=self.milvus_url,
            token=root_token
        )

    def create_collection_if_not_exists(self):

        if self.client.has_collection(
            collection_name=self.collection_name
        ):
            return

        schema = MilvusClient.create_schema(
            auto_id=False,
            enable_dynamic_field=False
        )

        schema.add_field(
            field_name="id",
            datatype=DataType.VARCHAR,
            max_length=36,
            is_primary=True
        )

        schema.add_field(
            field_name="embedding",
            datatype=DataType.FLOAT_VECTOR,
            dim=self.EMBEDDING_DIMENSION
        )

        index_params = (
            self.client.prepare_index_params()
        )

        index_params.add_index(
            field_name="id",
            index_type="AUTOINDEX"
        )

        index_params.add_index(
            field_name="embedding",
            index_type="AUTOINDEX",
            metric_type="COSINE"
        )

        self.client.create_collection(
            collection_name=self.collection_name,
            schema=schema,
            index_params=index_params
        )

    def insert(
        self,
        image_id: str,
        embedding: list[float]
    ):

        self.client.insert(
            collection_name=self.collection_name,
            data=[
                {
                    "id": image_id,
                    "embedding": embedding
                }
            ]
        )

    async def search(
        self,
        embedding: list[float],
        top_k: int = settings.TOP_K_SEARCH_RESULTS if settings.TOP_K_SEARCH_RESULTS else 10
    ) -> list[str]:

        results = self.client.search(
            collection_name=self.collection_name,
            data=[embedding],
            limit=top_k,
            output_fields=["id"]
        )

        image_ids = []

        for hit in results[0]:

            image_ids.append(
                hit["entity"]["id"]
            )

        return image_ids

    def delete_vectors(
        self,
        ids: list[str]
    ):

        expr = (
            f'id in '
            f'{ids}'
        )

        self.client.delete(
            collection_name=self.collection_name,
            filter=expr
        )

    def close_connection(self):

        self.client.close()