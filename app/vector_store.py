from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

class VectorStore:
    COLLECTION_NAME = "file_chunks"

    def __init__(
            self,
            path: str,
            vector_size: int,
    ):
        self.client = QdrantClient(path=path)

        if not self.client.collection_exists(
            self.COLLECTION_NAME
        ):
            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def add_points(
            self,
            points: list[PointStruct],
    ) -> None:
        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points,
        )

    def close(self) -> None:
        self.client.close()

