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