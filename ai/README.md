# CampusCare AI — RAG Layer

This folder contains the AI pipeline for CampusCare AI.

## Pipeline

~~~text
Student question
      |
      v
Text vectorization
      |
      v
Relevant knowledge retrieval
      |
      v
Grounded prompt
      |
      v
Optional LLM
      |
      v
Answer + source references
~~~

## Files

- document_loader.py — loads and validates the JSON knowledge base.
- chunker.py — splits documents into overlapping chunks.
- embeddings.py — creates dependency-light normalized text vectors.
- retriever.py — performs cosine-similarity vector search.
- prompt_builder.py — constructs a grounded prompt from retrieved context.
- llm_client.py — calls an LLM when credentials are configured.
- rag.py — orchestrates the complete RAG flow.
- build_index.py — writes a portable JSON vector index.
- config.py — central configuration.
- requirements.txt — AI dependencies.

## Setup

From the repository root:

~~~bash
python -m venv .venv
# Activate the environment for your operating system
pip install -r backend/requirements.txt
~~~

The current MVP deliberately avoids PyTorch, SciPy, NumPy, and scikit-learn so it can run on restricted Windows machines without native DLL loading problems.

## Try the RAG pipeline

~~~bash
python -c "from ai.rag import build_pipeline; r=build_pipeline().answer('I lost my student ID. What should I do?'); print(r.answer); print(r.sources)"
~~~

The default retrieval vectorizer is deterministic and dependency-light. It provides a local vector-search layer for the MVP. When an LLM is configured, retrieved context is passed to the LLM for grounded natural-language generation.

## Optional LLM

Set these environment variables locally:

~~~text
LLM_API_KEY=<your-key>
LLM_MODEL=<model-name>
~~~

Never commit a real API key.

When no LLM is configured, the pipeline falls back to the highest-ranked retrieved chunk so the MVP remains testable.

## Backend handoff

The backend can import:

~~~python
from ai.rag import build_pipeline

pipeline = build_pipeline()
result = pipeline.answer("How can I get medical assistance?")
~~~

The result contains the generated or fallback answer, source metadata, and retrieval results.

## Data note

The current `data/knowledge_base.json` is starter sample data. Before presenting real campus guidance, replace it with verified, permitted institutional/public information and document source URLs and licensing.
