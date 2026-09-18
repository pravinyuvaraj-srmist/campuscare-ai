from ai.chunker import Chunk
from ai.rag import RAGPipeline
from ai.retriever import RetrievalResult


class FakeRetriever:
    def search(self, query: str, top_k: int = 3):
        chunk = Chunk(
            chunk_id="test-1",
            text="Contact the hostel office for maintenance issues.",
            title="Hostel Support",
            source="unit-test",
            metadata={},
        )
        return [RetrievalResult(chunk=chunk, score=0.95)]


class FakeLLM:
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        assert "hostel office" in user_prompt
        return "Please contact the hostel office for maintenance support."


def test_rag_pipeline_uses_llm_and_returns_sources() -> None:
    pipeline = RAGPipeline(
        retriever=FakeRetriever(),
        llm_client=FakeLLM(),
        top_k=1,
    )

    response = pipeline.answer("My hostel room needs repair.")

    assert response.answer.startswith("Please contact")
    assert response.sources[0]["title"] == "Hostel Support"
    assert response.sources[0]["score"] == 0.95
