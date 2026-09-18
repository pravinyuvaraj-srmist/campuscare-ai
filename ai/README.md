# CampusCare AI — RAG Layer

This folder contains the AI pipeline for CampusCare AI.

## Pipeline

~~~text
Student question
      |
      v
Question embedding
      |
      v
Semantic vector retrieval
      |
      v
Top-k relevant knowledge chunks
      |
      v
Grounded LLM prompt
      |
      v
Answer + source references
~~~

## Files

- document_loader.py — loads and validates the JSON knowledge base.
- chunker.py — splits documents into overlapping chunks.
- embeddings.py — creates normalized sentence embeddings.
- retriever.py — performs cosine-similarity vector search.
- prompt_builder.py — constructs a grounded prompt from retrieved context.
- llm_client.py — calls an LLM when credentials are configured.
- rag.py — orchestrates the complete RAG flow.
- build_index.py — writes an embeddings index for later startup optimization.
- config.py — central configuration.
- requirements.txt — AI dependencies.

## Setup

From the repository root:

~~~bash
python -m venv .venv
# Activate the environment for your operating system
pip install -r ai/requirements.txt
~~~

## Run tests

~~~bash
python -m pytest ai/tests -q
~~~

## Try the RAG pipeline

~~~bash
python -c "from ai.rag import build_pipeline; r=build_pipeline().answer('I lost my student ID. What should I do?'); print(r.answer); print(r.sources)"
~~~

The first embedding run downloads the selected sentence-transformer model.

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

It receives an object containing the generated answer, source metadata, and retrieval results.

## Data note

The current data/knowledge_base.json is starter sample data. Before presenting real campus guidance, replace it with verified, permitted institutional/public information and document source URLs and licensing.
