from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "data" / "knowledge_base.json"
INDEX_DIR = ROOT_DIR / "data" / "ai_index"

# Uses a deterministic, dependency-light vectorizer by default.
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "hash-384")
LLM_MODEL = os.getenv("LLM_MODEL", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
TOP_K = int(os.getenv("RAG_TOP_K", "3"))
MAX_CONTEXT_CHARS = int(os.getenv("RAG_MAX_CONTEXT_CHARS", "6000"))
