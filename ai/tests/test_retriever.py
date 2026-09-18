import numpy as np

from ai.chunker import Chunk
from ai.retriever import RetrievalResult, VectorRetriever


class TestRetriever(VectorRetriever):
    def search(self, query: str, top_k: int = 3):
        query_vector = np.array([1.0, 0.0], dtype=np.float32)
        scores = self.embeddings @ query_vector
        indices = np.argsort(scores)[::-1][:top_k]
        return [
            RetrievalResult(
                chunk=self.chunks[int(index)],
                score=float(scores[int(index)]),
            )
            for index in indices
        ]


def test_retriever_ranks_similar_chunk_first():
    chunks = [
        Chunk("1", "lost id card", "ID Help", "source-a", {}),
        Chunk("2", "hostel maintenance", "Hostel", "source-b", {}),
    ]
    embeddings = np.array(
        [[1.0, 0.0], [0.0, 1.0]],
        dtype=np.float32,
    )

    retriever = TestRetriever(chunks, embeddings, "fake")
    results = retriever.search("lost student id", top_k=2)

    assert results[0].chunk.title == "ID Help"
    assert results[0].score > results[1].score
