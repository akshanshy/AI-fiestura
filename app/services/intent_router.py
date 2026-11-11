
from app.services.ai_provider import AIProvider
from app.tools.event_tools import search_events


def route_message(message: str, provider: AIProvider) -> dict:

    # Extract and validate the user's intent
    extracted = provider.extract_intent(message)

    # Event discovery
    if extracted.intent == "search_events":

        matching_events = search_events(
            max_price=extracted.max_price,
            category=extracted.category
        )

        reply = provider.generate_event_response(
            message,
            matching_events
        )

        return {
            "intent": "search_events",
            "events": matching_events,
            "reply": reply
        }

    # General Fiestura question
    elif extracted.intent == "general_question":

        return {
            "intent": "general_question",
            "events": [],
            "reply": provider.generate_response(message)
        }

    # Unrelated question
    elif extracted.intent == "out_of_scope":

        return {
            "intent": "out_of_scope",
            "events": [],
            "reply": (
                "I'm AI-Fiestura, an assistant focused on events. "
                "I can help you discover workshops, hackathons, "
                "conferences and learn about Fiestura."
            )
        }

    return {
        "intent": "unknown",
        "events": [],
        "reply": "Sorry, I couldn't understand your request."
    }
