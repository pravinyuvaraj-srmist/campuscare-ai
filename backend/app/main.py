import json
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .retriever import build_answer, retrieve

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "knowledge_base.json"

app = FastAPI(
    title="CampusCare AI API",
    description="Backend API for the CampusCare student assistance platform.",
    version="0.2.0",
)

# Frontend origins can be supplied as a comma-separated CORS_ORIGINS value.
# Example: CORS_ORIGINS=http://localhost:5173,https://your-frontend.example
raw_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
)
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=1000,
        description="Student's campus-related question.",
    )


class Source(BaseModel):
    title: str
    source: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


def load_knowledge() -> list[dict]:
    """Load the current knowledge base from the repository."""
    with DATA_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Knowledge base must contain a JSON list.")

    return data


@app.get("/")
def root() -> dict:
    return {
        "name": "CampusCare AI API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Return the most relevant campus guidance and its source."""
    question = request.question.strip()

    if not question:
        return ChatResponse(
            answer="Please enter a question.",
            sources=[],
        )

    # Keep retrieval separate so the AI/RAG member can replace this layer later.
    matches = retrieve(question, load_knowledge(), limit=3)
    answer = build_answer(question, matches)

    sources = [
        Source(title=item["title"], source=item["source"])
        for item in matches
    ]

    return ChatResponse(answer=answer, sources=sources)
