from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "data" / "knowledge_base.json"
INDEX_DIR = ROOT_DIR / "data" / "ai_index"

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)
LLM_MODEL = os.getenv("LLM_MODEL", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
TOP_K = int(os.getenv("RAG_TOP_K", "3"))
RAG_MIN_SCORE = float(os.getenv("RAG_MIN_SCORE", "0.35"))
MAX_CONTEXT_CHARS = int(os.getenv("RAG_MAX_CONTEXT_CHARS", "6000"))
