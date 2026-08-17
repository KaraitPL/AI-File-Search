import uuid

from app.chunking import chunk_text
from app.scanner import FileInfo
from app.embeddings import EmbeddingService
from app.indexed_chunk import IndexedChunk
from app.parsers import parse_file
from qdrant_client.models import PointStruct


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
            )
        )

    return indexed_chunks

def create_points(
        indexed_chunks: list[IndexedChunk]
) -> list[PointStruct]:
    points: list[PointStruct] = []

    for chunk in indexed_chunks:
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=chunk.embedding,
            payload={
                "file_path": str(chunk.file_path),
                "file_name": chunk.file_name,
                "chunk_index": chunk.chunk_index,
                "text": chunk.text,
            },
        )

        points.append(point)

    return points



