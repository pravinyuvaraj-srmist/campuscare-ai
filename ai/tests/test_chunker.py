from ai.chunker import chunk_documents
from ai.document_loader import Document


def test_chunker_creates_overlapping_chunks():
    document = Document(
        title="Test",
        content="one two three four five six seven eight nine ten",
        source="test",
        metadata={},
    )

    chunks = chunk_documents([document], chunk_size=5, overlap=2)

    assert len(chunks) == 3
    assert chunks[0].text == "one two three four five"
    assert chunks[1].text == "four five six seven eight"
