# CampusCare AI

CampusCare AI is an AI-assisted student support platform designed to help students quickly find campus support, emergency information, and institutional guidance.

## Open Innovation Track

### Problem

Students may struggle to locate the correct campus information when they need help with services, facilities, procedures, or urgent support.

### Proposed Solution

CampusCare AI provides a simple conversational interface. A student asks a question, the system retrieves relevant information from a curated knowledge base, and returns grounded guidance with source references.

### MVP Features

- Student-friendly chat interface
- Knowledge-base retrieval
- Retrieval-augmented AI response path
- Source references for retrieved information
- Loading and error states
- Simple architecture suitable for an end-to-end demo

### Technology

- Frontend: React + Vite
- Backend: Python + FastAPI
- AI/RAG: Python, lightweight vector retrieval, optional LLM API
- Data: Curated/sample campus-support knowledge base
- Deployment: To be selected

### Repository Structure

```
campuscare-ai/
├── ai/                  # AI/RAG pipeline
├── backend/             # FastAPI backend
├── data/                # Knowledge base
├── docs/                # Architecture and project documentation
├── frontend/            # React web application
├── .gitignore
└── README.md
```

### Run the MVP locally

From the repository root:

```bash
python -m venv .venv
# Activate the virtual environment for your OS
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

For the frontend:

```bash
cd frontend
npm install
npm run dev
```

The frontend defaults to `http://localhost:8000` for the backend.

### Current Status

The backend is connected to the RAG pipeline and returns answers with source metadata. The RAG layer uses a portable deterministic vector representation so the MVP can run on restricted Windows environments without PyTorch/SciPy. When `LLM_API_KEY` and `LLM_MODEL` are configured, the RAG layer can call the configured LLM to generate the grounded response; otherwise it falls back to the best retrieved knowledge chunk.

## Security

Never commit API keys or other credentials to GitHub. Use local environment variables for LLM configuration.
