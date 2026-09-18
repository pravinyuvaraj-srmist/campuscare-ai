from types import SimpleNamespace

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_uses_rag_pipeline(monkeypatch):
    fake_response = SimpleNamespace(
        answer="Report the lost ID to the student services desk.",
        sources=[
            {
                "title": "Lost Student ID Card",
                "source": "CampusCare sample knowledge base",
                "score": 0.91,
            }
        ],
    )

    class FakePipeline:
        def answer(self, question):
            assert question == "I lost my student ID. What should I do?"
            return fake_response

    monkeypatch.setattr("backend.app.main.get_rag_pipeline", lambda: FakePipeline())

    response = client.post(
        "/api/chat",
        json={"question": "I lost my student ID. What should I do?"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Report the lost ID to the student services desk.",
        "sources": [
            {
                "title": "Lost Student ID Card",
                "source": "CampusCare sample knowledge base",
                "score": 0.91,
            }
        ],
    }


def test_chat_rejects_empty_question():
    response = client.post("/api/chat", json={"question": ""})
    assert response.status_code == 422
