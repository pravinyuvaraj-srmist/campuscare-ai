from dataclasses import dataclass
from pathlib import Path

from .chunker import Chunk, chunk_documents
from .config import DATA_FILE, EMBEDDING_MODEL, RAG_MIN_SCORE, TOP_K
from .document_loader import load_documents
from .llm_client import LLMClient
from .prompt_builder import build_prompt
from .retriever import RetrievalResult, VectorRetriever


@dataclass(frozen=True)
class RAGResponse:
    answer: str
    sources: list[dict]
    retrievals: list[RetrievalResult]


class RAGPipeline:
    def __init__(
        self,
        retriever: VectorRetriever,
        llm_client: LLMClient | None = None,
        top_k: int = TOP_K,
        min_score: float = RAG_MIN_SCORE,
    ):
        if not 0 <= min_score <= 1:
            raise ValueError("min_score must be between 0 and 1.")

        self.retriever = retriever
        self.llm_client = llm_client or LLMClient()
        self.top_k = top_k
        self.min_score = min_score

    @classmethod
    def from_knowledge_base(
        cls,
        data_file: str | Path = DATA_FILE,
        model_name: str = EMBEDDING_MODEL,
        top_k: int = TOP_K,
        min_score: float = RAG_MIN_SCORE,
    ):
        documents = load_documents(data_file)
        chunks = chunk_documents(documents)
        retriever = VectorRetriever.build(chunks, model_name)
        return cls(retriever=retriever, top_k=top_k, min_score=min_score)

    def answer(self, question: str) -> RAGResponse:
        clean_question = question.strip()
        if not clean_question:
            return RAGResponse(
                answer="Please enter a question.",
                sources=[],
                retrievals=[],
            )

        retrievals = [
            result
            for result in self.retriever.search(clean_question, self.top_k)
            if result.score >= self.min_score
        ]

        if not retrievals:
            return RAGResponse(
                answer=(
                    "I could not find a reliable answer in the current "
                    "knowledge base. Please contact the relevant official "
                    "campus office."
                ),
                sources=[],
                retrievals=[],
            )

        system_prompt, user_prompt = build_prompt(clean_question, retrievals)

        try:
            answer = self.llm_client.generate(system_prompt, user_prompt)
        except RuntimeError:
            best = retrievals[0].chunk
            answer = (
                f"{best.text}\n\n"
                f"Sources: {best.title} — {best.source}"
            )

        sources = [
            {
                "title": result.chunk.title,
                "source": result.chunk.source,
                "score": round(result.score, 4),
            }
            for result in retrievals
        ]

        return RAGResponse(
            answer=answer,
            sources=sources,
            retrievals=retrievals,
        )


def build_pipeline() -> RAGPipeline:
    return RAGPipeline.from_knowledge_base()
