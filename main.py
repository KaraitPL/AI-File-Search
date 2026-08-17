from pathlib import Path
from app.indexer import file_needs_reindex, reindex_file
import argparse
from app.scanner import scan_directory
from app.embeddings import EmbeddingService
from app.vector_store import VectorStore

DB_PATH = "./data/qdrant"

def run_index(directory: Path) -> None:
    embedding_service = EmbeddingService()

    vector_store = VectorStore(
        path=DB_PATH,
        vector_size=embedding_service.dimension,
    )

    try:
        files = scan_directory(directory)

        if not files:
            return

        for file in files:
            if not file_needs_reindex(
                file,
                vector_store
            ):
                print(f"Skipping: {file.name}")
                continue

            print(f"Reindexing: {file.name}")
            reindex_file(
                file,
                embedding_service,
                vector_store
            )

    finally:
        vector_store.close()


def run_search(query: str) -> None:
    embedding_service = EmbeddingService()

    vector_store = VectorStore(
        path=DB_PATH,
        vector_size=embedding_service.dimension,
    )

    try:
        query_embedding = embedding_service.embed_query(query)

        results = vector_store.search(
            query_embedding,
            5,
        )

        for result in results:
            print("=" * 80)
            print(f"Score: {result.score}")
            print(f"File name: {result.payload['file_name']}")
            print(f"Text: {result.payload['text'][:200]}")
            print(f"Path: {result.payload['file_path']}")

    finally:
        vector_store.close()

def run_reset() -> None:
    embedding_service = EmbeddingService()
    vector_store = VectorStore(
        path=DB_PATH,
        vector_size=embedding_service.dimension,
    )
    try:
        vector_store.reset()
    finally:
        vector_store.close()




def main() -> None:
    parser = argparse.ArgumentParser(
        description="Semantic file search"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    index_parser = subparsers.add_parser(
        "index",
        help="Index files from a directory",
    )

    index_parser.add_argument(
        "directory",
        type=Path,
        help="Directory to index",
    )

    search_parser = subparsers.add_parser(
        "search",
        help="Search indexed files",
    )

    search_parser.add_argument(
        "query",
        type=str,
        help="Natural language search query",
    )

    reset_parser = subparsers.add_parser(
        "reset",
        help="Reset indexed files",
    )

    args = parser.parse_args()

    if args.command == "index":
        run_index(args.directory)

    if args.command == "search":
        run_search(args.query)

    if args.command == "reset":
        run_reset()




if __name__ == "__main__":
    main()





