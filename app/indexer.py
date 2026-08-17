import uuid

from app.chunking import chunk_text
from app.scanner import FileInfo
from app.embeddings import EmbeddingService
from app.indexed_chunk import IndexedChunk
from app.parsers import parse_file
from qdrant_client.models import PointStruct

from app.vector_store import VectorStore


def index_file(
        file: FileInfo,
        embedding_service: EmbeddingService,
) -> list[IndexedChunk]:

    text = parse_file(file.path)

    chunks = chunk_text(text)

    if not chunks:
        return []

    embeddings = embedding_service.embed_documents(chunks)

    indexed_chunks: list[IndexedChunk] = []

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        indexed_chunks.append(
            IndexedChunk(
                file_path=file.path,
                file_name=file.name,
                chunk_index=index,
                text=chunk,
                embedding=embedding,
                modified_at=file.modified_at,
                size=file.size,
            )
        )

    return indexed_chunks

def create_points(
        indexed_chunks: list[IndexedChunk]
) -> list[PointStruct]:
    points: list[PointStruct] = []

    for chunk in indexed_chunks:
        point = PointStruct(
            id=str(uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{chunk.file_path}:{chunk.chunk_index}",
            )),
            vector=chunk.embedding,
            payload={
                "file_path": str(chunk.file_path),
                "file_name": chunk.file_name,
                "chunk_index": chunk.chunk_index,
                "text": chunk.text,
                "modified_at": chunk.modified_at,
                "size": chunk.size,
            },
        )

        points.append(point)

    return points

def reindex_file(
        file: FileInfo,
        embedding_service: EmbeddingService,
        vector_store: VectorStore
) -> None:
    vector_store.delete_by_file_path(
        str(file.path)
    )

    indexed_chunks = index_file(
        file,
        embedding_service,
    )

    if not indexed_chunks:
        return

    points = create_points(indexed_chunks)

    vector_store.add_points(points)



def file_needs_reindex(
        file: FileInfo,
        vector_store: VectorStore,
) -> bool:
    metadata = vector_store.get_file_metadata(
        str(file.path)
    )

    if metadata is None:
        return True

    if metadata["modified_at"] != file.modified_at:
        return True

    if metadata["size"] != file.size:
        return True

    return False




