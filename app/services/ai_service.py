
import re

from app.tools.event_tools import search_events


def generate_ai_response(message: str) -> str:
    text = message.lower()

    # Recognize event-search requests
    event_keywords = ["event", "workshop", "hackathon", "coding contest"]

    if not any(keyword in text for keyword in event_keywords):
        return (
            f"AI-Fiestura received your message: '{message}'. "
            "I'm running in development mode without an LLM."
        )

    # Extract the maximum price
    max_price = None

    if "free" in text:
        max_price = 0
    else:
        match = re.search(
            r"(?:under|below|less than|up to|upto)"
            r"\s*₹?\s*(\d+)",
            text,
        )

        if match:
            max_price = int(match.group(1))

    # Recognize a category
    category = None

    if re.search(r"\bai\b", text):
        category = "AI"
    elif "technology" in text or "tech events" in text:
        category = "Technology"
    elif "programming" in text or "coding" in text:
        category = "Programming"

    # Execute our event-search tool
    events = search_events(
        max_price=max_price,
        category=category,
    )

    if not events:
        return "No matching events found. Try different filters."

    # Format the results for the user
    results = []

    for event in events:
        results.append(
            f"{event['title']} — "
            f"Category: {event['category']}, "
            f"Price: ₹{event['price']}"
        )

    return "Here are the matching events:\n" + "\n".join(results)
