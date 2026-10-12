
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing from .env")

client = OpenAI(api_key=api_key)



def generate_ai_response(message: str) -> str:
    """
    Temporary mock response for local development.
    Replace with real LLM integration when API access is available.
    """
    return (
        f"AI-Fiestura received your message: '{message}'. "
        "I'm currently running in development mode without an LLM."
    )

