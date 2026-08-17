from pathlib import Path
from app.indexer import index_file

from app.scanner import scan_directory
from app.search import search
from app.embeddings import EmbeddingService
from app.vector_store import VectorStore
from app.indexer import create_points


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

    print(
        f"Indexed {file.name}: "
        f"{len(points)} chunks"
    )


# print(f"Indexed chunks: {len(indexed_chunks)}")

# query = input("Search: ")
#
# results = search(
#     query=query,
#     indexed_chunks=indexed_chunks,
#     embedding_service=embedding_service,
#     limit=5,
# )
#
# for result in results:
#     print()
#     print(f"Score: {result.score:.3f}")
#     print(f"File: {result.chunk.file_name}")
#     print(f"Path: {result.chunk.file_path}")
#     print(f"Chunk: {result.chunk.chunk_index}")
#     print(f"Text: {result.chunk.text[:300]}")

vector_store.close()



