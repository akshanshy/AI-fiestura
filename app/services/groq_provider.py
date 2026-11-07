import os
from groq import Groq

from app.services.ai_provider import AIProvider


class GroqAIProvider(AIProvider):

    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = "llama-3.3-70b-versatile"

    def generate_response(self, message: str) -> str:

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are AI-Fiestura, a helpful event assistant."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
        )

        return completion.choices[0].message.content