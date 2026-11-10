import re
from abc import ABC, abstractmethod
from app.services.ai_service import generate_ai_response
from app.schemas.intent import EventIntent


class AIProvider(ABC):
    @abstractmethod
    def generate_response(self, message: str) -> str:
        pass

    @abstractmethod
    def extract_intent(self, message: str) -> EventIntent:
        pass


class RuleBasedAIProvider(AIProvider):
    def generate_response(self, message: str) -> str:
        return generate_ai_response(message)

    def extract_intent(self, message: str) -> EventIntent:
        normalized_message = message.lower()

        # 1. Check for event-search intent
        search_terms = ["workshop", "hackathon", "conference", "find events"]
        if any(term in normalized_message for term in search_terms):
            # Extract category (AI, technology, programming)
            category = None
            category_map = {
                "AI": [r"\bai\b", r"\bartificial intelligence\b"],
                "technology": [r"\btechnology\b", r"\btech\b"],
                "programming": [r"\bprogramming\b", r"\bcoding\b", r"\bdeveloper\b"],
            }
            for cat_name, patterns in category_map.items():
                if any(re.search(pattern, normalized_message) for pattern in patterns):
                    category = cat_name
                    break

            # Extract max_price ("free" -> 0, "under 500" -> 500, otherwise None)
            max_price = None
            if re.search(r"\bfree\b", normalized_message):
                max_price = 0
            else:
                price_match = re.search(
                    r"(?:under|below|less than|max|up to)\s*(?:₹|\$|rs\.?|inr|usd)?\s*(\d+)",
                    normalized_message,
                )
                if price_match:
                    max_price = int(price_match.group(1))

            return EventIntent(
                intent="search_events",
                category=category,
                max_price=max_price,
            )

        # 2. Check for general event question or mention of "fiestura"
        general_question_terms = [
            "fiestura",
            "event",
            "events",
            "ticket",
            "tickets",
            "register",
            "registration",
            "schedule",
            "venue",
            "location",
            "refund",
        ]
        if (
            "fiestura" in normalized_message
            or "?" in normalized_message
            and any(term in normalized_message for term in general_question_terms)
            or any(
                phrase in normalized_message
                for phrase in ["what is", "how do", "how to", "when is", "where is", "tell me about"]
            )
            and any(term in normalized_message for term in general_question_terms)
        ):
            return EventIntent(intent="general_question")

        # 3. Fallback for anything unrelated
        return EventIntent(intent="out_of_scope")
