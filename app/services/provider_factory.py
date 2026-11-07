import os
from dotenv import load_dotenv

from app.services.ai_provider import RuleBasedAIProvider
from app.services.groq_provider import GroqAIProvider

load_dotenv()


def get_ai_provider():

    provider = os.getenv("AI_PROVIDER", "rule_based").lower()

    if provider == "groq":
        return GroqAIProvider()

    elif provider == "rule_based":
        return RuleBasedAIProvider()

    else:
        raise ValueError(f"Unsupported AI provider: {provider}")