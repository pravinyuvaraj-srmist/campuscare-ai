# CampusCare AI

CampusCare AI is an AI-powered student assistance platform designed to help students quickly find campus support, emergency information, and institutional guidance.

## Open Innovation Track

### Problem
Students may struggle to locate the correct campus information when they need help with services, facilities, procedures, or urgent support.

### Proposed Solution
CampusCare AI provides a simple conversational interface. A student asks a question, the system retrieves relevant information from a curated campus knowledge base, and returns guidance with source references. The current scaffold uses deterministic retrieval so the end-to-end MVP can run without external API credentials; semantic retrieval and an LLM layer are planned next.

## MVP Features

- Student-friendly chat interface
- Knowledge-base / document retrieval
- AI-generated grounded answers
- Source references for retrieved information
- Basic feedback mechanism
- Simple architecture that can be demonstrated end-to-end

## Planned Technology

- Frontend: React + Vite
- Backend: Python + FastAPI
- AI/RAG: Python, embeddings, vector search, LLM API
- Data: Curated public/open campus-support information plus project sample data
- Deployment: To be selected during implementation

## Repository Structure

```
campuscare-ai/
├── ai/                  # AI/RAG pipeline
├── backend/             # FastAPI backend
├── data/                # Dataset notes and sample knowledge base
├── docs/                # Architecture and project documentation
├── frontend/            # Web application
├── .gitignore
└── README.md
```

## Run the MVP locally

### Backend

```bash
python -m venv .venv
# Activate the virtual environment for your OS
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal. The frontend defaults to `http://localhost:8000` for the backend.

## Current Milestone

Review 1 — Setup & Architecture

- Project concept defined
- Repository initialized
- System architecture documented
- MVP scope defined
- Implementation scaffold prepared

## Team

Hackathon team repository for the Code Cortex Open Innovation track.
