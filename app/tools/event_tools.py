from app.data.events import events

def search_events(max_price=None, category=None):
    results = events

    if max_price is not None:
        results = [
            event for event in results
            if event["price"] <= max_price
        ]

    if category is not None:
        results = [
            event for event in results
            if category.lower() in event["category"].lower()
        ]

    return results


def get_event_by_id(event_id: int):
    for event in events:
        if event["id"] == event_id:
            return event

    return None