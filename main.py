from pathlib import Path

from app.scanner import scan_directory

directory = Path.home() / "Documents"

items = scan_directory(directory)

for item in items:
    print(item)