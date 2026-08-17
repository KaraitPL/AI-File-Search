from app.chunking import chunk_text
from app.scanner import FileInfo
from app.embeddings import EmbeddingService
from app.indexed_chunk import IndexedChunk
from app.parsers import parse_file


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



