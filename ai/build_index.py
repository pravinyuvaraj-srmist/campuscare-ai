"""Build a local JSON vector index for CampusCare AI."""

import json

from .chunker import chunk_documents
from .config import DATA_FILE, EMBEDDING_MODEL, INDEX_DIR
from .document_loader import load_documents
from .embeddings import embed_texts


def main() -> None:
    documents = load_documents(DATA_FILE)
    chunks = chunk_documents(documents)

    texts = [chunk.title + " " + chunk.text for chunk in chunks]
    embeddings = embed_texts(texts, EMBEDDING_MODEL)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    with (INDEX_DIR / "embeddings.json").open("w", encoding="utf-8") as file:
        json.dump(embeddings, file)

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
    print(f"Saved vectors to: {INDEX_DIR / 'embeddings.json'}")
    print(f"Saved chunk metadata to: {INDEX_DIR / 'chunks.json'}")


if __name__ == "__main__":
    main()
