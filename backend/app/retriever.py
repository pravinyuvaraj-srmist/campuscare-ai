import re


def tokenize(text: str) -> set[str]:
    """Convert text into normalized words for lightweight retrieval."""
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9]+", text.lower())
        if len(token) >= 3
    }


def retrieve(question: str, knowledge: list[dict], limit: int = 3) -> list[dict]:
    """Return the knowledge-base entries with the highest keyword overlap."""
    query_terms = tokenize(question)
    scored: list[tuple[int, dict]] = []

    for item in knowledge:
        title = str(item.get("title", ""))
        content = str(item.get("content", ""))
        haystack = tokenize(f"{title} {content}")

        score = len(query_terms & haystack)
        if score > 0:
            scored.append((score, item))

    scored.sort(
        key=lambda pair: (
            -pair[0],
            str(pair[1].get("title", "")),
        )
    )

    return [item for _, item in scored[:limit]]


def build_answer(question: str, matches: list[dict]) -> str:
    """Build a safe MVP answer from retrieved approved content."""
    if not matches:
        return (
            "I could not find a reliable answer in the current CampusCare "
            "knowledge base. Please contact the relevant campus office or "
            "add an approved source."
        )

    top = matches[0]
    return (
        "Based on the current CampusCare knowledge base, the most relevant "
        f"guidance for '{question}' is: {top['content']}"
    )
