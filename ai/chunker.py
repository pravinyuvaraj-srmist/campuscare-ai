from dataclasses import dataclass
import re

from .document_loader import Document


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str
    title: str
    source: str
    metadata: dict


def _words(text: str) -> list[str]:
    return re.findall(r"S+", text)


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 120,
    overlap: int = 25,
) -> list[Chunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size.")

    chunks: list[Chunk] = []

    for document_index, document in enumerate(documents):
        words = _words(document.content)
        if not words:
            continue

        start = 0
        chunk_number = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            text = " ".join(words[start:end]).strip()

            chunks.append(
                Chunk(
                    chunk_id=f"doc-{document_index}-chunk-{chunk_number}",
                    text=text,
                    title=document.title,
                    source=document.source,
                    metadata=document.metadata,
                )
            )

            if end == len(words):
                break

            start = end - overlap
            chunk_number += 1

    return chunks
