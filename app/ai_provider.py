from abc import ABC, abstractmethod
from app.services.ai_service import generate_ai_response

class AIProvider(ABC):
    @abstractmethod
    def generate_response(self, message: str) -> str:
        pass


class RuleBasedAIProvider(AIProvider):
    def generate_response(self, message: str) -> str:
        return generate_ai_response(message)