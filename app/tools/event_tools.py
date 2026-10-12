
events = [
    {
        "id": 1,
        "title": "AI Workshop",
        "category": "AI",
        "price": 100
    },
    {
        "id": 2,
        "title": "Hackathon",
        "category": "Technology",
        "price": 200
    },
    {
        "id": 3,
        "title": "Coding Contest",
        "category": "Programming",
        "price": 0
    }
]


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
