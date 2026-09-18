from functools import lru_cache

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ai.rag import RAGPipeline, build_pipeline

app = FastAPI(title="CampusCare AI API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class Source(BaseModel):
    title: str
    source: str
    score: float | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


@lru_cache(maxsize=1)
def get_rag_pipeline() -> RAGPipeline:
    """Create the embedding/RAG pipeline once and reuse it for requests."""
    return build_pipeline()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    question = request.question.strip()

    if not question:
        return ChatResponse(answer="Please enter a question.", sources=[])

    try:
        result = get_rag_pipeline().answer(question)
    except Exception as exc:
        raise RuntimeError(
            "CampusCare AI could not initialize or run the RAG pipeline. "
            "Check the AI dependencies, model download, and environment variables."
        ) from exc

    return ChatResponse(
        answer=result.answer,
        sources=[
            Source(
                title=source["title"],
                source=source["source"],
                score=source.get("score"),
            )
            for source in result.sources
        ],
    )
