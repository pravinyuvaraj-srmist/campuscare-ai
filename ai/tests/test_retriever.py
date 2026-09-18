from ai.chunker import Chunk
from ai.embeddings import embed_texts
from ai.retriever import VectorRetriever


def test_retriever_ranks_similar_chunk_first():
    chunks = [
        Chunk("1", "lost id card", "ID Help", "source-a", {}),
        Chunk("2", "hostel maintenance", "Hostel", "source-b", {}),
    ]

    embeddings = embed_texts(
        [
            "ID Help lost id card student identification",
            "Hostel maintenance room repair",
        ]
    )

    retriever = VectorRetriever(chunks, embeddings, "hash-384")
    results = retriever.search("lost student id card", top_k=2)

    assert results
    assert results[0].chunk.title == "ID Help"
    assert results[0].score > results[1].score
