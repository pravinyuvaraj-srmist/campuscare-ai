from ai.chunker import Chunk
from ai.prompt_builder import build_prompt
from ai.retriever import RetrievalResult


def test_prompt_contains_question_and_source():
    chunk = Chunk(
        "1",
        "Report the lost card to student services.",
        "Lost ID",
        "CampusCare source",
        {},
    )
    system, user = build_prompt(
        "I lost my ID. What should I do?",
        [RetrievalResult(chunk=chunk, score=0.9)],
    )

    assert "I lost my ID" in user
    assert "CampusCare source" in user
    assert "only the supplied retrieved context" in system
