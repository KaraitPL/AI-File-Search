from dataclasses import dataclass
from pathlib import Path

@dataclass
class IndexedChunk:
    file_path: Path
    file_name: str
    chunk_index: int
    text: str
    embedding: list[float]
    modified_at: float
    size: int