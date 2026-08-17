def chunk_text(
        text: str,
        chunk_size: int = 400,
        overlap: int = 80,
) -> list[str]:
    if overlap >= chunk_size:
        raise ValueError(f"Overlap must be less than chunk_size")

    if not text.strip():
        return []

    chunks: list[str] = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks