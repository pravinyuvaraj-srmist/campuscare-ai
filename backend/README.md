# Backend

FastAPI backend for CampusCare AI.

## Endpoints

- `GET /` — basic API status
- `GET /health` — health check
- `POST /api/chat` — answer a campus question using the current knowledge base

## Windows local setup

From the repository root:

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd ..
python -m uvicorn backend.app.main:app --reload
```

Open the API documentation at:

`http://127.0.0.1:8000/docs`

## Test

From the repository root:

```powershell
pip install -r backend/requirements.txt
python -m pytest backend/tests -q
```

## CORS

The backend accepts the Vite development origins by default:

- `http://localhost:5173`
- `http://127.0.0.1:5173`

For another frontend URL, set `CORS_ORIGINS` to a comma-separated list.

## AI integration

The current backend uses lightweight keyword retrieval so the API is usable before
the full LLM/RAG pipeline is connected. The AI team can replace the retrieval
implementation without changing the frontend endpoint contract.
