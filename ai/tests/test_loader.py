import json

from ai.document_loader import load_documents


def test_load_documents(tmp_path) -> None:
    path = tmp_path / "knowledge.json"
    path.write_text(
        json.dumps(
            [
                {
                    "title": "Library",
                    "content": "Contact the library help desk.",
                    "source": "unit-test",
                    "category": "support",
                }
            ]
        ),
        encoding="utf-8",
    )

    documents = load_documents(path)

    assert len(documents) == 1
    assert documents[0].title == "Library"
    assert documents[0].source == "unit-test"
    assert documents[0].metadata["category"] == "support"
