
from app.services.ai_provider import AIProvider
from app.tools.event_tools import search_events


def route_message(message: str, provider: AIProvider) -> dict:
    """
    Extract the user's intent and route the request
    to the appropriate operation.
    """

    # Step 1: Extract structured intent
    extracted = provider.extract_intent(message)

    # Step 2: Handle event search
    if extracted.intent == "search_events":

        # Retrieve actual events using extracted filters
        matching_events = search_events(
            max_price=extracted.max_price,
            category=extracted.category
        )

        # Step 3: Handle empty search results
        if not matching_events:
            return {
                "intent": "search_events",
                "events": [],
                "reply": "No matching events found. Try changing your filters."
            }

        # Step 4: Return matching events
        return {
            "intent": "search_events",
            "events": matching_events,
            "reply": f"I found {len(matching_events)} matching events."
        }

    # Step 5: Handle general questions
    elif extracted.intent == "general_question":

        reply = provider.generate_response(message)

        return {
            "intent": "general_question",
            "events": [],
            "reply": reply
        }

    # Step 6: Handle unrelated queries
    elif extracted.intent == "out_of_scope":

        return {
            "intent": "out_of_scope",
            "events": [],
            "reply": (
                "I'm AI-Fiestura, an assistant focused on events. "
                "I can help you discover workshops, hackathons, "
                "conferences and answer questions about Fiestura."
            )
        }

    # Step 7: Defensive handling for unexpected intent
    return {
        "intent": "unknown",
        "events": [],
        "reply": "Sorry, I couldn't understand your request."
    }
