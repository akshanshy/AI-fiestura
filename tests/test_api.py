
import logging
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.tools.event_tools import search_events

client = TestClient(app)

MOCK_EVENTS = [
    {
        "id": 1,
        "title": "AI Workshop",
        "category": "AI",
        "price": 100,
    },
    {
        "id": 2,
        "title": "Hackathon",
        "category": "Technology",
        "price": 200,
    },
    {
        "id": 3,
        "title": "Coding Contest",
        "category": "Programming",
        "price": 0,
    },
]


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200


@patch("app.tools.event_tools.get_events", return_value=[
    # 1. Free Technical event
    {
        "id": 1,
        "title": "Introduction to Python Programming",
        "category": "Technical",
        "is_free": True,
        "price": 0.00
    },
    # 2. Paid Technical event
    {
        "id": 2,
        "title": "Advanced Microservices Architecture Workshop",
        "category": "Technical",
        "is_free": False,
        "price": 49.99
    },
    # 3. Free Non-Technical event
    {
        "id": 3,
        "title": "Community Networking & Coffee Mixer",
        "category": "Social",
        "is_free": True,
        "price": 0.00
    }
    ])
def test_chat_finds_free_technical_events(mock_get_events):
    response = client.post(
        "/chat",
        json={"message": "Find free technical events"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Find free technical events"
    reply = data["reply"]

    assert "Introduction to Python Programming" in reply
    assert "Advanced Microservices Architecture Workshop" not in reply
    assert "Community Networking & Coffee Mixer" not in reply


def test_chat_rejects_empty_message():
    response = client.post("/chat", json={"message": ""})
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


@patch("app.tools.event_tools.get_events", return_value=MOCK_EVENTS)
def test_search_events_by_max_price(mock_get_events):
    results = search_events(max_price=0)

    assert len(results) == 1
    assert results[0]["title"] == "Coding Contest"


@patch("app.tools.event_tools.get_events", return_value=MOCK_EVENTS)
def test_search_events_by_category(mock_get_events):
    results = search_events(category="AI")

    assert len(results) == 1
    assert results[0]["title"] == "AI Workshop"


@patch("app.tools.event_tools.get_events", return_value=MOCK_EVENTS)
def test_search_events_with_both_filters(mock_get_events):
    results = search_events(max_price=100, category="AI")

    assert len(results) == 1
    assert results[0]["title"] == "AI Workshop"


@patch("app.tools.event_tools.get_events", return_value=MOCK_EVENTS)
def test_get_existing_event(mock_get_events):
    response = client.get("/events/1")

    assert response.status_code == 200
    assert response.json()["title"] == "AI Workshop"


@patch("app.tools.event_tools.get_events", return_value=MOCK_EVENTS)
def test_get_missing_event(mock_get_events):
    response = client.get("/events/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


def test_chat_handles_unexpected_error(caplog):
    with patch(
        "app.main.generate_ai_response",
        side_effect=RuntimeError("Sensitive internal detail"),
    ):
        with caplog.at_level(logging.ERROR):
            response = client.post(
                "/chat",
                json={"message": "Find events"},
            )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "An unexpected error occurred while processing your request."
    )
    assert "Sensitive internal detail" not in response.text
    assert "Unexpected error while generating chat response" in caplog.text
    assert "Sensitive internal detail" in caplog.text

@patch(
    "app.tools.event_tools.get_events",
    side_effect=RuntimeError("Could not connect to Fiestura backend"),
)
def test_chat_handles_fiestura_backend_failure(mock_get_events):
    response = client.post(
        "/chat",
        json={"message": "Find free technical events"},
    )

    assert response.status_code == 500
    assert "Could not connect to Fiestura backend" not in response.text

@patch("app.tools.event_tools.get_events", return_value=[])
def test_chat_handles_no_matching_events(mock_get_events):
    response = client.post(
        "/chat",
        json={"message": "Find free technical events"}

        )
    assert response.status_code == 200
    assert response.json()["reply"] == ("No matching events found. Try different filters.")
