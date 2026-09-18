from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Document:
    title: str
    content: str
    source: str
    metadata: dict[str, Any]


def load_documents(path: str | Path) -> list[Document]:
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as file:
        raw_items = json.load(file)

    if not isinstance(raw_items, list):
        raise ValueError("Knowledge base must contain a JSON array.")

    documents: list[Document] = []
    for index, item in enumerate(raw_items):
        if not isinstance(item, dict):
            raise ValueError(f"Knowledge-base item {index} must be an object.")

        title = str(item.get("title", "")).strip()
        content = str(item.get("content", "")).strip()
        source = str(item.get("source", "")).strip()

        if not title or not content:
            raise ValueError(
                f"Knowledge-base item {index} must include title and content."
            )

        metadata = {
            key: value
            for key, value in item.items()
            if key not in {"title", "content", "source"}
        }

        documents.append(
            Document(
                title=title,
                content=content,
                source=source or "Unknown source",
                metadata=metadata,
            )
        )

    return documents
