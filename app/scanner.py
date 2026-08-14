from pathlib import Path
from dataclasses import dataclass

@dataclass
class FileInfo:
    path: Path
    name: str
    extension: str
    size: int
    modified_at: float

def scan_directory(directory: Path) -> list[FileInfo]:
    files: list[FileInfo] = []

    for path in directory.rglob("*"):
        if path.is_file():
            stat = path.stat()

            files.append(
                FileInfo(
                    path=path,
                    name=path.name,
                    extension=path.suffix.lower(),
                    size=stat.st_size,
                    modified_at=stat.st_mtime,
                )
            )

    return files