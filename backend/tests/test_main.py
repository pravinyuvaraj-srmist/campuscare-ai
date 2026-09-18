from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


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
    assert body["sources"][0]["title"] == "Lost Student ID Card"


def test_chat_rejects_blank_question():
    response = client.post(
        "/api/chat",
        json={"question": ""},
    )
    assert response.status_code == 422


def test_chat_returns_safe_fallback_when_no_match():
    response = client.post(
        "/api/chat",
        json={"question": "What is the history of the moon?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["sources"] == []
    assert "could not find a reliable answer" in body["answer"]
