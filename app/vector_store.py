from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from pathlib import Path
import shutil

class VectorStore:
    COLLECTION_NAME = "file_chunks"

    def __init__(
            self,
            path: str,
    ):
        self.path = Path(path)
        self.client = QdrantClient(
            path=str(self.path)
        )


    def ensure_collection(
        self,
        vector_size: int,
    ) -> None:
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

    def reset(self) -> None:
        self.close()

        if self.path.exists():
            shutil.rmtree(self.path)

    def search(
        self,
        vector: list[float],
        limit: int = 5,
    ):
        result = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=vector,
            limit=limit,
        )

        return result.points

    def delete_by_file_path(
            self,
            file_path: str,
    ) -> None:
        self.client.delete(
            collection_name=self.COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="file_path",
                        match=MatchValue(
                            value=file_path,
                        ),
                    )
                ]
            ),
        )

    def get_file_metadata(
            self,
            file_path: str,
    ):
        points, _ = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="file_path",
                        match=MatchValue(
                            value=file_path,
                        ),
                    )
                ]
            ),
            limit=1,
            with_payload=True,
            with_vectors=False,
        )

        if not points:
            return None

        return points[0].payload

