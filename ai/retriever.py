from dataclasses import dataclass

import numpy as np

from .chunker import Chunk
from .embeddings import embed_query


@dataclass(frozen=True)
class RetrievalResult:
    chunk: Chunk
    score: float


class VectorRetriever:
    def __init__(
        self,
        chunks: list[Chunk],
        embeddings: np.ndarray,
        model_name: str,
    ):
        if len(chunks) != len(embeddings):
            raise ValueError("Each chunk must have exactly one embedding.")

        self.chunks = chunks
        self.embeddings = embeddings
        self.model_name = model_name

    @classmethod
    def build(cls, chunks: list[Chunk], model_name: str):
        from .embeddings import embed_texts

        texts = [f"{chunk.title}
{chunk.text}" for chunk in chunks]
        embeddings = embed_texts(texts, model_name)
        return cls(chunks, embeddings, model_name)

    def search(self, query: str, top_k: int = 3) -> list[RetrievalResult]:
        if not query.strip() or not self.chunks:
            return []

        if top_k <= 0:
            return []

        query_vector = embed_query(query, self.model_name)
        scores = self.embeddings @ query_vector
        indices = np.argsort(scores)[::-1][:top_k]

        return [
            RetrievalResult(
                chunk=self.chunks[int(index)],
                score=float(scores[int(index)]),
            )
            for index in indices
        ]
