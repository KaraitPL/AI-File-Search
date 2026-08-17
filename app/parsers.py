from pathlib import Path
import pymupdf

def parse_text_file(path: Path) -> str:
    return path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

def parse_pdf(path: Path) -> str:
    document = pymupdf.open(path)

    pages: list[str] = []

    for page in document:
        text = page.get_text("text")
        pages.append(text)

    return "\n".join(pages)

def parse_file(path: Path):
    extension = path.suffix.lower()

    if extension in {".txt", ".md"}:
        return parse_text_file(path)

    if extension in {".pdf"}:
        return parse_pdf(path)

    raise ValueError(f"Unsupported file type: {extension}")