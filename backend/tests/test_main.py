from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_answer_and_sources():
    response = client.post(
        "/api/chat",
        json={"question": "I lost my student ID. What should I do?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["answer"]
    assert body["sources"]
