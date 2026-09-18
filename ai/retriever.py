from dataclasses import dataclass

from .chunker import Chunk
from .embeddings import embed_query, embed_texts


@dataclass(frozen=True)
class RetrievalResult:
    chunk: Chunk
    score: float


class VectorRetriever:
    def __init__(
        self,
        chunks: list[Chunk],
        embeddings: list[tuple[float, ...]],
        model_name: str,
    ):
        if len(chunks) != len(embeddings):
            raise ValueError("Each chunk must have exactly one embedding.")

        self.chunks = chunks
        self.embeddings = embeddings
        self.model_name = model_name

    @classmethod
    def build(cls, chunks: list[Chunk], model_name: str):
        texts = [chunk.title + " " + chunk.text for chunk in chunks]
        embeddings = embed_texts(texts, model_name)
        return cls(chunks, embeddings, model_name)

    def search(self, query: str, top_k: int = 3) -> list[RetrievalResult]:
        if not query.strip() or not self.chunks or top_k <= 0:
            return []

        query_vector = embed_query(query, self.model_name)
        scored: list[tuple[float, Chunk]] = []

        for chunk, vector in zip(self.chunks, self.embeddings):
            score = sum(a * b for a, b in zip(vector, query_vector))
            scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)

        return [
            RetrievalResult(
                chunk=chunk,
                score=round(float(score), 4),
            )
            for score, chunk in scored[:top_k]
            if score > 0.0
        ]
