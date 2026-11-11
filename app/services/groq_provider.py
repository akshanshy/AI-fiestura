from email.mime import message
import os
from unittest import result
from unittest import result
from groq import Groq
import json
from app.schemas.intent import EventIntent
from app.services.ai_provider import AIProvider


class GroqAIProvider(AIProvider):

    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = "openai/gpt-oss-20b"
    def generate_response(self, message: str) -> str:

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content":  "You are AI-Fiestura, an assistant for the Fiestura "
                                "event management platform. Answer questions about the "
                                "platform and events. Do not invent platform features. "
                                "If you do not know something, clearly say so."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
        )
      

        return completion.choices[0].message.content

    def extract_intent(self, message: str) -> EventIntent:

        completion = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {
                "role": "system",
                "content": """
                You are the intent extraction engine for AI-Fiestura.

                AI-Fiestura is an event discovery and management assistant.

                Identify the user's intent.

                Supported intents:
                1. search_events:
                   User wants to discover or search for events.

                2. general_question:
                   User asks about events, event details,
                   or the Fiestura platform.

                3. out_of_scope:
                   User asks something unrelated to events
                   or the Fiestura platform.

                Extract:
                - intent
                - category
                - max_price

                Rules:
                - If the user asks for free events, max_price = 0.
                - If a maximum budget is specified, extract it.
                - If no category is specified, use null.
                - If no price is specified, use null.
                - Never invent filters.
                - Return valid JSON only.
                """
            },
            {
                "role": "user",
                "content": message
            }
            ],
            response_format={"type": "json_object"}
            )

        result = completion.choices[0].message.content

        data = json.loads(result)

        return EventIntent.model_validate(data)
    
def generate_event_response(self, message: str, events: list) -> str:
    import json

    event_data = [
        {
            "id": event.get("_id"),
            "title": event.get("title"),
            "description": event.get("description"),
            "category": event.get("category"),
            "price": event.get("price"),
            "location": event.get("location"),
            "startDate": event.get("startDate"),
            "endDate": event.get("endDate"),
            "status": event.get("status"),
        }
        for event in events
    ]

    completion = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are AI-Fiestura, an assistant for the Fiestura "
                    "event management platform. Answer using only the "
                    "provided event data. Never invent event names, "
                    "prices, dates, locations, or platform features. "
                    "If information is unavailable, say so. "
                    "Clearly explain when no matching events exist."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"User request: {message}\n\n"
                    f"Retrieved Fiestura events:\n"
                    f"{json.dumps(event_data, ensure_ascii=False)}"
                ),
            },
        ],
    )

    return completion.choices[0].message.content
