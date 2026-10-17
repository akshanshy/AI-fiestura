
import os

from dotenv import load_dotenv

from app.clients.fiestura_client import fetch_fiestura_events

load_dotenv()

FIESTURA_API_URL = os.getenv(
    "FIESTURA_API_URL",
    "http://localhost:5000",
)


def get_events():
    """Fetch real events from the Fiestura backend."""
    response = fetch_fiestura_events(FIESTURA_API_URL)

    if "error" in response:
        raise RuntimeError(response["error"])

    return response.get("events", [])


def search_events(max_price=None, category=None):
    results = get_events()

    if max_price is not None:
        results = [
            event for event in results
            if event.get("price") is not None
            and event["price"] <= max_price
        ]

    if category is not None:
        results = [
            event for event in results
            if category.lower() in event.get("category", "").lower()
        ]

    return results


def get_event_by_id(event_id: int):
    for event in get_events():
        if str(event.get("id", event.get("_id"))) == str(event_id):
            return event

    return None
