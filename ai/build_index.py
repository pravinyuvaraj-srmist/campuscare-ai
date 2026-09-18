"""Build a local vector index for CampusCare AI."""

import json

import numpy as np

from .chunker import chunk_documents
from .config import DATA_FILE, EMBEDDING_MODEL, INDEX_DIR
from .document_loader import load_documents
from .embeddings import embed_texts


def main() -> None:
    documents = load_documents(DATA_FILE)
    chunks = chunk_documents(documents)

    texts = [f"{chunk.title}
{chunk.text}" for chunk in chunks]
    embeddings = embed_texts(texts, EMBEDDING_MODEL)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    np.save(INDEX_DIR / "embeddings.npy", embeddings)

    with (INDEX_DIR / "chunks.json").open("w", encoding="utf-8") as file:
        json.dump(
            [
                {
                    "chunk_id": chunk.chunk_id,
                    "text": chunk.text,
                    "title": chunk.title,
                    "source": chunk.source,
                    "metadata": chunk.metadata,
                }
                for chunk in chunks
            ],
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Created {len(chunks)} chunks.")
    print(f"Saved embeddings to: {INDEX_DIR / 'embeddings.npy'}")
    print(f"Saved chunk metadata to: {INDEX_DIR / 'chunks.json'}")


if __name__ == "__main__":
    main()
