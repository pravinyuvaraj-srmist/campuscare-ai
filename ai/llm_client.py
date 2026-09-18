import os
from typing import Any


class LLMClient:
    """Small LLM adapter. Uses OpenAI when configured."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        client: Any | None = None,
    ):
        self.api_key = api_key or os.getenv("LLM_API_KEY", "")
        self.model = model or os.getenv("LLM_MODEL", "")
        self.client = client

    @property
    def configured(self) -> bool:
        return bool(self.api_key and self.model)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self.configured:
            raise RuntimeError(
                "LLM is not configured. Set LLM_API_KEY and LLM_MODEL."
            )

        if self.client is None:
            from openai import OpenAI

            self.client = OpenAI(
                api_key=self.api_key,
                timeout=float(os.getenv("LLM_TIMEOUT_SECONDS", "30")),
            )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0.2,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
        except Exception as exc:
            raise RuntimeError("The LLM request failed.") from exc

        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("The LLM returned an empty response.")

        return content.strip()
