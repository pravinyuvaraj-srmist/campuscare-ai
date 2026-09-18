from ai.chunker import Chunk
from ai.rag import RAGPipeline
from ai.retriever import RetrievalResult


class FakeRetriever:
    def __init__(self, score):
        self.score = score

    def search(self, question, top_k):
        return [
            RetrievalResult(
                chunk=Chunk("1", "Campus guidance", "Campus Help", "sample", {}),
                score=self.score,
            )
        ]


def test_rag_refuses_low_confidence_matches():
    pipeline = RAGPipeline(FakeRetriever(score=0.12), min_score=0.35)

    response = pipeline.answer("What is the weather on Mars?")

    assert response.retrievals == []
    assert response.sources == []
    assert "could not find a reliable answer" in response.answer