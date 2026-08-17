from dataclasses import dataclass
from app.indexed_chunk import IndexedChunk
from app.embeddings import EmbeddingService
from app.math_functions import cosine_similarity


@dataclass
class SearchResult:
    score: float
    chunk: IndexedChunk

def search(
        query: str,
        indexed_chunks: list[IndexedChunk],
        embedding_service: EmbeddingService,
        limit: int
) -> list[SearchResult]:

    query_embedding = embedding_service.embed_query(query)

    results: list[SearchResult] = []

    for chunk in indexed_chunks:
        results.append(
            SearchResult(
                cosine_similarity(query_embedding, chunk.embedding),
                chunk
            )
        )

    results.sort(
        key=lambda result: result.score,
        reverse=True,
    )

    return results[:limit]
