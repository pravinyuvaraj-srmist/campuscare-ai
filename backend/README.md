# Backend

CampusCare AI uses Python + FastAPI.

## Endpoints

- `GET /health`
- `POST /api/chat`

## AI integration

`POST /api/chat` now calls the shared RAG pipeline in `ai/`.

Flow:

1. FastAPI receives the student's question.
2. The embedding model converts the question into a vector.
3. The vector retriever finds the most relevant knowledge-base chunks.
4. The RAG prompt is sent to the configured LLM when `LLM_API_KEY` and `LLM_MODEL` are available.
5. When no LLM is configured, the pipeline safely falls back to the highest-ranked retrieved guidance.
6. The API returns the answer plus source metadata.

## Run locally

From the repository root:

```bash
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

The first AI request may download the configured Sentence Transformers embedding model.

Optional LLM configuration can be provided through environment variables:

```text
LLM_API_KEY=your_key
LLM_MODEL=your_model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RAG_TOP_K=3
```

The API does not expose the LLM key to the frontend.
