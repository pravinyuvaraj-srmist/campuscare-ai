from functools import lru_cache

import numpy as np


@lru_cache(maxsize=2)
def get_model(model_name: str):
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


def embed_texts(texts: list[str], model_name: str) -> np.ndarray:
    if not texts:
        return np.empty((0, 0), dtype=np.float32)

    model = get_model(model_name)
    vectors = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return np.asarray(vectors, dtype=np.float32)


def embed_query(query: str, model_name: str) -> np.ndarray:
    return embed_texts([query], model_name)[0]
