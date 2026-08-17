from pathlib import Path
from app.indexer import index_file

from app.scanner import scan_directory
from app.parsers import parse_file
from app.chunking import chunk_text
from app.embeddings import EmbeddingService
from app.math_functions import cosine_similarity

directory = Path.home() / "AI-File-Search"

files = scan_directory(directory)

embedding_service = EmbeddingService()

for file in files[:3]:
    indexed_chunks = index_file(
        file,
        embedding_service,
    )

    print("=" * 80)
    print(file.name)
    print("Chunks: ", len(indexed_chunks))

    for chunk in indexed_chunks[:2]:
        print()
        print("Chunk index: ", chunk.chunk_index)
        print("Text: ", chunk.text[:200])
        print("Embedding size: ", len(chunk.embedding))



