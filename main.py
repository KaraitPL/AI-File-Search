from pathlib import Path

from app.scanner import scan_directory
from app.parsers import parse_file
from app.chunking import chunk_text
from app.embeddings import EmbeddingService

embedding_service = EmbeddingService()

text = [
    "Kubernetes służy do orkiestracji kontenerów",
    "Jak zarządzać klastrem k8s",
    "Przepis na ciasto czekoladowe",
]

for text in text:
    vector = embedding_service.embed(text)

    print(text)
    print(vector[:5])
    print()


# directory = Path.home() / "Documents"
#
# files = scan_directory(directory)
#
# for file in files:
#     print("=" * 80)
#     print("File: " + file.name)
#
#     text = parse_file(file.path)
#     chunks = chunk_text(text)
#
#     print(f"Characters: {len(text)}")
#     print(f"Chunks: {len(chunks)}")
#
#     for index, chunk in enumerate(chunks[:3], start=1):
#         print()
#         print(f"--- Chunk: {index} ---")
#         print(chunk[:300])


