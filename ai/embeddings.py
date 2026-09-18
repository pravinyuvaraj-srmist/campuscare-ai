"""Dependency-light deterministic text vectors.

This implementation intentionally avoids PyTorch, SciPy, and other native
ML libraries so CampusCare can run on locked-down Windows machines.
"""

from functools import lru_cache
import hashlib
import math
import re

VECTOR_SIZE = 384


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _index(token: str) -> int:
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "little") % VECTOR_SIZE


@lru_cache(maxsize=4096)
def embed_text(text: str, model_name: str = "hash-384") -> tuple[float, ...]:
    """Create a normalized hashed bag-of-words vector."""
    vector = [0.0] * VECTOR_SIZE

    for token in _tokens(text):
        vector[_index(token)] += 1.0

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0.0:
        return tuple(vector)

    return tuple(value / norm for value in vector)


def embed_texts(
    texts: list[str],
    model_name: str = "hash-384",
) -> list[tuple[float, ...]]:
    return [embed_text(text, model_name) for text in texts]


def embed_query(
    query: str,
    model_name: str = "hash-384",
) -> tuple[float, ...]:
    return embed_text(query, model_name)
