from types import SimpleNamespace

import pytest

from ai.llm_client import LLMClient


class FakeCompletions:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error

    def create(self, **kwargs):
        assert kwargs["model"] == "test-model"
        assert kwargs["temperature"] == 0.2
        if self.error:
            raise self.error
        return self.response


class FakeClient:
    def __init__(self, response=None, error=None):
        self.chat = SimpleNamespace(
            completions=FakeCompletions(response=response, error=error)
        )


def test_llm_client_returns_generated_content():
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="  Grounded answer. "))]
    )
    client = LLMClient(
        api_key="test-key",
        model="test-model",
        client=FakeClient(response=response),
    )

    assert client.generate("system", "user") == "Grounded answer."


def test_llm_client_wraps_provider_errors():
    client = LLMClient(
        api_key="test-key",
        model="test-model",
        client=FakeClient(error=ValueError("provider down")),
    )

    with pytest.raises(RuntimeError, match="LLM request failed"):
        client.generate("system", "user")