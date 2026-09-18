import os
import httpx

SYSTEM_PROMPT = (
    "You are CampusCare, a helpful student support assistant for a college campus. "
    "Answer ONLY using the provided context. If the context does not contain the answer, "
    "say you could not find it and suggest contacting the relevant campus office. "
    "Keep answers short, clear and friendly. Do not invent names, phone numbers or rules."
)


def llm_enabled() -> bool:
    return all(os.getenv(k) for k in ("LLM_PROVIDER", "LLM_API_KEY", "LLM_MODEL"))


def generate_answer(question: str, matches: list[dict]) -> str:
    provider = os.getenv("LLM_PROVIDER", "").lower()
    key = os.getenv("LLM_API_KEY", "")
    model = os.getenv("LLM_MODEL", "")

    context = "\n\n".join(f"[{m['title']}]\n{m['content']}" for m in matches)
    prompt = f"Context:\n{context}\n\nStudent question: {question}"

    with httpx.Client(timeout=30) as client:
        if provider == "anthropic":
            r = client.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": key, "anthropic-version": "2023-06-01"},
                json={
                    "model": model,
                    "max_tokens": 500,
                    "system": SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            r.raise_for_status()
            return r.json()["content"][0]["text"].strip()

        if provider == "openai":
            r = client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                },
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()

        if provider == "gemini":
            r = client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                headers={"x-goog-api-key": key},
                json={
                    "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                    "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                },
            )
            r.raise_for_status()
            return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")