
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200


def test_chat_finds_free_events():
    response = client.post(
        "/chat",
        json={"message": "Find free events"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Find free events"
    assert "Coding Contest" in data["reply"]


def test_chat_rejects_empty_message():
    response = client.post(
        "/chat",
        json={"message": ""},
    )

    assert response.status_code == 422


def test_chat_rejects_missing_message():
    response = client.post("/chat", json={})

    assert response.status_code == 422


def test_chat_rejects_long_message():
    response = client.post(
        "/chat",
        json={"message": "a" * 1001},
    )

    assert response.status_code == 422
