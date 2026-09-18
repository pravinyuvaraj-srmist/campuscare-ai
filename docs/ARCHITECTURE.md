# CampusCare AI — System Architecture

## Goal

Build a working student-support assistant that answers questions from a curated knowledge base and cites the information used.

## High-Level Flow

```
Student
   |
   v
React + Vite Frontend
   |
   v
FastAPI Backend
   |
   +--------------------+
   |                    |
   v                    v
Retriever          LLM / AI Model
   |                    |
   v                    |
Knowledge Base <--------+
   |
   v
Grounded Answer + Sources
   |
   v
Student

```

## Components

### Frontend
- Chat screen
- Question input
- Answer display
- Source cards
- Basic feedback control

### Backend
- REST API
- Request validation
- Retrieval orchestration
- AI service integration
- Response formatting

### AI / RAG
1. Load knowledge documents.
2. Split content into chunks.
3. Generate embeddings.
4. Store/search vectors.
5. Retrieve the most relevant chunks.
6. Send the question plus retrieved context to the language model.
7. Return an answer with source references.

### Data
The initial knowledge base will contain structured campus-support examples and approved public/open information. Project-specific real institutional data will only be added when the team has permission to use it.

## MVP Request Flow

```
POST /api/chat
      |
      v
Validate question
      |
      v
Retrieve top relevant chunks
      |
      v
Generate grounded response
      |
      v
Return:
{
  "answer": "...",
  "sources": [...]
}
```

## Security Notes

- Never commit API keys or secrets.
- Use environment variables for credentials.
- Treat user-submitted text as untrusted input.
- Avoid storing personal student information in the MVP.
