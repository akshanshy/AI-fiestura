
from fastapi.testclient import TestClient
from app.tools.event_tools import search_events
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

def test_search_events_by_max_price():
    results = search_events(max_price=0)

    assert len(results) == 1
    assert results[0]["title"] == "Coding Contest"


def test_search_events_by_category():
    results = search_events(category="AI")

    assert any(event["title"] == "AI Workshop" for event in results)


def test_search_events_with_both_filters():
    results = search_events(max_price=100, category="AI")

    assert len(results) == 1
    assert results[0]["title"] == "AI Workshop"

def test_get_existing_event():
    response = client.get("/events/1")

    assert response.status_code == 200
    assert response.json()["title"] == "AI Workshop"


def test_get_missing_event():
    response = client.get("/events/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"