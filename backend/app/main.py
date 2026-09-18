from pathlib import Path
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "knowledge_base.json"

app = FastAPI(title="CampusCare AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]


def load_knowledge() -> list[dict]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def retrieve(question: str, limit: int = 3) -> list[dict]:
    query_terms = {
        term.lower()
        for term in question.replace("?", " ").replace(",", " ").split()
        if len(term) >= 3
    }

    scored = []
    for item in load_knowledge():
        haystack = f"{item['title']} {item['content']}".lower()
        score = sum(1 for term in query_terms if term in haystack)
        if score:
            scored.append((score, item))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored[:limit]]


def build_answer(question: str, matches: list[dict]) -> str:
    if not matches:
        return (
            "I could not find a reliable answer in the current knowledge base. "
            "Please contact the relevant campus office or add an approved source."
        )

    top = matches[0]
    return (
        f"Based on the current CampusCare knowledge base, the most relevant "
        f"guidance for '{question}' is: {top['content']}"
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    question = request.question.strip()
    if not question:
        return ChatResponse(answer="Please enter a question.", sources=[])

    matches = retrieve(question)
    answer = build_answer(question, matches)
    sources = [
        {
            "title": item["title"],
            "source": item["source"],
        }
        for item in matches
    ]
    return ChatResponse(answer=answer, sources=sources)
