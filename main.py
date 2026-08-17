from pathlib import Path
from app.indexer import index_file
import shutil

from app.scanner import scan_directory
from app.search import search
from app.embeddings import EmbeddingService
from app.vector_store import VectorStore
from app.indexer import create_points

from qdrant_client import QdrantClient

directory = Path.home() / "Folder_Testowy"



embedding_service = EmbeddingService()

vector_store = VectorStore(
    path="./data/qdrant",
    vector_size=embedding_service.dimension,
)



print("Qdrant ready")

files = scan_directory(directory)

for file in files[:3]:
    indexed_chunks = index_file(
        file,
        embedding_service,
    )

    if not indexed_chunks:
        continue

    points = create_points(indexed_chunks)

    vector_store.add_points(points)



query = input("Search: ")

query_embedding = embedding_service.embed_query(query)

results = vector_store.search(
    vector=query_embedding,
    limit=5,
)




for result in results:
    print()
    print(f"Score: {result.score:.3f}")
    print(f"File: {result.payload['file_name']}")
    print(f"Path: {result.payload['file_path']}")
    print(f"Chunk: {result.payload['chunk_index']}")
    print(f"Text: {result.payload['text'][:300]}")

vector_store.close()
# vector_store.delete_collection(vector_store)



